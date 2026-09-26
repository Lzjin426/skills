#!/usr/bin/env python3
"""Extract PDF to Markdown using mineru-open-api (online API)."""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def find_extracted_files(output_dir: Path):
    """Locate the generated .md file and images directory in MinerU output."""
    md_files = list(output_dir.glob("*.md"))
    if not md_files:
        # MinerU sometimes creates a subdirectory named after the PDF
        subdirs = [d for d in output_dir.iterdir() if d.is_dir()]
        for sub in subdirs:
            md_files = list(sub.glob("*.md"))
            if md_files:
                output_dir = sub
                break

    if not md_files:
        return None, None

    md_file = md_files[0]
    images_dir = output_dir / "images"
    if not images_dir.exists():
        # Try common alternatives
        for candidate in (output_dir / "figures", output_dir / "assets"):
            if candidate.exists():
                images_dir = candidate
                break

    return md_file, images_dir if images_dir.exists() else None


def main():
    parser = argparse.ArgumentParser(description="Extract PDF to Markdown via MinerU online API.")
    parser.add_argument("--pdf", required=True, help="Path to input PDF")
    parser.add_argument("--output", required=True, help="Output directory for raw Markdown and images")
    parser.add_argument("--token", default=None, help="MinerU API token (defaults to MINERU_TOKEN env)")
    parser.add_argument("--model", default="pipeline", help="MinerU model: pipeline, vlm, MinerU-HTML")
    parser.add_argument("--ocr", action="store_true", help="Force OCR mode")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    output_dir = Path(args.output).resolve()

    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    token = args.token or os.environ.get("MINERU_TOKEN")
    if not token:
        print(
            "Error: MINERU_TOKEN not set.\n"
            "Please set it with: export MINERU_TOKEN=your_token\n"
            "Or run: mineru-open-api auth",
            file=sys.stderr,
        )
        return 1

    # Ensure mineru-open-api is available
    if shutil.which("mineru-open-api") is None:
        print("Error: mineru-open-api not found in PATH.", file=sys.stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["MINERU_TOKEN"] = token

    cmd = [
        "mineru-open-api",
        "extract",
        str(pdf_path),
        "-f", "md",
        "-o", str(output_dir),
        "--model", args.model,
    ]
    if args.ocr:
        cmd.append("--ocr")

    print(f"Running: {' '.join(cmd)}")
    rc, stdout, stderr = run_command(cmd, env=env)

    if rc != 0:
        print(f"MinerU extraction failed (code {rc}):\n{stderr}\n{stdout}", file=sys.stderr)
        return 1

    md_file, images_dir = find_extracted_files(output_dir)
    if not md_file:
        print("Error: Could not find extracted Markdown file.", file=sys.stderr)
        return 1

    result = {
        "pdf": str(pdf_path),
        "markdown": str(md_file),
        "images_dir": str(images_dir) if images_dir else None,
        "output_dir": str(output_dir),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
