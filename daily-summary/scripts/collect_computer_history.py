#!/usr/bin/env python3
"""Read Computer History event-stream evidence for one Shanghai date.

The Computer History MCP tool supplies the event-stream root and status. This
script only reads completed/current segments and memory files after that
read-only status check; it never changes observation settings or starts the
service.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

try:
    from zoneinfo import ZoneInfo

    TZ = ZoneInfo("Asia/Shanghai")
except Exception:  # pragma: no cover
    TZ = timezone(timedelta(hours=8))


TIME_KEYS = (
    "timestamp",
    "time",
    "ts",
    "created_at",
    "createdAt",
    "occurred_at",
    "occurredAt",
    "event_time",
    "eventTime",
)

AX_OUTCOME_RE = re.compile(
    r"(?:\binitial submission\b|\bsubmission overview\b|\bsubmission complete\b|"
    r"\bsubmitted successfully\b|\bunder consideration\b|\bcannot be edited\b|"
    r"\b(?:manuscript|submission).{0,120}(?:shared with|sent to|submitted to|under consideration)\b|"
    r"\bsubmission id\b|\bmanuscript id\b|\bdownload reviewer pdf\b|"
    r"\bupload (?:complete|successful)\b|"
    r"\b(?:manuscript|submission|paper) (?:has been )?(?:accepted|rejected|published)\b|"
    r"\b(?:submission|upload) failed\b|"
    r"已提交|投稿成功|提交成功|正在审理|审理中|审核中|不可编辑|上传成功|"
    r"(?:稿件|手稿|论文).{0,80}(?:正在与期刊编辑分享|已送交编辑部|已发送给编辑部|进入审理)|"
    r"(?:稿件|论文|投稿)(?:已|正在|当前|目前)?(?:被)?(?:接收|接受|拒绝|发表|审理|审核)|"
    r"投稿失败|上传失败)",
    re.IGNORECASE,
)
MAX_AX_EVIDENCE_LINES = 8
MAX_AX_EVIDENCE_LINE_CHARS = 360
MAX_AX_EVIDENCE_CHARS = 1800
URL_RE = re.compile(r"https?://[^\s|<>\"]+")
SECRET_QUERY_RE = re.compile(
    r"([?&](?:authToken|access_token|refresh_token|token|code|state|secret|signature|sig|ticket|"
    r"complete_account_hint|form_hint|xsec_token)=)[^&#\s]+",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect Computer History evidence")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--root", help="eventStreamRootPath from computer_history_status")
    parser.add_argument(
        "--memory-root",
        default="~/.codex/memories/extensions/skysight/resources",
        help="Computer History memory resource directory",
    )
    parser.add_argument(
        "--status",
        choices=("running", "paused", "stopped", "unknown"),
        default="unknown",
        help="Status returned by computer_history_status",
    )
    parser.add_argument("--memory-limit", type=int, default=12)
    parser.add_argument("--output", help="Output JSON path (default: stdout)")
    return parser.parse_args()


def parse_time(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    try:
        if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
            number = float(value)
            seconds = number / 1000 if abs(number) >= 10**11 else number
            return datetime.fromtimestamp(seconds, timezone.utc).astimezone(TZ)
        parsed = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=TZ)
        return parsed.astimezone(TZ)
    except (OverflowError, OSError, ValueError):
        return None


def object_time(value: Any) -> datetime | None:
    if not isinstance(value, dict):
        return None
    for key in TIME_KEYS:
        parsed = parse_time(value.get(key))
        if parsed:
            return parsed
    metadata = value.get("metadata")
    if isinstance(metadata, dict):
        return object_time(metadata)
    return None


def first_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(part for part in (first_text(item) for item in value) if part).strip()
    if isinstance(value, dict):
        for key in ("text", "value", "title", "name", "label"):
            text = first_text(value.get(key))
            if text:
                return text
    return ""


def pick(item: dict[str, Any], *keys: str) -> str:
    for key in keys:
        text = first_text(item.get(key))
        if text:
            return text
    return ""


def ax_text(item: dict[str, Any]) -> tuple[str, str]:
    """Read the AX field used by the event stream, with legacy-key fallback."""
    raw = item.get("ax") or item.get("ax_tree") or item.get("axTree") or item.get("ax_diff") or item.get("axDiff")
    if isinstance(raw, dict):
        return str(raw.get("mode") or ""), str(raw.get("text") or "")
    if isinstance(raw, str):
        return "", raw
    return "", ""


def ax_outcome_evidence(text: str) -> str:
    """Keep short UI status lines, not whole accessibility trees or page bodies."""
    kept: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = re.sub(r"^\s*[+~\-]*\s*\d+\s+", "", raw_line).strip()
        if not line or not AX_OUTCOME_RE.search(line):
            continue
        line = line[:MAX_AX_EVIDENCE_LINE_CHARS]
        key = line.casefold()
        if key in seen:
            continue
        kept.append(line)
        seen.add(key)
        if len(kept) >= MAX_AX_EVIDENCE_LINES:
            break
    result = " | ".join(kept)
    return result[:MAX_AX_EVIDENCE_CHARS]


def sanitize_url(value: str) -> str:
    """Keep URL identity while dropping query/fragment values that can contain credentials."""
    try:
        parsed = urlsplit(value.strip())
        if not parsed.scheme:
            return value.strip()
        host = parsed.hostname or ""
        if parsed.port:
            host = f"{host}:{parsed.port}"
        return urlunsplit((parsed.scheme, host, parsed.path, "", ""))
    except ValueError:
        return ""


def sanitize_text(value: str) -> str:
    text = SECRET_QUERY_RE.sub(r"\1[REDACTED]", value)
    return URL_RE.sub(lambda match: sanitize_url(match.group(0)), text)


def in_target(value: datetime | None, target_date: date) -> bool:
    return value is not None and value.date() == target_date


def segment_overlaps(metadata: dict[str, Any], target_date: date) -> bool:
    start_value = metadata.get("start") if isinstance(metadata, dict) else None
    end_value = metadata.get("end") if isinstance(metadata, dict) else None
    start = object_time(start_value) if isinstance(start_value, dict) else parse_time(start_value)
    end = object_time(end_value) if isinstance(end_value, dict) else parse_time(end_value)
    if start is None:
        for key in ("start_time", "startTime", "started_at", "startedAt"):
            start = parse_time(metadata.get(key))
            if start:
                break
    if end is None:
        for key in ("end_time", "endTime", "ended_at", "endedAt"):
            end = parse_time(metadata.get(key))
            if end:
                break
    day_start = datetime.combine(target_date, time.min, tzinfo=TZ)
    day_end = day_start + timedelta(days=1)
    if start and end:
        return start < day_end and end >= day_start
    if start:
        return start < day_end and start >= day_start - timedelta(days=1)
    if end:
        return end >= day_start and end < day_end + timedelta(days=1)
    return True


def event_record(item: dict[str, Any], segment: str, target_date: date) -> dict[str, Any] | None:
    timestamp = object_time(item)
    if not in_target(timestamp, target_date):
        return None
    app = pick(item, "app", "application", "app_name", "application_name", "bundle_id", "bundleID")
    window = pick(item, "window_title", "windowTitle", "title", "window")
    window_info = item.get("window")
    url = pick(item, "url", "href", "web_url")
    if not url and isinstance(window_info, dict):
        url = str(window_info.get("url") or "").strip()
    url = sanitize_url(url) if url else ""
    selected = pick(item, "selected_text", "selectedText", "selection")
    focused = pick(item, "focused_element", "focusedElement", "element")
    mouse = pick(item, "mouse_target", "mouseTarget", "target")
    keyboard = pick(item, "keyboard_target", "keyboardTarget")
    ax_mode, raw_ax_text = ax_text(item)
    ax_evidence = ax_outcome_evidence(raw_ax_text)
    summary = pick(item, "text", "summary", "description", "event")
    has_explicit_text = bool(summary)
    if not summary:
        summary = " | ".join(value for value in (app, window, url, selected, focused) if value)
    summary = sanitize_text(summary)[:1000]
    if ax_evidence:
        summary = " | ".join(part for part in (summary, f"AX outcome: {ax_evidence}") if part)
    return {
        "id": item.get("id", ""),
        "time": timestamp.isoformat() if timestamp else "",
        "app": app,
        "window_title": window,
        "url": url,
        "selected_text": sanitize_text(selected),
        "focused_element": sanitize_text(focused),
        "mouse_target": sanitize_text(mouse),
        "keyboard_target": sanitize_text(keyboard),
        "ax_mode": ax_mode,
        "ax_evidence": ax_evidence,
        "summary": summary,
        "has_explicit_text": has_explicit_text,
        "segment": segment,
        "evidence_level": "observed_ui_state" if ax_evidence else "observed_activity_only",
    }


def compact_duplicate_observations(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep one sample of an identical UI snapshot; repeated captures add no new evidence."""
    compacted: list[dict[str, Any]] = []
    seen_states: set[tuple[str, ...]] = set()
    for event in sorted(events, key=lambda item: item.get("time", "")):
        context = tuple(str(event.get(field) or "") for field in ("app", "window_title", "url"))
        evidence = str(event.get("ax_evidence") or "").strip()
        if evidence:
            key = (*context, "ui_state", evidence)
        elif event.get("has_explicit_text") or any(
            event.get(field) for field in ("selected_text", "focused_element", "mouse_target", "keyboard_target")
        ):
            key = (
                *context,
                "explicit_observation",
                str(event.get("summary") or ""),
                str(event.get("selected_text") or ""),
                str(event.get("focused_element") or ""),
                str(event.get("mouse_target") or ""),
                str(event.get("keyboard_target") or ""),
            )
        else:
            key = (*context, "view")
        if not any(key[:3]):
            key = (*key, str(event.get("summary") or ""))
        if key in seen_states:
            continue
        seen_states.add(key)
        compacted.append(event)
    return compacted


