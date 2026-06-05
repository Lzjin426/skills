---
name: daily-summary
description: >
  当用户要求"写日报""今日总结""生成日报""daily summary""今天做了什么"等任务时使用。
  从 Linear、嘀嗒清单、Claude Code、Codex、远程电脑的 Agent 对话等多数据源自动收集当天工作内容，
  交叉验证后生成简洁日报，写入飞书云空间 note2026/daily 文件夹。
  本技能也适用于回顾任意指定日期的总结（如"帮我补一下上周三的日报"）。
metadata:
  requires:
    bins: ["lark-cli"]
    mcps: ["linear"]
---

# Daily Summary — 每日总结

## 适用范围

- "写今天的日报" / "生成日报" / "今日总结"
- "帮我补一下 X 月 X 日的日报"
- "看看我今天做了什么"
- "总结今天的工作"

## 前置条件

1. **lark-cli** 已安装且已认证：
   ```bash
   lark-cli auth login
   ```
2. **Linear MCP** 可用（用于获取 issue 动态）。
3. **嘀嗒清单 MCP** 若已安装则自动使用；未安装则跳过该数据源。
4. **远程电脑 SSH**：`ssh main-long` 若可达则自动收集远程 Agent 对话；不可达则跳过。

## 数据源

| 数据源 | 收集方式 | 收集内容 |
|--------|---------|---------|
| Linear | MCP `list_issues` | 当天创建/更新的 issues |
| 嘀嗒清单 | MCP（若可用） | 当天完成的任务 |
| Claude Code（本地） | 读取 `~/.claude/history.jsonl` + `~/.claude/sessions/*.json` | 当天会话的 cwd（工作目录）和用户输入 |
| Codex（本地） | 读取 `~/.codex/session_index.jsonl` + `~/.codex/sessions/YYYY/MM/DD/*.jsonl` | 当天会话的标题和对话摘要 |
| Claude Code（远程） | SSH `main-long` 读取 `%USERPROFILE%\.claude\history.jsonl` | 远程电脑的会话信息 |
| Codex（远程） | SSH `main-long` 读取 `%USERPROFILE%\.codex\session_index.jsonl` | 远程电脑的会话信息 |
| OpenClaw/Qclaw（远程） | SSH `main-long` 读取对应路径 | 远程电脑的会话信息 |

## 工作流

### Step 0: 确定目标日期

- 默认：**今天**（按东八区计算）。
- 用户指定了日期（如"补一下 6 月 1 日的日报"），使用该日期。
- 日期格式内部统一使用 `YYYY-MM-DD`。

### Step 1: 收集多源数据

**1a. Linear（MCP）**

使用 MCP 查询当天创建或更新的 issues：

```
mcp__plugin_linear_linear__list_issues
  --createdAt "-P1D"  # 最近1天创建的
  --updatedAt "-P1D"  # 最近1天更新的
```

或指定具体日期范围：

```
mcp__plugin_linear_linear__list_issues
  --createdAt "2026-06-04T00:00:00+08:00"
```

收集：issue 标题、状态、优先级、assignee、url。

**1b. 嘀嗒清单（MCP，若可用）**

若 MCP 列表中有嘀嗒清单相关工具，查询当天完成的任务。

**1c. 本地 Claude Code 对话**

运行脚本收集：

```bash
python3 scripts/collect_claude_history.py --date YYYY-MM-DD
```

该脚本读取：
- `~/.claude/history.jsonl`：筛选目标日期的用户输入记录
- `~/.claude/sessions/*.json`：获取对应 session 的 `cwd`（工作目录）

输出每条记录的：**时间、工作目录、用户输入摘要**。

**1d. 本地 Codex 对话**

运行脚本收集：

```bash
python3 scripts/collect_codex_history.py --date YYYY-MM-DD
```

该脚本读取：
- `~/.codex/session_index.jsonl`：筛选目标日期的会话
- `~/.codex/sessions/YYYY/MM/DD/*.jsonl`：解析对话内容，提取用户消息和关键工具调用

输出每条会话的：**标题、时间、用户消息列表、工作目录**。

**1e. 远程电脑 Agent 对话（SSH）**

尝试 SSH 到 `main-long`：

```bash
ssh -o ConnectTimeout=5 main-long "echo reachable"
```

若可达，在远程执行类似 1c/1d 的收集逻辑（路径适配 Windows）：
- Claude Code: `%USERPROFILE%\.claude\history.jsonl`
- Codex: `%USERPROFILE%\.codex\session_index.jsonl`
- OpenClaw: `C:\Users\%USERNAME%\.openclaw\agents\*\sessions\`
- Qclaw: `C:\Users\%USERNAME%\.qclaw\` 或 `%APPDATA%\QClaw\`

若不可达，记录 "远程电脑不可达，跳过"。

### Step 2: 交叉验证与智能筛选

**交叉验证原则：**

- **项目一致性**：Claude Code 的 `cwd` 和 Codex 的 `cwd` 应对应同一个实际项目。若出现矛盾（如本地显示在 A 项目，远程显示在 B 项目），标注出来让用户知道。
- **任务闭环**：Linear issue 状态变化 + 嘀嗒清单任务完成 + Agent 对话中的相关讨论，应能相互印证。例如：Linear 中 issue 标记为 done，且 Codex 对话中出现了"修复了 bug"的讨论，说明这项任务确实已完成。
- **时间合理性**：同一时间段在不同 Agent 中的活动应不冲突。若本地 Claude Code 在 14:00 有会话，远程 Codex 在 14:05 也有会话，可能说明用户同时在两台电脑上工作，或存在时间戳误差。

**智能筛选原则（核心）：**

> **不是所有对话内容都应该被单领出来写下。**

以下类型**不记录**：
- 纯闲聊、问候（"你好""在吗"）
- 重复的相同问题（同一 bug 反复问）
- 极短的探索性查询（"ls""cat file"等无意义命令）
- 已明确取消或放弃的操作

以下类型**重点记录**：
- 实际完成的工作（修复 bug、写完文档、提交代码）
- 重要的决策和讨论（技术方案选择、需求变更）
- 跨工具的联动（"根据 Linear issue #123 修复了..."）
- 新发现和学习（"调研了 X 技术，结论是..."）

### Step 3: 生成日报 Markdown

**3a. 运行聚合脚本获取结构化数据**

```bash
python3 scripts/generate_daily.py \
  --date YYYY-MM-DD \
  --claude /tmp/daily_claude.json \
  --codex /tmp/daily_codex.json \
  --remote /tmp/daily_remote.json \
  --linear /tmp/daily_linear.json \
  -o /tmp/daily_structured.json
