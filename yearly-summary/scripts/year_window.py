#!/usr/bin/env python3
import argparse
import json
from datetime import date


def year_range(year: int) -> tuple[date, date]:
    return date(year, 1, 1), date(year, 12, 31)


def build_output(year: int) -> dict:
    start, end = year_range(year)
    title = f"{year}年"
    return {
        "year": year,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "yearly_title": title,
        "yearly_filename": f"{title}.md",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compute year window and local note naming metadata."
    )
    parser.add_argument(
        "--which",
        choices=["current", "last", "explicit"],
        default="current",
        help="Year window mode.",
    )
    parser.add_argument(
        "--reference-date",
        default=None,
        help="Reference date in YYYY-MM-DD (default: today).",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="Explicit year (e.g. 2025), required when --which explicit.",
    )
    args = parser.parse_args()

    if args.reference_date:
        from datetime import datetime
        ref = datetime.strptime(args.reference_date, "%Y-%m-%d").date()
    else:
        ref = date.today()

    if args.which == "explicit":
        if not args.year:
            raise SystemExit("--which explicit requires --year")
        year = args.year
    elif args.which == "last":
        year = ref.year - 1
    else:
        year = ref.year

    print(json.dumps(build_output(year), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
