#!/usr/bin/env python3
"""Offline smoke tests for generate_images.py; no API key or network required."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("generate_images.py")
SPEC = importlib.util.spec_from_file_location("generate_images", SCRIPT)
assert SPEC and SPEC.loader
generate_images = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generate_images
SPEC.loader.exec_module(generate_images)


def test_wait_for_tasks() -> None:
    states = iter([
        {"id": "task-a", "status": "queued"},
        {"id": "task-a", "status": "completed", "detail": {"data": [{"download_url": "https://example.test/a.png"}]}},
    ])
    with patch.object(generate_images, "get_task", side_effect=lambda *_: next(states)):
        results = generate_images.wait_for_tasks("unused", ["task-a"], 1, 1, 0.001)
    assert results["task-a"]["status"] == "completed"
    assert generate_images.extract_urls(results["task-a"]) == ["https://example.test/a.png"]


def test_main_parallel_flow() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir) / "images"
        submitted: list[str] = []

        def fake_submit(*_: str) -> dict[str, object]:
            task_id = f"task-{len(submitted) + 1}"
            submitted.append(task_id)
            return {"task_id": task_id, "submission": {"task_id": task_id, "status": "queued"}}

        def fake_wait(*args: object) -> dict[str, dict[str, object]]:
            task_ids = args[1]
            return {
                task_id: {
                    "id": task_id,
                    "status": "completed",
                    "detail": {"data": [{"download_url": f"https://example.test/{task_id}.png"}]},
                }
                for task_id in task_ids
            }

        def fake_download(_: str, path: Path) -> Path:
            path.write_bytes(b"fake-png")
            return path

        argv = [
            "generate_images.py",
            "--prompt",
            "offline test",
            "--count",
            "3",
            "--concurrency",
            "2",
            "--output-dir",
            str(output_dir),
        ]
        with (
            patch.object(generate_images, "submit_task", side_effect=fake_submit),
            patch.object(generate_images, "wait_for_tasks", side_effect=fake_wait),
            patch.object(generate_images, "download_image", side_effect=fake_download),
            patch.object(generate_images.os, "environ", {"APINEBULA_API_KEY": "test-key"}),
            patch.object(sys, "argv", argv),
        ):
            assert generate_images.main() == 0
        manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
        assert len(manifest["submissions"]) == 3
        assert len(manifest["downloads"]) == 3
        assert manifest["errors"] == []


def test_key_precedence_and_file_fallback() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        key_file = Path(temp_dir) / ".api_key"
        key_file.write_text("file-key\n", encoding="utf-8")
        with (
            patch.object(generate_images, "API_KEY_FILE", key_file),
            patch.object(generate_images.os, "environ", {"APINEBULA_API_KEY": "environment-key"}),
        ):
            assert generate_images.get_api_key() == "environment-key"
        with (
            patch.object(generate_images, "API_KEY_FILE", key_file),
            patch.object(generate_images.os, "environ", {}),
        ):
            assert generate_images.get_api_key() == "file-key"


if __name__ == "__main__":
    test_wait_for_tasks()
    test_main_parallel_flow()
    test_key_precedence_and_file_fallback()
    print("Offline smoke tests passed.")
