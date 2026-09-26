#!/usr/bin/env python3
"""Clean up temporary PDF page images after translation is complete."""

import argparse
import json
import shutil
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Remove temporary PDF page images.")
    parser.add_argument("--workspace", required=True, help="Workspace root directory")
    parser.add_argument("--pdf-pages", default=None, help="Path to pdf_pages directory (default: workspace/output/pdf_pages)")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    pdf_pages_dir = Path(args.pdf_pages).resolve() if args.pdf_pages else workspace / "output" / "pdf_pages"

    removed = False
    if pdf_pages_dir.exists():
        shutil.rmtree(pdf_pages_dir)
        removed = True

    result = {
        "pdf_pages_dir": str(pdf_pages_dir),
        "removed": removed,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
