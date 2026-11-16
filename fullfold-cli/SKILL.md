---
name: fullfold-cli
description: Read and write a Fullfold.md library from agents or scripts with the fullfold-cli binary. Use when the user asks to edit notes, patch blocks, manage boards, links, attachments, calendar notes, trash, conflicts, or PDF annotation sidecars in a Fullfold library. Never edit library files directly; call the CLI.
---

# fullfold-cli

## 何时使用

用户要在 Fullfold 文档库里读取或修改数据，而不是操作界面时：

- 笔记：列出、读取、搜索、大纲、追加、块级 patch、整篇替换、改名、移动、回收站。
- 画板：列出、读取 JSON Canvas、按节点/边 patch。
- 链接、附件、日历/日笔记、回收站、冲突稿。
- PDF：只读信息与 4+1 标注 sidecar（PDF 原文件永不改写）。
- 不负责 UI：标签、窗口、主题、缩放、阅读模式不属于 CLI。

## 第一原则

**不要用 `cat`、`sed`、`python`、重定向或任何直接文件写入去改库内 `.md`、`.canvas`、`.quiet/**` 或 PDF sidecar。** 先调用 `fullfold-cli`；它经过 `fdl_core` 的模型、Markdown、Canvas 和标注 API，能保留富内容、未知字段、冲突稿和原子写。

## 先发现命令

```sh
fullfold-cli capabilities --json
```

这是命令、参数、schema、features、退出码和 unsupported 列表的事实源。不要凭记忆猜子命令；用 `capabilities --command "doc.patch" --json` 看单个命令。

## 库与安全

- 库路径用 `--library <path>`；不传时按 `QUIET_MD_HOME` / 默认库发现。不要假设用户的库路径。
- 自动化测试和脚本一律用临时库；不要碰 `~/Documents/Quiet.md`、`~/Desktop/md 测试` 或用户正在使用的库。
- 写前先读，记下 `hash`；并发修改用 `--expect sha256:...`，不匹配时 CLI 退出 4 且不写。
- 不确定的写入先加 `--dry-run`，确认输出里的 `dryRun:true` 和计划结果。
- `doc.write` 是整篇覆盖，必须 `--replace`；能块级改就用 `doc.patch` 或 `doc.append`，避免丢 callout、分栏、合并表格、附件、图片裁剪和 rich HTML。
- 删除/清空/永久删除必须 `--yes`；不要替用户猜。
- 冲突默认保留冲突稿；不要用 `--conflict-copy never` 覆盖证据。
- 不要在用户库里生成 `AGENTS.md`、`CLAUDE.md` 或 `agent.md`。

## 常用流程

```sh
# 库概况
fullfold-cli --json --library /path/to/lib library info
fullfold-cli --json --library /path/to/lib doc list --kind note

# 读文档
fullfold-cli --json --library /path/to/lib doc read --id <id> --format md
fullfold-cli --json --library /path/to/lib doc read --id <id> --format model

# 块级修改（推荐；先 dry-run）
fullfold-cli --json --library /path/to/lib doc patch --id <id> --ops ops.json --dry-run
fullfold-cli --json --library /path/to/lib doc patch --id <id> --ops ops.json --expect sha256:<hash>

# 追加 Markdown 文件或 stdin
fullfold-cli --json --library /path/to/lib doc append --id <id> --markdown notes.md

# 整篇替换（必须 --replace）
fullfold-cli --json --library /path/to/lib doc write --id <id> --source new.md --replace --expect sha256:<hash>

# 画板 / 日历 / PDF 标注
fullfold-cli --json --library /path/to/lib board read --id <id> --format summary
fullfold-cli --json --library /path/to/lib board patch --id <id> --ops board-ops.json --expect sha256:<hash>
fullfold-cli --json --library /path/to/lib calendar read --date 2026-11-16
fullfold-cli --json --library /path/to/lib pdf annotations list --path paper.pdf
```

## 结果与退出码

- 一律优先加 `--json`：stdout 是一个 envelope：`{schemaVersion, ok, data, warnings, error}`。
- `ok:true` 看 `data`；`ok:false` 看 `error.code`、`error.hint`、`error.conflictCopy`。
- 退出码：0 ok、2 usage、3 not_found、4 conflict、5 invalid、6 permission、7 forbidden、8 unsupported、9 partial、10 internal。
- `8 unsupported` 表示本构建没有该能力（例如表格结构 ops、HTML/PDF 导出、compat 导入）；不要用别的命令拼一个降级版本。
- `4 conflict` 表示目标在读写之间被改动；重新读、拿新 hash、再试，不要覆盖磁盘。

## 找不到命令或二进制

- 先运行 `fullfold-cli --help` 和 `capabilities --json`；仍没有就明确告诉用户本构建不支持，不要用直接文件写入兜底。
- 找不到 `fullfold-cli` 时，问用户二进制路径；源码构建可用 `target/release/fullfold-cli`，不要假设它在 PATH。
