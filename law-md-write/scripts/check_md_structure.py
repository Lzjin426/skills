#!/usr/bin/env python3
"""只读检查 Markdown 文档的通用结构问题。

默认只做通用结构检查。传入 --attachments-dir 时，额外检查扫描范围内的媒体文件
是否都集中在该附件目录，以及附件引用能否按文件名命中。
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote


DEFAULT_SKIP_DIRS = {".git", ".hg", ".svn", ".obsidian", ".trash", "node_modules"}
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")
NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)(\.?)[ \t]+(.+?)\s*$")
STANDARD_LINK_RE = re.compile(
    r"!?\[[^\]]*\]\(\s*([^\s)]+)(?:\s+[^)]*)?\s*\)"
)
WIKILINK_RE = re.compile(r"!?\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
LOCAL_ABSOLUTE_RE = re.compile(
    r"^(?:file://|[A-Za-z]:[\\/]|/(?:Users|home|private|tmp|var|Volumes)/)"
)
INLINE_CODE_RE = re.compile(r"`+[^`]*`+")

# 附件只按扩展名识别，不猜测任何目录的含义。
MEDIA_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".tif", ".tiff",
    ".pdf", ".xlsx", ".xls", ".csv", ".docx", ".doc", ".pptx", ".ppt",
    ".zip", ".rar", ".7z", ".mp4", ".mov", ".wav", ".mp3",
}
EXTERNAL_PREFIXES = (
    "http://", "https://", "mailto:", "data:", "obsidian://", "#",
)
MARKDOWN_MEDIA_LINK_RE = re.compile(
    r"!?\[[^\]]*\]\(\s*(?:<([^>\n]+)>|([^\s)\n]+))"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="只读检查 Markdown 文档的通用结构问题。"
    )
    parser.add_argument(
        "target",
        type=Path,
        help="要检查的 Markdown 文件或目录；必须显式传入",
    )
    parser.add_argument(
        "--require-h1",
        action="store_true",
        help="要求含标题的独立文档以 H1 起头",
    )
    parser.add_argument(
        "--numbered",
        action="store_true",
        help="要求标题使用连续的 1. / 1.1 / 1.1.1 显式编号",
    )
    parser.add_argument(
        "--skip-dir",
        action="append",
        default=[],
        metavar="NAME",
        help="额外跳过的目录名，可重复指定",
    )
    parser.add_argument(
        "--attachments-dir",
        metavar="NAME",
        help=(
            "附件目录名（相对库根）。传入后额外检查：扫描范围内的媒体文件是否都"
            "集中在该目录，以及附件引用能否按文件名命中"
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="发现问题时以非零状态退出",
    )
    return parser.parse_args()


def iter_markdown_files(target: Path, skip_dirs: set[str]):
    if target.is_file():
        if target.suffix.lower() == ".md":
            yield target, target.parent
        return

    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = sorted(name for name in dirnames if name not in skip_dirs)
        for filename in sorted(filenames):
            if filename.lower().endswith(".md"):
                yield Path(dirpath) / filename, target


def iter_all_files(target: Path, skip_dirs: set[str]):
    """遍历目标下的全部文件；不跟随符号链接目录。"""
    if target.is_file():
        yield target
        return

    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = sorted(name for name in dirnames if name not in skip_dirs)
        for filename in sorted(filenames):
            yield Path(dirpath) / filename


def is_media_file(name: str) -> bool:
    lower = name.lower()
    if lower.endswith((".excalidraw.md", ".excalidraw")):
        return True
    return Path(lower).suffix in MEDIA_SUFFIXES


def build_file_index(root: Path, skip_dirs: set[str]) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in iter_all_files(root, skip_dirs):
        index.setdefault(path.name, []).append(path)
    return index


def resolve_attachments_root(target: Path, name: str) -> "Path | None":
    base = target if target.is_dir() else target.parent
    for candidate in (base, *base.parents):
        if (candidate / name).is_dir():
            return candidate
    return None


def reference_resolves(name: str, index: dict[str, list[Path]]) -> bool:
    if name in index:
        return True
    # Obsidian 的 Excalidraw 嵌入写成 [[图.excalidraw]]，实际文件是 .excalidraw.md。
    if name.lower().endswith(".excalidraw") and (name + ".md") in index:
        return True
    return False


def check_attachment_refs(
    path: Path,
    root: Path,
    text: str,
    index: dict[str, list[Path]],
    issues,
):
    for line_number, line in outside_fence_lines(text):
        if line is None:
            continue

        for match in MARKDOWN_MEDIA_LINK_RE.finditer(line):
            destination = (match.group(1) or match.group(2) or "").strip()
            if not destination or destination.lower().startswith(EXTERNAL_PREFIXES):
                continue
            cleaned = unquote(destination.split("#", 1)[0].split("?", 1)[0])
            name = Path(cleaned).name
            if not is_media_file(name) or reference_resolves(name, index):
                continue
            add_issue(
                issues, "附件引用未解析", path, root, f"L{line_number} {destination[:80]}"
            )

        for match in WIKILINK_RE.finditer(line):
            target_name = unquote(match.group(1).strip())
            name = Path(target_name).name
            if not is_media_file(name) or reference_resolves(name, index):
                continue
            add_issue(
                issues, "附件引用未解析", path, root, f"L{line_number} {target_name[:80]}"
            )


def outside_fence_lines(text: str):
    """Yield (line_number, line) for normal Markdown lines; fence content is None."""
    in_fence = False
    fence_char = ""
    fence_length = 0

    for line_number, line in enumerate(text.splitlines(), 1):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            char = marker[0]
            if not in_fence:
                in_fence = True
                fence_char = char
                fence_length = len(marker)
            elif char == fence_char and len(marker) >= fence_length:
                in_fence = False
                fence_char = ""
                fence_length = 0
            yield line_number, None
        elif in_fence:
            yield line_number, None
        else:
            yield line_number, line


def headings(text: str):
    result = []
    for line_number, line in outside_fence_lines(text):
        if line is None:
            continue
        match = HEADING_RE.match(line)
        if match:
            result.append((line_number, len(match.group(1)), match.group(2)))
    return result


def add_issue(issues, kind: str, path: Path, root: Path, detail: str):
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = path
    issues.append((kind, str(relative), detail))


def check_headings(
    path: Path,
    root: Path,
    text: str,
    require_h1: bool,
    numbered: bool,
    issues,
):
    hs = headings(text)
    if not hs:
        return

    if require_h1 and hs[0][1] != 1:
        add_issue(issues, "首标题不是 H1", path, root, f"H{hs[0][1]} {hs[0][2][:50]}")

    previous_level = 0
    counters = [0] * 7
    for line_number, level, title in hs:
        if previous_level and level > previous_level + 1:
            add_issue(
                issues,
                "标题跳级",
                path,
                root,
                f"L{line_number} H{previous_level}->H{level} {title[:40]}",
            )
        previous_level = level

        if not numbered:
            continue

        counters[level] += 1
        for deeper in range(level + 1, 7):
            counters[deeper] = 0
        expected = ".".join(str(counters[index]) for index in range(1, level + 1))
        if level == 1:
            expected += "."

        match = NUMBER_RE.match(title)
        if not match:
            add_issue(issues, "标题缺少编号", path, root, f"L{line_number} {title[:50]}")
            continue
        actual = match.group(1) + match.group(2)
        if actual != expected:
            add_issue(
                issues,
                "编号不连续",
                path,
                root,
                f"L{line_number} 实{actual} 应{expected}",
            )


def check_body(path: Path, root: Path, text: str, issues):
    blank_lines = 0
    for line_number, line in outside_fence_lines(text):
        if line is None:
            blank_lines = 0
            continue

        if not line.strip():
            blank_lines += 1
            if blank_lines == 3:
                add_issue(issues, "连续空行", path, root, f"L{line_number}")
        else:
            blank_lines = 0

        # 反引号里的是代码或术语引用，不按公式判定。
        without_code = INLINE_CODE_RE.sub("", line)
        if "$$" in without_code and without_code.strip() != "$$":
            add_issue(issues, "行内使用 $$", path, root, f"L{line_number}")
            break

    for line_number, line in outside_fence_lines(text):
        if line is None:
            continue
        for match in STANDARD_LINK_RE.finditer(line):
            destination = match.group(1).strip().strip("<>")
            if LOCAL_ABSOLUTE_RE.match(destination):
                add_issue(
                    issues,
                    "链接使用本机绝对路径",
                    path,
                    root,
                    f"L{line_number} {destination[:80]}",
                )
                break
        else:
            for match in WIKILINK_RE.finditer(line):
                destination = match.group(1).strip()
                if LOCAL_ABSOLUTE_RE.match(destination):
                    add_issue(
                        issues,
                        "链接使用本机绝对路径",
                        path,
                        root,
                        f"L{line_number} {destination[:80]}",
                    )
                    break


def main() -> int:
    args = parse_args()
    target = args.target.expanduser()
    if not target.exists():
        print(f"目标不存在：{target}", file=sys.stderr)
        return 2
    if not target.is_file() and not target.is_dir():
        print(f"目标不是文件或目录：{target}", file=sys.stderr)
        return 2

    skip_dirs = DEFAULT_SKIP_DIRS | set(args.skip_dir)
    issues = []

    index = None
    attachments_root = None
    if args.attachments_dir:
        attachments_root = resolve_attachments_root(target, args.attachments_dir)
        if attachments_root is None:
            print(
                f"未找到附件目录：{args.attachments_dir}（已从 {target} 向上查找）",
                file=sys.stderr,
            )
            return 2
        attachments_dir = (attachments_root / args.attachments_dir).resolve()
        index = build_file_index(attachments_root, skip_dirs)
        scan_base = target if target.is_dir() else target.parent
        for media_path in iter_all_files(scan_base, skip_dirs):
            if not is_media_file(media_path.name):
                continue
            try:
                media_path.resolve().relative_to(attachments_dir)
            except ValueError:
                add_issue(
                    issues,
                    "附件未集中",
                    media_path,
                    attachments_root,
                    "不在附件目录内",
                )

    files = list(iter_markdown_files(target, skip_dirs))
    for path, root in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            add_issue(issues, "无法读取", path, root, str(error))
            continue
        check_headings(path, root, text, args.require_h1, args.numbered, issues)
        check_body(path, root, text, issues)
        if index is not None:
            check_attachment_refs(path, root, text, index, issues)

    print(f"扫描 {len(files)} 篇 Markdown")
    if index is not None:
        print(f"附件目录 {args.attachments_dir}：库根 {attachments_root}，索引 {len(index)} 个文件名")
    if not issues:
        print("无结构问题")
        return 0

    grouped = {}
    for kind, relative, detail in issues:
        grouped.setdefault(kind, []).append((relative, detail))
    for kind, entries in sorted(grouped.items(), key=lambda item: -len(item[1])):
        print(f"\n[{kind}] {len(entries)} 处")
        for relative, detail in entries[:8]:
            print(f"   {relative}  —  {detail}")
        if len(entries) > 8:
            print(f"   … 另外 {len(entries) - 8} 处")

    return 1 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
