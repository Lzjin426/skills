#!/usr/bin/env python3
"""Collect Lark/Feishu daily/weekly/monthly/yearly docs needed for a yearly summary.

Reads `summary-shared/lark_folders.json` for folder tokens and queries the Lark
Drive API via `lark-cli` to find:

  - all 12 monthly docx for the target year (existing + missing)
  - all weekly docx that overlap the target year (cross-year week edges included)
  - daily coverage statistics per month (count by listing the daily folder)
  - target yearly docx filename (`YYYY年`) and whether it already exists
  - the previous year's yearly docx (in root folder), as style reference
"""

import argparse
import json
import re
import shutil
import subprocess
from calendar import monthrange
from datetime import date
from pathlib import Path


SHARED_CONFIG_RELATIVE = Path("..") / ".." / "summary-shared" / "lark_folders.json"


def load_config(explicit: Path | None) -> dict:
    path = explicit if explicit else (Path(__file__).parent / SHARED_CONFIG_RELATIVE).resolve()
    if not path.exists():
        raise SystemExit(f"shared config not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


_LARK_CLI: str | None = None


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


def parse_daily_filename(name: str) -> tuple[int, int, int] | None:
    m = re.fullmatch(r"(\d{1,2})\.(\d{1,2})-(\d{2})", name)
    if not m:
        return None
    return 2000 + int(m.group(3)), int(m.group(1)), int(m.group(2))


def parse_weekly_filename(name: str) -> tuple[date, date] | None:
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


def parse_monthly_filename(name: str) -> tuple[int, int] | None:
    m = re.fullmatch(r"(\d{1,2})月-(\d{2})", name)
    if not m:
        return None
    return 2000 + int(m.group(2)), int(m.group(1))


def parse_yearly_filename(name: str) -> int | None:
    m = re.fullmatch(r"(\d{4})年", name)
    if not m:
        return None
    return int(m.group(1))


def find_named_docx(files: list[dict], name: str) -> dict | None:
    for f in files:
        if f.get("type") == "docx" and f.get("name") == name:
            return f
    return None


def collect(config: dict, year: int) -> dict:
    daily_token = config["daily_folder_token"]
    weekly_token = config["weekly_folder_token"]
    monthly_token = config["monthly_folder_token"]
    yearly_token = config["yearly_folder_token"]  # same as root by default

    daily_files = lark_list_folder(daily_token)
    weekly_files = lark_list_folder(weekly_token)
    monthly_files = lark_list_folder(monthly_token)
    yearly_files = lark_list_folder(yearly_token)

    yy = year % 100

    # --- Monthly summaries ---
    existing_monthly: list[dict] = []
    missing_months: list[str] = []
    for month in range(1, 13):
        target_name = f"{month}月-{yy:02d}"
        f = find_named_docx(monthly_files, target_name)
        if f is not None:
            existing_monthly.append({
                "month": month,
                "name": f["name"],
                "token": f["token"],
                "url": f["url"],
            })
        else:
            missing_months.append(f"{month}月")

    # --- Weekly summaries that overlap the target year ---
    overlapping_weekly: list[dict] = []
    weekly_records = []
    for f in weekly_files:
        if f.get("type") != "docx":
            continue
        rng = parse_weekly_filename(f.get("name", ""))
        if not rng:
            continue
        ws, we = rng
        if ws.year == year or we.year == year:
            weekly_records.append((ws, f))
    weekly_records.sort(key=lambda x: x[0])
    overlapping_weekly = [
        {"name": f["name"], "token": f["token"], "url": f["url"]}
        for (_, f) in weekly_records
    ]

    # --- Daily coverage by month ---
    # Build a set of (year, month, day) tuples that exist on the daily folder
    daily_exists: set[tuple[int, int, int]] = set()
    for f in daily_files:
        if f.get("type") != "docx":
            continue
        parsed = parse_daily_filename(f.get("name", ""))
        if parsed is None:
            continue
        daily_exists.add(parsed)

    daily_coverage_by_month = {}
    total_existing = 0
    total_days = 0
    densest = (None, -1)
    sparsest = (None, 10**9)
    for month in range(1, 13):
        days_in_month = monthrange(year, month)[1]
        total_days += days_in_month
        existing_count = sum(
            1 for day in range(1, days_in_month + 1)
            if (year, month, day) in daily_exists
        )
        total_existing += existing_count
        daily_coverage_by_month[f"{year}-{month:02d}"] = {
            "total": days_in_month,
            "existing": existing_count,
        }
        if existing_count > densest[1]:
            densest = (f"{year}-{month:02d}", existing_count)
        if existing_count < sparsest[1]:
            sparsest = (f"{year}-{month:02d}", existing_count)

    # --- Output target & previous year's yearly summary ---
    yearly_title = f"{year}年"
    output_basename = yearly_title
    output_basename_v2 = f"{output_basename}_v2"
    target_existing = find_named_docx(yearly_files, output_basename)

    prev_year_name = f"{year - 1}年"
    prev_yearly = find_named_docx(yearly_files, prev_year_name)
    style_reference_files = []
    if prev_yearly is not None:
        style_reference_files.append({
            "name": prev_yearly["name"],
            "token": prev_yearly["token"],
            "url": prev_yearly["url"],
        })

    return {
        "year": year,
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31",
        "yearly_folder_token": yearly_token,
        "yearly_title": yearly_title,
        "yearly_output_basename": output_basename,
        "yearly_output_filename": f"{output_basename}.md",
        "yearly_output_exists": target_existing is not None,
        "yearly_output_existing_url": (target_existing or {}).get("url"),
        "yearly_output_existing_token": (target_existing or {}).get("token"),
        "yearly_output_basename_v2": output_basename_v2,
        "existing_monthly_files": existing_monthly,
        "missing_months": missing_months,
        "monthly_coverage": f"{len(existing_monthly)}/12",
        "existing_weekly_files": overlapping_weekly,
        "weekly_count": len(overlapping_weekly),
        "daily_coverage_by_month": daily_coverage_by_month,
        "total_daily_coverage": f"{total_existing}/{total_days}",
        "daily_coverage_rate": (
            round(total_existing / total_days * 100, 1) if total_days else 0
        ),
        "daily_densest_month": {"month": densest[0], "count": densest[1]} if densest[0] else None,
        "daily_sparsest_month": {"month": sparsest[0], "count": sparsest[1]} if sparsest[0] else None,
        "style_reference_files": {"yearly_files": style_reference_files},
    }


def main():
    parser = argparse.ArgumentParser(
        description="Collect Lark daily/weekly/monthly/yearly docs needed for a yearly summary."
    )
    parser.add_argument("--year", type=int, required=True, help="Year (e.g. 2025).")
    parser.add_argument(
        "--config",
        default=None,
        help="Path to shared lark_folders.json (default: ../../summary-shared/lark_folders.json).",
    )
    args = parser.parse_args()

    config = load_config(Path(args.config) if args.config else None)
    result = collect(config, args.year)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
