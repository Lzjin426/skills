---
name: daily-summary
description: >
  当用户要求"写日报""今日总结""生成日报""daily summary""今天做了什么"等任务时使用。
  从飞书新建/有改动的文档、嘀嗒清单、GitHub、Claude Code、Codex、OpenCode、Craft Agent 等多数据源自动收集当天工作内容，
  交叉验证后生成简洁日报，写入飞书云空间 note2026/daily 文件夹。
  本技能也适用于回顾任意指定日期的总结（如"帮我补一下上周三的日报"）。
metadata:
  requires:
    bins: ["lark-cli"]
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
2. **GitHub CLI** 已安装且已认证：
   ```bash
   gh auth status
   ```
3. **嘀嗒清单 MCP** 若已安装则自动使用；未安装则跳过该数据源。
4. **远程电脑 SSH**：`ssh main-long` 若可达则自动收集远程 Agent 对话；不可达则跳过。

## 数据源

| 数据源 | 收集方式 | 收集内容 |
|--------|---------|---------|
| 飞书文档 | `lark-cli` 查询云盘/文档 | 当天新创建或有改动的文档、标题、链接、修改时间 |
| 嘀嗒清单 | MCP（若可用） | 当天完成的任务 |
| GitHub | `gh` CLI + 本地 git 仓库 | 当天与本人相关的通知、PR、issue、review、commit、release，以及 Agent 对话提到的仓库/编号反查结果 |
| Claude Code（本地） | 读取 `~/.claude/history.jsonl` + `~/.claude/sessions/*.json` | 当天会话的 cwd（工作目录）、**git 仓库名**、**git 分支**和用户输入 |
| Codex（本地） | 读取 `~/.codex/session_index.jsonl` + `~/.codex/sessions/YYYY/MM/DD/*.jsonl` | 当天会话的 cwd（工作目录）、**git 仓库名**、**git 分支**和对话摘要 |
| OpenCode / Craft Agent（本地） | 读取对应本地会话目录（若存在） | 当天会话的 cwd、git 仓库名、git 分支和对话摘要 |
| Claude Code（远程） | SSH `main-long` 读取 `%USERPROFILE%\.claude\history.jsonl` | 远程电脑的会话信息 |
| Codex（远程） | SSH `main-long` 读取 `%USERPROFILE%\.codex\session_index.jsonl` | 远程电脑的会话信息 |
| OpenCode / Craft Agent / OpenClaw / Qclaw（远程） | SSH `main-long` 读取对应路径 | 远程电脑的会话信息 |

## 工作流

### Step 0: 确定目标日期

- 默认：**今天**（按东八区计算）。
- 用户指定了日期（如"补一下 6 月 1 日的日报"），使用该日期。
- 日期格式内部统一使用 `YYYY-MM-DD`。

### Step 1: 收集多源数据

**1a. 飞书新建/有改动的文档**

使用 `lark-cli` 查询知识库和云盘中当天新创建或有改动的文档，优先覆盖用户默认知识库目录和 `note2026` 相关目录。

收集：文档标题、链接、创建时间、修改时间、所在文件夹。只把有实际产出的文档放入 `# 记录` 区；普通历史日报、周报的自动更新不要重复当作新产出。

**1b. 嘀嗒清单（MCP，若可用）**

若 MCP 列表中有嘀嗒清单相关工具，查询当天完成的任务。

**1c. GitHub 活动**

目标是尽量覆盖**与本人有关、本人有权限访问、或当天工作上下文中出现过的 GitHub 新动态**。不要理解为 GitHub 全站所有动态。

优先按以下顺序收集：

1. **GitHub 通知**
   - 使用 `gh api /notifications` 查询未读和近期通知。
   - 对通知中的 issue、PR、release、discussion 继续拉取详情，判断是否发生在目标日期。

2. **本人相关 PR / issue 搜索**
   - 使用 `gh search prs` / `gh search issues` 查询目标日期内与本人相关的内容。
   - 覆盖 author、assignee、mentions、commenter、review-requested、reviewed-by、involves 等维度。
   - 同时查询目标日期内 created、updated、merged 的 PR/issue。

3. **本地和已知仓库活动**
   - 从 Agent 对话 cwd、本地 git 仓库、近期工作目录、GitHub 通知中抽取 repo 列表。
   - 对这些 repo 查询当天更新的 PR、issue、release、workflow 失败/成功等关键动态。

4. **本地 git 提交**
   - 在当天涉及的本地仓库执行 `git log --since --until --author`，收集本人当天提交。
   - 若提交已推送，尽量用 `gh` 补充对应 PR 或 commit 链接。