def read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def collect_segments(root: Path, target_date: date, errors: list[str]) -> list[dict[str, Any]]:
    segments_root = root / "segments"
    if not segments_root.exists():
        errors.append(f"segments directory not found: {segments_root}")
        return []

    events: list[dict[str, Any]] = []
    for segment_dir in sorted(path for path in segments_root.iterdir() if path.is_dir()):
        metadata_path = segment_dir / "metadata.json"
        metadata = read_json(metadata_path) if metadata_path.exists() else {}
        if isinstance(metadata, dict) and not segment_overlaps(metadata, target_date):
            continue
        events_path = segment_dir / "events.jsonl"
        if not events_path.exists():
            continue
        try:
            with events_path.open("r", encoding="utf-8", errors="replace") as handle:
                for line_number, line in enumerate(handle, start=1):
                    if not line.strip():
                        continue
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        errors.append(f"{events_path}:{line_number}: invalid JSON")
                        continue
                    if not isinstance(item, dict):
                        continue
                    record = event_record(item, segment_dir.name, target_date)
                    if record:
                        events.append(record)
        except OSError as exc:
            errors.append(f"{events_path}: {exc}")
    return events


def memory_timestamp(path: Path) -> datetime | None:
    match = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}[-:]\d{2}[-:]\d{2})", path.name)
    if match:
        try:
            date_part, time_part = match.group(1).split("T", 1)
            return datetime.fromisoformat(f"{date_part}T{time_part.replace('-', ':')}").replace(
                tzinfo=timezone.utc
            ).astimezone(TZ)
        except ValueError:
            pass
    # mtime only tells us when the summary file changed, not when the
    # observed activity happened.  Do not use it for natural-day attribution.
    return None


