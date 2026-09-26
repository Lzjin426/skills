#!/usr/bin/env python3
"""Collect completed tasks from the domestic Dida365 CLI for one Shanghai day."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo

    TZ = ZoneInfo("Asia/Shanghai")
except Exception:  # pragma: no cover
    TZ = timezone(timedelta(hours=8))

UTC = timezone.utc
EMPTY_MESSAGES = ("未找到已完成任务", "没有已完成任务", "暂无已完成任务", "no completed tasks")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect domestic Dida365 completed tasks")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--output", help="Output JSON path (default: stdout)")
    return parser.parse_args()


def target_window(target_date: date) -> tuple[datetime, datetime]:
    start = datetime.combine(target_date, time.min, tzinfo=TZ)
    return start, start + timedelta(days=1)


def cli_time(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_time(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    try:
        if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
            number = float(value)
            seconds = number / 1000 if abs(number) >= 10**11 else number
            return datetime.fromtimestamp(seconds, UTC).astimezone(TZ)
        text = str(value).strip().replace("Z", "+00:00")
        text = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", text)
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=TZ)
        return parsed.astimezone(TZ)
    except (OverflowError, OSError, ValueError):
        return None


def in_window(value: Any, start: datetime, end: datetime) -> bool:
    parsed = parse_time(value)
    return parsed is not None and start <= parsed < end


def run_json(command: list[str]) -> tuple[Any | None, str | None]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        return None, f"{type(exc).__name__}: {exc}"
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        return None, detail or f"dida exited with {result.returncode}"

    stdout = result.stdout.strip()
    try:
        decoder = json.JSONDecoder()
        for index, character in enumerate(stdout):
            if character not in "[{":
                continue
            try:
                value, _ = decoder.raw_decode(stdout[index:])
                if isinstance(value, dict) and (
                    value.get("ok") is False or value.get("success") is False or value.get("error")
                ):
                    return None, str(value.get("error") or value.get("message") or "dida request failed")
                return value, None
            except json.JSONDecodeError:
                continue
    except (TypeError, ValueError):
        pass
    if any(message.casefold() in stdout.casefold() for message in EMPTY_MESSAGES):
        return [], None
    return None, "dida returned no valid JSON"


def records(payload: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in (*keys, "items", "data", "projects", "tasks"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            nested = records(value, *keys)
            if nested or not value:
                return nested
    return []


def project_index(payload: Any) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in records(payload, "projects"):
        project_id = str(item.get("projectId") or item.get("project_id") or item.get("id") or "").strip()
        name = str(item.get("name") or item.get("title") or item.get("projectName") or "").strip()
        if project_id:
            result[project_id] = name
    return result


def normalize_task(raw: dict[str, Any], projects: dict[str, str], start: datetime, end: datetime) -> dict[str, Any] | None:
    completed = raw.get("completedTime") or raw.get("completed_time") or raw.get("completedAt")
    completed_at = parse_time(completed)
    if completed_at is None or not (start <= completed_at < end):
        return None
    title = str(raw.get("title") or raw.get("name") or raw.get("content") or "").strip()
    if not title:
        return None
    project_id = str(raw.get("projectId") or raw.get("project_id") or "").strip()
    project_name = str(raw.get("projectName") or raw.get("project_name") or projects.get(project_id) or "").strip()
    task_id = str(raw.get("id") or raw.get("taskId") or raw.get("task_id") or "").strip()
    return {
        "id": task_id,
        "title": title,
        "text": title,
        "project": project_name,
        "projectId": project_id,
        "timestamp": completed_at.isoformat(),
        "completedTime": completed_at.isoformat(),
        "status": "completed",
        "url": str(raw.get("url") or raw.get("webUrl") or "").strip(),
    }


def collect(target_date: date) -> dict[str, Any]:
    start, end = target_window(target_date)
    errors: list[str] = []
    project_payload, project_error = run_json(["dida", "project", "list", "--json"])
    if project_error:
        errors.append(f"project list: {project_error}")
        projects: dict[str, str] = {}
    else:
        projects = project_index(project_payload)

    command = ["dida", "task", "completed"]
    if projects:
        command.extend(["--projects", ",".join(projects)])
    command.extend(["--start-date", cli_time(start), "--end-date", cli_time(end), "--json"])
    task_payload, task_error = run_json(command)
    tasks: list[dict[str, Any]] = []
    if task_error:
        errors.append(f"completed tasks: {task_error}")
    else:
        for item in records(task_payload, "tasks"):
            normalized = normalize_task(item, projects, start, end)
            if normalized:
                tasks.append(normalized)

    return {
        "date": target_date.isoformat(),
        "timezone": "Asia/Shanghai",
        "source": "dida",
        "available": task_error is None,
        "projects_checked": len(projects),
        "tasks": tasks,
        "errors": errors,
    }


def main() -> None:
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    output = json.dumps(collect(target_date), ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Dida365 data written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