5. **Agent 对话反查**
   - 对 Claude Code、Codex、OpenCode、Craft Agent 等对话中出现的 repo、分支、commit hash、PR/issue 编号进行反查。
   - 如果对话提到"已合并 PR"、"修复 issue"、"发布 release"等事件，必须用 GitHub 数据验证。

收集字段：仓库名、分支、PR/issue/release 标题、状态、链接、更新时间、参与方式、commit 摘要。

边界说明：
- 只能看到当前 GitHub 登录身份有权限访问的内容。
- 对于私有仓库，取决于 `gh` 当前 token 的 scope。
- 不把所有 GitHub 动态都写进日报；只记录与当天工作、交付、决策、故障、协作有关的内容。

**1d. 本地 Claude Code 对话**

运行脚本收集：

```bash
python3 scripts/collect_claude_history.py --date YYYY-MM-DD
```

该脚本读取：
- `~/.claude/history.jsonl`：筛选目标日期的用户输入记录
- `~/.claude/sessions/*.json`：获取对应 session 的 `cwd`（工作目录）

输出每条记录的：**时间、工作目录、git 仓库名、git 分支、用户输入摘要**。

**1e. 本地 Codex 对话**

运行脚本收集：

```bash
python3 scripts/collect_codex_history.py --date YYYY-MM-DD
```

该脚本读取：
- `~/.codex/session_index.jsonl`：筛选目标日期的会话
- `~/.codex/sessions/YYYY/MM/DD/*.jsonl`：解析对话内容，提取用户消息和关键工具调用

输出每条会话的：**标题、时间、用户消息列表、工作目录**。

**1f. 本地 OpenCode / Craft Agent 对话**

若本地存在 OpenCode、Craft Agent 或同类 Agent 的历史目录，读取目标日期的会话。优先提取：时间、工作目录、git 仓库名、git 分支、用户输入和对话摘要。

常见候选路径包括但不限于：
- `~/.opencode/`
- `~/.craft/`
- `~/.craft-agent/`
- 应用自身配置目录中的 `sessions` / `history` 文件

如果路径不存在或格式无法稳定解析，记录为"该数据源不可用"，不要阻断日报生成。

**1g. 远程电脑 Agent 对话（SSH）**

尝试 SSH 到 `main-long`：

```bash
ssh -o ConnectTimeout=5 main-long "echo reachable"
```

若可达，在远程执行类似 1c/1d 的收集逻辑（路径适配 Windows）：
- Claude Code: `%USERPROFILE%\.claude\history.jsonl`
- Codex: `%USERPROFILE%\.codex\session_index.jsonl`
- OpenCode: `%USERPROFILE%\.opencode\` 或 `%APPDATA%\OpenCode\`
- Craft Agent: `%USERPROFILE%\.craft\`、`%USERPROFILE%\.craft-agent\` 或 `%APPDATA%\Craft\`
- OpenClaw: `C:\Users\%USERNAME%\.openclaw\agents\*\sessions\`
- Qclaw: `C:\Users\%USERNAME%\.qclaw\` 或 `%APPDATA%\QClaw\`

若不可达，记录 "远程电脑不可达，跳过"。

### Step 2: 交叉验证与智能筛选

**交叉验证原则：**

- **项目一致性**：Claude Code 的 `cwd` 和 Codex 的 `cwd` 应对应同一个实际项目。若出现矛盾（如本地显示在 A 项目，远程显示在 B 项目），标注出来让用户知道。
- **任务闭环**：飞书文档产出 + 嘀嗒清单任务完成 + GitHub PR/commit + Agent 对话中的相关讨论，应能相互印证。例如：GitHub 中 PR 已合并，且 Codex 对话中出现了"修复了 bug"的讨论，说明这项任务确实已完成。
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
- 跨工具的联动（"根据 GitHub PR/commit、飞书文档或嘀嗒清单任务完成了..."）
- 新发现和学习（"调研了 X 技术，结论是..."）

**历史内容匹配与任务路径推理（追加场景）：**

当日报已存在时，新数据不应被孤立处理。必须先读取原有日报内容，进行**任务路径推理**：

- **识别已有任务线索**：原有日报中的 bullet 往往暗示了一个未完成的任务或正在推进的方向。例如原有记录"上午开会，要求做强度校核"，说明当天有一项"强度校核相关工程任务"在进行。
- **判断新旧关联**：新收集到的数据是否与已有任务属于**同一工作流的不同阶段**？如果是，应合并表述，体现推进关系。
- **合并表述示例**：
  - ❌ 原有：`上午开会，要求做强度校核` / 新增：`修复GA离散优化的并行池问题`
  - ✅ 合并：`推进10MW滑轴齿轮箱设计：上午与甲方开会明确强度校核和扭矩密度交付物要求；下午修复macOS上GA离散优化的并行池兼容性问题，为后续大规模计算扫清障碍`
- **区分独立任务**：如果新数据与已有记录完全无关（如上午做A项目、下午做B项目），则分别列出，不要强行合并。

### Step 3: 生成日报 Markdown

**3a. 运行聚合脚本获取结构化数据**

```bash
python3 scripts/generate_daily.py \
  --date YYYY-MM-DD \
  --lark-docs /tmp/daily_lark_docs.json \
  --github /tmp/daily_github.json \
  --claude /tmp/daily_claude.json \
  --codex /tmp/daily_codex.json \
  --opencode /tmp/daily_opencode.json \
  --craft /tmp/daily_craft.json \
  --remote /tmp/daily_remote.json \
  -o /tmp/daily_structured.json
