#!/usr/bin/env python3
"""Prepare translated Markdown + images for Feishu output."""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


def collect_images(md_content: str, md_path: Path, images_dir: Path):
    """Find all image references and resolve them to actual files."""
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    refs = []
    for m in re.finditer(pattern, md_content):
        alt, src = m.group(1), m.group(2)
        refs.append({"alt": alt, "src": src})
    return refs


def number_headings(content: str) -> str:
    """Add explicit numbering to section headings for Feishu documents.

    The document title (first # heading) is left unnumbered.
    Heading numbering follows outline style: 1, 1.1, 1.1.1.
    """
    heading_re = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
    counters = [0, 0, 0, 0, 0, 0]  # indexes 0..5 map to levels 1..6
    title_seen = False

    def replace_heading(match):
        nonlocal title_seen
        hashes = match.group(1)
        text = match.group(2).strip()
        level = len(hashes)

        # First level-1 heading is the document title; do not number it.
        if level == 1 and not title_seen:
            title_seen = True
            return match.group(0)

        # Increment counter for current level and reset lower levels.
        counters[level - 1] += 1
        for i in range(level, 6):
            counters[i] = 0

        # Build number string from active counters up to current level.
        number = ".".join(str(counters[i]) for i in range(level) if counters[i] > 0)

        # Remove any existing leading number like "1 ", "1.1 " to avoid duplication.
        text = re.sub(r"^\d+(\.\d+)*\s*", "", text)

        return f"{hashes} {number} {text}"

    return heading_re.sub(replace_heading, content)


def prepare_feishu_folder(md_path: Path, images_dir: Path, output_dir: Path, number_headings_flag: bool = False):
    """Copy md + images into a self-contained folder with relative paths."""
    output_dir.mkdir(parents=True, exist_ok=True)

    md_name = md_path.name
    out_md = output_dir / md_name
    out_images = output_dir / "images"
    out_images.mkdir(exist_ok=True)

    content = md_path.read_text(encoding="utf-8")

    if number_headings_flag:
        content = number_headings(content)

    # Track which images we found
    found_images = []
    missing_images = []

    def replace_ref(match):
        alt, src = match.group(1), match.group(2)
        original = src
        # Strip URL fragments / queries for local files
        src_path = src.split("?")[0].split("#")[0]
        src_path = Path(src_path)

        if src_path.is_absolute():
            candidate = src_path
        else:
            candidate = images_dir / src_path
            if not candidate.exists():
                candidate = md_path.parent / src_path

        if candidate.exists():
            # Preserve the original directory structure relative to the markdown file.
            if "/" in original or "\\" in original:
                rel_parts = Path(original.replace("\\", "/")).parts
                dest_dir = output_dir
                for part in rel_parts[:-1]:
                    dest_dir = dest_dir / part
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / rel_parts[-1]
            else:
                dest = out_images / candidate.name
            if not dest.exists():
                shutil.copy2(candidate, dest)
            found_images.append(str(candidate))
            return f"![{alt}]({original})"
        else:
            missing_images.append(original)
            return match.group(0)

    new_content = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_ref, content)
    out_md.write_text(new_content, encoding="utf-8")

    return out_md, out_images, found_images, missing_images


def main():
    parser = argparse.ArgumentParser(description="Prepare Markdown + images for Feishu.")
    parser.add_argument("--md", required=True, help="Path to translated Markdown")
    parser.add_argument("--images", required=True, help="Directory containing images")
    parser.add_argument("--mode", choices=["create_doc", "upload_md"], default="create_doc",
                        help="create_doc: generate Feishu doc; upload_md: upload raw md")
    parser.add_argument("--output", default=None, help="Output directory for Feishu-ready files")
    parser.add_argument("--number-headings", action="store_true",
                        help="Add explicit section numbering to headings for Feishu docs")
    args = parser.parse_args()

    md_path = Path(args.md).resolve()
    images_dir = Path(args.images).resolve()

    if not md_path.exists():
        print(f"Error: Markdown file not found: {md_path}", file=sys.stderr)
        return 1

    if args.output:
        output_dir = Path(args.output).resolve()
    else:
        output_dir = md_path.parent / "feishu_ready"

    out_md, out_images, found, missing = prepare_feishu_folder(
        md_path, images_dir, output_dir, number_headings_flag=args.number_headings
    )

    result = {
        "mode": args.mode,
        "source_md": str(md_path),
        "source_images": str(images_dir),
        "feishu_ready_md": str(out_md),
        "feishu_ready_images": str(out_images),
        "images_found": len(found),
        "images_missing": missing,
        "next_step": "create_doc" if args.mode == "create_doc" else "upload_md",
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if missing:
        print(f"\nWarning: {len(missing)} image(s) could not be resolved:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
