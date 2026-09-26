#!/usr/bin/env python3
"""Collect Codex local conversation history for a specific date.

Reads ~/.codex/session_index.jsonl to find sessions for the target date,
then parses the corresponding ~/.codex/sessions/YYYY/MM/DD/*.jsonl files
to extract conversation content.

Output: JSON array of session records.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import date, datetime, timezone, timedelta
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Collect Codex history for a date")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--codex-dir", default="~/.codex", help="Path to .codex directory")
    return parser.parse_args()


def load_session_index(codex_dir: Path) -> list[dict]:
    """Read session_index.jsonl and return all session entries."""
    index_path = codex_dir / "session_index.jsonl"
    sessions = []
    if not index_path.exists():
        return sessions

    with index_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                sessions.append(obj)
            except json.JSONDecodeError:
                continue

    return sessions


def get_git_info(cwd: str) -> dict[str, str]:
    """Get git branch and repo name for a given directory.

    For worktrees, returns the original repo name (not the worktree directory name).
    """
    result = {"branch": "", "repo": ""}
    if not cwd or not Path(cwd).exists():
        return result

    try:
        branch_proc = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if branch_proc.returncode == 0:
            result["branch"] = branch_proc.stdout.strip()

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
                git_file = Path(toplevel) / ".git"
                if git_file.is_file():
                    try:
                        content = git_file.read_text().strip()
                        if content.startswith("gitdir:"):
                            gitdir = content.split(":", 1)[1].strip()
                            gitdir_path = Path(gitdir)
                            parent = gitdir_path.parent
                            if parent.name == "worktrees":
                                original_git = parent.parent
                                original_repo = original_git.parent
                                if original_repo.exists():
                                    result["repo"] = original_repo.name
                                    return result
                    except (OSError, ValueError):
                        pass
                result["repo"] = Path(toplevel).name
    except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
        pass

    return result


def parse_iso_datetime(dt_str: str) -> datetime | None:
    """Parse ISO 8601 datetime, handling fractional seconds with >6 digits."""
    if not dt_str:
        return None
    # Replace Z with +00:00
    s = dt_str.replace("Z", "+00:00")
    # Truncate fractional seconds to 6 digits (Python limit)
    import re
    # Match any number of fractional digits after the dot
    m = re.match(r"(.+?)(\.\d+)([\+\-]\d{2}:\d{2})", s)
    if m:
        frac = m.group(2)[:7]  # Keep dot + up to 6 digits
        s = m.group(1) + frac + m.group(3)
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def filter_sessions_by_date(sessions: list[dict], target_date: date) -> list[dict]:
    """Filter sessions where updated_at falls on target date (UTC+8)."""
    tz = timezone(timedelta(hours=8))
    target_start = datetime.combine(target_date, datetime.min.time(), tzinfo=tz)
    target_end = datetime.combine(target_date, datetime.max.time(), tzinfo=tz)

    result = []
    for sess in sessions:
        updated_str = sess.get("updated_at", "")
        updated_dt = parse_iso_datetime(updated_str)
        if updated_dt is None:
            continue

        updated_local = updated_dt.astimezone(tz)

        if target_start <= updated_local <= target_end:
            result.append({
                "id": sess.get("id", ""),
                "thread_name": sess.get("thread_name", ""),
                "updated_at": updated_local.isoformat(),
            })

    return result


def find_session_files(codex_dir: Path, session_id: str, target_date: date) -> list[Path]:
    """Find jsonl files for a session on the target date."""
    year_str = str(target_date.year)
    month_str = f"{target_date.month:02d}"
    day_str = f"{target_date.day:02d}"

    date_dir = codex_dir / "sessions" / year_str / month_str / day_str
    if not date_dir.exists():
        return []

    # Files are named: rollout-YYYY-MM-DDTHH-MM-SS-<session_id>.jsonl
    pattern = f"*{session_id}*.jsonl"
    return list(date_dir.glob(pattern))


def parse_session_jsonl(file_path: Path) -> dict:
    """Parse a Codex session jsonl file and extract conversation content."""
    user_messages = []
    assistant_messages = []
    cwd = ""
    model = ""

    with file_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_type = obj.get("type")
            payload = obj.get("payload", {})

            if msg_type == "session_meta":
                meta = payload
                cwd = meta.get("cwd", "")
                model = meta.get("model_provider", "") + "/" + meta.get("model", "")

            elif msg_type == "event_msg":
                event_type = payload.get("event_type", "")
                if event_type == "user_message":
                    content = payload.get("content", "")
                    if content:
                        user_messages.append(content)

            elif msg_type == "response_item":
                content = payload.get("content", "")
                if content:
                    assistant_messages.append(str(content)[:500])

    return {
        "cwd": cwd,
        "model": model,
        "user_messages": user_messages,
        "assistant_preview": assistant_messages[:3],  # Only first few for brevity
    }


def collect_sessions(codex_dir: Path, target_date: date) -> list[dict]:
    """Main collection logic."""
    all_index = load_session_index(codex_dir)
    filtered = filter_sessions_by_date(all_index, target_date)

    results = []
    for sess in filtered:
        files = find_session_files(codex_dir, sess["id"], target_date)
        if not files:
            # Try without date restriction (some sessions might span days)
            # Search all subdirectories
            sessions_root = codex_dir / "sessions"
            if sessions_root.exists():
                files = list(sessions_root.rglob(f"*{sess['id']}*.jsonl"))

        session_data = {
            "session_id": sess["id"],
            "thread_name": sess["thread_name"],
            "updated_at": sess["updated_at"],
            "files_found": len(files),
            "cwd": "",
            "user_messages": [],
        }

        # Parse the first found file for content
        if files:
            parsed = parse_session_jsonl(files[0])
            session_data["cwd"] = parsed["cwd"]
            session_data["user_messages"] = parsed["user_messages"]

        # Get git info for the session's cwd
        git_info = get_git_info(session_data["cwd"])
        session_data["git_branch"] = git_info["branch"]
        session_data["git_repo"] = git_info["repo"]

        results.append(session_data)

    return results


def main():
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    codex_dir = Path(args.codex_dir).expanduser()

    results = collect_sessions(codex_dir, target_date)

    total_messages = sum(len(s["user_messages"]) for s in results)

    print(json.dumps({
        "date": args.date,
        "source": "codex_local",
        "session_count": len(results),
        "total_user_messages": total_messages,
        "sessions": results,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
