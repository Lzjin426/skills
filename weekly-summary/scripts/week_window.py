#!/usr/bin/env python3
import argparse
import json
import re
from datetime import date, datetime, timedelta


def parse_ymd(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def monday_of(d: date) -> date:
    return d - timedelta(days=d.weekday())


def parse_week_title(value: str) -> tuple[date, date]:
    value = value.strip()

    iso_match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})～(\d{4}-\d{2}-\d{2})", value)
    if iso_match:
        start = parse_ymd(iso_match.group(1))
        end = parse_ymd(iso_match.group(2))
        return start, end

    legacy_match = re.fullmatch(
        r"(\d{1,2})\.(\d{1,2})～(\d{1,2})\.(\d{1,2})-(\d{2})", value
    )
    if legacy_match:
        start_month = int(legacy_match.group(1))
        start_day = int(legacy_match.group(2))
        end_month = int(legacy_match.group(3))
        end_day = int(legacy_match.group(4))
        year = 2000 + int(legacy_match.group(5))
        start = date(year, start_month, start_day)
        end = date(year, end_month, end_day)
        return start, end

    raise SystemExit(f"unsupported week title format: {value}")


def to_legacy_daily_title(d: date, pad_day: bool) -> str:
    yy = d.year % 100
    if pad_day:
        return f"{d.month}.{d.day:02d}-{yy:02d}"
    return f"{d.month}.{d.day}-{yy:02d}"


def unique_keep_order(values):
    seen = set()
    out = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def build_output(start: date, end: date) -> dict:
    days = []
    current = start
    while current <= end:
        days.append(
            {
                "date": current.isoformat(),
                "legacy_daily_title_candidates": unique_keep_order(
                    [
                        to_legacy_daily_title(current, pad_day=True),
                        to_legacy_daily_title(current, pad_day=False),
                    ]
                ),
                "daily_filename": f"{current.isoformat()}.md",
            }
        )
        current += timedelta(days=1)

    yy = start.year % 100
    legacy_title = f"{start.month}.{start.day:02d}～{end.month}.{end.day:02d}-{yy:02d}"
    legacy_title_alt = f"{start.month}.{start.day}～{end.month}.{end.day}-{yy:02d}"
    iso_title = f"{start.isoformat()}～{end.isoformat()}"

    return {
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "legacy_weekly_title": legacy_title,
        "legacy_weekly_title_candidates": unique_keep_order(
            [legacy_title, legacy_title_alt]
        ),
        "weekly_filename": f"{iso_title}.md",
        "weekly_output_basename": iso_title,
        "days": days,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compute week window and local note naming metadata."
    )
    parser.add_argument(
        "--which",
        choices=["current", "last", "explicit", "title"],
        default="current",
        help="Week window mode.",
    )
    parser.add_argument(
        "--reference-date",
        default=None,
        help="Reference date in YYYY-MM-DD (default: today).",
    )
    parser.add_argument("--start", default=None, help="Start date (YYYY-MM-DD).")
    parser.add_argument("--end", default=None, help="End date (YYYY-MM-DD).")
    parser.add_argument(
        "--title",
        default=None,
        help="Week title in legacy format (M.DD～M.DD-YY) or ISO format (YYYY-MM-DD～YYYY-MM-DD).",
    )
    args = parser.parse_args()

    ref = parse_ymd(args.reference_date) if args.reference_date else date.today()

    if args.which == "explicit":
        if not args.start or not args.end:
            raise SystemExit("--which explicit requires --start and --end")
        start = parse_ymd(args.start)
        end = parse_ymd(args.end)
    elif args.which == "last":
        this_monday = monday_of(ref)
        end = this_monday - timedelta(days=1)
        start = end - timedelta(days=6)
    elif args.which == "title":
        if not args.title:
            raise SystemExit("--which title requires --title")
        start, end = parse_week_title(args.title)
    else:
        start = monday_of(ref)
        end = start + timedelta(days=6)

    if start > end:
        raise SystemExit("start date cannot be after end date")

    print(json.dumps(build_output(start, end), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
