#!/usr/bin/env python3
"""Objective grading script for doc-translator-zh outputs.

Checks file existence, workspace structure, image refs, headings, formulas, and OCR noise.
Run this on the output directory of a translation task.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from review_md import (
    find_headings,
    check_heading_hierarchy,
    find_image_refs,
    check_image_refs,
    check_math_delimiters,
    check_formula_numbering,
    check_ocr_noise,
)


def check_heading_numbering(content: str):
    """Check that section headings (level >= 2) have explicit numbering."""
    headings = find_headings(content)
    if len(headings) <= 1:
        return True, "Only one heading (treated as title)"

    title_seen = False
    issues = []
    for level, text, line in headings:
        if level == 1 and not title_seen:
            title_seen = True
            continue
        if not re.match(r"^\d+(\.\d+)*\s+", text):
            issues.append(f"line {line}: '{text}'")

    return len(issues) == 0, issues


def find_markdown_file(output_dir: Path):
    """Find the primary translated Markdown file (not summary.txt or raw/)."""
    candidates = [
        p for p in output_dir.rglob("*.md")
        if p.name != "summary.txt" and "raw" not in p.parts
    ]
    if not candidates:
        return None
    # Prefer files directly under output/ or output/<basename>_zh.md
    for c in candidates:
        if c.parent.name == "output" or "_zh" in c.name:
            return c
    return candidates[0]


def check_workspace_structure(output_dir: Path):
    """Check for input/, output/, script/ folders somewhere under output_dir."""
    has_input = any((p / "input").exists() for p in [output_dir] + list(output_dir.parents))
    has_output = any((p / "output").exists() for p in [output_dir] + list(output_dir.parents))
    has_script = any((p / "script").exists() for p in [output_dir] + list(output_dir.parents))
    return has_input and has_output and has_script


def check_chinese_text(content: str):
    """Check that content contains Chinese characters."""
    return bool(re.search(r"[一-鿿]", content))


def check_formula_syntax(content: str):
    """Check that at least one standard math delimiter exists and delimiters are balanced."""
    has_inline = bool(re.search(r"(?<!\$)\$[^$\n]+\$(?!\$)", content))
    has_block = bool(re.search(r"\$\$[\s\S]+?\$\$", content))
    unbalanced = check_math_delimiters(content)
    return (has_inline or has_block) and len(unbalanced) == 0


def main():
    parser = argparse.ArgumentParser(description="Objective grading for doc-translator-zh output.")
    parser.add_argument("--output-dir", required=True, help="Directory containing run outputs")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--feishu", action="store_true", help="Also check Feishu formatting (numbered headings)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    md_file = find_markdown_file(output_dir)

    results = []

    # 1. Markdown file exists
    if md_file and md_file.exists():
        results.append({
            "text": "A final Chinese Markdown file exists in the output directory.",
            "passed": True,
            "evidence": f"Found {md_file}",
        })
        content = md_file.read_text(encoding="utf-8")
    else:
        results.append({
            "text": "A final Chinese Markdown file exists in the output directory.",
            "passed": False,
            "evidence": f"No Markdown file found in {output_dir}",
        })
        content = ""

    # 2. Contains Chinese text
    if content:
        has_chinese = check_chinese_text(content)
        results.append({
            "text": "The Markdown contains Chinese text translating the original content.",
            "passed": has_chinese,
            "evidence": "Found Chinese characters" if has_chinese else "No Chinese characters found",
        })

    # 3. Workspace structure
    has_structure = check_workspace_structure(output_dir)
    results.append({
        "text": "The workspace contains input/, output/, and script/ folders.",
        "passed": has_structure,
        "evidence": "Workspace structure found" if has_structure else "Missing input/output/script folders",
    })

    # Image and formula checks require content
    if content:
        # Image refs in Markdown are relative to the Markdown file's directory.
        images_dir = md_file.parent if md_file else None
        if not images_dir or not images_dir.exists():
            images_dir = output_dir

        # 4. Image refs resolve
        image_issues = check_image_refs(content, images_dir)
        has_images = len(find_image_refs(content)) > 0
        if has_images:
            results.append({
                "text": "The image reference(s) resolve to existing files.",
                "passed": len(image_issues) == 0,
                "evidence": f"{len(find_image_refs(content))} image refs, {len(image_issues)} missing"
                            + (f"; missing: {[i['message'] for i in image_issues]}" if image_issues else ""),
            })

        # 5. Formula syntax
        formula_ok = check_formula_syntax(content)
        results.append({
            "text": "Formulas use standard Markdown math syntax and are balanced.",
            "passed": formula_ok,
            "evidence": "Standard math delimiters found and balanced" if formula_ok else "Missing or unbalanced math delimiters",
        })

        # 6. Heading hierarchy
        headings = find_headings(content)
        heading_issues = check_heading_hierarchy(headings)
        results.append({
            "text": "Heading hierarchy has no skipped levels.",
            "passed": len(heading_issues) == 0,
            "evidence": f"{len(headings)} headings, {len(heading_issues)} level skips"
                        + (f"; {heading_issues[0]['message']}" if heading_issues else ""),
        })

        # 6.5 Feishu heading numbering
        if args.feishu:
            numbered_ok, numbered_issues = check_heading_numbering(content)
            results.append({
                "text": "Section headings have explicit numbering for Feishu output.",
                "passed": numbered_ok,
                "evidence": "All section headings are numbered" if numbered_ok else f"Missing numbering: {numbered_issues}",
            })

        # 7. Formula numbering (only if there are numbered formulas)
        formula_num_issues = check_formula_numbering(content)
        # Only enforce if we found at least 2 numbered formulas
        numbered = re.findall(r"[（(]\s*\d+\s*[）)]", content)
        if len(numbered) >= 2:
            results.append({
                "text": "Formula numbering is continuous with no missing numbers.",
                "passed": len(formula_num_issues) == 0,
                "evidence": f"{len(numbered)} numbered formulas, issues: {formula_num_issues}" if formula_num_issues else "Numbering is continuous",
            })

        # 8. OCR noise
        noise_issues = check_ocr_noise(content)
        results.append({
            "text": "OCR noise such as isolated page numbers, separator lines, and copyright footers is removed.",
            "passed": len(noise_issues) == 0,
            "evidence": f"{len(noise_issues)} noise patterns detected" + (f"; first: {noise_issues[0]['message']}" if noise_issues else ""),
        })

    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    summary = {
        "expectations": results,
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": passed / total if total else 0,
        },
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Graded {output_dir}")
        print(f"Passed: {passed}/{total}")
        for r in results:
            status = "✅" if r["passed"] else "❌"
            print(f"{status} {r['text']}")
            print(f"   {r['evidence']}")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