```

该脚本输出结构化 JSON，包含按项目分组的关键输入、飞书文档、GitHub 活动、TickTick 任务、Agent 对话和远程状态等。

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

- **同一主题的多条输入合并为粗粒度概括**。例如：
  - 原始输入：".venv-transoptima-ui 是什么？" → "帮我删掉这个环境"
             → "a_output_new 被哪些入口调用？" → "统一所有输出到 a_output"
  - 总结写法：**写论文前对 TransOptima 代码进行规范性整理：清理旧虚拟环境、统一输出接口**

> 注意：上例中虽然涉及多个具体操作（清理环境、接口重构），但它们属于同一目标（代码规范整理），应合并为一条概括，而不是拆成两条细项。

**输出分两种场景：**

**场景 A：日报不存在（全新创建）**

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

**场景 B：日报已存在（补充追加）**

> **绝不重复 `# 主要内容`、`# 记录` 等顶级标题，绝不重复已有项目的 `## 项目名` 标题。**

**追加前必须先读取现有日报**，提取已有项目列表（所有 `## ` 开头的二级标题）。然后按以下规则生成追加内容：

1. **已有项目**：只生成 bullet 列表，不重复生成 `## 项目名` 标题
2. **全新项目**：生成完整的 `## 新项目名` + bullet 列表
3. **合并后统一写入**：将所有内容（原有 + 新增）重新组织为一份完整文档，使用 `overwrite` 命令写入，避免追加导致标题重复

**错误示例（不要这样做）：**

```markdown
## 已有项目A
- 原有内容

## 其他
- 原有内容

---

## 已有项目A    ← 错误！重复标题
- 新增内容

## 其他          ← 错误！重复标题
- 新增内容
```

**正确示例（合并后重写）：**

```markdown
# 主要内容

## 已有项目A
- 原有内容
- 新增内容（合并到同一项目下）

## 新项目B
- 新增内容

## 其他
- 原有内容
- 新增内容（合并到同一项目下）

---

# 记录
- 原有链接
- 新增链接
```

**任务路径推理与合并操作步骤：**

1. **读取并解析原有日报**
   - `fetch` 现有日报全文
   - 提取所有 `## ` 项目标题和每个项目下的 bullet 内容
   - 理解原有记录中已经存在的任务线索和工作状态

2. **新旧内容匹配**
   - 将新收集的数据按项目分组
   - 对每个新项目 bullet，判断它与原有日报中同一项目的 bullet 是否存在**任务路径关联**：
     - 是同一任务的延续？（如"调研方向"→"确定方向"）
     - 是同一目标的推进？（如"开会提需求"→"修复阻碍问题的bug"）
     - 是完全独立的全新工作？

3. **合并表述（核心）**
   - **有关联的任务**：合并为一条连贯的描述，体现推进关系。用时间词或逻辑词连接。
     - 示例：原有"上午开会明确强度校核要求" + 新增"修复并行池bug" → 合并为"推进10MW齿轮箱设计：上午明确强度校核交付物，下午修复GA并行池兼容性问题保障后续计算"
   - **无关联的任务**：原有 bullet 保留，新增 bullet 在同一项目下独立列出。
   - **注意**：合并时不要丢失原有记录的关键信息，原有内容作为背景，新增内容作为推进。

4. **重新组织输出**
   - 每个项目的最终内容 = 原有 bullet（已与新内容合并或保留） + 无法合并的全新 bullet
   - 新项目创建完整标题
   - 用 `overwrite` 写入合并后的完整文档

