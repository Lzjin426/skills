#!/usr/bin/env python3
"""Lightweight lint for knowledge-base Markdown drafts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")


@dataclass
class Issue:
    level: str
    code: str
    message: str


def visible_len(text: str) -> int:
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", "", text)
    text = re.sub(r"\s+", "", text)
    return len(text)


def split_sections(lines: list[str]) -> tuple[list[tuple[int, str]], list[dict]]:
    headings: list[tuple[int, str]] = []
    sections: list[dict] = []
    current = {"level": 0, "title": "__lead__", "lines": []}

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            sections.append(current)
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append((level, title))
            current = {"level": level, "title": title, "lines": []}
        else:
            current["lines"].append(line)
    sections.append(current)
    return headings, sections


def lint(text: str) -> dict:
    lines = text.splitlines()
    headings, sections = split_sections(lines)
    issues: list[Issue] = []

    h1 = [title for level, title in headings if level == 1]
    h2 = [title for level, title in headings if level == 2]
    h3 = [title for level, title in headings if level == 3]
    max_depth = max([level for level, _ in headings], default=0)

    if len(h1) > 1:
        issues.append(Issue("warn", "multiple_h1", f"Found {len(h1)} H1 headings; knowledge docs usually need one title."))
    if len(h2) > 9:
        issues.append(Issue("warn", "too_many_h2", f"Found {len(h2)} H2 headings; consider merging shallow sections."))
    if max_depth > 4:
        issues.append(Issue("warn", "deep_heading_tree", f"Heading depth reaches H{max_depth}; deep trees often become fragmented."))

    short_sections = []
    empty_sections = []
    meta_title_re = re.compile(r"(参考|来源|延伸阅读|references|sources)", re.IGNORECASE)
    for section in sections:
        if section["title"] == "__lead__" or section["level"] == 1:
            continue
        if meta_title_re.search(section["title"]):
            continue
        body = "\n".join(section["lines"]).strip()
        length = visible_len(body)
        if length == 0:
            empty_sections.append(section["title"])
        elif section["level"] <= 3 and length < 120:
            short_sections.append((section["title"], length))

    if empty_sections:
        issues.append(Issue("error", "empty_sections", "Empty sections: " + "; ".join(empty_sections[:8])))
    if len(short_sections) >= 3:
        detail = "; ".join(f"{title}({length})" for title, length in short_sections[:8])
        issues.append(Issue("warn", "many_short_sections", f"Found {len(short_sections)} short sections: {detail}"))

    list_lines = sum(1 for line in lines if LIST_RE.match(line))
    nonblank_lines = sum(1 for line in lines if line.strip())
    bullet_ratio = list_lines / nonblank_lines if nonblank_lines else 0.0
    if bullet_ratio > 0.38 and nonblank_lines > 30:
        issues.append(Issue("warn", "bullet_heavy", f"List lines are {bullet_ratio:.0%} of nonblank lines; check for bullet-soup writing."))

    reference_words = ("参考", "来源", "References", "参考资料", "延伸阅读", "Source")
    if not any(word in text for word in reference_words):
        issues.append(Issue("warn", "missing_sources", "No obvious references/source section found."))

    visual_words = ("图", "diagram", "mermaid", "svg", "图片", "流程图", "结构图", "示意")
    if visible_len(text) > 2500 and not any(word.lower() in text.lower() for word in visual_words):
        issues.append(Issue("warn", "missing_visual_plan", "Long abstract draft has no obvious visual or diagram plan."))

    ai_phrases = ["值得注意的是", "总而言之", "综上所述", "在当今", "随着技术的发展", "具有重要意义"]
    found_phrases = [phrase for phrase in ai_phrases if phrase in text]
    if found_phrases:
        issues.append(Issue("info", "possible_ai_phrases", "Review generic phrases: " + ", ".join(found_phrases)))

    return {
        "stats": {
            "characters": visible_len(text),
            "h1": len(h1),
            "h2": len(h2),
            "h3": len(h3),
            "max_heading_depth": max_depth,
            "list_lines": list_lines,
            "nonblank_lines": nonblank_lines,
            "bullet_ratio": round(bullet_ratio, 3),
        },
        "issues": [asdict(issue) for issue in issues],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a Markdown knowledge-base draft for shallow structure and missing basics.")
    parser.add_argument("path", nargs="?", help="Markdown file path. Reads stdin when omitted or '-'.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args()

    if not args.path or args.path == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.path).read_text(encoding="utf-8")

    result = lint(text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Knowledge Doc Outline Lint")
        print(json.dumps(result["stats"], ensure_ascii=False, indent=2))
        if result["issues"]:
            print("\nIssues:")
            for issue in result["issues"]:
                print(f"- [{issue['level']}] {issue['code']}: {issue['message']}")
        else:
            print("\nNo issues found.")
    return 1 if any(issue["level"] == "error" for issue in result["issues"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
