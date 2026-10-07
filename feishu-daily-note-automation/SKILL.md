---
name: feishu-daily-note-automation
agent_created: true
description: This skill should be used when Lzjin asks to create or modify a recurring automation that generates a daily note in Feishu note2026 daliy folder, with the title format M.D-26 and sections "主要内容" and "记录".
---

# Feishu Daily Note Automation

## Overview

This skill automates the creation of a daily note document in Lzjin's Feishu note2026 `daliy` folder. The document follows a fixed template with title `M.D-26` (e.g., `7.3-26`) and two top-level sections: `主要内容` and `记录`.

Use this skill when:
- Lzjin asks to create a daily note automation.
- Lzjin wants to modify the schedule, title format, or content sections of the daily note.
- Lzjin asks why a daily note was not created or how to debug the automation.

## Required Resources

- Feishu folder `note2026` > `daliy` (daily notes folder).
- Folder token for `daliy`: `MCCafZNY3lwajKd3L5Yce2cpnue`.
- lark-cli path: `C:\Users\Full stop\.workbuddy\binaries\node\cli-connector-packages\lark-cli`
- The lark-cli must be authenticated with user identity and have permission to create documents in the target folder.

## Daily Note Template

- **Title**: `M.D-26` where `M` is the current month (no leading zero) and `D` is the current day (no leading zero). Examples: `7.3-26`, `12.31-26`.
- **Content** (markdown format):
  ```markdown
  # 主要内容

  - 上下班打卡（上班打卡 / 下班打卡）
  - 论文阅读：

  ---

  # 记录
  ```
- **Parent folder token**: `MCCafZNY3lwajKd3L5Yce2cpnue`

## Automation Configuration

Create or update the automation with the following settings:

- **Name**: `每日日笔记创建（note2026）`
- **Schedule**: Recurring daily at 07:00 local time
- **RRULE**: `FREQ=DAILY;BYHOUR=7;BYMINUTE=0;BYSECOND=0`
- **Workspace**: `C:\Users\Full stop\WorkBuddy\Claw`
- **Status**: `ACTIVE`

## Execution Workflow

When creating the automation prompt, include these exact steps:

1. Compute the current date title: `date '+%-m.%-d-26'` in Git Bash.
2. List existing files in the `daliy` folder using:
   ```bash
   "/c/Users/Full stop/.workbuddy/binaries/node/cli-connector-packages/lark-cli" drive files list --folder-token MCCafZNY3lwajKd3L5Yce2cpnue --json
   ```
3. Check whether a docx file with the same title already exists. If yes, skip creation and report "今日日笔记已存在，无需创建".
4. If not, create the document using:
   ```bash
   "/c/Users/Full stop/.workbuddy/binaries/node/cli-connector-packages/lark-cli" docs +create --title "<M.D-26>" --parent-token MCCafZNY3lwajKd3L5Yce2cpnue --doc-format markdown --content '# 主要内容\n\n- 上下班打卡（上班打卡 / 下班打卡）\n- 论文阅读：\n\n---\n\n# 记录'
   ```
5. On success, output the document title and URL. On failure, report the error exactly as returned by lark-cli.

## Troubleshooting

- If the document is not created, verify lark-cli authentication: `lark-cli auth status`.
- If the folder token changes, update this skill and the automation prompt with the new token.
- Duplicate titles are prevented by listing the folder first. Do not create documents without checking.

## Notes

- The path to `lark-cli` contains spaces. Always quote the full path when invoking it from bash.
- The `--doc-format markdown` flag is required so the `--content` payload is interpreted as Markdown.
- The title format `M.D-26` uses no leading zeros for month and day.
