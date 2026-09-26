#!/usr/bin/env python3
"""Collect date-scoped Feishu document metadata and personal style samples.

The collector uses lark-cli in read-only mode. Daily reports in the configured
daily folder are treated as style references, not as new work output.
"""

from __future__ import annotations

import argparse
import html
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


DAILY_NAME = re.compile(r"^\d{1,2}\.\d{1,2}-\d{2}$")
MAX_SEARCH_PAGES = 50


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect Feishu documents and recent daily-note style samples"
    )
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument(
        "--config",
        default="~/.claude/skills/summary-shared/lark_folders.json",
        help="Folder-token JSON configuration",
    )
    parser.add_argument(
        "--folder-token",
        action="append",
        dest="folder_tokens",
        help="Folder token to inspect; may be repeated",
    )
    parser.add_argument(
        "--style-limit", type=int, default=6, help="Number of recent daily notes to sample"
    )
    parser.add_argument(
        "--fetch-content",
        action="store_true",
        help="Fetch Markdown content for changed non-daily documents",
    )
    parser.add_argument("--output", help="Output JSON path (default: stdout)")
    return parser.parse_args()


def target_window(target_date: date) -> tuple[datetime, datetime]:
    start = datetime.combine(target_date, time.min, tzinfo=TZ)
    return start, start + timedelta(days=1)


def parse_time(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    try:
        if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
            number = float(value)
            seconds = number / 1000 if abs(number) >= 10**11 else number
            return datetime.fromtimestamp(seconds, timezone.utc).astimezone(TZ)
        text = str(value).strip().replace("Z", "+00:00")
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=TZ)
        return parsed.astimezone(TZ)
    except (OverflowError, OSError, ValueError):
        return None


def iso(value: Any) -> str:
    parsed = parse_time(value)
    return parsed.isoformat() if parsed else ""


def in_window(value: Any, start: datetime, end: datetime) -> bool:
    parsed = parse_time(value)
    return parsed is not None and start <= parsed < end


def extract_json(stdout: str) -> Any:
    """Parse lark-cli JSON even when pagination progress precedes it."""
    decoder = json.JSONDecoder()
    for index, char in enumerate(stdout):
        if char not in "[{":
            continue
        try:
            value, _ = decoder.raw_decode(stdout[index:])
            return value
        except json.JSONDecodeError:
            continue
    raise ValueError("lark-cli did not return JSON")


def run_lark(args: list[str]) -> Any:
    command = ["lark-cli", *args, "--format", "json", "--as", "user"]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=90,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(detail or f"lark-cli exited with {result.returncode}")
    payload = extract_json(result.stdout)
    if isinstance(payload, dict) and payload.get("ok") is False:
        raise RuntimeError(str(payload.get("error") or payload.get("message") or "lark-cli request failed"))
    return payload


def load_config(path: str) -> dict[str, Any]:
    file_path = Path(path).expanduser()
    if not file_path.exists():
        return {}
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}


def files_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        data = payload.get("data", payload)
        if isinstance(data, dict):
            files = data.get("files", data.get("items", []))
            return [item for item in files if isinstance(item, dict)]
    return []


def search_page(payload: Any) -> tuple[list[dict[str, Any]], bool, str]:
    data = payload.get("data", payload) if isinstance(payload, dict) else {}
    if not isinstance(data, dict):
        raise ValueError("global search response has no data object")
    if "results" not in data and "items" not in data:
        raise ValueError("global search response has no results field")
    results = data.get("results", data.get("items", []))
    rows = [item for item in results if isinstance(item, dict)] if isinstance(results, list) else []
    return rows, bool(data.get("has_more")), str(data.get("page_token") or "")


