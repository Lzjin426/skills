#!/usr/bin/env python3
"""Collect Claude Code local conversation history for a specific date.

Reads ~/.claude/history.jsonl and ~/.claude/sessions/*.json to extract
user inputs, working directories, and git branch info for the target date.

Output: JSON array of session records, each containing:
  - session_id, started_at, cwd, git_branch, git_repo, inputs[]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import date, datetime, timezone, timedelta
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Collect Claude Code history for a date")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--history", default="~/.claude/history.jsonl", help="Path to history.jsonl")
    parser.add_argument("--sessions-dir", default="~/.claude/sessions", help="Path to sessions directory")
    parser.add_argument("--output", help="Output JSON path (default: stdout)")
    return parser.parse_args()


def load_history(history_path: Path, target_date: date) -> list[dict]:
    """Read history.jsonl and filter entries by target date."""
    records = []
    if not history_path.exists():
        return records

    # Target date in UTC+8 (Shanghai)
    tz = timezone(timedelta(hours=8))
    target_start = datetime.combine(target_date, datetime.min.time(), tzinfo=tz)
    target_end = datetime.combine(target_date, datetime.max.time(), tzinfo=tz)

    with history_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            ts = obj.get("timestamp")
            if not ts:
                continue

            # timestamp is milliseconds since epoch
            dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
            dt_local = dt.astimezone(tz)

            if target_start <= dt_local <= target_end:
                records.append({
                    "timestamp": dt_local.isoformat(),
                    "display": obj.get("display", ""),
                    "project": obj.get("project", ""),
                    "session_id": obj.get("sessionId", ""),
                })

    return records


def load_sessions(sessions_dir: Path) -> dict[str, dict]:
    """Load session metadata from sessions/*.json, keyed by session_id."""
    sessions = {}
    if not sessions_dir.exists():
        return sessions

    for f in sessions_dir.glob("*.json"):
        try:
            with f.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            sid = data.get("sessionId")
            if sid:
                sessions[sid] = {
                    "cwd": data.get("cwd", ""),
                    "started_at_ms": data.get("startedAt"),
                    "version": data.get("version", ""),
                    "entrypoint": data.get("entrypoint", ""),
                }
        except (json.JSONDecodeError, OSError):
            continue

    return sessions


def get_git_info(cwd: str) -> dict[str, str]:
    """Get git branch and repo name for a given directory.

    Returns {"branch": "main", "repo": "project-name"} or empty strings if not a git repo.
    For worktrees, returns the original repo name (not the worktree directory name).
    """
    result = {"branch": "", "repo": ""}
    if not cwd or not Path(cwd).exists():
        return result

    try:
        # Get current branch
        branch_proc = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if branch_proc.returncode == 0:
            result["branch"] = branch_proc.stdout.strip()

        # Get repo toplevel
        repo_proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if repo_proc.returncode == 0:
            toplevel = repo_proc.stdout.strip()
            if toplevel:
                # Check if this is a worktree (toplevel/.git is a file, not directory)
                git_file = Path(toplevel) / ".git"
                if git_file.is_file():
                    # Worktree: read gitdir from .git file to find original repo
                    # gitdir: /path/to/original/.git/worktrees/xxx
                    try:
                        content = git_file.read_text().strip()
                        if content.startswith("gitdir:"):
                            gitdir = content.split(":", 1)[1].strip()
                            # Walk up from gitdir to find original repo toplevel
                            # gitdir is like: /repo/.git/worktrees/xxx
                            # We want the directory containing .git
                            gitdir_path = Path(gitdir)
                            # Walk up: worktrees/xxx -> .git -> repo root
                            parent = gitdir_path.parent  # .git/worktrees
                            if parent.name == "worktrees":
                                original_git = parent.parent  # .git directory
                                original_repo = original_git.parent  # repo root
                                if original_repo.exists():
                                    result["repo"] = original_repo.name
                                    return result
                    except (OSError, ValueError):
                        pass
                # Regular repo or fallback
                result["repo"] = Path(toplevel).name
    except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
        pass

    return result


def group_by_session(history_records: list[dict], sessions: dict[str, dict]) -> list[dict]:
    """Group history records by session, enriching with session metadata."""
    session_map: dict[str, dict] = {}

    for rec in history_records:
        sid = rec["session_id"]
        if sid not in session_map:
            meta = sessions.get(sid, {})
            # Convert started_at_ms to readable time
            started_ms = meta.get("started_at_ms")
            started_str = None
            if started_ms:
                started_dt = datetime.fromtimestamp(started_ms / 1000, tz=timezone.utc)
                started_str = started_dt.astimezone(timezone(timedelta(hours=8))).isoformat()

            # If no session metadata, use first input time as started_at
            if started_str is None:
                started_str = rec["timestamp"]

            cwd = meta.get("cwd", rec.get("project", ""))
            git_info = get_git_info(cwd)

            session_map[sid] = {
                "session_id": sid,
                "started_at": started_str,
                "cwd": cwd,
                "git_branch": git_info["branch"],
                "git_repo": git_info["repo"],
                "entrypoint": meta.get("entrypoint", ""),
                "inputs": [],
            }
        session_map[sid]["inputs"].append({
            "time": rec["timestamp"],
            "text": rec["display"],
        })

    return list(session_map.values())


def main():
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    history_path = Path(args.history).expanduser()
    sessions_dir = Path(args.sessions_dir).expanduser()

    history_records = load_history(history_path, target_date)
    sessions = load_sessions(sessions_dir)
    result = group_by_session(history_records, sessions)

    # Sort by first input time
    result.sort(key=lambda x: x["inputs"][0]["time"] if x["inputs"] else "")

    rendered = json.dumps({
        "date": args.date,
        "source": "claude_code_local",
        "session_count": len(result),
        "total_inputs": sum(len(s["inputs"]) for s in result),
        "sessions": result,
    }, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        print(f"Claude history written to: {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
