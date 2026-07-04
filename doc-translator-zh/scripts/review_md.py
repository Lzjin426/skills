#!/usr/bin/env python3
"""Automated review of translated Markdown for common OCR and formatting issues."""

import argparse
import json
import re
import sys
from pathlib import Path


def find_headings(content: str):
    """Return list of (level, text, line_number)."""
    headings = []
    for i, line in enumerate(content.splitlines(), start=1):
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append((level, text, i))
    return headings


def check_heading_hierarchy(headings):
    """Detect skipped heading levels (e.g., # -> ###)."""
    issues = []
    prev_level = 0
    for level, text, line in headings:
        if prev_level > 0 and level > prev_level + 1:
            issues.append({
                "type": "heading_skip",
                "line": line,
                "message": f"Heading level jumps from {prev_level} to {level}: '{text}'",
            })
        prev_level = level
    return issues


def find_image_refs(content: str):
    """Find Markdown image references: ![alt](path)."""
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    return [(m.group(2), m.start()) for m in re.finditer(pattern, content)]


def check_image_refs(content: str, images_dir: Path):
    """Check that image references point to existing files."""
    issues = []
    refs = find_image_refs(content)
    lines = content.splitlines()

    for ref, pos in refs:
        # Count line number from position
        line_num = content[:pos].count("\n") + 1
        # Resolve relative to markdown file location
        if images_dir:
            candidate = images_dir / ref
        else:
            candidate = Path(ref)

        if not candidate.exists():
            issues.append({
                "type": "missing_image",
                "line": line_num,
                "message": f"Image not found: '{ref}' (looked at {candidate})",
            })
    return issues


def check_math_delimiters(content: str):
    """Check for unbalanced $ and $$ delimiters."""
    issues = []
    lines = content.splitlines()
    for i, line in enumerate(lines, start=1):
        # Count single $ not inside $$
        # Simple heuristic: remove $$ pairs first
        simplified = line.replace("$$", "")
        singles = simplified.count("$")
        if singles % 2 != 0:
            issues.append({
                "type": "unbalanced_inline_math",
                "line": i,
                "message": f"Possibly unbalanced inline math delimiters: {line.strip()[:80]}",
            })
    return issues


def check_formula_numbering(content: str):
    """Detect gaps in formula numbers like (1), (2), (4)."""
    issues = []
    # Match Chinese or Arabic formula labels at end of math blocks or lines
    pattern = re.compile(r"[（(]\s*(\d+)\s*[）)]")
    numbers = []
    lines = content.splitlines()
    for i, line in enumerate(lines, start=1):
        for m in pattern.finditer(line):
            numbers.append((int(m.group(1)), i))

    if len(numbers) < 2:
        return issues

    nums_only = [n for n, _ in numbers]
    expected = list(range(min(nums_only), max(nums_only) + 1))
    missing = [n for n in expected if n not in nums_only]
    if missing:
        issues.append({
            "type": "missing_formula_number",
            "line": numbers[-1][1],
            "message": f"Possibly missing formula numbers: {missing}",
        })
    return issues


def check_ocr_noise(content: str):
    """Detect common OCR noise patterns."""
    issues = []
    lines = content.splitlines()

    noise_patterns = [
        (re.compile(r"^\s*\d+\s*$"), "isolated_page_number"),
        (re.compile(r"^\s*[-=_]{3,}\s*$"), "separator_line"),
        (re.compile(r"^[\s\d]*第\s*\d+\s*[页页].*$"), "page_header_footer"),
        (re.compile(r"^\s*Copyright\s*[©®]?.*$", re.IGNORECASE), "copyright_footer"),
    ]

    for i, line in enumerate(lines, start=1):
        for pattern, issue_type in noise_patterns:
            if pattern.match(line):
                issues.append({
                    "type": issue_type,
                    "line": i,
                    "message": f"Possible OCR noise: {line.strip()[:80]}",
                })
    return issues


def main():
    parser = argparse.ArgumentParser(description="Review translated Markdown for quality issues.")
    parser.add_argument("--md", required=True, help="Path to Markdown file to review")
    parser.add_argument("--images", default=None, help="Directory containing images")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    md_path = Path(args.md)
    images_dir = Path(args.images) if args.images else md_path.parent / "images"

    if not md_path.exists():
        print(f"Error: Markdown file not found: {md_path}", file=sys.stderr)
        return 1

    content = md_path.read_text(encoding="utf-8")

    headings = find_headings(content)
    issues = []
    issues.extend(check_heading_hierarchy(headings))
    issues.extend(check_image_refs(content, images_dir))
    issues.extend(check_math_delimiters(content))
    issues.extend(check_formula_numbering(content))
    issues.extend(check_ocr_noise(content))

    result = {
        "markdown": str(md_path),
        "images_dir": str(images_dir) if images_dir.exists() else None,
        "heading_count": len(headings),
        "issue_count": len(issues),
        "issues": issues,
        "passed": len(issues) == 0,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Reviewed: {md_path}")
        print(f"Headings: {len(headings)}")
        print(f"Issues found: {len(issues)}")
        for issue in issues:
            print(f"  [line {issue['line']}] {issue['type']}: {issue['message']}")
        if result["passed"]:
            print("✅ Passed automated review.")
        else:
            print("❌ Please fix the issues above.")

    return 0 if result["passed"] else 2


if __name__ == "__main__":
    sys.exit(main())
