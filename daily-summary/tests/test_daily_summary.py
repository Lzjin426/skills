from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


generate_daily = load_module("daily_summary_generate", ROOT / "scripts/generate_daily.py")
collect_codex = load_module("daily_summary_codex", ROOT / "scripts/collect_codex_history.py")
collect_computer = load_module(
    "daily_summary_computer", ROOT / "scripts/collect_computer_history.py"
)
validate_report = load_module(
    "daily_summary_validate", ROOT / "scripts/validate_daily_report.py"
)
collect_lark = load_module("daily_summary_lark", ROOT / "scripts/collect_lark_docs.py")


def namespace_for(**paths: str | None) -> argparse.Namespace:
    values = {name: None for name in generate_daily.SOURCE_OPTIONS}
    values.update({"existing_report": None, "style_samples": None, "date": "2026-09-14"})
    values.update(paths)
    return argparse.Namespace(**values)


class GenerateDailyTests(unittest.TestCase):
    def write_json(self, directory: Path, name: str, value: object) -> str:
        path = directory / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return str(path)

    def test_unifies_all_sources_without_dropping_short_work_item(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            claude = self.write_json(
                directory,
                "claude.json",
                {
                    "sessions": [
                        {
                            "cwd": "/tmp/demo",
                            "git_repo": "demo",
                            "git_branch": "main",
                            "inputs": [
                                {
                                    "time": "2026-09-14T09:00:00+08:00",
                                    "text": "提交 PR #12",
                                }
                            ],
                        }
                    ]
                },
            )
            lark = self.write_json(
                directory,
                "lark.json",
                {
                    "documents": [
                        {
                            "name": "实验记录",
                            "modified_time": "2026-09-14T09:00:00+08:00",
                            "url": "https://my.feishu.cn/docx/demo",
                        }
                    ]
                },
            )
            github = self.write_json(
                directory,
                "github.json",
                {
                    "events": [
                        {
                            "id": "pr-12",
                            "repo": "owner/demo",
                            "updated_at": "2026-09-14T10:00:00Z",
                            "title": "Fix summary",
                            "html_url": "https://github.com/owner/demo/pull/12",
                            "status": "merged",
                        }
                    ]
                },
            )
            computer = self.write_json(
                directory,
                "computer.json",
                {
                    "status": "running",
                    "events": [
                        {
                            "timestamp": "2026-09-14T11:00:00+08:00",
                            "app": "Terminal",
                            "window_title": "demo",
                            "summary": "观察活动",
                        }
                    ],
                },
            )
            args = namespace_for(
                claude=claude,
                lark_docs=lark,
                github=github,
                computer_history=computer,
            )
            packet = generate_daily.build_packet(args)
            sources = {event["source"] for event in packet["events"]}
            texts = {event["text"] for event in packet["events"]}
            self.assertEqual({"claude", "lark_docs", "github", "computer_history"}, sources)
            self.assertIn("提交 PR #12", texts)
            self.assertEqual(packet["timezone"], "Asia/Shanghai")
            self.assertEqual(packet["source_status"]["ticktick"]["status"], "not_requested")
            self.assertIn("Two low-cost subagents", packet["_instructions"])
            self.assertIn("main model", packet["_instructions"])

    def test_bad_optional_json_is_reported_not_fatal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            bad = Path(temp) / "bad.json"
            bad.write_text("{not json", encoding="utf-8")
            packet = generate_daily.build_packet(namespace_for(github=str(bad)))
            self.assertEqual(packet["source_status"]["github"]["status"], "invalid")
            self.assertEqual(packet["events"], [])

    def test_unparseable_or_missing_event_time_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            github = self.write_json(
                directory,
                "github.json",
                {
                    "events": [
                        {"id": "bad", "updated_at": "not-a-time", "title": "异常时间"},
                        {"id": "missing", "title": "缺少时间"},
                        {
                            "id": "good",
                            "updated_at": "2026-09-14T09:00:00+08:00",
                            "title": "目标日期",
                        },
                    ]
                },
            )
            packet = generate_daily.build_packet(namespace_for(github=github))
            self.assertEqual([event["title"] for event in packet["events"]], ["目标日期"])

    def test_style_samples_and_existing_report_are_kept_in_one_packet(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            style = self.write_json(
                directory,
                "style.json",
                {"style_samples": [{"name": "9.13-26", "content": "# 主要内容\n- 短句"}]},
            )
            existing = directory / "existing.md"
            existing.write_text("# 主要内容\n\n- 已有事实\n", encoding="utf-8")
            packet = generate_daily.build_packet(
                namespace_for(style_samples=style, existing_report=str(existing))
            )
            self.assertEqual(packet["style_samples"][0]["name"], "9.13-26")
            self.assertIn("已有事实", packet["existing_report"])

    def test_unavailable_source_is_distinguished_from_readable_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            computer = self.write_json(
                Path(temp),
                "computer.json",
                {"source": "computer_history", "status": "stopped", "available": False},
            )
            packet = generate_daily.build_packet(namespace_for(computer_history=computer))
            status = packet["source_status"]["computer_history"]
            self.assertEqual(status["status"], "unavailable")
            self.assertEqual(status["load_status"], "ok")
            self.assertEqual(status["source_state"], "stopped")


class CodexCollectorTests(unittest.TestCase):
    def test_filters_each_message_and_reads_all_rollout_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = root / "sessions/2026/09/13"
            second = root / "sessions/2026/09/14"
            first.mkdir(parents=True)
            second.mkdir(parents=True)
            session_id = "01234567-89ab-cdef-0123-456789abcdef"
            lines = [
                {
                    "type": "session_meta",
                    "payload": {"id": session_id, "cwd": str(root)},
                },
                {
                    "type": "event_msg",
                    "payload": {
                        "event_type": "user_message",
                        "timestamp": "2026-09-13T23:59:00+08:00",
                        "content": "前一天消息",
                    },
                },
                {
                    "type": "event_msg",
                    "payload": {
                        "event_type": "user_message",
                        "timestamp": "2026-09-14T00:01:00+08:00",
                        "content": "目标日期消息",
                    },
                },
            ]
            (first / f"rollout-{session_id}.jsonl").write_text(
                "\n".join(json.dumps(line) for line in lines), encoding="utf-8"
            )
            (second / f"rollout-{session_id}-second.jsonl").write_text(
                json.dumps(
                    {
                        "type": "event_msg",
                        "payload": {
                            "event_type": "user_message",
                            "timestamp": "2026-09-14T12:00:00+08:00",
                            "content": "第二个 rollout 文件",
                        },
                    }
                ),
                encoding="utf-8",
            )
            sessions = collect_codex.collect_sessions(root, date(2026, 9, 14), True)
            self.assertEqual(len(sessions), 1)
            messages = [item["text"] for item in sessions[0]["user_messages"]]
            self.assertEqual(messages, ["目标日期消息", "第二个 rollout 文件"])


class ComputerHistoryCollectorTests(unittest.TestCase):
    def test_reads_target_date_events_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "history"
            segment = root / "segments/2026-09-14T00-00-00"
            segment.mkdir(parents=True)
            (segment / "metadata.json").write_text(
                json.dumps(
                    {
                        "start_time": "2026-09-14T00:00:00+08:00",
                        "end_time": "2026-09-14T23:00:00+08:00",
                    }
                ),
                encoding="utf-8",
            )
            (segment / "events.jsonl").write_text(
                "\n".join(
                    json.dumps(item)
                    for item in (
                        {
                            "timestamp": "2026-09-14T09:00:00+08:00",
                            "app": "Terminal",
                            "window_title": "demo",
                            "text": "查看项目",
                        },
                        {
                            "timestamp": "2026-09-13T23:59:00+08:00",
                            "app": "Safari",
                            "text": "旧事件",
                        },
                    )
                ),
                encoding="utf-8",
            )
            errors: list[str] = []
            events = collect_computer.collect_segments(root, date(2026, 9, 14), errors)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["app"], "Terminal")
            self.assertEqual(events[0]["evidence_level"], "observed_activity_only")

    def test_segment_start_end_strings_and_unknown_memory_time_are_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "history"
            segment = root / "segments/segment-a"
            segment.mkdir(parents=True)
            (segment / "metadata.json").write_text(
                json.dumps(
                    {
                        "start": "2026-09-14T08:00:00+08:00",
                        "end": "2026-09-14T09:00:00+08:00",
                    }
                ),
                encoding="utf-8",
            )
            (segment / "events.jsonl").write_text(
                json.dumps(
                    {
                        "timestamp": "2026-09-14T08:30:00+08:00",
                        "app": "Terminal",
                        "text": "目标事件",
                    }
                ),
                encoding="utf-8",
            )
            errors: list[str] = []
            events = collect_computer.collect_segments(root, date(2026, 9, 14), errors)
            self.assertEqual(len(events), 1)

            memory_root = Path(temp) / "memories"
            memory_root.mkdir()
            unknown = memory_root / "summary-without-event-time.md"
            unknown.write_text("不应按修改时间归属", encoding="utf-8")
            memories = collect_computer.collect_memories(
                memory_root, date(2026, 9, 14), 12, errors
            )
            self.assertEqual(memories, [])


class LarkCollectorTests(unittest.TestCase):
    def test_extracts_json_after_pagination_progress(self) -> None:
        payload = collect_lark.extract_json("[page 1] fetching...\n{\"ok\": true, \"data\": {}}")
        self.assertEqual(payload["ok"], True)

    def test_document_record_uses_target_timezone(self) -> None:
        start, end = collect_lark.target_window(date(2026, 9, 14))
        record = collect_lark.document_record(
            {
                "name": "实验记录",
                "token": "doc-1",
                "modified_time": "2026-09-14T09:00:00+08:00",
            },
            "folder-1",
            start,
            end,
        )
        self.assertTrue(record["changed_on_target_date"])
        self.assertEqual(record["token"], "doc-1")


class ReportValidationTests(unittest.TestCase):
    def test_valid_compact_report(self) -> None:
        report = "# 主要内容\n\n## 开发\n\n- 完成设置\n\n# 记录\n\n- 晚上吃饭\n"
        result = validate_report.validate_report(report)
        self.assertTrue(result["valid"])
        self.assertEqual(result["bullet_count"], 2)

    def test_duplicate_heading_is_invalid(self) -> None:
        report = "# 主要内容\n\n## 开发\n- 一\n## 开发\n- 二\n"
        result = validate_report.validate_report(report)
        self.assertFalse(result["valid"])
        self.assertTrue(any("duplicate" in error for error in result["errors"]))

    def test_strict_validation_rejects_compactness_warning(self) -> None:
        report = "# 主要内容\n\n" + "\n".join(f"- 事项 {i}" for i in range(11)) + "\n"
        result = validate_report.validate_report(report)
        self.assertTrue(result["valid"])
        self.assertTrue(result["warnings"])

    def test_strict_validation_returns_failure_for_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report_path = Path(temp) / "report.md"
            report_path.write_text(
                "# 主要内容\n\n" + "\n".join(f"- 事项 {i}" for i in range(11)) + "\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with mock.patch.object(
                sys, "argv", ["validate_daily_report.py", "--file", str(report_path), "--strict"]
            ), contextlib.redirect_stdout(stdout):
                with self.assertRaises(SystemExit) as raised:
                    validate_report.main()
            self.assertEqual(raised.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
