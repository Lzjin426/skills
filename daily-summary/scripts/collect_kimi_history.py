#!/usr/bin/env python3
"""Collect Kimi Code local conversation history for a specific date.

Kimi Code (CLI) stores sessions under:
  ~/.kimi-code/sessions/<wd-sanitized>/session_<uuid>/
      state.json            # cwd, title, createdAt/updatedAt, forkedFrom
      agents/<name>/wire.jsonl   # wire protocol records (turn.prompt etc.)

Legacy/alternate location (also scanned):
  ~/.kimi/sessions/<root>/<session-id>/... wire.jsonl / context.jsonl

This script extracts user prompts (turn.prompt) that fall on the target date,
deduplicating fork-inherited history: forked sessions replay the parent's
prompts verbatim, so the same (timestamp, text) pair is kept only once.

Output: JSON with the same shape as collect_codex_history.py.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

TZ = timezone(timedelta(hours=8))

DEFAULT_ROOTS = ["~/.kimi-code", "~/.kimi"]


def parse_args():
    parser = argparse.ArgumentParser(description="Collect Kimi Code history for a date")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--kimi-dir", nargs="+", default=DEFAULT_ROOTS,
                        help="Kimi config dirs (default: ~/.kimi-code ~/.kimi)")
    parser.add_argument("--output", help="Output JSON path (default: stdout)")
    return parser.parse_args()


def get_git_info(cwd: str) -> dict[str, str]:
    """Get git branch and repo name for a given directory (worktree-aware)."""
    result = {"branch": "", "repo": ""}
    if not cwd or not Path(cwd).exists():
        return result
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=5,
        )
        if branch.returncode == 0:
            result["branch"] = branch.stdout.strip()

        toplevel = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd, capture_output=True, text=True, timeout=5,
        )
        if toplevel.returncode == 0 and toplevel.stdout.strip():
            root = Path(toplevel.stdout.strip())
            git_file = root / ".git"
            if git_file.is_file():
                content = git_file.read_text().strip()
                if content.startswith("gitdir:"):
                    gitdir = Path(content.split(":", 1)[1].strip())
                    if gitdir.parent.name == "worktrees":
                        original = gitdir.parent.parent.parent
                        if original.exists():
                            result["repo"] = original.name
                            return result
            result["repo"] = root.name
    except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
        pass
    return result


def ms_to_dt(ts_ms: float | int | None) -> datetime | None:
    """Convert millisecond epoch to UTC+8 datetime."""
    if not ts_ms:
        return None
    try:
        return datetime.fromtimestamp(float(ts_ms) / 1000.0, tz=TZ)
    except (ValueError, OSError, OverflowError):
        return None


def text_from_input(input_list) -> str:
    """Join text parts of a turn.prompt input; mark images as [图片]."""
    if not isinstance(input_list, list):
        return str(input_list or "")
    parts = []
    for item in input_list:
        if not isinstance(item, dict):
            continue
        itype = item.get("type")
        if itype in ("text",):
            parts.append(item.get("text", ""))
        elif itype in ("image_url", "image"):
            parts.append("[图片]")
    return "\n".join(p for p in parts if p)


def find_state_files(root: Path) -> list[Path]:
    """Find all state.json (new layout) and legacy session dirs."""
    if not root.exists():
        return []
    states = sorted(root.glob("sessions/*/session_*/state.json"))
    # Legacy: <root>/sessions/<root-id>/<session-id>/... (no state.json)
    legacy_dirs = sorted(
        d for d in (root / "sessions").glob("*/[0-9a-f-]*") if d.is_dir()
    ) if (root / "sessions").exists() else []
    return states, legacy_dirs


def parse_wire_prompts(wire_path: Path, target_start: datetime, target_end: datetime) -> list[tuple[int, str]]:
    """Extract (timestamp_ms, text) user prompts from a wire.jsonl."""
    prompts: list[tuple[int, str]] = []
    if not wire_path.exists():
        return prompts
    try:
        with wire_path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("type") != "turn.prompt":
                    continue
                ts_ms = obj.get("time") or 0
                dt = ms_to_dt(ts_ms)
                if dt is None or not (target_start <= dt <= target_end):
                    continue
                text = text_from_input(obj.get("input") or obj.get("prompt"))
                if text.strip():
                    prompts.append((int(ts_ms), text))
    except OSError:
        return prompts
    return prompts


def collect(root: Path, target_date: date, seen_global: set) -> list[dict]:
    """Collect session records from one kimi root."""
    tz = TZ
    target_start = datetime.combine(target_date, time.min, tzinfo=tz)
    target_end = datetime.combine(target_date, time.max, tzinfo=tz)

    states, legacy_dirs = find_state_files(root)
    results = []

    for state_path in states:
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        updated_at = ms_to_dt(state.get("updatedAt"))
        created_at = ms_to_dt(state.get("createdAt"))
        # Session counts only if it was active around the target date
        if updated_at is None or not (target_start - timedelta(days=2) <= updated_at <= target_end):
            continue

        # Find wire.jsonl files (main agent + subagents)
        session_dir = state_path.parent
        wire_files = sorted(session_dir.glob("**/wire.jsonl"))
        # Sort: main agent first (path contains '/agents/main/' or closest to root)
        wire_files.sort(key=lambda p: (0 if "agents/main" in str(p) and "subagents" not in str(p) else 1, str(p)))

        prompts: list[tuple[int, str]] = []
        for wf in wire_files[:6]:  # cap for perf
            prompts.extend(parse_wire_prompts(wf, target_start, target_end))
        prompts.sort()

        # Global dedupe across fork tree: (ts, text) kept once, earliest session wins
        unique = []
        for ts_ms, text in prompts:
            key = (ts_ms, text[:120])
            if key in seen_global:
                continue
            seen_global.add(key)
            unique.append(text)
        if not unique:
            continue

        rec = {
            "session_id": state.get("id", state_path.parent.name),
            "title": state.get("title", ""),
            "forked_from": state.get("forkedFrom", ""),
            "cwd": state.get("cwd", ""),
            "created_at": created_at.isoformat() if created_at else "",
            "updated_at": updated_at.isoformat() if updated_at else "",
            "user_messages": unique,
            "last_prompt": state.get("lastPrompt", ""),
        }
        git = get_git_info(rec["cwd"])
        rec["git_branch"] = git["branch"]
        rec["git_repo"] = git["repo"]
        results.append(rec)

    # Legacy layout: session dir without state.json
    for d in legacy_dirs:
        wire_files = sorted(d.glob("**/wire.jsonl"))
        prompts: list[tuple[int, str]] = []
        for wf in wire_files[:6]:
            prompts.extend(parse_wire_prompts(wf, target_start, target_end))
        prompts.sort()
        unique = []
        for ts_ms, text in prompts:
            key = (ts_ms, text[:120])
            if key in seen_global:
                continue
            seen_global.add(key)
            unique.append(text)
        if not unique:
            continue
        # Try to find cwd from context.jsonl parent or session_index
        cwd = ""
        rec = {
            "session_id": d.name,
            "title": "",
            "forked_from": "",
            "cwd": cwd,
            "created_at": "",
            "updated_at": datetime.fromtimestamp(d.stat().st_mtime, tz=tz).isoformat(),
            "user_messages": unique,
            "last_prompt": "",
        }
        git = get_git_info(rec["cwd"])
        rec["git_branch"] = git["branch"]
        rec["git_repo"] = git["repo"]
        results.append(rec)

    return results


def main():
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()

    seen_global: set = set()
    sessions: list[dict] = []
    for d in args.kimi_dir:
        root = Path(d).expanduser()
        sessions.extend(collect(root, target_date, seen_global))

    total = sum(len(s["user_messages"]) for s in sessions)
    rendered = json.dumps({
        "date": args.date,
        "source": "kimi_code_local",
        "session_count": len(sessions),
        "total_user_messages": total,
        "sessions": sessions,
    }, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        print(f"Kimi history written to: {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
