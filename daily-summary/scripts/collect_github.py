#!/usr/bin/env python3
"""Collect GitHub activity and local git commits for one Shanghai date.

The collector is intentionally bounded to notifications, explicitly known
repositories, and explicitly supplied local repositories. It does not scan all
of GitHub.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote
from typing import Any

try:
    from zoneinfo import ZoneInfo

    TZ = ZoneInfo("Asia/Shanghai")
except Exception:  # pragma: no cover
    TZ = timezone(timedelta(hours=8))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect bounded GitHub activity")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--repo", action="append", default=[], help="GitHub repo owner/name; repeatable")
    parser.add_argument(
        "--repo-path", action="append", default=[], help="Local git repository path; repeatable"
    )
    parser.add_argument("--author", help="Optional git author filter")
    parser.add_argument("--skip-search", action="store_true", help="Only collect notifications and commits")
    parser.add_argument("--output", help="Output JSON path (default: stdout)")
    return parser.parse_args()


def parse_time(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    try:
        if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
            number = float(value)
            seconds = number / 1000 if abs(number) >= 10**11 else number
            return datetime.fromtimestamp(seconds, timezone.utc).astimezone(TZ)
        parsed = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=TZ)
        return parsed.astimezone(TZ)
    except (OverflowError, OSError, ValueError):
        return None


def in_target(value: Any, target_date: date) -> bool:
    parsed = parse_time(value)
    return parsed is not None and parsed.date() == target_date


def iso(value: Any) -> str:
    parsed = parse_time(value)
    return parsed.isoformat() if parsed else ""


def run_json(command: list[str]) -> tuple[Any | None, str | None]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        return None, f"{type(exc).__name__}: {exc}"
    if result.returncode != 0:
        return None, (result.stderr or result.stdout).strip() or f"exit {result.returncode}"
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"


def run_text(command: list[str]) -> tuple[str, str | None]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        return "", f"{type(exc).__name__}: {exc}"
    if result.returncode != 0:
        return "", (result.stderr or result.stdout).strip() or f"exit {result.returncode}"
    return result.stdout.strip(), None


def repo_from_remote(url: str) -> str:
    match = re.search(r"(?:github\.com[:/])([^/]+/[^/]+?)(?:\.git)?$", url.strip())
    return match.group(1) if match else ""


def local_commit_events(repo_path: str, target_date: date, author: str | None) -> tuple[list[dict[str, Any]], str | None, str]:
    path = Path(repo_path).expanduser()
    if not path.exists():
        return [], f"repo path does not exist: {path}", ""

    start = datetime.combine(target_date, datetime.min.time(), tzinfo=TZ).isoformat()
    end = (datetime.combine(target_date, datetime.min.time(), tzinfo=TZ) + timedelta(days=1)).isoformat()
    command = [
        "git",
        "-C",
        str(path),
        "log",
        "--since",
        start,
        "--until",
        end,
        "--format=%H%x09%aI%x09%an%x09%ae%x09%s",
    ]
    if author:
        command.append(f"--author={author}")
    output, error = run_text(command)
    if error:
        return [], f"{path}: {error}", ""

    remote, _ = run_text(["git", "-C", str(path), "config", "--get", "remote.origin.url"])
    repo = repo_from_remote(remote) or path.name
    events: list[dict[str, Any]] = []
    for line in output.splitlines():
        parts = line.split("\t", 4)
        if len(parts) != 5:
            continue
        commit, timestamp, author_name, author_email, subject = parts
        events.append(
            {
                "id": commit,
                "kind": "commit",
                "repo": repo,
                "cwd": str(path),
                "timestamp": iso(timestamp),
                "title": subject,
                "summary": subject,
                "author": f"{author_name} <{author_email}>",
                "url": f"https://github.com/{repo}/commit/{commit}" if "/" in repo else "",
                "status": "committed",
            }
        )
    return events, None, repo


def notification_events(payload: Any, target_date: date) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        return []
    events: list[dict[str, Any]] = []
    for item in payload:
        if not isinstance(item, dict) or not in_target(item.get("updated_at"), target_date):
            continue
        repository = item.get("repository") or {}
        subject = item.get("subject") or {}
        repo = repository.get("full_name", "") if isinstance(repository, dict) else str(repository)
        events.append(
            {
                "id": item.get("id", ""),
                "kind": str(subject.get("type") or "notification").lower(),
                "repo": repo,
                "timestamp": iso(item.get("updated_at")),
                "title": subject.get("title", ""),
                "summary": f"{item.get('reason', '')}: {subject.get('title', '')}".strip(": "),
                "url": "",
                "status": "notified",
                "reason": item.get("reason", ""),
            }
        )
    return events


def search_events(repo: str, target_date: date) -> tuple[list[dict[str, Any]], str | None]:
    query = f"repo:{repo} updated:{target_date.isoformat()}..{target_date.isoformat()}"
    endpoint = f"search/issues?q={quote(query)}&per_page=100"
    payload, error = run_json(["gh", "api", endpoint])
    if error:
        return [], f"{repo}: {error}"
    items = payload.get("items", []) if isinstance(payload, dict) else []
    events: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict) or not in_target(item.get("updated_at"), target_date):
            continue
        kind = "pull_request" if item.get("pull_request") else "issue"
        events.append(
            {
                "id": item.get("node_id") or item.get("id"),
                "kind": kind,
                "repo": repo,
                "timestamp": iso(item.get("updated_at")),
                "title": item.get("title", ""),
                "summary": item.get("body", "")[:800] if isinstance(item.get("body"), str) else "",
                "url": item.get("html_url", ""),
                "status": "open" if item.get("state") == "open" else item.get("state", ""),
                "author": (item.get("user") or {}).get("login", "") if isinstance(item.get("user"), dict) else "",
            }
        )
    return events, None


def release_events(repo: str, target_date: date) -> tuple[list[dict[str, Any]], str | None]:
    payload, error = run_json(["gh", "api", f"repos/{repo}/releases?per_page=100"])
    if error:
        return [], f"{repo} releases: {error}"
    events: list[dict[str, Any]] = []
    for item in payload if isinstance(payload, list) else []:
        if not isinstance(item, dict) or not in_target(item.get("published_at"), target_date):
            continue
        events.append(
            {
                "id": item.get("id"),
                "kind": "release",
                "repo": repo,
                "timestamp": iso(item.get("published_at")),
                "title": item.get("name") or item.get("tag_name", ""),
                "summary": item.get("body", "")[:800] if isinstance(item.get("body"), str) else "",
                "url": item.get("html_url", ""),
                "status": "published",
            }
        )
    return events, None


def main() -> None:
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    errors: list[str] = []
    events: list[dict[str, Any]] = []
    repos = set(args.repo)

    user, error = run_json(["gh", "api", "user"])
    if error:
        errors.append(f"gh authentication unavailable: {error}")

    notifications, error = run_json(["gh", "api", "notifications?all=true&per_page=100"])
    if error:
        errors.append(f"notifications: {error}")
    else:
        events.extend(notification_events(notifications, target_date))
        for item in notifications if isinstance(notifications, list) else []:
            if isinstance(item, dict) and isinstance(item.get("repository"), dict):
                repo = item["repository"].get("full_name")
                if repo:
                    repos.add(repo)

    for repo_path in args.repo_path:
        commit_events, commit_error, repo = local_commit_events(repo_path, target_date, args.author)
        events.extend(commit_events)
        if commit_error:
            errors.append(commit_error)
        if repo and "/" in repo:
            repos.add(repo)

    if not args.skip_search:
        for repo in sorted(repos):
            found, search_error = search_events(repo, target_date)
            events.extend(found)
            if search_error:
                errors.append(search_error)
            found, release_error = release_events(repo, target_date)
            events.extend(found)
            if release_error:
                errors.append(release_error)

    unique: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for event in events:
        key = (
            str(event.get("kind", "")),
            str(event.get("repo", "")),
            str(event.get("id", "")),
            str(event.get("timestamp", "")),
        )
        unique[key] = event

    output = {
        "date": args.date,
        "timezone": "Asia/Shanghai",
        "source": "github",
        "available": not (errors and not events),
        "repos": sorted(repos),
        "authenticated_user": (user or {}).get("login", "") if isinstance(user, dict) else "",
        "events": sorted(unique.values(), key=lambda item: item.get("timestamp", "")),
        "errors": errors,
    }
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        print(f"GitHub data written to: {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
