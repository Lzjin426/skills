---
name: push-code
description: 主控式并行开发流程：主会话只讨论方向、拆分与整合，为每个独立功能开新会话和独立 git worktree，开发完成后强制新的 review agent 审查，通过后合并、测试、交付并清理分支/worktree。只在用户明确说使用 push-code、要求主控开发、并行开 worktree 开发、或显式要求 multi-session/worktree review 时启用；不要用于普通开发或普通代码修改。Use only when the user explicitly asks for push-code, a controller-led multi-session/worktree development batch, or worktree branch review.
---

# push-code

## Overview

多功能开发批次使用这个流程。主会话是主控：对齐方向、拆分、委派、强制 review、整合、验证、交付和清理。主会话不亲自实现功能代码，除非用户明确要求做一个小修。

**只在用户明确调用时启用**：普通开发或普通代码修改不要自动套用这套流程。

**决策必须先拍板**：交互手势、产品行为、存储方案、Skill 的设计与内容，都必须先把选项、取舍和影响摆给用户，得到明确批准后再实施。不要把"可以""做""推进"当成对未列出细节的授权；先做后问视为错误。

## 角色

- **主控（当前会话）**：方向讨论、任务拆分、文件归属、审阅方案与真实改动、合并、集中验证、交付、清理。
- **执行会话**：一个独立功能一个会话、一个 worktree、一个分支；负责开发、定向测试、本地提交（不 push、不合并 main）。
- **review agent**：每个 worktree 完成后，在执行会话内启动的**新 agent**，只读审查，不能由开发会话自审。

## 1. 对齐方向

- 先读仓库的 AGENTS.md / README / docs/CONTEXT.md，确认当前计划与约束。
- 先讨论再动手：产品取舍、交互方式、数据安全等问题用 AskUserQuestion 让用户拍板；未确认时只做只读探查。
- 交互细节（普通点击/修饰键/右键菜单）、存储方案和 Skill 结构要先列出选项与取舍，等用户逐项确认；简短回复只覆盖已经列出的内容，不覆盖未列出的细节。
- 新需求默认接在已批准计划之后，不打断正在执行的任务。

## 2. 拆分

- 只并行真正独立的功能；为每个 worktree 明确文件归属，避免两个会话同时改同一批文件。
- 批次保持小而完整；先做低风险小修，再做需要方案的大功能。
- 为每个任务确定 worktree 路径、分支名（如 `qoder/<slug>`）和基线 main HEAD。
- 拆分方案（做哪些功能、每个会话的文件归属、哪些并行/串行）先给用户确认，再创建会话。

## 3. 委派

- 用内置 `create_chat_session`（默认 agent，`callbackMode: supervise`）创建独立会话。新会话没有历史，prompt 必须自包含：仓库路径、基线 HEAD、需求、边界、验证方式、汇报格式。
- 要求执行会话自己建 worktree：

```sh
git worktree add -b qoder/<slug> "<worktrees-root>/<slug>/<repo>" main
```

- 统一约束：不 push、不合并 main、不跑仓库禁止的格式化（如 rustfmt）、不启动或强关用户正在用的预览窗口、不碰用户数据；遵守仓库 AGENTS。
- 大功能或方向不完全确定时，第一轮只做只读调研并交方案；**用户批准后**再动代码。

## 4. 跟踪

- 优先依赖 supervise 回调，不要轮询；需要看进度时用 `read_chat_session`，需要纠偏时用 `send_message_to_chat_session`。
- 「Turn 完成」不等于工作被接受：读最终汇报并用 `git log` / `git status` 核对实际状态。
- 会话执行失败时先读现场，工作通常已保留；让原会话从断点继续，不要另起重复实现。

## 5. Review（强制）

- 每个 worktree 完成后、合并前，向该会话发 follow-up：**启动一个新的 review agent**（Agent 工具的「示例」代码审查员，或 general-purpose），只读审查 `git diff main...HEAD`。
- **严格模式**：如果会话工具或 MCP 不可用，暂停 review 和合并，等连接恢复后继续；不要用主控本地 review agent 替代会话内审查，也不要跳过 review 直接合并。
- 审查重点：需求符合度、真实缺陷与遗漏、数据安全、测试缺口；不做风格挑刺。结论按严重程度列出并带文件:行。
- 开发会话修正确认成立的问题，**新增 commit**（不 amend、不 push），重跑受影响测试后再汇报。review 不通过不合并。
- 已合并的分支也补 review；有修复再合并一次。

## 6. 整合

- 主控亲自看 diff（`git show`），不能只看汇报。
- main 前进后先 rebase 分支，再 `git merge --ff-only`；保持线性历史。
- 每个整合后的代码状态集中跑一次仓库完整检查（有 `scripts/check.sh` 就跑它）；同一状态通过的结果直接复用，只对受影响部分补测。
- 按约定构建和交付；用户窗口在运行时不要强制关闭，先准备新二进制或请用户关闭后重启。
- 合并和清理可以按流程做；**push 前必须单独询问用户**，得到明确同意后再推送。归档会话同样先问，不要擅自批量归档。

## 7. 清理

- 每批合并后执行 `git worktree list` 和 `git branch --merged main`。
- 只删除「已并入 main 且 worktree 干净」的分支：

```sh
git worktree remove "<worktree-path>" && git branch -d "qoder/<slug>"
```

- 保留正在开发的 worktree；其他工具遗留的 detached worktree 未经用户确认不要删。
- 在汇报里列出保留和删除的 worktree；归档已完成会话前先问用户，不要擅自批量归档。

## 测试门槛

- 核心/存储/编辑内核改动：跑定向测试，按仓库要求补 fuzz 种子；交付前跑完整检查。
- UI 改动：优先使用平台自带的电脑控制（computer-use skill / 宿主提供的 Node REPL 与 Computer Use SDK）实际运行、操作软件并查看真实窗口行为；截图保存成文件并给出绝对路径。编译和单测不能代替体验验收；无法实测时明确说明。不要强关用户正在使用的窗口，也不要改动用户数据。
- 一个代码状态只跑一次完整检查，不要为每个小提交重复全套。

## 汇报

- 用日常语言，先结论和影响，再给细节；说明做完、未完成和验证边界。
- 告诉用户可以实际测试什么；不要用提交数或测试数量代替用户可用的结果。

## 参考

- [委派与 review 的 prompt 模板](references/prompts.md)
