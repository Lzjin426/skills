#!/usr/bin/env python3
"""Render each page of a PDF to a PNG image at 200 DPI.

Output files are named page_001.png, page_002.png, etc.
"""

import argparse
import json
import sys
from pathlib import Path


def pdf_to_images(pdf_path: Path, output_dir: Path, dpi: int = 200):
    """Render all pages of a PDF to PNG images."""
    try:
        import fitz  # PyMuPDF
    except ImportError as e:
        raise RuntimeError("PyMuPDF (fitz) is required. Install: pip install pymupdf") from e

    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    images = []

    # PyMuPDF uses a default 72 DPI; scale factor = dpi / 72
    scale = dpi / 72.0
    matrix = fitz.Matrix(scale, scale)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=matrix)
        filename = f"page_{page_num + 1:03d}.png"
        output_path = output_dir / filename
        pix.save(str(output_path))
        images.append(str(output_path))

    doc.close()
    return images


def main():
    parser = argparse.ArgumentParser(description="Render PDF pages to PNG images at 200 DPI.")
    parser.add_argument("--pdf", required=True, help="Path to input PDF")
    parser.add_argument("--output", required=True, help="Output directory for page images")
    parser.add_argument("--dpi", type=int, default=300, help="Rendering DPI (default: 300)")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    output_dir = Path(args.output).resolve()

    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    try:
        images = pdf_to_images(pdf_path, output_dir, dpi=args.dpi)
    except Exception as e:
        print(f"Error rendering PDF: {e}", file=sys.stderr)
        return 1

    result = {
        "pdf": str(pdf_path),
        "output_dir": str(output_dir),
        "dpi": args.dpi,
        "page_count": len(images),
        "images": images,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
