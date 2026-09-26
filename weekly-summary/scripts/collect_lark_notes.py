#!/usr/bin/env python3
"""Collect Lark/Feishu daily/weekly/monthly docs needed for a weekly summary.

Reads `summary-shared/lark_folders.json` for folder tokens, then queries the Lark
Drive API via the local `lark-cli` binary to enumerate files in the daily,
weekly and monthly folders. Returns a JSON payload describing:

  - daily_files: docx tokens/urls for each date in the window
  - missing_dates: dates inside the window with no matching daily docx
  - weekly_output_*: target filename, whether it already exists, and a fallback `_v2` name
  - historical_context_files: recent past weeklies and monthlies for cross-period reading

Cross-year aware: filenames carry a `-YY` suffix, so a window spanning Dec/Jan
matches files with both year suffixes.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


SHARED_CONFIG_RELATIVE = Path("..") / ".." / "summary-shared" / "lark_folders.json"


def _resolve_lark_cli() -> str:
    """Resolve `lark-cli` to an absolute path. On Windows it's a `.CMD` shim
    that subprocess.run cannot invoke without an explicit path."""
    resolved = shutil.which("lark-cli")
    if resolved:
        return resolved
    raise SystemExit(
        "lark-cli not found in PATH. Install via `npm i -g @larksuiteoapi/lark-cli` "
        "or activate the lark CLI environment."
    )


_LARK_CLI = None


def _lark_cli_path() -> str:
    global _LARK_CLI
    if _LARK_CLI is None:
        _LARK_CLI = _resolve_lark_cli()
    return _LARK_CLI


def parse_ymd(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def load_config(explicit: Path | None) -> dict:
    if explicit is not None:
        path = explicit
    else:
        path = (Path(__file__).parent / SHARED_CONFIG_RELATIVE).resolve()
    if not path.exists():
        raise SystemExit(f"shared config not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def lark_list_folder(folder_token: str) -> list[dict]:
    """Return all files in a Drive folder, paging through `lark-cli drive files list`."""
    files: list[dict] = []
    page_token = ""
    while True:
        params = {"folder_token": folder_token, "page_size": 200}
        if page_token:
            params["page_token"] = page_token
        cmd = [
            _lark_cli_path(), "drive", "files", "list",
            "--params", json.dumps(params, ensure_ascii=False),
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
        )
        if result.returncode != 0:
            raise SystemExit(
                f"lark-cli failed for folder {folder_token}:\n{result.stderr}"
            )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            raise SystemExit(f"failed to parse lark-cli output: {e}\n{result.stdout[:500]}")
        code = payload.get("code")
        if code is not None and code != 0:
            raise SystemExit(f"lark-cli returned error: {payload}")
        data = payload.get("data") or {}
        files.extend(data.get("files") or [])
        if not data.get("has_more"):
            break
        page_token = data.get("next_page_token") or ""
        if not page_token:
            break
    return files


def daily_name_candidates(d: date) -> list[str]:
    """Possible filenames for a daily docx — Feishu uses `M.D-YY` (no pad)."""
    yy = d.year % 100
    return list(dict.fromkeys([
        f"{d.month}.{d.day}-{yy:02d}",
        f"{d.month}.{d.day:02d}-{yy:02d}",
    ]))


def parse_daily_filename(name: str) -> tuple[int, int, int] | None:
    """Return (year, month, day) from a daily filename, or None if not parseable."""
    m = re.fullmatch(r"(\d{1,2})\.(\d{1,2})-(\d{2})", name)
    if not m:
        return None
    return 2000 + int(m.group(3)), int(m.group(1)), int(m.group(2))


def parse_weekly_filename(name: str) -> tuple[int, int, int] | None:
    """Return (year, start_month, start_day) for sorting; supports M.D and M.DD."""
    m = re.fullmatch(
        r"(\d{1,2})\.(\d{1,2})～(\d{1,2})\.(\d{1,2})-(\d{2})", name
    )
    if not m:
        return None
    return 2000 + int(m.group(5)), int(m.group(1)), int(m.group(2))


def parse_monthly_filename(name: str) -> tuple[int, int] | None:
    m = re.fullmatch(r"(\d{1,2})月-(\d{2})", name)
    if not m:
        return None
    return 2000 + int(m.group(2)), int(m.group(1))


def match_daily_file(files: list[dict], d: date) -> dict | None:
    candidates = set(daily_name_candidates(d))
    for f in files:
        if f.get("type") == "docx" and f.get("name") in candidates:
            return f
    return None


def find_weekly_output(files: list[dict], output_basename: str) -> dict | None:
    for f in files:
        if f.get("type") == "docx" and f.get("name") == output_basename:
            return f
    return None


def collect(config: dict, start: date, end: date,
            weekly_context_limit: int = 8,
            monthly_context_limit: int = 2) -> dict:
    daily_token = config["daily_folder_token"]
    weekly_token = config["weekly_folder_token"]
    monthly_token = config["monthly_folder_token"]

    daily_files = lark_list_folder(daily_token)
    weekly_files = lark_list_folder(weekly_token)
    monthly_files = lark_list_folder(monthly_token)

    # Daily window
    days = []
    matched: list[dict] = []
    missing: list[str] = []
    cur = start
    while cur <= end:
        f = match_daily_file(daily_files, cur)
        item = {
            "date": cur.isoformat(),
            "matched": f is not None,
        }
        if f is not None:
            item.update({
                "name": f["name"],
                "token": f["token"],
                "url": f["url"],
            })
            matched.append({
                "date": cur.isoformat(),
                "name": f["name"],
                "token": f["token"],
                "url": f["url"],
            })
        else:
            missing.append(cur.isoformat())
        days.append(item)
        cur += timedelta(days=1)

    # Weekly target name & existence
    yy = start.year % 100
    output_basename = f"{start.month}.{start.day:02d}～{end.month}.{end.day:02d}-{yy:02d}"
    output_basename_v2 = f"{output_basename}_v2"
    target_existing = find_weekly_output(weekly_files, output_basename)

    # Historical weekly context: files whose start date < this window's start
    weekly_with_key = []
    for f in weekly_files:
        if f.get("type") != "docx":
            continue
        key = parse_weekly_filename(f.get("name", ""))
        if key is None:
            continue
        weekly_with_key.append((key, f))
    weekly_with_key.sort(key=lambda x: x[0])
    target_key = (start.year, start.month, start.day)
    older_weekly = [(k, f) for (k, f) in weekly_with_key if k < target_key]
    weekly_context = [
        {"name": f["name"], "token": f["token"], "url": f["url"]}
        for (_, f) in list(reversed(older_weekly))[:weekly_context_limit]
    ]

    # Historical monthly context
    monthly_with_key = []
    for f in monthly_files:
        if f.get("type") != "docx":
            continue
        key = parse_monthly_filename(f.get("name", ""))
        if key is None:
            continue
        monthly_with_key.append((key, f))
    monthly_with_key.sort(key=lambda x: x[0])
    target_month_key = (end.year, end.month)
    older_monthly = [(k, f) for (k, f) in monthly_with_key if k < target_month_key]
    monthly_context = [
        {"name": f["name"], "token": f["token"], "url": f["url"]}
        for (_, f) in list(reversed(older_monthly))[:monthly_context_limit]
    ]

    return {
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "weekly_folder_token": weekly_token,
        "weekly_output_basename": output_basename,
        "weekly_output_filename": f"{output_basename}.md",
        "weekly_output_exists": target_existing is not None,
        "weekly_output_existing_url": (target_existing or {}).get("url"),
        "weekly_output_existing_token": (target_existing or {}).get("token"),
        "weekly_output_basename_v2": output_basename_v2,
        "days": days,
        "matched_daily_files": matched,
        "missing_dates": missing,
        "historical_context_files": {
            "weekly_files": weekly_context,
            "monthly_files": monthly_context,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Collect Lark daily/weekly/monthly docs needed for a weekly summary."
    )
    parser.add_argument("--start", required=True, help="Start date in YYYY-MM-DD.")
    parser.add_argument("--end", required=True, help="End date in YYYY-MM-DD.")
    parser.add_argument(
        "--config",
        default=None,
        help="Path to shared lark_folders.json (default: ../../summary-shared/lark_folders.json).",
    )
    parser.add_argument(
        "--weekly-context-limit", type=int, default=8,
        help="How many older weekly summaries to surface for cross-period reading.",
    )
    parser.add_argument(
        "--monthly-context-limit", type=int, default=2,
        help="How many recent monthly summaries to surface for cross-period reading.",
    )
    args = parser.parse_args()

    config = load_config(Path(args.config) if args.config else None)
    result = collect(
        config,
        parse_ymd(args.start),
        parse_ymd(args.end),
        args.weekly_context_limit,
        args.monthly_context_limit,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