def collect_memories(root: Path, target_date: date, limit: int, errors: list[str]) -> list[dict[str, Any]]:
    if limit <= 0 or not root.exists():
        return []
    candidates = []
    for path in root.glob("*.md"):
        timestamp = memory_timestamp(path)
        if timestamp and timestamp.date() == target_date:
            candidates.append((timestamp, path))
    candidates.sort(reverse=True)
    memories = []
    for timestamp, path in candidates[:limit]:
        try:
            memories.append(
                {
                    "time": timestamp.isoformat(),
                    "name": path.name,
                    "content": path.read_text(encoding="utf-8"),
                    "evidence_level": "observed_activity_summary",
                }
            )
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path}: {exc}")
    return memories


def main() -> None:
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    errors: list[str] = []
    root = Path(args.root).expanduser() if args.root else None
    events = compact_duplicate_observations(collect_segments(root, target_date, errors)) if root else []
    if not root:
        errors.append("eventStreamRootPath was not supplied by computer_history_status")
    elif not root.exists():
        errors.append(f"eventStreamRootPath does not exist: {root}")
    memories = collect_memories(Path(args.memory_root).expanduser(), target_date, args.memory_limit, errors)
    output = {
        "date": args.date,
        "timezone": "Asia/Shanghai",
        "source": "computer_history",
        "status": args.status,
        "available": bool(events or memories) and bool(root and root.exists()),
        "evidence_quality": "observed_ui_state_and_activity" if any(event.get("ax_evidence") for event in events) else "observed_activity_only",
        "events": events,
        "memories": memories,
        "errors": errors,
    }
    if args.status == "paused":
        output["note"] = "Computer History is paused; existing records were read and the target window may be incomplete."
    elif args.status == "stopped":
        output["note"] = "Computer History is stopped; only previously completed records were read."
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        print(f"Computer History data written to: {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
