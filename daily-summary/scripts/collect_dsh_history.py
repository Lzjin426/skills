#!/usr/bin/env python3
"""Collect DeepSeek Harness (DSH) local conversation history for a specific date.

DSH stores sessions as zstd-compressed JSONL files under:
  ~/.dsh/sessions/<cwd-sanitized>/session-<uuid>/session.jsonl.zstd

This script scans those files, filters by file mtime AND by per-message
timestamps (milliseconds, UTC+8), and extracts:
  - cwd, git repo/branch
  - session title
  - user messages (system-injected reminders are filtered out)
  - brief assistant message previews

Output: JSON with the same shape as collect_codex_history.py so that
generate_daily.py can consume it unchanged.

Requires the `zstd` CLI (fallback: python `zstandard` package).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

TZ = timezone(timedelta(hours=8))

# System-injected message prefixes that carry no user intent
SKIP_TEXT_PREFIXES = (
    "<system-reminder>",
    "<skill_content",
    "<available_skills>",
    "Current runtime context.",
    "Instructions from:",
)


def parse_args():
    parser = argparse.ArgumentParser(description="Collect DeepSeek Harness history for a date")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--dsh-dir", default="~/.dsh", help="Path to .dsh directory")
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


def decompress(path: Path) -> str | None:
    """Decompress a zstd file; returns text or None on failure."""
    # Prefer CLI
    if shutil.which("zstd"):
        try:
            proc = subprocess.run(
                ["zstd", "-dc", str(path)],
                capture_output=True, text=True, timeout=60,
            )
            if proc.returncode == 0:
                return proc.stdout
        except (subprocess.TimeoutExpired, OSError):
            pass
    # Fallback: python zstandard
    try:
        import zstandard  # type: ignore
    except ImportError:
        return None
    try:
        with path.open("rb") as fh:
            return zstandard.ZstdDecompressor().decompress(fh.read()).decode("utf-8", "replace")
    except Exception:
        return None


def extract_text_from_content(content) -> str:
    """Extract plain text from a DSH content field (str or list of dicts)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") in ("text", "input_text", "output_text"):
                    parts.append(item.get("text", ""))
        return "\n".join(p for p in parts if p)
    return ""


def parse_session_file(path: Path, target_start: datetime, target_end: datetime) -> dict | None:
    """Parse one session.jsonl.zstd into a session record (messages within target date)."""
    text = decompress(path)
    if text is None:
        return None

    record = {
        "session_id": path.parent.name,
        "title": "",
        "created_at": "",
        "updated_at": "",
        "cwd": "",
        "user_messages": [],
        "assistant_preview": [],
        "tool_names": [],
        "decompression_failed": False,
    }

    seen_msgs = set()  # dedupe (time, text) across spliced/inbox copies
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        mtype = obj.get("type")
        # Some record types carry fields at top level (e.g. "session"),
        # others nest them under "data" (e.g. "user/message", "session/title").
        data = obj.get("data") if isinstance(obj.get("data"), dict) else obj
        ts_ms = obj.get("time") or 0
        ts = datetime.fromtimestamp(ts_ms / 1000, tz=TZ) if ts_ms else None

        if mtype == "session":
            record["cwd"] = data.get("cwd", "") or record["cwd"]
            created = data.get("createdAt") or 0
            if created:
                record["created_at"] = datetime.fromtimestamp(created / 1000, tz=TZ).isoformat()

        elif mtype == "session/title":
            title = data.get("title") or ""
            if isinstance(title, str) and title and not title.startswith("("):
                record["title"] = title

        elif mtype in ("user/message", "bubble/user"):
            if ts and not (target_start <= ts <= target_end):
                continue
            text_content = extract_text_from_content(data.get("content", []))
            if not text_content:
                continue
            if any(text_content.strip().startswith(p) for p in SKIP_TEXT_PREFIXES):
                continue
            key = (int(ts_ms), text_content[:120])
            if key in seen_msgs:
                continue
            seen_msgs.add(key)
            record["user_messages"].append(text_content)

        elif mtype == "assistant/message":
            if ts and not (target_start <= ts <= target_end):
                continue
            text_content = extract_text_from_content(data.get("content", []))
            if text_content and len(record["assistant_preview"]) < 3:
                record["assistant_preview"].append(text_content[:400])

        elif mtype == "tool/call":
            name = data.get("name") or ""
            if name and name not in record["tool_names"]:
                record["tool_names"].append(name)
            ts_last = ts

    if record["updated_at"]:
        pass
    record["updated_at"] = record["updated_at"] or (
        datetime.fromtimestamp(path.stat().st_mtime, tz=TZ).isoformat()
    )
    return record


def find_session_files(dsh_dir: Path) -> list[Path]:
    """Find all session.jsonl.zstd files under ~/.dsh/sessions/."""
    sessions_root = dsh_dir / "sessions"
    if not sessions_root.exists():
        return []
    return sorted(sessions_root.glob("*/session-*/session.jsonl.zstd"))


def collect(dsh_dir: Path, target_date: date) -> list[dict]:
    tz = TZ
    target_start = datetime.combine(target_date, time.min, tzinfo=tz)
    target_end = datetime.combine(target_date, time.max, tzinfo=tz)

    results = []
    for path in find_session_files(dsh_dir):
        # Quick filter: file mtime within date window (fast path)
        mtime_dt = datetime.fromtimestamp(path.stat().st_mtime, tz=tz)
        if not (target_start - timedelta(days=1) <= mtime_dt <= target_end + timedelta(days=1)):
            continue

        rec = parse_session_file(path, target_start, target_end)
        if rec is None:
            continue
        # Precise filter: keep only if it has messages in the target date window
        if not rec["user_messages"] and not rec["assistant_preview"]:
            continue

        git = get_git_info(rec["cwd"])
        rec["git_branch"] = git["branch"]
        rec["git_repo"] = git["repo"]
        results.append(rec)

    return results


def main():
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    dsh_dir = Path(args.dsh_dir).expanduser()

    sessions = collect(dsh_dir, target_date)
    total = sum(len(s["user_messages"]) for s in sessions)

    print(json.dumps({
        "date": args.date,
        "source": "dsh_local",
        "session_count": len(sessions),
        "total_user_messages": total,
        "sessions": sessions,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
