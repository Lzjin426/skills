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
collect_github = load_module("daily_summary_github", ROOT / "scripts/collect_github.py")
collect_dida = load_module("daily_summary_dida", ROOT / "scripts/collect_dida.py")


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
            self.assertEqual(packet["source_status"]["dida"]["status"], "not_requested")
            self.assertIn("Two low-cost subagents", packet["_instructions"])
            self.assertIn("main model", packet["_instructions"])
            self.assertIn("login troubleshooting", packet["_instructions"])

    def test_dida_completed_time_is_normalized_as_a_completed_task(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            dida = self.write_json(
                Path(temp),
                "dida.json",
                {
                    "source": "dida",
                    "tasks": [
                        {
                            "id": "task-1",
                            "title": "第一篇论文重新投稿",
                            "completedTime": "2026-09-14T01:19:23Z",
                        }
                    ],
                },
            )
            packet = generate_daily.build_packet(namespace_for(dida=dida))
        self.assertEqual(len(packet["events"]), 1)
        event = packet["events"][0]
        self.assertEqual(event["source"], "dida")
        self.assertEqual(event["status"], "completed")
        self.assertEqual(event["time"], "2026-09-14T09:19:23+08:00")

    def test_summary_contract_prioritizes_outcomes_and_omits_routine_process(self) -> None:
        policy = " ".join(generate_daily.SUMMARY_CONTRACT["selection_policy"])
        self.assertIn("稿件进入审理", policy)
        self.assertIn("登录/权限/网页故障排查", policy)
        self.assertIn("归因有冲突", policy)

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

    def test_extracts_compact_ax_submission_state_and_normalizes_it(self) -> None:
        raw = {
            "id": "submission-status",
            "timestamp": "2026-09-14T09:00:00+08:00",
            "app": "Chrome",
            "window": {"title": "Wiley Authors", "url": "https://submission.example/review?authToken=secret123"},
            "ax": {
                "mode": "fullTree",
                "text": "1 Initial Submission\n2 This submission is under consideration and cannot be edited.\n3 Network error unrelated to the submission\n4 文本 已完成库存比对\n5 您的手稿正在与期刊编辑分享，您将收到投稿确认邮件",
            },
        }
        record = collect_computer.event_record(raw, "segment-1", date(2026, 9, 14))
        self.assertIsNotNone(record)
        self.assertIn("under consideration", record["ax_evidence"])
        self.assertIn("手稿正在与期刊编辑分享", record["ax_evidence"])
        self.assertNotIn("Network error", record["ax_evidence"])
        self.assertNotIn("库存比对", record["ax_evidence"])
        self.assertEqual(record["url"], "https://submission.example/review")
        self.assertNotIn("secret123", record["summary"])
        self.assertEqual(record["evidence_level"], "observed_ui_state")
        normalized = generate_daily.computer_history_events(
            {"events": [record]}, date(2026, 9, 14)
        )
        self.assertEqual(len(normalized), 1)
        self.assertIn("under consideration", normalized[0]["text"])
        self.assertEqual(normalized[0]["evidence_level"], "observed_ui_state")

    def test_compacts_repeated_identical_status_snapshots(self) -> None:
        repeated = {
            "time": "2026-09-14T09:00:00+08:00",
            "app": "Safari",
            "window_title": "Final Review",
            "url": "https://submission.example/final",
            "ax_evidence": "This submission is under consideration",
        }
        events = [dict(repeated), {**repeated, "time": "2026-09-14T12:00:00+08:00"}]
        compacted = collect_computer.compact_duplicate_observations(events)
        self.assertEqual(len(compacted), 1)
        self.assertEqual(compacted[0]["time"], "2026-09-14T09:00:00+08:00")


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

    def test_search_result_supports_global_wiki_documents_and_highlights(self) -> None:
        start, end = collect_lark.target_window(date(2026, 9, 14))
        page = {
            "data": {
                "has_more": True,
                "page_token": "next-page",
                "results": [
                    {
                        "entity_type": "wiki",
                        "result_meta": {
                            "token": "wiki-token",
                            "url": "https://my.feishu.cn/wiki/wikcn123",
                            "doc_types": ["wiki"],
                            "create_time_iso": "2026-09-13T12:00:00+08:00",
                            "update_time_iso": "2026-09-14T09:00:00+08:00",
                            "edit_user_name": "Fullstop",
                        },
                        "title_highlighted": "<h>讲座心得</h>",
                        "summary_highlighted": "补入<hb>几何精确结构</hb>心得",
                    }
                ],
            }
        }
        rows, has_more, token = collect_lark.search_page(page)
        self.assertEqual(len(rows), 1)
        self.assertTrue(has_more)
        self.assertEqual(token, "next-page")
        record = collect_lark.search_document_record(rows[0], start, end)
        self.assertEqual(record["name"], "讲座心得")
        self.assertEqual(record["type"], "wiki")
        self.assertTrue(record["changed_on_target_date"])
        self.assertEqual(record["summary"], "补入几何精确结构心得")

    def test_global_document_search_paginates(self) -> None:
        first = {
            "data": {
                "has_more": True,
                "page_token": "page-2",
                "results": [{"result_meta": {"token": "one", "update_time_iso": "2026-09-14T09:00:00+08:00"}, "title_highlighted": "一"}],
            }
        }
        second = {
            "data": {
                "has_more": False,
                "page_token": "",
                "results": [{"result_meta": {"token": "two", "update_time_iso": "2026-09-14T10:00:00+08:00"}, "title_highlighted": "二"}],
            }
        }
        with mock.patch.object(collect_lark, "run_lark", side_effect=[first, second]) as run:
            docs, errors = collect_lark.collect_edited_documents(
                *collect_lark.target_window(date(2026, 9, 14))
            )
        self.assertEqual([item["token"] for item in docs], ["one", "two"])
        self.assertEqual(errors, [])
        self.assertEqual(run.call_count, 2)
        self.assertIn("page-2", run.call_args_list[1].args[0])


class DidaCollectorTests(unittest.TestCase):
    def test_uses_shanghai_day_as_utc_window_and_filters_completion_time(self) -> None:
        start, end = collect_dida.target_window(date(2026, 9, 22))
        self.assertEqual(collect_dida.cli_time(start), "2026-09-21T16:00:00Z")
        self.assertEqual(collect_dida.cli_time(end), "2026-09-22T16:00:00Z")
        inside = collect_dida.normalize_task(
            {"id": "task-1", "title": "已完成任务", "projectId": "project-1", "completedTime": "2026-09-21T16:00:00Z"},
            {"project-1": "论文"},
            start,
            end,
        )
        outside = collect_dida.normalize_task(
            {"id": "task-2", "title": "次日任务", "completedTime": "2026-09-22T16:00:00Z"},
            {},
            start,
            end,
        )
        self.assertEqual(inside["project"], "论文")
        self.assertEqual(inside["timestamp"], "2026-09-22T00:00:00+08:00")
        self.assertIsNone(outside)

    def test_accepts_dida_cli_offset_without_colon(self) -> None:
        parsed = collect_dida.parse_time("2026-09-23T05:19:23.000+0000")
        self.assertEqual(parsed.isoformat(), "2026-09-23T13:19:23+08:00")
        start, end = collect_dida.target_window(date(2026, 9, 23))
        task = collect_dida.normalize_task(
            {"id": "paper", "title": "第一篇论文重新投稿", "completedTime": "2026-09-23T05:19:23.000+0000"},
            {},
            start,
            end,
        )
        self.assertEqual(task["title"], "第一篇论文重新投稿")

    def test_collect_reads_projects_then_completed_tasks(self) -> None:
        projects = {"data": {"projects": [{"id": "p1", "name": "论文"}]}}
        tasks = {"data": {"tasks": [{"id": "t1", "title": "重新投稿", "projectId": "p1", "completedTime": "2026-09-22T02:00:00Z"}]}}
        with mock.patch.object(collect_dida, "run_json", side_effect=[(projects, None), (tasks, None)]) as run:
            result = collect_dida.collect(date(2026, 9, 22))
        self.assertTrue(result["available"])
        self.assertEqual(result["source"], "dida")
        self.assertEqual(result["tasks"][0]["project"], "论文")
        task_command = run.call_args_list[1].args[0]
        self.assertIn("--projects", task_command)
        self.assertIn("2026-09-21T16:00:00Z", task_command)
        self.assertIn("2026-09-22T16:00:00Z", task_command)

    def test_unavailable_cli_is_not_reported_as_an_empty_success(self) -> None:
        with mock.patch.object(collect_dida, "run_json", side_effect=[(None, "not logged in"), (None, "API unavailable")]):
            result = collect_dida.collect(date(2026, 9, 22))
        self.assertFalse(result["available"])
        self.assertEqual(result["tasks"], [])
        self.assertEqual(len(result["errors"]), 2)


class GithubCollectorTests(unittest.TestCase):
    def test_search_keeps_only_authenticated_users_actions_on_action_date(self) -> None:
        search_result = {
            "items": [
                {"number": 1, "title": "本人创建", "html_url": "u/1", "created_at": "2026-09-14T01:00:00Z", "updated_at": "2026-09-14T10:00:00Z", "state": "open", "user": {"login": "me"}},
                {"number": 2, "title": "他人合并", "html_url": "u/2", "created_at": "2026-09-13T10:00:00Z", "updated_at": "2026-09-14T10:00:00Z", "state": "closed", "user": {"login": "other"}, "pull_request": {}},
                {"number": 3, "title": "旧合并被更新", "html_url": "u/3", "created_at": "2026-09-13T10:00:00Z", "updated_at": "2026-09-14T10:00:00Z", "state": "closed", "user": {"login": "other"}, "pull_request": {}},
                {"number": 4, "title": "本人合并", "html_url": "u/4", "created_at": "2026-09-13T10:00:00Z", "updated_at": "2026-09-14T10:00:00Z", "state": "closed", "user": {"login": "other"}, "pull_request": {}},
                {"number": 5, "title": "本人关闭", "html_url": "u/5", "created_at": "2026-09-13T10:00:00Z", "updated_at": "2026-09-14T10:00:00Z", "state": "closed", "user": {"login": "other"}},
            ]
        }
        details = [
            ({"merged_at": "2026-09-14T02:00:00Z", "merged_by": {"login": "other"}}, None),
            ({"merged_at": "2026-09-13T10:00:00Z", "merged_by": {"login": "me"}}, None),
            ({"merged_at": "2026-09-14T03:00:00Z", "merged_by": {"login": "me"}}, None),
            ({"closed_at": "2026-09-14T04:00:00Z", "closed_by": {"login": "me"}}, None),
        ]
        with mock.patch.object(collect_github, "run_json", side_effect=[(search_result, None), *details]) as run:
            events, errors = collect_github.search_events("owner/repo", date(2026, 9, 14), "me")
        self.assertEqual(errors, [])
        self.assertEqual([(event["number"], event["action"]) for event in events], [(1, "opened"), (4, "merged"), (5, "closed")])
        self.assertEqual(events[0]["timestamp"], "2026-09-14T09:00:00+08:00")
        self.assertIn("2026-09-13..2026-09-14", run.call_args_list[0].args[0][2])


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