```

该脚本输出结构化 JSON，包含按项目分组的关键输入、Linear issues、TickTick 任务、远程状态等。

**3b. 读取结构化数据，进行智能总结**

> **核心原则：不要罗列原始输入，要写总结性描述。**

读取 `/tmp/daily_structured.json`，基于原始数据进行**语义聚类和总结**：

- **同一主题的多条输入合并为 1 条总结**。例如：
  - 原始输入：".venv-transoptima-ui 是什么？" → "帮我删掉这个环境" → "帮我清理"
  - 总结写法：**清理 TransOptima 项目中的 .venv-transoptima-ui 虚拟环境**

- **问答型对话提炼结论**。例如：
  - 原始输入："当前的 git 提交是去掉 UI 对吧？" → "确认一下"
  - 总结写法：**确认 git 提交已去除 UI 相关开发内容**

- **探索性/调研型对话提炼成果**。例如：
  - 原始输入："调研 trae、workbuddy、qoder 的第三方模型接入"
  - 总结写法：**调研 trae、workbuddy、qoder 的第三方模型接入方案**

**按以下模板输出：**

```markdown
# 主要内容

- {项目A 的核心成果：一句话概括}
- {项目B 的核心成果：一句话概括}
- {其他重要工作：一句话概括}

## {项目A}

- {具体事项：总结性描述，非原始输入}
- {具体事项：总结性描述，非原始输入}

## {项目B}

- {具体事项：总结性描述，非原始输入}

## 其他

- {有实际行动的事项：安装、排查、提交等}
- {无产出的了解类事项：简单一句话，不展开}

---

# 记录

- {有产出的飞书文档链接}
- {待办或补充说明（可选）}
```

**生成规则：**

1. **总结性**：每条 bullet 是对一组相关工作的概括，不是原始输入的复制。
2. **简洁高效**：每条不超过 2 句话。避免 AI 腔，像人写的。
3. **项目分组**：按工作目录/项目名分组（`## 项目名`）。无明确项目的归入 `# 主要内容`。
4. **时间隐含**：不强制写时间点，除非对理解工作内容有帮助。
5. **不写元信息**：不要写远程电脑连接状态、日报生成时间、数据收集过程等工具层面的信息。

**关于"调研/了解"类内容的处理：**

- **有产出的调研**（产出了飞书文档、代码提交、配置变更等实际成果）：在对应项目下正常记录，并在 `# 记录` 区保留文档链接。
- **无产出的调研**（只是了解、问问、看看，没有落到文档或代码）：简单写一个点即可，不展开细节。例如："了解 CLAUDE.md 多层级读取机制"、"了解 Agent 自我进化方案"。
- **同一项目下多个同类调研**：合并为一个点。例如："了解 Agent 自我进化与第三方模型接入方案（Coze、trae、workbuddy、qoder）"。

**关于 `# 记录` 区：**

- 只保留**有意义的产出链接**（飞书文档、实际创建的文档等）。
- 不要写 Linear issue 的格式化链接（如 `[LZJ-93: ...](...)`）。
- 不要写远程电脑状态、不要写日报生成时间。
- 如果当天没有产出链接，可以只写待办事项或补充说明，也可以留空。

### Step 4: 写入飞书

**4a. 检查是否已存在**

日报文件名格式：`M.D-YY`（如 `6.4-26`）。

查询 daily 文件夹：

```bash
lark-cli drive files list --params '{"folder_token":"MCCafZNY3lwajKd3L5Yce2cpnue","page_size":200}'
```

从 `summary-shared/lark_folders.json` 读取 `daily_folder_token`。

**4b. 创建或更新**

- 若不存在：创建新 docx，标题为 `M.D-YY`。
- 若已存在：读取现有内容，将新生成的 Markdown **追加**到末尾（保留原有内容，用 `---` 分隔），或根据用户指令覆盖。

使用 `lark-cli docs +create` 或 `lark-cli docs +update` 操作。

默认行为：**追加模式**（保留已有内容，避免覆盖）。用户明确说"覆盖"时才覆盖。

## 参考

- [summary-shared](../summary-shared/lark_folders.json) — 飞书文件夹 token 配置
- [weekly-summary](../weekly-summary/SKILL.md) — 周报 skill（读取本 skill 生成的日报）
- [lark-doc](../lark-doc/SKILL.md) — 飞书文档操作详细用法
