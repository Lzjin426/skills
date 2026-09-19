#!/usr/bin/env python3
"""Collect date-scoped Codex conversation history.

Codex sessions may span dates and may be split across several rollout files.
This collector filters individual user messages by Asia/Shanghai date and
merges every matching file, instead of trusting only session ``updated_at`` or
the first rollout file.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo

    TZ = ZoneInfo("Asia/Shanghai")
except Exception:  # pragma: no cover
    TZ = timezone(timedelta(hours=8))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect Codex history for a date")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--codex-dir", default="~/.codex", help="Path to .codex directory")
    parser.add_argument(
        "--scan-all",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Scan all rollout files to catch sessions spanning dates",
    )
    parser.add_argument("--output", help="Output JSON path (default: stdout)")
    return parser.parse_args()


def get_git_info(cwd: str) -> dict[str, str]:
    """Get current git metadata as a fallback, clearly marked by the caller."""
    result = {"branch": "", "repo": ""}
    if not cwd or not Path(cwd).exists():
        return result
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if branch.returncode == 0:
            result["branch"] = branch.stdout.strip()

        root_proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if root_proc.returncode != 0:
            return result
        root = Path(root_proc.stdout.strip())
        git_file = root / ".git"
        if git_file.is_file():
            content = git_file.read_text(encoding="utf-8").strip()
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


def parse_iso_datetime(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        number = float(value)
        if abs(number) >= 10**11:
            number /= 1000
        try:
            return datetime.fromtimestamp(number, timezone.utc).astimezone(TZ)
        except (OverflowError, OSError, ValueError):
            return None
    text = str(value).strip()
    if text.isdigit():
        return parse_iso_datetime(int(text))
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=TZ)
    return parsed.astimezone(TZ)


def event_timestamp(obj: dict[str, Any], payload: dict[str, Any]) -> datetime | None:
    for container in (obj, payload):
        for key in ("timestamp", "time", "created_at", "createdAt", "ts"):
            parsed = parse_iso_datetime(container.get(key))
            if parsed:
                return parsed
    return None


def content_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                text = item.get("text") or item.get("content") or item.get("value")
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())
            elif isinstance(item, str) and item.strip():
                parts.append(item.strip())
        return "\n".join(parts).strip()
    if isinstance(value, dict):
        return content_text(value.get("text") or value.get("content") or value.get("value") or "")
    return ""


def user_message_from_record(
    obj: dict[str, Any], payload: dict[str, Any]
) -> tuple[datetime | None, str] | None:
    msg_type = obj.get("type")
    event_type = payload.get("event_type")
    is_user = (msg_type == "event_msg" and event_type == "user_message") or (
        msg_type == "response_item" and payload.get("role") == "user"
    )
    if not is_user:
        return None
    value = payload.get("content")
    if value is None:
        value = payload.get("message") or payload.get("text")
    text = content_text(value)
    if not text:
        return None
    return event_timestamp(obj, payload), text


def parse_session_jsonl(
    file_path: Path,
    target_date: date,
) -> dict[str, Any]:
    user_messages: list[dict[str, str]] = []
    assistant_messages: list[str] = []
    cwd = ""
    model = ""
    session_id = ""
    unknown_time_messages = 0

    with file_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(obj, dict):
                continue
            payload = obj.get("payload", {})
            if not isinstance(payload, dict):
                payload = {}
            msg_type = obj.get("type")

            if msg_type == "session_meta":
                session_id = str(payload.get("id") or payload.get("session_id") or session_id)
                cwd = str(payload.get("cwd") or cwd)
                model = "/".join(
                    value
                    for value in (payload.get("model_provider", ""), payload.get("model", ""))
                    if value
                )
                continue

            user_message = user_message_from_record(obj, payload)
            if user_message:
                timestamp, text = user_message
                if timestamp is None:
                    unknown_time_messages += 1
                elif timestamp.date() != target_date:
                    continue
                user_messages.append(
                    {"time": timestamp.isoformat() if timestamp else "", "text": text}
                )
                continue

            if msg_type == "response_item":
                text = content_text(payload.get("content"))
                if text and len(assistant_messages) < 3:
                    assistant_messages.append(text[:500])

    return {
        "session_id": session_id,
        "cwd": cwd,
        "model": model,
        "user_messages": user_messages,
        "assistant_preview": assistant_messages,
        "unknown_time_messages": unknown_time_messages,
        "file": str(file_path),
    }


def load_session_index(codex_dir: Path) -> dict[str, dict[str, Any]]:
    index_path = codex_dir / "session_index.jsonl"
    result: dict[str, dict[str, Any]] = {}
    if not index_path.exists():
        return result
    try:
        with index_path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(item, dict) and item.get("id"):
                    result[str(item["id"])] = item
    except OSError:
        return result
    return result


def find_session_files(codex_dir: Path, target_date: date, scan_all: bool) -> list[Path]:
    root = codex_dir / "sessions"
    if not root.exists():
        return []
    date_dir = root / str(target_date.year) / f"{target_date.month:02d}" / f"{target_date.day:02d}"
    files: set[Path] = set(date_dir.glob("*.jsonl")) if date_dir.exists() else set()
    if scan_all:
        files.update(root.rglob("*.jsonl"))
    return sorted(files)


def merge_records(records: list[dict[str, Any]], index: dict[str, Any], target_date: date) -> dict[str, Any]:
    session_id = str(index.get("id") or "")
    cwd = ""
    model = ""
    messages: list[dict[str, str]] = []
    previews: list[str] = []
    files: list[str] = []
    unknown_time_messages = 0
    for record in records:
        session_id = session_id or record.get("session_id", "")
        cwd = cwd or record.get("cwd", "")
        model = model or record.get("model", "")
        messages.extend(record.get("user_messages", []))
        previews.extend(record.get("assistant_preview", []))
        files.append(record.get("file", ""))
        unknown_time_messages += int(record.get("unknown_time_messages", 0))

    unique_messages: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for message in sorted(messages, key=lambda item: (item.get("time", ""), item.get("text", ""))):
        key = (message.get("time", ""), message.get("text", ""))
        if key in seen:
            continue
        seen.add(key)
        unique_messages.append(message)

    updated_at = parse_iso_datetime(index.get("updated_at"))
    created_at = parse_iso_datetime(index.get("created_at"))
    git = get_git_info(cwd)
    return {
        "session_id": session_id,
        "thread_name": str(index.get("thread_name") or ""),
        "started_at": created_at.isoformat() if created_at else "",
        "updated_at": updated_at.isoformat() if updated_at else "",
        "cwd": cwd,
        "git_branch": git["branch"],
        "git_repo": git["repo"],
        "git_metadata_scope": "current_fallback" if cwd else "unavailable",
        "model": model,
        "files_found": len(files),
        "files": files,
        "user_messages": unique_messages,
        "assistant_preview": previews[:3],
        "unknown_time_messages": unknown_time_messages,
        "date": target_date.isoformat(),
    }


def collect_sessions(codex_dir: Path, target_date: date, scan_all: bool) -> list[dict[str, Any]]:
    index = load_session_index(codex_dir)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    orphan_records: list[dict[str, Any]] = []

    for file_path in find_session_files(codex_dir, target_date, scan_all):
        parsed = parse_session_jsonl(file_path, target_date)
        if not parsed["user_messages"]:
            continue
        session_id = parsed.get("session_id", "")
        if not session_id:
            match = re.search(
                r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
                file_path.name,
                re.I,
            )
            session_id = match.group(1) if match else file_path.stem
            parsed["session_id"] = session_id
        grouped[session_id].append(parsed)

    results = []
    for session_id, records in grouped.items():
        results.append(merge_records(records, index.get(session_id, {"id": session_id}), target_date))
    results.sort(key=lambda item: item.get("user_messages", [{}])[0].get("time", ""))
    return results


def main() -> None:
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    codex_dir = Path(args.codex_dir).expanduser()
    sessions = collect_sessions(codex_dir, target_date, args.scan_all)
    output = {
        "date": args.date,
        "timezone": "Asia/Shanghai",
        "source": "codex_local",
        "scan_all": args.scan_all,
        "session_count": len(sessions),
        "total_user_messages": sum(len(item["user_messages"]) for item in sessions),
        "sessions": sessions,
    }
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        print(f"Codex history written to: {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
