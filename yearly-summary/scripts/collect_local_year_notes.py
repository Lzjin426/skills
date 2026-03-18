#!/usr/bin/env python3
import argparse
import json
import re
from calendar import monthrange
from datetime import date, datetime
from pathlib import Path


def parse_week_file_range(path: Path) -> tuple[date, date] | None:
    """Parse week file range from both legacy and ISO formats."""
    stem = path.stem
    if "～" not in stem:
        return None
    start_text, end_text = stem.split("～", 1)

    try:
        return (
            datetime.strptime(start_text, "%Y-%m-%d").date(),
            datetime.strptime(end_text, "%Y-%m-%d").date(),
        )
    except ValueError:
        pass

    legacy_match = re.fullmatch(
        r"(\d{1,2})\.(\d{1,2})～(\d{1,2})\.(\d{1,2})-(\d{2})", stem
    )
    if legacy_match:
        year = 2000 + int(legacy_match.group(5))
        try:
            return (
                date(year, int(legacy_match.group(1)), int(legacy_match.group(2))),
                date(year, int(legacy_match.group(3)), int(legacy_match.group(4))),
            )
        except ValueError:
            return None

    return None


def _parse_monthly_sort_key(path: Path) -> tuple[int, int]:
    stem = path.stem
    legacy = re.fullmatch(r"(\d{1,2})月-(\d{2})", stem)
    if legacy:
        return 2000 + int(legacy.group(2)), int(legacy.group(1))
    iso = re.fullmatch(r"(\d{4})-(\d{2})", stem)
    if iso:
        return int(iso.group(1)), int(iso.group(2))
    return (0, 0)


def collect(root: Path, year: int) -> dict:
    note_root = root / "05-note"
    if not note_root.exists():
        raise SystemExit(f"05-note not found under: {root}")

    # --- Monthly summaries ---
    monthly_dir = note_root / str(year) / "Monthly"
    existing_monthly_files = []
    missing_months = []

    for month in range(1, 13):
        legacy_name = f"{month}月-{year % 100:02d}.md"
        iso_name = f"{year}-{month:02d}.md"
        legacy_path = monthly_dir / legacy_name
        iso_path = monthly_dir / iso_name
        if legacy_path.exists():
            existing_monthly_files.append(str(legacy_path))
        elif iso_path.exists():
            existing_monthly_files.append(str(iso_path))
        else:
            missing_months.append(f"{month}月")

    # --- Weekly summaries ---
    existing_weekly_files = []
    weekly_dir = note_root / str(year) / "Weekly"
    if weekly_dir.exists():
        for weekly_path in sorted(weekly_dir.glob("*.md")):
            week_range = parse_week_file_range(weekly_path)
            if not week_range:
                continue
            week_start, week_end = week_range
            if week_start.year == year or week_end.year == year:
                existing_weekly_files.append(str(weekly_path))

    # --- Daily coverage by month ---
    daily_dir = note_root / str(year) / "Daily"
    daily_coverage_by_month = {}
    total_existing = 0
    total_days = 0

    for month in range(1, 13):
        days_in_month = monthrange(year, month)[1]
        total_days += days_in_month
        existing_count = 0
        for day in range(1, days_in_month + 1):
            daily_path = daily_dir / f"{date(year, month, day).isoformat()}.md"
            if daily_path.exists():
                existing_count += 1
        total_existing += existing_count
        daily_coverage_by_month[f"{year}-{month:02d}"] = {
            "total": days_in_month,
            "existing": existing_count,
        }

    # --- Output path ---
    yearly_dir = note_root / str(year) / "Yearly"
    yearly_title = f"{year}年"
    output_path = yearly_dir / f"{yearly_title}.md"

    # --- Style reference: previous year's yearly summary ---
    style_reference_files = []
    prev_yearly = note_root / str(year - 1) / "Yearly" / f"{year - 1}年.md"
    if prev_yearly.exists():
        style_reference_files.append(str(prev_yearly))

    return {
        "note_root": str(note_root),
        "year": year,
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31",
        "yearly_title": yearly_title,
        "yearly_output_path": str(output_path),
        "yearly_output_exists": output_path.exists(),
        "existing_monthly_files": existing_monthly_files,
        "missing_months": missing_months,
        "monthly_coverage": f"{len(existing_monthly_files)}/12",
        "existing_weekly_files": existing_weekly_files,
        "daily_coverage_by_month": daily_coverage_by_month,
        "total_daily_coverage": f"{total_existing}/{total_days}",
        "style_reference_files": style_reference_files,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Collect local note availability for a yearly summary."
    )
    parser.add_argument("--root", default=".", help="Workspace root containing 05-note.")
    parser.add_argument("--year", required=True, type=int, help="Year (e.g. 2025).")
    args = parser.parse_args()

    result = collect(root=Path(args.root).resolve(), year=args.year)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
