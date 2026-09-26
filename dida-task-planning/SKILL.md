---
agent_created: true
title: "将用户口头/文本待办拆分为 Dida 任务"
summary: "当用户梳理一堆要做的事情并要求创建滴答清单任务时使用。把事项按 deadline 和优先级拆成独立任务，设置提醒，并可带子任务。"
---

# 将用户口头/文本待办拆分为 Dida 任务

## 触发条件

用户说类似以下的话：
- "帮我梳理一下最近要做的事情"
- "把这些加到滴答清单"
- "帮我拆一下任务"
- "最近要做什么什么，你帮我安排一下"

## 工作流程

### 1. 理解并整理

把用户给的事项按以下维度整理：
- **硬 deadline**：必须完成的日期
- **目标日期**： ideally 完成但可以延后
- **背后推进事项**：需要跟进、不是自己做的工作
- **优先级**：高（硬 deadline）、中（跟进/可延后）、低

先用 Markdown 表格或列表向用户确认一遍拆分方案，再执行创建。

### 2. 选择 Dida 清单

列出用户项目，选择最匹配的清单：

```bash
cd "/c/Users/Full stop/AppData/Roaming/npm" && node node_modules/@suibiji/dida-cli/dist/index.js project list --json
```

常用清单（根据 Lzjin 当前环境）：
- `68839998e4b08798d961198c` — 学业与核心科研
- `66d1352d2035d108903e3de5` — 生活与行政

### 3. 创建任务

使用 `dida task create`，推荐参数：

```bash
node node_modules/@suibiji/dida-cli/dist/index.js task create \
  --title "任务标题" \
  --project <projectId> \
  --all-day \
  --start-date "YYYY-MM-DDTHH:mm:ss.000Z" \
  --due-date "YYYY-MM-DDTHH:mm:ss.000Z" \
  --priority <0|1|3|5> \
  --content "补充说明" \
  --items "子任务1,子任务2,子任务3"
```

参数说明：
- `--all-day`：**必须显式添加**。用户没指定时间时默认创建全天任务；如果不加，任务会变成 0:00 的具体时间任务，App 里会显示"0 点到 0 点"。
- `--start-date`：**开始日期**。只设 deadline 的任务不会在"今天"视图里提前显示；把开始日期设为今天，任务才会从今天起出现在"今天"视图中。
- `--due-date`：**必须带完整时间戳，且要用 UTC 格式 `.000Z`**。滴答清单按用户时区（Asia/Shanghai）展示，所以要让 App 显示为"某天"，需要传该天北京时间 0 点对应的 UTC 时间。例如：
  - 6 月 26 日（北京时间 0:00）→ `2026-06-25T16:00:00.000Z`
  - 7 月 3 日（北京时间 0:00）→ `2026-07-02T16:00:00.000Z`
  - 只写 `YYYY-MM-DD` 时 CLI 返回成功但实际不会保存 deadline。
- `--priority`：`0=无，1=低，3=中，5=高`
- `--reminders`：逗号分隔多个提醒时间。**仅在用户明确说"几点提醒我"时才设置，否则不要默认添加。**
- `--items`：子任务，**用逗号分隔标题**；JSON 数组在 `create` 时会导致 API 500 错误
- `--content`：任务正文/备注

### 4. 给父任务加子任务或提醒（如创建时漏掉）

如果创建时 `--items` 失败，或者后续需要补提醒/子任务，用 `task update`：

```bash
node node_modules/@suibiji/dida-cli/dist/index.js task update <taskId> \
  --id <taskId> \
  --project <projectId> \
  --all-day \
  --start-date "YYYY-MM-DDTHH:mm:ss.000Z" \
  --due-date "YYYY-MM-DDTHH:mm:ss.000Z" \
  --reminders "...,..." \
  --items "子任务1,子任务2"
```

`update` 时 `--items` 同样用**逗号分隔**，不要用 JSON 数组。如果要修正已有任务为全天，更新时也必须带 `--all-day`，并把日期改为 UTC 格式。

### 5. 清理测试任务

如果为了测试命令创建了临时任务，创建完后立即删除：

```bash
node node_modules/@suibiji/dida-cli/dist/index.js task delete <projectId> <taskId>
```

### 6. 汇总回复

最后给用户一个清晰的汇总：
- 创建了多少任务
- 分别是什么
- 截止日期
- 提醒时间（如有，且必须是用户明确指定的）
- 是否有子任务

## 注意事项

- 不要把所有事情塞进一个任务；按可执行、可验收的最小单元拆分。
- 硬 deadline 的任务优先级设为 `5`（高）。
- 跟进类任务优先级设为 `3`（中）。
- **除非用户明确说"几点提醒我"，否则不要自动添加 reminders。** 默认只设日期，任务会按日期出现在"今天"视图和日历中。
- 如果用户没有指定时间，默认创建为全天任务（符合 Lzjin 偏好）。
