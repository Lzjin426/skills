#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


CITATION_RE = re.compile(r"\[(?:\d+(?:\s*[-,，]\s*\d+)*)\]")
SENTENCE_SPLIT_RE = re.compile(r"[。！？；;]")
HEADING_RE = re.compile(r"^\s*#")

CLAIM_KEYWORDS = (
    "研究",
    "方法",
    "现有",
    "近年来",
    "主要",
    "通常",
    "广泛",
    "已",
    "能够",
    "存在",
    "不足",
    "问题",
    "挑战",
    "提升",
    "降低",
    "适用",
    "效率",
    "精度",
    "鲁棒",
    "一致性",
    "控制",
)

CURRENT_WORK_MARKERS = ("本文", "本研究", "我们", "所提方法", "本方法", "该文")


def iter_paragraphs(text: str):
    lines = text.splitlines()
    start = None
    buf = []
    for idx, line in enumerate(lines, start=1):
        if line.strip():
            if start is None:
                start = idx
            buf.append(line)
        else:
            if buf:
                yield start, "\n".join(buf)
                start = None
                buf = []
    if buf:
        yield start, "\n".join(buf)


def sentence_count(paragraph: str) -> int:
    parts = [p for p in SENTENCE_SPLIT_RE.split(paragraph) if p.strip()]
    return max(1, len(parts))


def has_claim_keyword(paragraph: str) -> bool:
    return any(k in paragraph for k in CLAIM_KEYWORDS)


def has_current_work_marker(paragraph: str) -> bool:
    return any(k in paragraph for k in CURRENT_WORK_MARKERS)


def should_skip(paragraph: str) -> bool:
    stripped = paragraph.strip()
    if not stripped:
        return True
    if HEADING_RE.match(stripped):
        return True
    if len(stripped) < 25:
        return True
    if stripped.startswith("(") or stripped.startswith("（"):
        return True
    if stripped.startswith("![]"):
        return True
    if stripped.startswith("<table>"):
        return True
    if re.match(r"^\[\d+\]", stripped):
        return True
    if stripped.startswith("图") or stripped.startswith("表"):
        return True
    return False


def classify_flags(paragraph: str):
    flags = []
    citations = list(CITATION_RE.finditer(paragraph))
    citation_count = len(citations)
    sent_count = sentence_count(paragraph)

    if citation_count == 0 and has_claim_keyword(paragraph) and not has_current_work_marker(paragraph):
        flags.append("可能缺引用")

    if citation_count == 1 and sent_count >= 4:
        last = citations[0]
        if last.start() > int(len(paragraph) * 0.65):
            flags.append("疑似整段末尾单次补引")

    if citation_count >= 3 and has_current_work_marker(paragraph):
        flags.append("疑似本文句过度补引")

    if citation_count >= sent_count + 2:
        flags.append("引用可能过密")

    return citation_count, sent_count, flags


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Audit citation density and placement in a Chinese draft.")
    parser.add_argument("path", help="Path to a markdown or text draft")
    args = parser.parse_args()

    path = Path(args.path)
    text = path.read_text(encoding="utf-8")

    total_paras = 0
    flagged = 0

    print(f"FILE: {path}")
    print()

    for line_no, para in iter_paragraphs(text):
        if should_skip(para):
            continue
        total_paras += 1
        citation_count, sent_count, flags = classify_flags(para)
        if not flags:
            continue
        flagged += 1
        preview = para.replace("\n", " ")
        if len(preview) > 120:
            preview = preview[:117] + "..."
        print(f"Line {line_no}: sentences={sent_count}, citations={citation_count}, flags={', '.join(flags)}")
        print(f"  {preview}")

    print()
    print(f"Paragraphs checked: {total_paras}")
    print(f"Flagged paragraphs: {flagged}")


if __name__ == "__main__":
    main()
