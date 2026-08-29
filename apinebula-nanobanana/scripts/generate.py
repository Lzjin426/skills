#!/usr/bin/env python3
"""Generate one image with APINebula Nano Banana (gemini-3.1-flash-image)."""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import mimetypes
import os
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


MODEL = "gemini-3.1-flash-image"
API_URL = f"https://img-api.apinebula.ai/v1beta/models/{MODEL}:generateContent"
ASPECT_RATIOS = {
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5",
    "5:4", "8:1", "9:16", "16:9", "21:9",
}
IMAGE_SIZES = {"1K", "2K", "4K"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one image with APINebula Nano Banana.")
    prompts = parser.add_mutually_exclusive_group(required=True)
    prompts.add_argument("--prompt", help="Image-generation prompt.")
    prompts.add_argument("--prompt-file", type=Path, help="UTF-8 file containing the prompt.")
    parser.add_argument("--output", type=Path, default=Path("nanobanana-image.png"))
    parser.add_argument("--aspect-ratio", choices=sorted(ASPECT_RATIOS), default="1:1")
    parser.add_argument("--image-size", choices=sorted(IMAGE_SIZES), default="1K")
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    return args


def read_prompt(args: argparse.Namespace) -> str:
    prompt = args.prompt if args.prompt is not None else args.prompt_file.read_text(encoding="utf-8")
    prompt = prompt.strip()
    if not prompt:
        raise SystemExit("Prompt must not be empty.")
    return prompt


def build_payload(prompt: str, args: argparse.Namespace) -> dict:
    return {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": args.aspect_ratio,
                "imageSize": args.image_size,
            },
        },
    }


def api_key() -> str | None:
    value = os.environ.get("APINEBULA_API_KEY", "").strip()
    if value:
        return value
    key_file = Path(__file__).resolve().parents[1] / ".api_key"
    try:
        return key_file.read_text(encoding="utf-8").strip() or None
    except FileNotFoundError:
        return None


def request_json(payload: dict, key: str, timeout: float) -> dict:
    request = Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"APINebula returned HTTP {error.code}: {detail[:1000]}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach APINebula: {error.reason}") from error
    try:
        result = json.loads(body)
    except json.JSONDecodeError as error:
        raise RuntimeError("APINebula returned invalid JSON.") from error
    if not isinstance(result, dict):
        raise RuntimeError("APINebula returned an unexpected response body.")
    return result


def extract_image(result: dict) -> tuple[bytes, str]:
    candidates = result.get("candidates")
    if not isinstance(candidates, list):
        raise RuntimeError("No image candidate was returned.")
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        parts = candidate.get("content", {}).get("parts", [])
        for part in parts if isinstance(parts, list) else []:
            inline = part.get("inlineData") if isinstance(part, dict) else None
            if isinstance(inline, dict) and isinstance(inline.get("data"), str):
                try:
                    data = base64.b64decode(inline["data"], validate=True)
                except (ValueError, binascii.Error) as error:
                    raise RuntimeError("Image data was not valid Base64.") from error
                return data, str(inline.get("mimeType", "image/png"))
    raise RuntimeError("No inline image data was returned.")


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(data)
    temporary.replace(path)


def main() -> int:
    args = parse_args()
    payload = build_payload(read_prompt(args), args)
    if args.dry_run:
        print(json.dumps({"model": MODEL, "url": API_URL, **payload}, ensure_ascii=False, indent=2))
        return 0
    key = api_key()
    if not key:
        print("缺少 APINEBULA_API_KEY 或本 skill 目录下的 .api_key。", file=sys.stderr)
        return 2
    try:
        data, mime = extract_image(request_json(payload, key, args.timeout))
        suffix = mimetypes.guess_extension(mime) or ".png"
        if suffix == ".jpe":
            suffix = ".jpg"
        output = args.output if args.output.suffix.lower() == suffix else args.output.with_suffix(suffix)
        write_atomic(output, data)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1
    print(output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
