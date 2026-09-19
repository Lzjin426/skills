#!/usr/bin/env python3
"""Validate the compact structure of a generated personal daily note."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def validate_report(text: str, *, max_bullets: int = 10, allow_detailed: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    top_headings: list[str] = []
    project_headings: list[str] = []
    bullet_count = 0
    bullets_by_section: dict[str, int] = {}
    bullet_texts: list[str] = []
    current_section = ""

    for line_number, line in enumerate(text.splitlines(), start=1):
        if re.match(r"^#\s+", line):
            heading = re.sub(r"^#\s+", "", line).strip()
            top_headings.append(heading)
            if heading not in {"主要内容", "记录", "其他"}:
                warnings.append(f"line {line_number}: unexpected top-level heading {heading!r}")
            current_section = heading
        elif re.match(r"^##\s+", line):
            heading = re.sub(r"^##\s+", "", line).strip()
            project_headings.append(heading)
            current_section = heading
        elif re.match(r"^\s*[-*+]\s+", line):
            bullet_count += 1
            bullets_by_section[current_section] = bullets_by_section.get(current_section, 0) + 1
            bullet_texts.append(re.sub(r"^\s*[-*+]\s+", "", line).strip())

    if top_headings.count("主要内容") != 1:
        errors.append("report must contain exactly one '# 主要内容'")
    if top_headings.count("记录") > 1:
        errors.append("report must contain at most one '# 记录'")
    if top_headings.count("其他") > 1:
        errors.append("report must contain at most one '# 其他'")
    duplicates = sorted({heading for heading in project_headings if project_headings.count(heading) > 1})
    if duplicates:
        errors.append(f"duplicate project headings: {', '.join(duplicates)}")
    duplicate_bullets = sorted({text for text in bullet_texts if bullet_texts.count(text) > 1 and text})
    if duplicate_bullets:
        errors.append("duplicate bullet content detected; merge instead of appending a second copy")
    if bullet_count > max_bullets and not allow_detailed:
        warnings.append(f"report has {bullet_count} bullets; normal target is <= {max_bullets}")
    if len(project_headings) > 4:
        warnings.append(f"report has {len(project_headings)} project headings; merge related work when possible")
    if any(count > 3 for count in bullets_by_section.values()):
        warnings.append("a project section has more than 3 bullets; keep only action-relevant detail")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "top_headings": top_headings,
        "project_headings": project_headings,
        "bullet_count": bullet_count,
        "bullets_by_section": bullets_by_section,
        "duplicate_bullets": duplicate_bullets,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a daily-summary Markdown report")
    parser.add_argument("--file", required=True, help="Markdown report path")
    parser.add_argument("--allow-detailed", action="store_true")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return a failure exit code when compactness warnings remain",
    )
    args = parser.parse_args()
    result = validate_report(Path(args.file).read_text(encoding="utf-8"), allow_detailed=args.allow_detailed)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    failed = not result["valid"] or (args.strict and bool(result["warnings"]))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
