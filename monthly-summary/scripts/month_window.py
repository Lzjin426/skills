#!/usr/bin/env python3
import argparse
import json
import re
from datetime import date, datetime, timedelta


def parse_ymd(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_month(value: str) -> tuple[int, int]:
    dt = datetime.strptime(value, "%Y-%m")
    return dt.year, dt.month


def parse_month_title(value: str) -> tuple[int, int]:
    value = value.strip()

    iso_match = re.fullmatch(r"(\d{4})-(\d{2})", value)
    if iso_match:
        return int(iso_match.group(1)), int(iso_match.group(2))

    legacy_match = re.fullmatch(r"(\d{1,2})月-(\d{2})", value)
    if legacy_match:
        return 2000 + int(legacy_match.group(2)), int(legacy_match.group(1))

    raise SystemExit(f"unsupported month title format: {value}")


def month_range(year: int, month: int) -> tuple[date, date]:
    start = date(year, month, 1)
    if month == 12:
        next_start = date(year + 1, 1, 1)
    else:
        next_start = date(year, month + 1, 1)
    end = next_start - timedelta(days=1)
    return start, end


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


def to_month_title(d: date) -> str:
    yy = d.year % 100
    return f"{d.month}月-{yy:02d}"


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

    title = to_month_title(start)
    iso_month = start.strftime("%Y-%m")
    return {
        "month": iso_month,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "legacy_monthly_title": title,
        "legacy_monthly_title_candidates": [title],
        "monthly_filename": f"{iso_month}.md",
        "monthly_output_basename": iso_month,
        "days": days,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compute month window and local note naming metadata."
    )
    parser.add_argument(
        "--which",
        choices=["current", "last", "explicit", "title"],
        default="current",
        help="Month window mode.",
    )
    parser.add_argument(
        "--reference-date",
        default=None,
        help="Reference date in YYYY-MM-DD (default: today).",
    )
    parser.add_argument(
        "--month",
        default=None,
        help="Explicit month in YYYY-MM, required when --which explicit.",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Month title in legacy format (M月-YY) or ISO format (YYYY-MM).",
    )
    args = parser.parse_args()

    ref = parse_ymd(args.reference_date) if args.reference_date else date.today()

    if args.which == "explicit":
        if not args.month:
            raise SystemExit("--which explicit requires --month YYYY-MM")
        year, month = parse_month(args.month)
    elif args.which == "last":
        if ref.month == 1:
            year, month = ref.year - 1, 12
        else:
            year, month = ref.year, ref.month - 1
    elif args.which == "title":
        if not args.title:
            raise SystemExit("--which title requires --title")
        year, month = parse_month_title(args.title)
    else:
        year, month = ref.year, ref.month

    start, end = month_range(year, month)
    print(json.dumps(build_output(start, end), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
