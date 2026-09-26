#!/usr/bin/env python3
"""Build one unified evidence packet for a daily-summary subagent.

This script deliberately does not write prose. It normalizes all available
source files into one date-scoped packet so that two scoped low-cost subagents
can aggregate the complete picture before the main model writes one report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    from zoneinfo import ZoneInfo

    TZ = ZoneInfo("Asia/Shanghai")
except Exception:  # pragma: no cover - only for unusually old Python builds
    TZ = timezone(timedelta(hours=8))


SOURCE_OPTIONS = (
    "lark_docs",
    "github",
    "claude",
    "codex",
    "kimi",
    "dsh",
    "opencode",
    "craft",
    "computer_history",
    "remote",
    "linear",
    "dida",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize daily-summary sources into one evidence packet"
    )
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--lark-docs", dest="lark_docs", help="Lark documents JSON")
    parser.add_argument("--github", help="GitHub activity JSON")
    parser.add_argument("--claude", help="Claude Code history JSON")
    parser.add_argument("--codex", help="Codex history JSON")
    parser.add_argument("--kimi", help="Kimi Code history JSON")
    parser.add_argument("--dsh", help="DeepSeek Harness history JSON")
    parser.add_argument("--opencode", help="OpenCode history JSON")
    parser.add_argument("--craft", help="Craft Agent history JSON")
    parser.add_argument(
        "--computer-history",
        dest="computer_history",
        help="Computer History observations JSON",
    )
    parser.add_argument("--remote", help="Remote agent history JSON")
    parser.add_argument("--linear", help="Linear issues JSON")
    parser.add_argument(
        "--dida", "--ticktick", dest="dida", help="Domestic Dida365 completed tasks JSON"
    )
    parser.add_argument(
        "--existing-report",
        help="Existing report Markdown or JSON wrapper to include in the packet",
    )
    parser.add_argument(
        "--style-samples",
        help="Recent personal daily-note samples JSON or Markdown",
    )
    parser.add_argument("-o", "--output", help="Output packet path (default: stdout)")
    return parser.parse_args()


def load_json(path: str | None) -> tuple[Any | None, dict[str, Any]]:
    """Load an optional JSON file without making one bad source fatal."""
    if not path:
        return None, {"status": "not_requested"}

    file_path = Path(path).expanduser()
    if not file_path.exists():
        return None, {"status": "missing", "path": str(file_path)}

    try:
        with file_path.open("r", encoding="utf-8") as handle:
            return json.load(handle), {"status": "ok", "path": str(file_path)}
    except (OSError, UnicodeError) as exc:
        return None, {
            "status": "error",
            "path": str(file_path),
            "error": f"{type(exc).__name__}: {exc}",
        }
    except json.JSONDecodeError as exc:
        return None, {
            "status": "invalid",
            "path": str(file_path),
            "error": f"JSONDecodeError: {exc}",
        }


def load_text_or_json(path: str | None) -> tuple[Any | None, dict[str, Any]]:
    """Load Markdown as text and JSON as structured data."""
    if not path:
        return None, {"status": "not_requested"}

    file_path = Path(path).expanduser()
    if not file_path.exists():
        return None, {"status": "missing", "path": str(file_path)}

    try:
        text = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, {
            "status": "error",
            "path": str(file_path),
            "error": f"{type(exc).__name__}: {exc}",
        }

    try:
        return json.loads(text), {"status": "ok", "path": str(file_path)}
    except json.JSONDecodeError:
        return text, {"status": "ok", "path": str(file_path), "format": "text"}


def parse_datetime(value: Any) -> datetime | None:
    """Parse common epoch and ISO-8601 timestamp forms into Asia/Shanghai."""
    if value is None or value == "":
        return None

    if isinstance(value, (int, float)):
        try:
            number = float(value)
            seconds = number / 1000 if abs(number) >= 10**11 else number
            return datetime.fromtimestamp(seconds, tz=timezone.utc).astimezone(TZ)
        except (OverflowError, OSError, ValueError):
            return None

    if not isinstance(value, str):
        return None

    text = value.strip()
    if not text:
        return None
    if text.isdigit():
        return parse_datetime(int(text))

    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=TZ)
    return parsed.astimezone(TZ)


def iso_time(value: Any) -> str:
    parsed = parse_datetime(value)
    return parsed.isoformat() if parsed else ""


def is_target_date(value: Any, target_date: date) -> bool:
    parsed = parse_datetime(value)
    # A record without a parseable timestamp cannot be assigned to a natural
    # day.  Dropping it is safer than leaking an event from another day.
    return parsed is not None and parsed.date() == target_date


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def first_nonempty(*values: Any) -> Any:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        if isinstance(value, (list, dict)) and not value:
            continue
        return value
    return ""


def text_value(value: Any) -> str:
    """Extract text from a source item without interpreting it as instructions."""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = [text_value(item) for item in value]
        return "\n".join(part for part in parts if part).strip()
    if not isinstance(value, dict):
        return str(value).strip() if value is not None else ""

    for key in ("text", "display", "content", "body", "summary", "description"):
        candidate = value.get(key)
        if isinstance(candidate, (str, list)):
            text = text_value(candidate)
            if text:
                return text
    return ""


def nested_name(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return str(
            first_nonempty(value.get("full_name"), value.get("name"), value.get("login"), "")
        ).strip()
    return ""


def project_fields(
    item: dict[str, Any], session: dict[str, Any] | None = None
) -> tuple[str, str, str, str]:
    session = session or {}
    repository = first_nonempty(
        item.get("repository"),
        item.get("repo"),
        item.get("git_repo"),
        session.get("repository"),
        session.get("repo"),
        session.get("git_repo"),
    )
    repo = nested_name(repository)
    branch = str(
        first_nonempty(
            item.get("branch"),
            item.get("git_branch"),
            session.get("branch"),
            session.get("git_branch"),
            "",
        )
    ).strip()
    cwd = str(first_nonempty(item.get("cwd"), session.get("cwd"), "")).strip()

    project = repo
    if not project and cwd:
        parts = [part for part in re.split(r"[/\\]", cwd) if part]
        ignored = {"users", "fullstop", "desktop", "documents", "code", "workspace", "home"}
        for part in reversed(parts):
            if part.lower() not in ignored and not part.startswith("."):
                project = part
                break
    if not project:
        project = str(first_nonempty(item.get("project"), session.get("project"), "其他")).strip() or "其他"

    project_key = project
    if branch and branch not in {"main", "master", "HEAD"}:
        project_key = f"{project} ({branch})"
    return project_key, repo, branch, cwd


def event_id(
    source: str, item: dict[str, Any], *, text: str, timestamp: str, index: int
) -> str:
    raw = first_nonempty(
        item.get("id"),
        item.get("node_id"),
        item.get("token"),
        item.get("url"),
        item.get("html_url"),
        f"{timestamp}|{text}|{index}",
    )
    digest = hashlib.sha1(f"{source}|{raw}".encode("utf-8", "replace")).hexdigest()[:16]
    return f"{source}:{digest}"


def make_event(
    source: str,
    item: dict[str, Any],
    *,
    session: dict[str, Any] | None = None,
    kind: str,
    index: int,
    target_date: date,
    default_status: str = "unknown",
    evidence_level: str = "source_record",
) -> dict[str, Any] | None:
    project, repo, branch, cwd = project_fields(item, session)
    raw_time = first_nonempty(
        item.get("timestamp"),
        item.get("time"),
        item.get("updated_at"),
        item.get("modified_time"),
        item.get("modifiedTime"),
        item.get("modified_at"),
        item.get("created_at"),
        item.get("created_time"),
        item.get("createdAt"),
        item.get("published_at"),
        item.get("merged_at"),
        item.get("completedTime"),
        item.get("completed_time"),
        (session or {}).get("timestamp"),
        (session or {}).get("updated_at"),
        (session or {}).get("started_at"),
    )
    if not raw_time or not is_target_date(raw_time, target_date):
        return None
    timestamp = iso_time(raw_time)
    if not timestamp:
        return None

    title = str(
        first_nonempty(
            item.get("title"),
            item.get("name"),
            item.get("thread_name"),
            item.get("subject"),
            "",
        )
    ).strip()
    text = text_value(item)
    if not text and title:
        text = title
    if not text and not title:
        return None

    status_value = first_nonempty(
        item.get("status"), item.get("state"), item.get("action"), default_status
    )
    if isinstance(status_value, dict):
        status_value = first_nonempty(status_value.get("name"), default_status)
    status = str(status_value).strip()

    url = str(first_nonempty(item.get("url"), item.get("html_url"), item.get("web_url"), "")).strip()
    evidence = [url] if url else []
    return {
        "event_id": event_id(source, item, text=text, timestamp=timestamp, index=index),
        "source": source,
        "time": timestamp,
        "project": project,
        "repo": repo,
        "branch": branch,
        "cwd": cwd,
        "kind": kind,
        "status": status,
        "title": title,
        "text": text,
        "url": url,
        "evidence": evidence,
        "evidence_level": evidence_level,
    }


def source_items(data: Any, *keys: str) -> list[Any]:
    if isinstance(data, list):
        return data
    if not isinstance(data, dict):
        return []
    for key in keys:
        if key in data:
            return as_list(data[key])
    nested = data.get("data")
    if isinstance(nested, dict):
        for key in keys:
            if key in nested:
                return as_list(nested[key])
    return []


def session_events(
    source: str,
    data: Any,
    target_date: date,
    *,
    remote: bool = False,
) -> list[dict[str, Any]]:
    sessions: list[dict[str, Any]] = []
    if isinstance(data, dict):
        if remote:
            sessions.extend(
                {**item, "_remote_kind": "claude"}
                for item in source_items(data, "claude_sessions")
                if isinstance(item, dict)
            )
            sessions.extend(
                {**item, "_remote_kind": "codex"}
                for item in source_items(data, "codex_sessions")
                if isinstance(item, dict)
            )
        else:
            sessions.extend(item for item in source_items(data, "sessions") if isinstance(item, dict))
    elif isinstance(data, list):
        sessions.extend(item for item in data if isinstance(item, dict))

    events: list[dict[str, Any]] = []
    index = 0
    for session in sessions:
        messages = first_nonempty(
            session.get("inputs"),
            session.get("user_messages"),
            session.get("messages"),
            [],
        )
        if not isinstance(messages, list):
            messages = [messages]
        if not messages:
            fallback = first_nonempty(
                session.get("display"),
                session.get("thread_name"),
                session.get("title"),
                session.get("last_prompt"),
                "",
            )
            messages = [fallback] if fallback else []

        for message in messages:
            item = dict(message) if isinstance(message, dict) else {"text": str(message)}
            if not item.get("text") and item.get("display"):
                item["text"] = item["display"]
            event = make_event(
                source,
                item,
                session=session,
                kind="conversation",
                index=index,
                target_date=target_date,
                default_status="observed" if remote else "unknown",
                evidence_level="observed_activity" if remote else "user_input",
            )
            index += 1
            if event:
                events.append(event)
    return events


def documents_events(source: str, data: Any, target_date: date) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, raw in enumerate(source_items(data, "documents", "files", "items")):
        if not isinstance(raw, dict):
            continue
        item = dict(raw)
        item["text"] = first_nonempty(
            item.get("summary"),
            item.get("content_preview"),
            item.get("name"),
            item.get("title"),
            "",
        )
        event = make_event(
            source,
            item,
            kind="document",
            index=index,
            target_date=target_date,
            default_status="updated",
            evidence_level="document_metadata",
        )
        if event:
            events.append(event)
    return events


def github_events(data: Any, target_date: date) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not isinstance(data, dict):
        return events

    collections = (
        ("events", "github_event"),
        ("notifications", "github_notification"),
        ("commits", "commit"),
        ("prs", "pull_request"),
        ("pull_requests", "pull_request"),
        ("issues", "issue"),
        ("reviews", "review"),
        ("releases", "release"),
        ("workflows", "workflow"),
    )
    index = 0
    for key, kind in collections:
        for raw in source_items(data, key):
            if not isinstance(raw, dict):
                continue
            event = make_event(
                "github",
                raw,
                kind=kind,
                index=index,
                target_date=target_date,
                default_status="observed",
                evidence_level="github_record",
            )
            index += 1
            if event:
                events.append(event)
    return events


def task_events(source: str, data: Any, target_date: date, key: str, kind: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, raw in enumerate(source_items(data, key, "items", "data")):
        if not isinstance(raw, dict):
            continue
        event = make_event(
            source,
            raw,
            kind=kind,
            index=index,
            target_date=target_date,
            default_status="completed" if source == "dida" else "observed",
            evidence_level="task_record" if source == "dida" else "issue_record",
        )
        if event:
            events.append(event)
    return events


def computer_history_events(data: Any, target_date: date) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not isinstance(data, dict):
        return events
    observations = source_items(data, "events", "observations")
    memories = source_items(data, "memories", "summaries")
    for index, raw in enumerate([*observations, *memories]):
        if not isinstance(raw, dict):
            raw = {"text": text_value(raw)}
        item = dict(raw)
        ax_evidence = str(item.get("ax_evidence") or "").strip()
        observed_text = first_nonempty(
            item.get("summary"),
            item.get("text"),
            item.get("selected_text"),
            item.get("focused_element"),
            item.get("window_title"),
            item.get("url"),
            item.get("app"),
            "",
        )
        if ax_evidence and ax_evidence not in str(observed_text):
            observed_text = " | ".join(
                part for part in (str(observed_text), f"AX outcome: {ax_evidence}") if part
            )
        item["text"] = str(observed_text)[:2200]
        evidence_level = "observed_ui_state" if ax_evidence else "observed_activity_only"
        event = make_event(
            "computer_history",
            item,
            kind="computer_observation",
            index=index,
            target_date=target_date,
            default_status="observed",
            evidence_level=evidence_level,
        )
        if event:
            events.append(event)
    return events


def exact_dedupe(events: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove only exact duplicates; semantic grouping belongs to the subagent."""
    result = []
    seen: set[tuple[str, str, str, str]] = set()
    for event in events:
        key = (
            str(event.get("source", "")),
            str(event.get("time", "")),
            str(event.get("text", "")),
            str(event.get("url", "")),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(event)
    return result


def style_items(value: Any) -> list[Any]:
    if isinstance(value, str):
        return [{"content": value}]
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return as_list(
            first_nonempty(value.get("style_samples"), value.get("documents"), value.get("files"), value)
        )
    return []


def compact_source_metadata(value: Any) -> dict[str, Any]:
    """Keep small source-level fields without duplicating every event payload."""
    if not isinstance(value, dict):
        return {}
    metadata: dict[str, Any] = {}
    useful_keys = {
        "source",
        "status",
        "available",
        "reachable",
        "host",
        "note",
        "errors",
        "repos",
        "folder_tokens",
        "target_name",
        "evidence_quality",
        "scan_all",
        "timezone",
    }
    for key in useful_keys:
        if key not in value:
            continue
        item = value[key]
        if isinstance(item, (str, int, float, bool)) or item is None:
            metadata[key] = item
        elif isinstance(item, list) and all(isinstance(part, (str, int, float, bool)) for part in item):
            metadata[key] = item
    return metadata


def source_load_status(data: Any, load_status: dict[str, Any]) -> dict[str, Any]:
    """Distinguish a readable JSON file from an unavailable upstream source."""
    result = dict(load_status)
    if not isinstance(data, dict) or result.get("status") != "ok":
        return result

    upstream_state = data.get("status")
    if isinstance(upstream_state, (str, int, float, bool)):
        result["source_state"] = upstream_state
    if data.get("available") is False or data.get("reachable") is False:
        result["load_status"] = "ok"
        result["status"] = "unavailable"
    elif data.get("errors"):
        result["status"] = "partial"
    return result


SUMMARY_CONTRACT = {
    "language": "zh-CN",
    "voice": "短句、记录式、自然口语；允许保留用户的判断和不确定性",
    "structure": [
        "只保留一个 # 主要内容",
        "事情少时直接列 bullet，不强行创建项目标题",
        "项目较多时使用 2-4 个简短的 ## 标题；每个项目通常 1-3 条",
        "普通日报控制在约 4-10 条；高信息量日只保留影响后续行动的明细",
        "# 记录只放生活琐事、临时杂事、零散链接和补充备注",
    ],
    "retain": ["事实", "结果", "数量", "截止时间", "状态", "地点", "渠道", "下一步", "真实感受"],
    "merge": ["同一目标的多次对话", "同类投递/沟通", "没有独立结果的零散操作"],
    "selection_policy": [
        "先找已落地的结果和状态变化，例如论文投稿、稿件进入审理、代码合并、任务完成；不要让过程细节盖过结果",
        "每条主要内容必须对应明确项目/目标，并有可定位证据；优先用最终文档、平台状态或完成任务记录，Computer History 的明确页面状态可作状态证据",
        "普通浏览、重复查询、登录/权限/网页故障排查、读指南、工具安装过程默认省略；只有形成重要决定、真实阻塞或明确下一步时才保留结果",
        "面试企业等归因有冲突或尚未核实的内容不写成事实；无后续行动价值的待核实线索不进入日报",
        "用滴答清单（国内版）的完成任务核对当天工作，并与文档、会话或 Computer History 证据关联；不能把计划任务说成已完成",
    ],
    "avoid": [
        "按数据源分栏",
        "逐条复制 Agent 用户输入",
        "凭空补写完成结论",
        "项目背景、工具层状态、采集过程",
        "不痛不痒的中间操作、没有结果的搜索和浏览、纯故障排查记录",
        "全面推进、取得阶段性成果等报告腔",
    ],
    "completion_policy": "只有最终产物、权威平台状态、本人 GitHub 动作或已完成任务记录支持时才写确定结果；普通 Computer History 活动和用户提问只是活动线索，明确的界面终态可作为状态证据并尽量交叉核对。",
}


def build_packet(args: argparse.Namespace) -> dict[str, Any]:
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    loaded: dict[str, Any] = {}
    source_status: dict[str, dict[str, Any]] = {}
    source_metadata: dict[str, dict[str, Any]] = {}

    for source in SOURCE_OPTIONS:
        path = getattr(args, source)
        data, status = load_json(path)
        source_status[source] = source_load_status(data, status)
        if data is not None:
            loaded[source] = data
            source_metadata[source] = compact_source_metadata(data)

    existing_report, existing_status = load_text_or_json(args.existing_report)
    style_samples, style_status = load_text_or_json(args.style_samples)

    events: list[dict[str, Any]] = []
    events.extend(documents_events("lark_docs", loaded.get("lark_docs"), target_date))
    events.extend(github_events(loaded.get("github"), target_date))
    for source in ("claude", "codex", "kimi", "dsh", "opencode", "craft"):
        events.extend(session_events(source, loaded.get(source), target_date))
    events.extend(session_events("remote", loaded.get("remote"), target_date, remote=True))
    events.extend(task_events("linear", loaded.get("linear"), target_date, "issues", "linear_issue"))
    events.extend(task_events("dida", loaded.get("dida"), target_date, "tasks", "task"))
    events.extend(computer_history_events(loaded.get("computer_history"), target_date))
    events = exact_dedupe(events)
    events.sort(key=lambda item: (item.get("time", ""), item.get("source", ""), item.get("event_id", "")))

    by_project: dict[str, list[str]] = defaultdict(list)
    for event in events:
        by_project[event["project"]].append(event["event_id"])

    return {
        "date": args.date,
        "timezone": "Asia/Shanghai",
        "source_status": source_status,
        "events": events,
        "events_by_project": dict(sorted(by_project.items())),
        "source_metadata": source_metadata,
        "style_samples": style_items(style_samples),
        "style_samples_status": style_status,
        "existing_report": existing_report if existing_report is not None else "",
        "existing_report_status": existing_status,
        "summary_contract": SUMMARY_CONTRACT,
        "_instructions": (
            "This is one unified evidence packet. Two low-cost subagents must read the same packet in parallel: "
            "the local-scope agent extracts material outcomes from every non-remote source, and the remote-scope agent summarizes only "
            "remote activity. They must output structured evidence digests, not a final report. The main model "
            "then reads both digests, the existing report, and personal style samples before drafting one concise "
            "Chinese daily note. Do not create a separate paragraph for each source. Treat observed "
            "routine Computer History activity and user requests as evidence of activity only, not proof of "
            "completion. Keep missing/failed sources out of the prose unless they materially affect "
            "confidence. Prefer outcomes and actionable next steps; omit routine browsing, login troubleshooting, "
            "unresolved attribution, and intermediate process detail. The main model owns cross-source selection "
            "and final wording; the two subagents only prepare scoped evidence digests."
        ),
    }


def main() -> None:
    args = parse_args()
    packet = build_packet(args)
    output = json.dumps(packet, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Unified evidence packet written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