**追加规则：**
- 先 `fetch` 现有日报全文，解析所有 `## ` 项目标题和 bullet 内容
- 进行任务路径推理，将有关联的新旧内容合并表述
- 将无关的新增 bullet 追加到对应已有项目下，新项目单独创建标题
- 使用 `overwrite` 命令写入合并后的完整内容，不要简单 `append` 到末尾
- 如果没有新增产出链接，`# 记录` 区只保留原有内容
- 绝不再出现 `# 主要内容` 或 `# 记录` 的重复标题

**生成规则：**

1. **总结性**：每条 bullet 是对一组相关工作的概括，不是原始输入的复制。
2. **简洁高效**：每条不超过 2 句话。避免 AI 腔，像人写的。
3. **项目分组**：优先按 **git 仓库名** 分组；若在同一仓库的不同分支工作，分支名附加在项目名称中（如 `TransOptima_Fullstop (third-paper)`）。无 git 信息时按工作目录名分组，无明确项目的归入 `# 主要内容`。
4. **时间隐含**：不强制写时间点，除非对理解工作内容有帮助。
5. **不写元信息**：不要写远程电脑连接状态、日报生成时间、数据收集过程等工具层面的信息。

**关于"调研/了解"类内容的处理：**

- **有产出的调研**（产出了飞书文档、代码提交、配置变更等实际成果）：在对应项目下正常记录，并在 `# 记录` 区保留文档链接。
- **无产出的调研**（只是了解、问问、看看，没有落到文档或代码）：简单写一个点即可，不展开细节。例如："了解 CLAUDE.md 多层级读取机制"、"了解 Agent 自我进化方案"。
- **同一项目下多个同类调研**：合并为一个点。例如："了解 Agent 自我进化与第三方模型接入方案（Coze、trae、workbuddy、qoder）"。

**关于 `# 记录` 区：**

- 只保留**有意义的产出链接**（飞书文档、实际创建的文档等）。
- 不要把 GitHub PR/issue 链接堆在 `# 记录` 区；只有它本身是当天关键交付物时才保留。
- 不要写远程电脑状态、不要写日报生成时间。
- 如果当天没有产出链接，可以只写待办事项或补充说明，也可以留空。

### Step 3c: 总结质量自检（写入飞书前）

生成 Markdown 后，在写入飞书前执行以下自检。如果发现问题，回头改写：

1. **同项目细项过多？**
   - 如果同一 `## 项目` 下有超过 3 条 bullet，检查是否属于同一主题，可合并为 1-2 条概括性描述。
   - ❌ `清理 .venv-transoptima-ui 虚拟环境`
   - ❌ `规划 a_output 输出脚本重构：以 arc/output/a_output 统一替代旧 a_output.m`
   - ✅ `写论文前对 TransOptima 代码进行规范性整理：删除旧虚拟环境、统一输出接口到 arc/output`

2. **纯操作罗列？**
   - 如果某条 bullet 只描述了"做了什么"而没有"为什么/成果是什么"，尝试改写。
   - ❌ `将结果输出统一归档到 results/YYYY-MM-DD`
   - ✅ `统一结果输出路径，迁移既有报告到 results/日期归档`

3. **补充场景结构正确？**
   - 如果是追加已有日报，确认没有出现重复的 `# 主要内容` 或 `# 记录`。
   - 确认 `---` 分隔符只在补充块前后使用，没有把原有内容切成碎片。

4. **任务路径是否连贯？**
   - 同一项目下的 bullet 之间是否有明确的推进关系？读者能否看出工作的发展脉络？
   - ❌ 原有：`上午开会，要求做强度校核` / 新增：`修复GA离散优化的并行池问题`（两条独立bullet，看不出关联）
   - ✅ 合并：`推进10MW齿轮箱设计：上午明确强度校核与扭矩密度交付物要求；下午修复GA并行池兼容性问题，为后续大规模计算扫清障碍`（体现同一工作流的推进）
   - 如果同一项目下出现多条无关联的细项，检查是否应分到不同项目或合并为概括性描述。

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
- 若已存在：
  1. 先用 `docs +fetch` 读取现有日报完整内容
  2. 提取已有项目标题（所有 `## ` 开头的二级标题）
  3. 将新生成的 bullet 合并到对应已有项目下，新项目创建新标题
  4. 使用 `docs +update --command overwrite` 写入合并后的完整文档

**禁止**使用 `--command append` 直接追加到文档末尾，这会导致项目标题重复。

## 参考

- [summary-shared](../summary-shared/lark_folders.json) — 飞书文件夹 token 配置
- [weekly-summary](../weekly-summary/SKILL.md) — 周报 skill（读取本 skill 生成的日报）
- [lark-doc](../lark-doc/SKILL.md) — 飞书文档操作详细用法
