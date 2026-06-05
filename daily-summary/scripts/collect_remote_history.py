#!/usr/bin/env python3
"""Collect Agent conversation history from remote Windows PC via SSH.

Tries to connect to `main-long` and collect history from:
- Claude Code: %USERPROFILE%\.claude\history.jsonl
- Codex: %USERPROFILE%\.codex\session_index.jsonl + sessions/
- OpenClaw: %USERPROFILE%\.openclaw\agents\*\sessions\
- Qclaw: %APPDATA%\Qclaw\ or %USERPROFILE%\.qclaw\

If SSH is unreachable, returns empty result with a note.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date, datetime, timezone, timedelta
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Collect remote Agent history")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--host", default="main-long", help="SSH host name")
    parser.add_argument("--timeout", type=int, default=10, help="SSH connection timeout in seconds")
    return parser.parse_args()


def check_ssh(host: str, timeout: int) -> bool:
    """Check if SSH host is reachable."""
    try:
        result = subprocess.run(
            ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "BatchMode=yes", host, "echo ok"],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        return result.returncode == 0 and "ok" in result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def run_remote_cmd(host: str, cmd: str) -> tuple[bool, str]:
    """Run a command on the remote host via SSH, returning (success, output)."""
    try:
        result = subprocess.run(
            ["ssh", host, cmd],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        return result.returncode == 0, result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return False, str(e)


def collect_claude_remote(host: str, target_date: date) -> list[dict]:
    """Collect Claude Code history from remote Windows PC."""
    # PowerShell command to read history.jsonl and filter by date
    ps_cmd = (
        f'$date = "{target_date.strftime("%Y-%m-%d")}"; '
        '$tz = [System.TimeZoneInfo]::FindSystemTimeZoneById("China Standard Time"); '
        '$hist = Get-Content "$env:USERPROFILE\.claude\history.jsonl" -ErrorAction SilentlyContinue; '
        '$results = @(); '
        'foreach ($line in $hist) { '
        '  if ($line.Trim() -eq "") { continue }; '
        '  try { '
        '    $obj = $line | ConvertFrom-Json; '
        '    $ts = [datetime]::new(1970, 1, 1, 0, 0, 0, [System.DateTimeKind]::Utc).AddMilliseconds($obj.timestamp); '
        '    $local = [System.TimeZoneInfo]::ConvertTimeFromUtc($ts, $tz); '
        '    if ($local.ToString("yyyy-MM-dd") -eq $date) { '
        '      $results += @{ timestamp=$local.ToString("o"); display=$obj.display; project=$obj.project; sessionId=$obj.sessionId } '
        '    } '
        '  } catch {} '
        '}; '
        '$results | ConvertTo-Json -Compress'
    )

    success, output = run_remote_cmd(host, f'powershell -Command "{ps_cmd}"')
    if not success or not output.strip():
        return []

    try:
        data = json.loads(output)
        if isinstance(data, dict):
            data = [data]
        return data
    except json.JSONDecodeError:
        return []


def collect_codex_remote(host: str, target_date: date) -> list[dict]:
    """Collect Codex session index from remote Windows PC."""
    ps_cmd = (
        f'$date = "{target_date.strftime("%Y-%m-%d")}"; '
        '$idx = Get-Content "$env:USERPROFILE\.codex\session_index.jsonl" -ErrorAction SilentlyContinue; '
        '$results = @(); '
        'foreach ($line in $idx) { '
        '  if ($line.Trim() -eq "") { continue }; '
        '  try { '
        '    $obj = $line | ConvertFrom-Json; '
        '    $updated = [datetime]::Parse($obj.updated_at).ToString("yyyy-MM-dd"); '
        '    if ($updated -eq $date) { '
        '      $results += @{ id=$obj.id; thread_name=$obj.thread_name; updated_at=$obj.updated_at } '
        '    } '
        '  } catch {} '
        '}; '
        '$results | ConvertTo-Json -Compress'
    )

    success, output = run_remote_cmd(host, f'powershell -Command "{ps_cmd}"')
    if not success or not output.strip():
        return []

    try:
        data = json.loads(output)
        if isinstance(data, dict):
            data = [data]
        return data
    except json.JSONDecodeError:
        return []


def main():
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()

    # Check SSH connectivity
    if not check_ssh(args.host, args.timeout):
        print(json.dumps({
            "date": args.date,
            "source": "remote",
            "host": args.host,
            "reachable": False,
            "note": f"SSH to {args.host} timed out or failed. Skipping remote collection.",
            "claude_sessions": [],
            "codex_sessions": [],
        }, ensure_ascii=False, indent=2))
        return

    # Collect remote data
    claude_sessions = collect_claude_remote(args.host, target_date)
    codex_sessions = collect_codex_remote(args.host, target_date)

    print(json.dumps({
        "date": args.date,
        "source": "remote",
        "host": args.host,
        "reachable": True,
        "claude_sessions": claude_sessions,
        "codex_sessions": codex_sessions,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
