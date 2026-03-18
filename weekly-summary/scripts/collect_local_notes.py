#!/usr/bin/env python3
import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path


def parse_ymd(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def legacy_weekly_title(start: date, end: date) -> str:
    yy = start.year % 100
    return f"{start.month}.{start.day:02d}～{end.month}.{end.day:02d}-{yy:02d}"


def list_style_references(note_root: Path, output_path: Path, limit: int) -> list[str]:
    weekly_files = sorted(note_root.glob("*/Weekly/*.md"))
    older = [path for path in weekly_files if path != output_path and path.name < output_path.name]
    newer = [path for path in weekly_files if path != output_path and path.name > output_path.name]

    selected = list(reversed(older))[:limit]
    if len(selected) < limit:
        selected.extend(newer[: limit - len(selected)])
    return [str(path) for path in selected]


def collect(root: Path, start: date, end: date, reference_count: int) -> dict:
    note_root = root / "05-note"
    if not note_root.exists():
        raise SystemExit(f"05-note not found under: {root}")

    days = []
    missing_dates = []
    existing_files = []

    current = start
    while current <= end:
        daily_path = note_root / str(current.year) / "Daily" / f"{current.isoformat()}.md"
        exists = daily_path.exists()
        day_item = {
            "date": current.isoformat(),
            "daily_path": str(daily_path),
            "exists": exists,
        }
        days.append(day_item)
        if exists:
            existing_files.append(str(daily_path))
        else:
            missing_dates.append(current.isoformat())
        current += timedelta(days=1)

    weekly_dir = note_root / str(start.year) / "Weekly"
    output_basename = f"{start.isoformat()}～{end.isoformat()}.md"
    weekly_output_path = weekly_dir / output_basename
    weekly_output_path_v2 = weekly_dir / f"{start.isoformat()}～{end.isoformat()}_v2.md"

    return {
        "note_root": str(note_root),
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "legacy_weekly_title": legacy_weekly_title(start, end),
        "weekly_output_path": str(weekly_output_path),
        "weekly_output_exists": weekly_output_path.exists(),
        "weekly_output_path_v2": str(weekly_output_path_v2),
        "existing_daily_files": existing_files,
        "missing_dates": missing_dates,
        "days": days,
        "style_reference_files": list_style_references(
            note_root, weekly_output_path, reference_count
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Collect local daily note availability for a weekly summary."
    )
    parser.add_argument("--root", default=".", help="Workspace root containing 05-note.")
    parser.add_argument("--start", required=True, help="Start date in YYYY-MM-DD.")
    parser.add_argument("--end", required=True, help="End date in YYYY-MM-DD.")
    parser.add_argument(
        "--reference-count",
        type=int,
        default=3,
        help="How many historical weekly files to return for style reference.",
    )
    args = parser.parse_args()

    result = collect(
        root=Path(args.root).resolve(),
        start=parse_ymd(args.start),
        end=parse_ymd(args.end),
        reference_count=args.reference_count,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