def clean_highlight(value: Any) -> str:
    text = str(value or "")
    text = re.sub(r"</?h(?:b)?\s*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def document_record(raw: dict[str, Any], folder_token: str, start: datetime, end: datetime) -> dict[str, Any]:
    created = parse_time(
        raw.get("created_time") or raw.get("createdTime") or raw.get("create_time_iso") or raw.get("create_time")
    )
    modified = parse_time(
        raw.get("modified_time")
        or raw.get("modifiedTime")
        or raw.get("modified_at")
        or raw.get("update_time_iso")
        or raw.get("update_time")
    )
    name = str(raw.get("name") or raw.get("title") or "").strip()
    return {
        "name": name,
        "token": str(raw.get("token") or raw.get("document_id") or ""),
        "url": str(raw.get("url") or "").strip(),
        "type": str(raw.get("type") or ""),
        "folder_token": folder_token,
        "created_at": created.isoformat() if created else "",
        "modified_at": modified.isoformat() if modified else "",
        "changed_on_target_date": bool(
            (created and start <= created < end) or (modified and start <= modified < end)
        ),
        "is_daily_report": bool(DAILY_NAME.match(name)),
    }


def search_document_record(raw: dict[str, Any], start: datetime, end: datetime) -> dict[str, Any]:
    meta = raw.get("result_meta") if isinstance(raw.get("result_meta"), dict) else raw
    item = dict(meta)
    item["name"] = clean_highlight(raw.get("title_highlighted") or meta.get("name") or meta.get("title"))
    item["url"] = str(meta.get("url") or raw.get("url") or "").strip()
    doc_types = meta.get("doc_types") or raw.get("entity_type") or ""
    item["type"] = ",".join(str(value) for value in doc_types) if isinstance(doc_types, list) else str(doc_types)
    record = document_record(item, "", start, end)
    record["summary"] = clean_highlight(raw.get("summary_highlighted"))
    record["edit_user_name"] = str(meta.get("edit_user_name") or "")
    record["container_id"] = str(meta.get("space_id") or meta.get("folder_token") or "")
    record["source"] = "global_edit_search"
    return record


def collect_edited_documents(start: datetime, end: datetime) -> tuple[list[dict[str, Any]], list[str]]:
    documents: list[dict[str, Any]] = []
    errors: list[str] = []
    page_token = ""
    seen_tokens: set[str] = set()
    for page_number in range(MAX_SEARCH_PAGES):
        command = [
            "drive",
            "+search",
            "--query",
            "",
            "--edited-since",
            start.isoformat(),
            "--edited-until",
            end.isoformat(),
            "--doc-types",
            "doc,docx,wiki",
            "--sort",
            "edit_time",
            "--page-size",
            "20",
        ]
        if page_token:
            command.extend(["--page-token", page_token])
        try:
            rows, has_more, next_token = search_page(run_lark(command))
        except (RuntimeError, ValueError, subprocess.SubprocessError) as exc:
            errors.append(f"global edited-document search: {exc}")
            break
        documents.extend(search_document_record(row, start, end) for row in rows)
        if not has_more:
            break
        if not next_token or next_token in seen_tokens:
            errors.append("global edited-document search returned an invalid/repeated page token")
            break
        seen_tokens.add(next_token)
        page_token = next_token
    else:
        errors.append(f"global edited-document search stopped after {MAX_SEARCH_PAGES} pages; results may be incomplete")
    return documents, errors


def fetch_content(doc_ref: str) -> str:
    if not doc_ref:
        return ""
    payload = run_lark(["docs", "+fetch", "--doc", doc_ref, "--doc-format", "markdown"])
    data = payload.get("data", payload) if isinstance(payload, dict) else {}
    document = data.get("document", {}) if isinstance(data, dict) else {}
    return str(document.get("content") or "")


def main() -> None:
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    start, end = target_window(target_date)
    config = load_config(args.config)
    folder_tokens = args.folder_tokens or ([config.get("daily_folder_token")] if config.get("daily_folder_token") else [])
    folder_tokens = [token for token in folder_tokens if token]

    errors: list[str] = []
    all_files: list[dict[str, Any]] = []
    folder_queries_succeeded = 0
    for folder_token in folder_tokens:
        try:
            payload = run_lark(
                [
                    "drive",
                    "files",
                    "list",
                    "--folder-token",
                    folder_token,
                    "--page-size",
                    "200",
                    "--order-by",
                    "EditedTime",
                    "--direction",
                    "DESC",
                    "--page-all",
                    "--page-limit",
                    "10",
                ]
            )
            folder_queries_succeeded += 1
            all_files.extend(
                document_record(item, folder_token, start, end)
                for item in files_from_payload(payload)
            )
        except (RuntimeError, ValueError, subprocess.SubprocessError) as exc:
            errors.append(f"folder {folder_token}: {exc}")

    global_documents, search_errors = collect_edited_documents(start, end)
    all_files.extend(global_documents)
    errors.extend(search_errors)

    unique_files: dict[str, dict[str, Any]] = {}
    for item in all_files:
        key = item["token"] or f"{item['folder_token']}:{item['name']}:{item['modified_at']}"
        unique_files[key] = item

    target_name = f"{target_date.month}.{target_date.day}-{str(target_date.year)[-2:]}"
    target_reports = [
        item for item in unique_files.values() if item["is_daily_report"] and item["name"] == target_name
    ]
    target_reports.sort(key=lambda item: item["modified_at"] or item["created_at"], reverse=True)
    if len(target_reports) == 1:
        try:
            target_reports[0]["content"] = fetch_content(target_reports[0]["url"] or target_reports[0]["token"])
        except (RuntimeError, ValueError, subprocess.SubprocessError) as exc:
            target_reports[0]["content_error"] = str(exc)
    elif len(target_reports) > 1:
        errors.append(f"multiple daily reports match {target_name}; do not write until the target is resolved")

    changed_documents = [
        item
        for item in unique_files.values()
        if item["changed_on_target_date"]
        and not (item["is_daily_report"] and item["name"] == target_name)
        and not item["is_daily_report"]
    ]
    changed_documents.sort(key=lambda item: item["modified_at"], reverse=True)

    if args.fetch_content:
        for item in changed_documents:
            try:
                item["content"] = fetch_content(item["url"] or item["token"])
            except (RuntimeError, ValueError, subprocess.SubprocessError) as exc:
                item["content_error"] = str(exc)

    style_candidates = [
        item
        for item in unique_files.values()
        if item["is_daily_report"] and item["name"] != target_name
    ]
    style_candidates.sort(key=lambda item: item["modified_at"] or item["created_at"], reverse=True)
    style_samples: list[dict[str, Any]] = []
    for item in style_candidates[: max(args.style_limit, 0)]:
        sample = dict(item)
        try:
            sample["content"] = fetch_content(item["url"] or item["token"])
        except (RuntimeError, ValueError, subprocess.SubprocessError) as exc:
            sample["content_error"] = str(exc)
        style_samples.append(sample)

    output = {
        "date": args.date,
        "timezone": "Asia/Shanghai",
        "source": "lark_docs",
        "available": bool(folder_queries_succeeded or global_documents or not search_errors),
        "folder_tokens": folder_tokens,
        "target_name": target_name,
        "target_reports": target_reports,
        "target_ambiguous": len(target_reports) > 1,
        "documents": changed_documents,
        "style_samples": style_samples,
        "errors": errors,
    }
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        print(f"Lark document data written to: {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
