#!/usr/bin/env python3
"""Generate one publication-figure draft through APINebula Nano Banana 2."""

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


API_BASE = "https://img-api.apinebula.ai/v1beta/models"
DEFAULT_MODEL = "gemini-3.1-flash-image"
VALID_ASPECT_RATIOS = {
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5",
    "5:4", "8:1", "9:16", "16:9", "21:9",
}
VALID_IMAGE_SIZES = {"1K", "2K", "4K"}


def sibling_key_file() -> Path:
    return Path(__file__).resolve().parents[2] / "apinebula-gpt-image" / ".api_key"


def get_api_key() -> str | None:
    key = os.environ.get("APINEBULA_API_KEY", "").strip()
    if key:
        return key
    try:
        return sibling_key_file().read_text(encoding="utf-8").strip() or None
    except FileNotFoundError:
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one PaperBanana-planned schematic with APINebula Nano Banana 2."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", help="Final English image-generation prompt.")
    group.add_argument("--prompt-file", type=Path, help="UTF-8 file containing the final prompt.")
    parser.add_argument("--output", type=Path, default=Path("paperbanana-figure.png"))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--aspect-ratio", default="16:9", choices=sorted(VALID_ASPECT_RATIOS))
    parser.add_argument("--image-size", default="2K", choices=sorted(VALID_IMAGE_SIZES))
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--dry-run", action="store_true", help="Print the request payload without calling APINebula.")
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


def request_image(payload: dict, api_key: str, args: argparse.Namespace) -> dict:
    request = Request(
        f"{API_BASE}/{args.model}:generateContent",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=args.timeout) as response:
            raw = response.read()
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"APINebula returned HTTP {error.code}: {body[:1000]}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach APINebula: {error.reason}") from error
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeError("APINebula returned invalid JSON.") from error
    if not isinstance(result, dict):
        raise RuntimeError("APINebula returned an unexpected response body.")
    return result


def extract_image(response: dict) -> tuple[bytes, str]:
    candidates = response.get("candidates")
    if not isinstance(candidates, list):
        raise RuntimeError("No image candidate was returned.")
    for candidate in candidates:
        parts = candidate.get("content", {}).get("parts", []) if isinstance(candidate, dict) else []
        for part in parts:
            inline_data = part.get("inlineData") if isinstance(part, dict) else None
            if isinstance(inline_data, dict) and isinstance(inline_data.get("data"), str):
                try:
                    return (
                        base64.b64decode(inline_data["data"], validate=True),
                        inline_data.get("mimeType", "image/png"),
                    )
                except (ValueError, binascii.Error) as error:
                    raise RuntimeError("Image data was not valid Base64.") from error
    raise RuntimeError("No inline image data was returned.")


def output_path_for_mime(path: Path, mime_type: str) -> Path:
    suffix = mimetypes.guess_extension(mime_type) or ".png"
    if suffix == ".jpe":
        suffix = ".jpg"
    return path if path.suffix.lower() == suffix else path.with_suffix(suffix)


def atomic_write(path: Path, image_data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        temporary_path = Path(handle.name)
        handle.write(image_data)
    temporary_path.replace(path)


def main() -> int:
    args = parse_args()
    prompt = read_prompt(args)
    payload = build_payload(prompt, args)
    if args.dry_run:
        print(json.dumps({"model": args.model, **payload}, ensure_ascii=False, indent=2))
        return 0

    api_key = get_api_key()
    if not api_key:
        print("缺少 APINEBULA_API_KEY 或 apinebula-gpt-image/.api_key。", file=sys.stderr)
        return 2

    try:
        response = request_image(payload, api_key, args)
        image_data, mime_type = extract_image(response)
        output_path = output_path_for_mime(args.output, mime_type)
        atomic_write(output_path, image_data)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1

    print(output_path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
