#!/usr/bin/env python3
"""
Supplement markdown report files with OCR text from their images/ directories.

For every markdown file (default: full.md) that has a sibling images/ directory,
run mineru-open-api flash-extract on each image and append the OCR results to a
new file named <original>_complete.md (default: full_complete.md). The original
file is never modified.
"""
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
DEFAULT_MD_NAME = "full.md"
DEFAULT_WORKERS = 2
TIMEOUT_SECONDS = 120


def ocr_image(image_path: Path, language: str = "ch") -> str:
    """Run mineru-open-api flash-extract on a single image and return markdown."""
    cmd = [
        "mineru-open-api",
        "flash-extract",
        str(image_path),
        "--ocr",
        "--language", language,
        "--table",
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
        if result.returncode != 0:
            return f"\n> OCR 失败 (code {result.returncode}): {result.stderr.strip()[:200]}\n"
        text = result.stdout.strip()
        # Remove trailing "Done" if present
        if text.endswith("Done"):
            text = text[:-4].strip()
        return text
    except subprocess.TimeoutExpired:
        return "\n> OCR 超时\n"
    except Exception as e:
        return f"\n> OCR 异常: {e}\n"


def find_report_dirs(base_dir: Path, md_name: str = DEFAULT_MD_NAME, filters=None):
    """Find all directories containing md_name and an images/ subdirectory."""
    reports = []
    for md_path in base_dir.rglob(md_name):
        images_dir = md_path.parent / "images"
        if not images_dir.is_dir():
            continue
        if filters:
            rel = str(md_path.relative_to(base_dir))
            if not any(f in rel for f in filters):
                continue
        reports.append((md_path, images_dir))
    return sorted(reports)


def process_report(md_path: Path, images_dir: Path, max_workers: int = DEFAULT_WORKERS):
    """OCR all images for a report and write a complete markdown file."""
    images = sorted(
        p for p in images_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )

    if not images:
        print(f"[SKIP] 无图片: {md_path}")
        return

    complete_path = md_path.parent / f"{md_path.stem}_complete.md"
    print(f"[PROCESS] {md_path} ({len(images)} 张图片) -> {complete_path}")

    supplements = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_image = {executor.submit(ocr_image, img): img for img in images}
        for future in as_completed(future_to_image):
            img = future_to_image[future]
            text = future.result()
            supplements.append((img.name, text))

    # Stable order by filename
    supplements.sort(key=lambda x: x[0])

    with open(complete_path, "w", encoding="utf-8") as f:
        f.write(md_path.read_text(encoding="utf-8"))
        f.write("\n\n---\n\n")
        f.write("## 图片补充信息（由 mineru 从报告截图 OCR 补充）\n\n")
        for name, text in supplements:
            if not text.strip():
                continue
            f.write(f"### 图片 {name}\n\n")
            f.write(text)
            f.write("\n\n")

    print(f"[DONE] {complete_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Supplement markdown files with OCR from accompanying images."
    )
    parser.add_argument(
        "base_dir",
        nargs="?",
        default=".",
        help="Base directory to search for markdown reports (default: current directory).",
    )
    parser.add_argument(
        "--md-name",
        default=DEFAULT_MD_NAME,
        help="Markdown filename to look for (default: full.md).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help="Concurrent OCR workers per report (default: 2).",
    )
    parser.add_argument(
        "--filter",
        action="append",
        dest="filters",
        help="Only process reports whose relative path contains this string. Can be repeated.",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir).expanduser().resolve()
    reports = find_report_dirs(base_dir, md_name=args.md_name, filters=args.filters)
    print(f"发现 {len(reports)} 个报告目录")
    if args.filters:
        print(f"过滤条件: {args.filters}")

    for md_path, images_dir in reports:
        process_report(md_path, images_dir, max_workers=args.workers)

    print("全部完成")


if __name__ == "__main__":
    main()
