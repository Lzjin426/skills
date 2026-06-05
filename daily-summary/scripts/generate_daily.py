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
      "inputs": ["user input 1", "user input 2", ...],
      "codex_sessions": [{"thread_name": "...", "user_messages": [...]}],
      "source": "local|remote|both"
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


def extract_cwd_name(cwd: str) -> str:
    """Extract a readable project name from cwd path."""
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


SKIP_PATTERNS = [
    re.compile(r"^(你好|在吗|hi|hello|hey)\b", re.I),
    re.compile(r"^(谢谢|thanks|thx)\b", re.I),
    re.compile(r"^(ok|okay|好的|行|嗯)\b", re.I),
    re.compile(r"^(claude|codex)\b", re.I),
    re.compile(r"^(给我|帮我|请)\s+(看看|查一下|找一下)\b", re.I),
]

SLASH_COMMAND_PATTERN = re.compile(r"^/[a-zA-Z\-_]+$")


def is_significant_input(text: str) -> bool:
    """Judge whether a user input is worth recording."""
    if not text or len(text) < 5:
        return False
    if SLASH_COMMAND_PATTERN.match(text.strip()):
        return False
    for pattern in SKIP_PATTERNS:
        if pattern.match(text.strip()):
            return False
    return True


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

    # Projects: merge local + remote inputs
    projects: dict[str, dict] = {}

    def ensure_project(name: str) -> dict:
        if name not in projects:
            projects[name] = {
                "inputs": [],
                "codex_sessions": [],
                "source": set(),
            }
        return projects[name]

    # Local Claude Code
    if claude_data:
        for sess in claude_data.get("sessions", []):
            proj = extract_cwd_name(sess.get("cwd", ""))
            p = ensure_project(proj)
            p["source"].add("local")
            for inp in sess.get("inputs", []):
                text = inp.get("text", "")
                if is_significant_input(text):
                    p["inputs"].append(text)

    # Local Codex
    if codex_data:
        for sess in codex_data.get("sessions", []):
            proj = extract_cwd_name(sess.get("cwd", ""))
            p = ensure_project(proj)
            p["source"].add("local")
            msgs = [m for m in sess.get("user_messages", []) if is_significant_input(m)]
            if msgs:
                p["codex_sessions"].append({
                    "thread_name": sess.get("thread_name", ""),
                    "user_messages": msgs,
                })
            p["inputs"].extend(msgs)

    # Remote
    remote_status = {"reachable": False, "host": "", "note": ""}
    if remote_data:
        remote_status["reachable"] = remote_data.get("reachable", False)
        remote_status["host"] = remote_data.get("host", "")
        if not remote_status["reachable"]:
            remote_status["note"] = remote_data.get("note", "")

        if remote_status["reachable"]:
            for sess in remote_data.get("claude_sessions", []):
                # Remote inputs don't have cwd, so group as "远程"
                p = ensure_project("远程")
                p["source"].add("remote")
                text = sess.get("display", "")
                if is_significant_input(text):
                    p["inputs"].append(text)

            for sess in remote_data.get("codex_sessions", []):
                p = ensure_project("远程")
                p["source"].add("remote")
                name = sess.get("thread_name", "").strip()
                if name:
                    p["codex_sessions"].append({"thread_name": name, "user_messages": []})

    # Deduplicate inputs within each project
    for proj_name, proj_data in projects.items():
        seen = set()
        unique = []
        for inp in proj_data["inputs"]:
            key = inp.lower().strip()
            if key and key not in seen and not any(key in existing or existing in key for existing in seen):
                seen.add(key)
                unique.append(inp)
        proj_data["inputs"] = unique[:15]  # Cap at 15 per project
        proj_data["source"] = sorted(proj_data["source"])

    return {
        "date": args.date,
        "linear_issues": linear_issues,
        "ticktick_tasks": ticktick_tasks,
        "projects": {k: v for k, v in sorted(projects.items())},
        "remote_status": remote_status,
        "_instructions": (
            "This is structured raw data. An LLM should read this and generate "
            "a concise, summarized daily report. Do NOT list raw inputs as bullets. "
            "Instead, group related inputs by theme and write 1-2 sentence summaries. "
            "Each bullet should capture the essence of what was accomplished or decided, "
            "not repeat the user's original wording."
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
