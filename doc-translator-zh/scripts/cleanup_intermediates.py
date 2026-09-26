#!/usr/bin/env python3
"""Clean up intermediate files after translation is complete.

Removes:
- output/raw/        (raw MinerU extraction output)
- output/pdf_pages/  (temporary PDF page images used for verification)
- script/ temp files matching *.log, temp_*, chunk_*, .tmp

Keeps:
- input/             (original source files)
- output/<final>.md  (translated markdown)
- output/images/     (extracted/used images)
- output/feishu_ready/ (prepared Feishu output, if any)
- script/summary.txt and other non-temp files
"""

import argparse
import json
import shutil
import sys
from pathlib import Path


def remove_dir(path: Path):
    """Remove a directory if it exists."""
    if path.exists():
        shutil.rmtree(path)
        return True
    return False


def clean_temp_files_in_script(script_dir: Path, dry_run: bool = False):
    """Remove (or list) obvious temporary files from script/ directory."""
    removed = []
    seen = set()
    if not script_dir.exists():
        return removed

    temp_patterns = ("*.log", "temp_*", "chunk_*", "*.tmp", "*.bak")
    for pattern in temp_patterns:
        for f in script_dir.glob(pattern):
            if f.is_file() and str(f) not in seen:
                seen.add(str(f))
                removed.append(str(f))
                if not dry_run:
                    f.unlink()
    return removed


def main():
    parser = argparse.ArgumentParser(description="Clean up intermediate translation files.")
    parser.add_argument("--workspace", required=True, help="Workspace root directory")
    parser.add_argument("--keep-raw", action="store_true", help="Keep output/raw/ directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be removed without removing")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    output_dir = workspace / "output"
    script_dir = workspace / "script"

    targets = []

    if not args.keep_raw:
        targets.append(("raw MinerU output", output_dir / "raw"))
    targets.append(("PDF page images", output_dir / "pdf_pages"))

    result = {
        "workspace": str(workspace),
        "dry_run": args.dry_run,
        "removed_dirs": [],
        "removed_script_files": [],
    }

    for name, path in targets:
        if path.exists():
            if args.dry_run:
                result["removed_dirs"].append(f"[would remove] {name}: {path}")
            else:
                shutil.rmtree(path)
                result["removed_dirs"].append(f"{name}: {path}")

    if args.dry_run:
        temp_files = clean_temp_files_in_script(script_dir, dry_run=True)
        result["removed_script_files"] = [f"[would remove] {f}" for f in temp_files]
    else:
        result["removed_script_files"] = clean_temp_files_in_script(script_dir, dry_run=False)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
