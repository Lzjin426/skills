#!/usr/bin/env python3
"""Aggregate and structure collected daily data from all sources.

Reads JSON outputs from collect_claude_history.py, collect_codex_history.py,
collect_remote_history.py, and optional Linear/TickTick MCP data.

Produces a structured JSON that an LLM can read to generate a concise,
summarized daily report (NOT a direct Markdown output — the summarization
should be done by the AI using this skill).

Output JSON structure:
{
  "date": "YYYY-MM-DD",
  "linear_issues": [...],
  "ticktick_tasks": [...],
  "projects": {
    "ProjectName": {
      "themes": [
        {"name": "主题名", "inputs": [...], "keywords": [...]}
      ],
      "source": ["local"]
    }
  },
  "remote_status": {"reachable": true|false, "host": "...", "note": "..."}
}
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Aggregate daily data into structured JSON")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--claude", help="Path to collect_claude_history.py output JSON")
    parser.add_argument("--codex", help="Path to collect_codex_history.py output JSON")
    parser.add_argument("--remote", help="Path to collect_remote_history.py output JSON")
    parser.add_argument("--linear", help="Path to Linear issues JSON (from MCP)")
    parser.add_argument("--ticktick", help="Path to TickTick tasks JSON (from MCP)")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    return parser.parse_args()


def load_json(path: str | None) -> dict | None:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    with p.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def extract_project_name(cwd: str, git_repo: str = "", git_branch: str = "") -> str:
    """Extract a readable project name from git metadata or cwd path.

    Priority:
    1. git_repo if available
    2. git_branch (if not main/master) appended to repo name for context
    3. cwd path fallback
    """
    # Use git repo name as primary project identifier
    if git_repo:
        project = git_repo
        # Append branch if it's a feature/work branch (not main/master)
        if git_branch and git_branch not in ("main", "master", "HEAD"):
            project = f"{git_repo} ({git_branch})"
        return project

    # Fallback: extract from cwd
    if not cwd:
        return "其他"
    parts = [p for p in cwd.replace("\\", "/").split("/") if p]
    if not parts:
        return "其他"
    skip = {"users", "fullstop", "desktop", "documents", "code", "workspace", "home"}
    for part in reversed(parts):
        lower = part.lower()
        if lower not in skip and not lower.startswith("."):
            return part
    return "其他"


# ── 1. 增强输入过滤 ──────────────────────────────────────────────

SKIP_PATTERNS = [
    re.compile(r"^(你好|在吗|hi|hello|hey)\b", re.I),
    re.compile(r"^(谢谢|thanks|thx)\b", re.I),
    re.compile(r"^(ok|okay|好的|行|嗯|确认|知道|明白)\b", re.I),
    re.compile(r"^(claude|codex)\b", re.I),
    re.compile(r"^(给我|帮我|请)\s+(看看|查一下|找一下)\b", re.I),
    # 纯命令/探索性查询
    re.compile(r"^(ls|cd|cat|pwd|echo|rm|mkdir|touch|grep|find|git\s+status|git\s+log|git\s+diff)\s*$", re.I),
    re.compile(r"^(open|查看|打开|运行|执行)\s+.*$", re.I),
    # 纯路径引用（无上下文）
    re.compile(r"^(/Users/[^\s]+|/home/[^\s]+|\w:\\[^\s]+)\s*$"),
    # 纯数字/单字
    re.compile(r"^\d+$"),
    re.compile(r"^[\d\s]+$"),
]

# 纯 skill 调用（无额外内容）
PURE_SKILL_PATTERN = re.compile(r"^/[a-zA-Z0-9_\-:]+$")


def is_significant_input(text: str) -> bool:
    """Judge whether a user input is worth recording."""
    if not text or len(text.strip()) < 15:
        return False
    stripped = text.strip()
    if PURE_SKILL_PATTERN.match(stripped):
        return False
    for pattern in SKIP_PATTERNS:
        if pattern.match(stripped):
            return False
    return True


# ── 2. 主题聚类 ──────────────────────────────────────────────────

# 主题 → 触发关键词（任意匹配即归入该主题）
THEME_KEYWORDS: dict[str, list[str]] = {
    "输出层重构": ["output", "a_output", "输出", "结果", "归档", "统一接口"],
    "版本控制": ["git", "提交", "commit", "分支", "merge", "pull", "push"],
    "MATLAB MCP": ["matlab", "mcp"],
    "开发规范": ["claude.md", "规范", "提交规范", "前缀", "git 提交"],
    "文档整理": ["paper", "论文", "文档", "整理", "文件夹", "分类"],
    "工具配置": ["安装", "配置", "hud", "cli", "bridge", "webbridge"],
    "调研": ["调研", "了解", "看看", "方案", "对比", "评估"],
    "代码审查": ["review", "审查", "检查", "code review"],
    "环境清理": ["清理", "删除", "移除", "废弃", "弃用", "venv", "环境"],
    "调试排查": ["bug", "修复", "问题", "报错", "调试", "排查", "错误"],
}


def extract_keywords(text: str) -> set[str]:
    """从文本中提取所有匹配的主题关键词。"""
    lower = text.lower()
    matched = set()
    for theme, keywords in THEME_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in lower:
                matched.add(theme)
                break
    return matched


def _theme_score(text: str, theme: str) -> int:
    """计算文本与主题的匹配分数：命中关键词数 * 10 + 文本长度/10。"""
    keywords = THEME_KEYWORDS.get(theme, [])
    hits = sum(1 for kw in keywords if kw.lower() in text.lower())
    return hits * 10 + len(text) // 10


def cluster_inputs_by_theme(inputs: list[str]) -> list[dict]:
    """将输入按主题聚类，每条输入只分配到最匹配的主题，每个主题保留 2 条最具代表性的输入。"""
    # 先为每条输入找到最佳匹配主题
    themed: dict[str, list[tuple[str, int]]] = {}  # theme -> [(input, score), ...]
    unclassified: list[str] = []

    for inp in inputs:
        all_themes = list(THEME_KEYWORDS.keys())
        scores = [(t, _theme_score(inp, t)) for t in all_themes]
        scores.sort(key=lambda x: x[1], reverse=True)

        best_theme, best_score = scores[0]
        if best_score >= 10:  # 至少命中 1 个关键词
            themed.setdefault(best_theme, []).append((inp, _theme_score(inp, best_theme)))
        else:
            unclassified.append(inp)

    # 每个主题保留得分最高的 2 条
    result = []
    for theme, items in sorted(themed.items()):
        items.sort(key=lambda x: x[1], reverse=True)
        kept = [inp for inp, _ in items[:2]]
        result.append({
            "name": theme,
            "inputs": kept,
            "keywords": list(THEME_KEYWORDS.get(theme, [])),
        })

    # 未分类的单独处理：最多保留 3 条最长的
    if unclassified:
        unclassified.sort(key=len, reverse=True)
        result.append({
            "name": "其他",
            "inputs": unclassified[:3],
            "keywords": [],
        })

    return result


# ── 3. 问答链压缩 ────────────────────────────────────────────────

def compress_qa_chain(inputs: list[str]) -> list[str]:
    """压缩同一主题的连续问答链，保留最具代表性的一条。"""
    if len(inputs) <= 1:
        return inputs

    compressed = []
    i = 0
    while i < len(inputs):
        current = inputs[i]
        current_themes = extract_keywords(current)
        chain = [current]
        j = i + 1
        while j < len(inputs):
            next_themes = extract_keywords(inputs[j])
            # 如果共享至少一个主题，或都是未分类但前30字符相似度>50%
            shared = current_themes & next_themes
            if shared:
                chain.append(inputs[j])
                j += 1
            else:
                # 检查前 30 字符相似度
                prefix_a = current[:30].lower()
                prefix_b = inputs[j][:30].lower()
                if prefix_a and prefix_b:
                    common = sum(1 for a, b in zip(prefix_a, prefix_b) if a == b)
                    min_len = min(len(prefix_a), len(prefix_b))
                    if min_len > 0 and common / min_len > 0.5:
                        chain.append(inputs[j])
                        j += 1
                        current_themes = current_themes | next_themes
                    else:
                        break
                else:
                    break

        # 从链中选一条：优先选最长的（通常包含完整指令或结论）
        if len(chain) > 1:
            chain.sort(key=len, reverse=True)
            compressed.append(chain[0])
        else:
            compressed.append(current)
        i = j

    return compressed


# ── 4. 改进去重 ──────────────────────────────────────────────────

def similarity(a: str, b: str) -> float:
    """计算两条输入的相似度（基于最长公共子串比例）。"""
    a, b = a.lower().strip(), b.lower().strip()
    if not a or not b:
        return 0.0
    # 简化版：基于公共子串
    shorter, longer = (a, b) if len(a) < len(b) else (b, a)
    if not shorter:
        return 0.0

    # 使用滑动窗口找最长公共子串
    max_len = 0
    for i in range(len(shorter)):
        for j in range(i + 1, len(shorter) + 1):
            substr = shorter[i:j]
            if substr in longer:
                max_len = max(max_len, j - i)

    return max_len / max(len(a), len(b))


def deduplicate_inputs(inputs: list[str]) -> list[str]:
    """去重：相似度 > 60% 的视为重复，保留较长的一条。"""
    unique = []
    for inp in inputs:
        is_dup = False
        for existing in unique:
            if similarity(inp, existing) > 0.6:
                # 保留较长的
                if len(inp) > len(existing):
                    unique[unique.index(existing)] = inp
                is_dup = True
                break
        if not is_dup:
            unique.append(inp)
    return unique


# ── 5. 主构建逻辑 ────────────────────────────────────────────────

def build_structured_data(
    target_date: date,
    claude_data: dict | None,
    codex_data: dict | None,
    remote_data: dict | None,
    linear_data: dict | None,
    ticktick_data: dict | None,
) -> dict:
    """Build the structured output from all data sources."""

    # Linear issues
    linear_issues = []
    if linear_data:
        issues = linear_data.get("issues", linear_data.get("data", []))
        for issue in issues:
            linear_issues.append({
                "identifier": issue.get("identifier", ""),
                "title": issue.get("title", ""),
                "state": issue.get("state", {}).get("name", ""),
                "priority": issue.get("priority", ""),
                "url": issue.get("url", ""),
                "assignee": issue.get("assignee", {}).get("name", "") if issue.get("assignee") else "",
            })

    # TickTick tasks
    ticktick_tasks = []
    if ticktick_data:
        tasks = ticktick_data.get("tasks", [])
        for task in tasks:
            ticktick_tasks.append({
                "title": task.get("title", ""),
                "status": task.get("status", ""),
                "due_date": task.get("dueDate", ""),
            })

    # Projects: collect raw inputs first
    projects_raw: dict[str, list[str]] = {}

    def add_input(proj: str, text: str) -> None:
        if not is_significant_input(text):
            return
        projects_raw.setdefault(proj, []).append(text)

    # Local Claude Code
    if claude_data:
        for sess in claude_data.get("sessions", []):
            proj = extract_project_name(
                sess.get("cwd", ""),
                sess.get("git_repo", ""),
                sess.get("git_branch", ""),
            )
            session_inputs = []
            for inp in sess.get("inputs", []):
                text = inp.get("text", "")
                if is_significant_input(text):
                    session_inputs.append(text)
            # 先压缩问答链
            compressed = compress_qa_chain(session_inputs)
            for text in compressed:
                add_input(proj, text)

    # Local Codex
    if codex_data:
        for sess in codex_data.get("sessions", []):
            proj = extract_project_name(
                sess.get("cwd", ""),
                sess.get("git_repo", ""),
                sess.get("git_branch", ""),
            )
            msgs = [m for m in sess.get("user_messages", []) if is_significant_input(m)]
            compressed = compress_qa_chain(msgs)
            for text in compressed:
                add_input(proj, text)

    # Remote
    remote_status = {"reachable": False, "host": "", "note": ""}
    if remote_data:
        remote_status["reachable"] = remote_data.get("reachable", False)
        remote_status["host"] = remote_data.get("host", "")
        if not remote_status["reachable"]:
            remote_status["note"] = remote_data.get("note", "")

        if remote_status["reachable"]:
            for sess in remote_data.get("claude_sessions", []):
                text = sess.get("display", "")
                if is_significant_input(text):
                    add_input("远程", text)

            for sess in remote_data.get("codex_sessions", []):
                name = sess.get("thread_name", "").strip()
                if name and is_significant_input(name):
                    add_input("远程", name)

    # 去重 + 主题聚类
    projects: dict[str, dict] = {}
    for proj_name, raw_inputs in projects_raw.items():
        deduped = deduplicate_inputs(raw_inputs)
        # 每个项目最多保留 12 条原始输入（去重后）
        deduped = deduped[:12]
        themes = cluster_inputs_by_theme(deduped)
        projects[proj_name] = {
            "themes": themes,
            "source": ["local"] if proj_name != "远程" else ["remote"],
        }

    return {
        "date": args.date,
        "linear_issues": linear_issues,
        "ticktick_tasks": ticktick_tasks,
        "projects": {k: v for k, v in sorted(projects.items())},
        "remote_status": remote_status,
        "_instructions": (
            "This is structured raw data grouped by themes. An LLM should read this and generate "
            "a concise, summarized daily report. For each theme, write 1-2 sentence summaries that "
            "capture the essence of the work, NOT a list of individual operations. "
            "Merge related themes into broader descriptions when possible. "
            "If this is a SUPPLEMENT to an existing report, do NOT repeat top-level headings like "
            "'# 主要内容' or '# 记录'. Instead, append new content directly under the relevant project sections."
        ),
    }


def main():
    global args
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()

    claude_data = load_json(args.claude)
    codex_data = load_json(args.codex)
    remote_data = load_json(args.remote)
    linear_data = load_json(args.linear)
    ticktick_data = load_json(args.ticktick)

    structured = build_structured_data(
        target_date,
        claude_data,
        codex_data,
        remote_data,
        linear_data,
        ticktick_data,
    )

    output = json.dumps(structured, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output)
        print(f"Structured data written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
