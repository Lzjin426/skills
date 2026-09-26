#!/usr/bin/env python3
"""Generate one or more gpt-image-2 images through APINebula async tasks."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import mimetypes
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


API_BASE_URL = "https://apinebula.ai"
TERMINAL_SUCCESS = {"completed", "succeeded"}
TERMINAL_FAILURE = {"failed", "cancelled", "canceled"}
API_KEY_FILE = Path(__file__).resolve().parents[1] / ".api_key"


class ApiError(RuntimeError):
    """A readable error returned while communicating with the image API."""


def get_api_key() -> str | None:
    """Read an environment key first, then the skill-local private key file."""
    environment_key = os.environ.get("APINEBULA_API_KEY", "").strip()
    if environment_key:
        return environment_key
    try:
        file_key = API_KEY_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return None
    return file_key or None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit APINebula gpt-image-2 tasks concurrently and download results."
    )
    parser.add_argument("--prompt", required=True, help="Image-generation prompt.")
    parser.add_argument("--count", type=int, default=1, help="Number of images to generate (default: 1).")
    parser.add_argument(
        "--concurrency",
        type=int,
        default=3,
        help="Maximum simultaneous requests (default: 3).",
    )
    parser.add_argument("--model", default="gpt-image-2", help="Image model (default: gpt-image-2).")
    parser.add_argument(
        "--quality",
        choices=("low", "medium", "high", "auto"),
        default="medium",
        help="Image quality (default: medium).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=600,
        help="Total seconds to wait for all tasks after submission (default: 600).",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=3,
        help="Seconds between task-status polls (default: 3).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for downloaded images and manifest.json.",
    )
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be at least 1")
    if args.concurrency < 1:
        parser.error("--concurrency must be at least 1")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0")
    if args.poll_interval <= 0:
        parser.error("--poll-interval must be greater than 0")
    args.concurrency = min(args.concurrency, args.count)
    return args


def api_request(
    api_key: str, path: str, *, payload: dict[str, Any] | None = None
) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(
        f"{API_BASE_URL}{path}", data=data, headers=headers, method="POST" if data else "GET"
    )
    try:
        with urlopen(request, timeout=60) as response:
            raw_response = response.read()
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise ApiError(f"API returned HTTP {error.code}: {body[:1000]}") from error
    except URLError as error:
        raise ApiError(f"Could not reach APINebula: {error.reason}") from error

    try:
        response_data = json.loads(raw_response)
    except json.JSONDecodeError as error:
        raise ApiError("API returned invalid JSON") from error
    if not isinstance(response_data, dict):
        raise ApiError("API returned an unexpected response body")
    return response_data


def submit_task(api_key: str, prompt: str, model: str, quality: str) -> dict[str, Any]:
    response = api_request(
        api_key,
        "/v1/image-tasks/generations",
        payload={
            "model": model,
            "prompt": prompt,
            "quality": quality,
            "response_format": "url",
        },
    )
    task_id = response.get("task_id") or response.get("id")
    if not isinstance(task_id, str) or not task_id:
        raise ApiError(f"Task submission returned no task ID: {json.dumps(response, ensure_ascii=False)}")
    return {"task_id": task_id, "submission": response}


def get_task(api_key: str, task_id: str) -> dict[str, Any]:
    return api_request(api_key, f"/v1/image-tasks/{task_id}?detail=true")


def wait_for_tasks(
    api_key: str,
    task_ids: list[str],
    concurrency: int,
    timeout: float,
    poll_interval: float,
) -> dict[str, dict[str, Any]]:
    pending = set(task_ids)
    results: dict[str, dict[str, Any]] = {}
    deadline = time.monotonic() + timeout

    while pending:
        if time.monotonic() >= deadline:
            for task_id in pending:
                results[task_id] = {"id": task_id, "status": "timeout"}
            break
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(concurrency, len(pending))) as executor:
            futures = {executor.submit(get_task, api_key, task_id): task_id for task_id in pending}
            for future in concurrent.futures.as_completed(futures):
                task_id = futures[future]
                try:
                    task = future.result()
                except ApiError as error:
                    results[task_id] = {"id": task_id, "status": "poll_error", "error": str(error)}
                    pending.remove(task_id)
                    print(f"任务 {task_id} 查询失败：{error}", file=sys.stderr)
                    continue
                status = str(task.get("status", "unknown")).lower()
                print(f"任务 {task_id}：{status}")
                if status in TERMINAL_SUCCESS | TERMINAL_FAILURE:
                    results[task_id] = task
                    pending.remove(task_id)
        if pending:
            time.sleep(min(poll_interval, max(0, deadline - time.monotonic())))
    return results


def suffix_from_url(url: str) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return suffix
    return ".png"


def download_image(url: str, output_path: Path) -> Path:
    request = Request(url, headers={"User-Agent": "apinebula-gpt-image-skill/1.0"})
    try:
        with urlopen(request, timeout=120) as response:
            content = response.read()
            content_type = response.headers.get_content_type()
    except (HTTPError, URLError) as error:
        raise ApiError(f"Could not download image: {error}") from error
    if not content:
        raise ApiError("Downloaded image was empty")
    guessed_suffix = mimetypes.guess_extension(content_type) if content_type else None
    if guessed_suffix in {".png", ".jpg", ".jpeg", ".webp"} and output_path.suffix != guessed_suffix:
        output_path = output_path.with_suffix(guessed_suffix)
    output_path.write_bytes(content)
    return output_path


def extract_urls(task: dict[str, Any]) -> list[str]:
    detail = task.get("detail")
    if not isinstance(detail, dict):
        return []
    data = detail.get("data")
    if not isinstance(data, list):
        return []
    return [item["download_url"] for item in data if isinstance(item, dict) and isinstance(item.get("download_url"), str)]


def main() -> int:
    args = parse_args()
    api_key = get_api_key()
    if not api_key:
        print("缺少 APINEBULA_API_KEY 环境变量或技能目录下的 .api_key 文件。", file=sys.stderr)
        return 2

    output_dir = args.output_dir or Path.cwd() / f"apinebula-images-{datetime.now():%Y%m%d-%H%M%S}"
    output_dir.mkdir(parents=True, exist_ok=False)
    print(f"提交 {args.count} 个 {args.model} 图片任务（并发上限 {args.concurrency}）…")

    submissions: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = {
            executor.submit(submit_task, api_key, args.prompt, args.model, args.quality): index
            for index in range(1, args.count + 1)
        }
        for future in concurrent.futures.as_completed(futures):
            index = futures[future]
            try:
                submission = future.result()
                submissions.append({"index": index, **submission})
                print(f"已提交第 {index} 张：{submission['task_id']}")
            except ApiError as error:
                errors.append({"stage": "submit", "index": str(index), "error": str(error)})
                print(f"第 {index} 张提交失败：{error}", file=sys.stderr)

    task_results = wait_for_tasks(
        api_key,
        [item["task_id"] for item in submissions],
        args.concurrency,
        args.timeout,
        args.poll_interval,
    )
    task_to_index = {item["task_id"]: item["index"] for item in submissions}
    downloads: list[dict[str, str]] = []
    download_jobs: list[tuple[str, Path, str]] = []
    for task_id, task in task_results.items():
        status = str(task.get("status", "unknown")).lower()
        if status not in TERMINAL_SUCCESS:
            errors.append({"stage": "task", "task_id": task_id, "status": status, "error": str(task.get("error", ""))})
            continue
        urls = extract_urls(task)
        if not urls:
            errors.append({"stage": "result", "task_id": task_id, "error": "No download_url in completed task."})
            continue
        for number, url in enumerate(urls, start=1):
            index = task_to_index[task_id]
            output_path = output_dir / f"image-{index:02d}-{number:02d}{suffix_from_url(url)}"
            download_jobs.append((task_id, output_path, url))

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(args.concurrency, max(1, len(download_jobs)))) as executor:
        futures = {executor.submit(download_image, url, path): (task_id, path, url) for task_id, path, url in download_jobs}
        for future in concurrent.futures.as_completed(futures):
            task_id, path, url = futures[future]
            try:
                saved_path = future.result()
                downloads.append({"task_id": task_id, "url": url, "file": str(saved_path)})
                print(f"已下载：{saved_path}")
            except ApiError as error:
                errors.append({"stage": "download", "task_id": task_id, "url": url, "error": str(error)})
                print(f"下载失败（{task_id}）：{error}", file=sys.stderr)

    manifest = {
        "model": args.model,
        "prompt": args.prompt,
        "quality": args.quality,
        "requested_count": args.count,
        "submissions": submissions,
        "tasks": task_results,
        "downloads": downloads,
        "errors": errors,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"完成：{len(downloads)} 张已下载；清单：{manifest_path}")
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("已中断；已提交的服务端任务仍可能继续执行。", file=sys.stderr)
        raise SystemExit(130)
