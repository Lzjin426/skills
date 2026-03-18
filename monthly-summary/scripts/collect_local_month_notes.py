#!/usr/bin/env python3
import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path


def parse_month(value: str) -> tuple[int, int]:
    dt = datetime.strptime(value, "%Y-%m")
    return dt.year, dt.month


def parse_week_file_range(path: Path) -> tuple[date, date] | None:
    """Parse week file range from both legacy (M.DD～M.DD-YY) and ISO (YYYY-MM-DD～YYYY-MM-DD) formats."""
    stem = path.stem
    if "～" not in stem:
        return None
    start_text, end_text = stem.split("～", 1)

    # Try ISO format first: YYYY-MM-DD～YYYY-MM-DD
    try:
        return (
            datetime.strptime(start_text, "%Y-%m-%d").date(),
            datetime.strptime(end_text, "%Y-%m-%d").date(),
        )
    except ValueError:
        pass

    # Try legacy short format: M.DD～M.DD-YY
    import re
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


def month_range(year: int, month: int) -> tuple[date, date]:
    start = date(year, month, 1)
    if month == 12:
        end = date(year, 12, 31)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)
    return start, end


def legacy_month_title(year: int, month: int) -> str:
    return f"{month}月-{year % 100:02d}"


def list_style_references(
    note_root: Path, output_path: Path, month_end: date, limit: int
) -> list[str]:
    monthly_files = sorted(note_root.glob("*/Monthly/*.md"))
    older_monthly = [
        path for path in monthly_files if path != output_path and path.name < output_path.name
    ]
    selected = list(reversed(older_monthly))[:limit]
    if len(selected) >= limit:
        return [str(path) for path in selected]

    weekly_files = sorted(note_root.glob("*/Weekly/*.md"))
    older_weekly = []
    for path in weekly_files:
        week_range = parse_week_file_range(path)
        if not week_range:
            continue
        _, week_end = week_range
        if week_end <= month_end:
            older_weekly.append(path)

    for path in reversed(older_weekly):
        if path in selected:
            continue
        selected.append(path)
        if len(selected) >= limit:
            break
    return [str(path) for path in selected]


def collect(root: Path, year: int, month: int, reference_count: int) -> dict:
    note_root = root / "05-note"
    if not note_root.exists():
        raise SystemExit(f"05-note not found under: {root}")

    start, end = month_range(year, month)

    daily_dir = note_root / str(year) / "Daily"
    days = []
    existing_daily_files = []
    missing_dates = []

    current = start
    while current <= end:
        daily_path = daily_dir / f"{current.isoformat()}.md"
        exists = daily_path.exists()
        days.append(
            {
                "date": current.isoformat(),
                "daily_path": str(daily_path),
                "exists": exists,
            }
        )
        if exists:
            existing_daily_files.append(str(daily_path))
        else:
            missing_dates.append(current.isoformat())
        current += timedelta(days=1)

    weekly_dir = note_root / str(year) / "Weekly"
    supplementary_weekly_files = []
    for weekly_path in sorted(weekly_dir.glob("*.md")):
        week_range = parse_week_file_range(weekly_path)
        if not week_range:
            continue
        week_start, week_end = week_range
        if week_end < start or week_start > end:
            continue
        supplementary_weekly_files.append(str(weekly_path))

    monthly_dir = note_root / str(year) / "Monthly"
    legacy_name = f"{month}月-{year % 100:02d}"
    output_path = monthly_dir / f"{legacy_name}.md"
    output_path_v2 = monthly_dir / f"{legacy_name}_v2.md"

    return {
        "note_root": str(note_root),
        "month": f"{year:04d}-{month:02d}",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "legacy_monthly_title": legacy_month_title(year, month),
        "monthly_output_path": str(output_path),
        "monthly_output_exists": output_path.exists(),
        "monthly_output_path_v2": str(output_path_v2),
        "existing_daily_files": existing_daily_files,
        "missing_dates": missing_dates,
        "days": days,
        "supplementary_weekly_files": supplementary_weekly_files,
        "style_reference_files": list_style_references(
            note_root, output_path, end, reference_count
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Collect local daily note availability for a monthly summary."
    )
    parser.add_argument("--root", default=".", help="Workspace root containing 05-note.")
    parser.add_argument("--month", required=True, help="Month in YYYY-MM.")
    parser.add_argument(
        "--reference-count",
        type=int,
        default=3,
        help="How many historical monthly or weekly files to return for style reference.",
    )
    args = parser.parse_args()

    year, month = parse_month(args.month)
    result = collect(
        root=Path(args.root).resolve(),
        year=year,
        month=month,
        reference_count=args.reference_count,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
