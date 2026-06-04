#!/usr/bin/env python3
"""Collect Lark/Feishu daily/weekly/monthly docs needed for a monthly summary.

Reads `summary-shared/lark_folders.json` for folder tokens and queries the Lark
Drive API via `lark-cli` to find:

  - daily docs that fall within the target month (with cross-year aware match)
  - weekly docs that overlap the target month (supplementary evidence)
  - the target monthly docx filename (`M月-YY`) and whether it already exists
  - the most recent N monthly docs before the target month (historical context)
"""

import argparse
import json
import re
import shutil
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional


SHARED_CONFIG_RELATIVE = Path("..") / ".." / "summary-shared" / "lark_folders.json"


def parse_month_arg(value: str) -> tuple[int, int]:
    dt = datetime.strptime(value, "%Y-%m")
    return dt.year, dt.month


def month_range(year: int, month: int) -> tuple[date, date]:
    start = date(year, month, 1)
    if month == 12:
        end = date(year, 12, 31)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)
    return start, end


def load_config(explicit: Optional[Path]) -> dict:
    path = explicit if explicit else (Path(__file__).parent / SHARED_CONFIG_RELATIVE).resolve()
    if not path.exists():
        raise SystemExit(f"shared config not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


_LARK_CLI: Optional[str] = None


def _lark_cli_path() -> str:
    global _LARK_CLI
    if _LARK_CLI is None:
        resolved = shutil.which("lark-cli")
        if not resolved:
            raise SystemExit("lark-cli not found in PATH")
        _LARK_CLI = resolved
    return _LARK_CLI


def lark_list_folder(folder_token: str) -> list[dict]:
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
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            raise SystemExit(
                f"lark-cli failed for folder {folder_token}:\n{result.stderr}"
            )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            raise SystemExit(f"failed to parse lark-cli output: {e}\n{result.stdout[:500]}")
        if payload.get("code") != 0:
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
    yy = d.year % 100
    return list(dict.fromkeys([
        f"{d.month}.{d.day}-{yy:02d}",
        f"{d.month}.{d.day:02d}-{yy:02d}",
    ]))


def parse_weekly_filename(name: str) -> Optional[tuple[date, date]]:
    m = re.fullmatch(r"(\d{1,2})\.(\d{1,2})～(\d{1,2})\.(\d{1,2})-(\d{2})", name)
    if not m:
        return None
    year = 2000 + int(m.group(5))
    try:
        return (
            date(year, int(m.group(1)), int(m.group(2))),
            date(year, int(m.group(3)), int(m.group(4))),
        )
    except ValueError:
        return None


def parse_monthly_filename(name: str) -> Optional[tuple[int, int]]:
    m = re.fullmatch(r"(\d{1,2})月-(\d{2})", name)
    if not m:
        return None
    return 2000 + int(m.group(2)), int(m.group(1))


def match_daily_file(files: list[dict], d: date) -> Optional[dict]:
    candidates = set(daily_name_candidates(d))
    for f in files:
        if f.get("type") == "docx" and f.get("name") in candidates:
            return f
    return None


def find_monthly_output(files: list[dict], output_basename: str) -> Optional[dict]:
    for f in files:
        if f.get("type") == "docx" and f.get("name") == output_basename:
            return f
    return None


def collect(config: dict, year: int, month: int,
            monthly_context_limit: int = 6) -> dict:
    daily_token = config["daily_folder_token"]
    weekly_token = config["weekly_folder_token"]
    monthly_token = config["monthly_folder_token"]

    daily_files = lark_list_folder(daily_token)
    weekly_files = lark_list_folder(weekly_token)
    monthly_files = lark_list_folder(monthly_token)

    start, end = month_range(year, month)

    days = []
    matched: list[dict] = []
    missing: list[str] = []
    cur = start
    while cur <= end:
        f = match_daily_file(daily_files, cur)
        item = {"date": cur.isoformat(), "matched": f is not None}
        if f is not None:
            item.update({"name": f["name"], "token": f["token"], "url": f["url"]})
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

    # Weekly docs that overlap the month
    supplementary_weekly: list[dict] = []
    for f in weekly_files:
        if f.get("type") != "docx":
            continue
        rng = parse_weekly_filename(f.get("name", ""))
        if not rng:
            continue
        ws, we = rng
        if we < start or ws > end:
            continue
        supplementary_weekly.append({"name": f["name"], "token": f["token"], "url": f["url"]})

    # Monthly target name & existence
    yy = year % 100
    output_basename = f"{month}月-{yy:02d}"
    output_basename_v2 = f"{output_basename}_v2"
    target_existing = find_monthly_output(monthly_files, output_basename)

    # Historical monthly context (older than this month)
    monthly_with_key = []
    for f in monthly_files:
        if f.get("type") != "docx":
            continue
        key = parse_monthly_filename(f.get("name", ""))
        if key is None:
            continue
        monthly_with_key.append((key, f))
    monthly_with_key.sort(key=lambda x: x[0])
    target_key = (year, month)
    older_monthly = [(k, f) for (k, f) in monthly_with_key if k < target_key]
    monthly_context = [
        {"name": f["name"], "token": f["token"], "url": f["url"]}
        for (_, f) in list(reversed(older_monthly))[:monthly_context_limit]
    ]

    return {
        "month": f"{year:04d}-{month:02d}",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "monthly_folder_token": monthly_token,
        "monthly_output_basename": output_basename,
        "monthly_output_filename": f"{output_basename}.md",
        "monthly_output_exists": target_existing is not None,
        "monthly_output_existing_url": (target_existing or {}).get("url"),
        "monthly_output_existing_token": (target_existing or {}).get("token"),
        "monthly_output_basename_v2": output_basename_v2,
        "days": days,
        "matched_daily_files": matched,
        "missing_dates": missing,
        "supplementary_weekly_files": supplementary_weekly,
        "historical_context_files": {
            "monthly_files": monthly_context,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Collect Lark daily/weekly/monthly docs needed for a monthly summary."
    )
    parser.add_argument("--month", required=True, help="Month in YYYY-MM.")
    parser.add_argument(
        "--config",
        default=None,
        help="Path to shared lark_folders.json (default: ../../summary-shared/lark_folders.json).",
    )
    parser.add_argument(
        "--monthly-context-limit", type=int, default=6,
        help="How many older monthly summaries to surface for cross-period reading.",
    )
    args = parser.parse_args()

    config = load_config(Path(args.config) if args.config else None)
    year, month = parse_month_arg(args.month)
    result = collect(config, year, month, args.monthly_context_limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
