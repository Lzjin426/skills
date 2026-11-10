# push-code prompt 模板

把 `<>` 占位符替换成实际内容。所有委派 prompt 都必须自包含：新会话没有历史。

## 1. Worktree 准备

执行会话在自己的第一轮里运行（路径按仓库和 slug 替换）：

```sh
git worktree add -b qoder/<slug> "<worktrees-root>/<slug>/<repo>" main
```

约定：

- 分支名 `qoder/<slug>`，基线是当时 main 的 HEAD。
- 之后所有工作在 worktree 内进行；不改主工作区。
- 不 push、不合并 main；完成后本地提交并汇报。

## 2. 委派 prompt 模板

```text
你在 Qoder Desktop 的独立会话中工作，作为执行 agent。主控会 review 并整合你的分支。
仓库：<repo-path>（<platform>，Git，main 分支，HEAD <baseline-sha>）。

任务：<one-feature-summary>

要求：
1. <requirement 1>
2. <requirement 2>
3. 文件归属：只改 <files>；不要碰 <excluded-files>。
4. 遵守仓库 AGENTS.md：不跑 <forbidden-formatter>，紧凑风格照周围代码；不改存储格式和用户数据。
5. 测试：<targeted-tests>；改了核心/编辑内核时按仓库要求补 fuzz 种子。

工作方式：
- 先创建 worktree：git worktree add -b qoder/<slug> "<worktrees-root>/<slug>/<repo>" main
- 之后所有工作都在该 worktree；不要启动或强关用户正在用的预览窗口。
- 完成后在该 worktree 本地提交（不 push、不合并 main）。

汇报（最终消息）：worktree、分支、commit SHA、改动文件、测试命令与结果、未验证项。不要贴大段 diff。
```

大功能或方向不确定时，把第一轮改成只读调研，要求交付：

```text
第一阶段只做只读调研并给出实现方案，不改代码。方案按「推荐方案 / 改动文件与改动点 / 代价与风险 / 验收建议」组织。主控转交用户批准后再实现。
```

## 3. Review follow-up 模板

在开发会话完成回调之后、合并之前发送。必须在**同一个会话窗口**里启动新 agent：

```text
主控流程要求：每个 worktree 完成后，要在本对话窗口里启动一个新的 review agent 审查，不能由开发会话自审。

1. 使用 Agent 工具启动一个新的 review agent（subagent_type 用“【示例】代码审查员”；不可用则用 general-purpose），对 worktree <worktree-path> 的提交 <sha>（分支 <branch>，diff 以 git diff main...HEAD 为准）做只读审查。
2. 审查重点：
   - 需求符合度：<requirements>
   - 找实际缺陷与遗漏：行为错误、边界、数据安全、未同步调用方、测试缺口；不要风格挑刺。
   - review agent 只读，不改代码；结论按严重程度列出，带文件:行。
3. 拿到结论后：确认成立的缺陷由你修复，新增 commit（不 amend、不 push），在 worktree 里重跑受影响测试，再汇报：review 发现、哪些已修、修复 commit SHA、剩余问题；无缺陷也请明确说明。
```

已经合并的分支也补发同样的 review；有修复时再合并一次。

## 4. 合并与清理清单

```sh
# 1. 确认分支已合并且工作区干净
git -C "<worktree-path>" status --porcelain
git branch --merged main | cat

# 2. main 前进过则先 rebase，再快进合并
git -C "<worktree-path>" rebase main
git merge --ff-only qoder/<slug>

# 3. 该代码状态跑一次完整检查（有则跑）
scripts/check.sh

# 4. 删除已合并的 worktree 和分支
git worktree remove "<worktree-path>"
git branch -d qoder/<slug>

# 5. 确认剩余状态
git worktree list
git branch | cat

# 6. 推送前先问用户；得到明确同意后再执行
git push origin main
```

只删除确认已并入 main 且干净的；保留正在开发的；其他工具遗留的 detached worktree 未经用户确认不要删。合并和清理可以按流程做，但 **push 和归档会话前必须单独询问用户**。

## 5. UI 验收（平台电脑控制）

UI 改动交付前，用平台自带的电脑控制实际运行并操作软件：

- 使用 computer-use skill（宿主 Node REPL + Computer Use SDK）打开、点击、输入、截图。
- 截图保存成文件（PNG），在汇报里给绝对路径。
- 查看有代表性的真实画面；不要用“截图文件生成”或“测试通过”代替体验判断。
- 不强关用户正在使用的窗口；不改用户数据；测试文档库用隔离副本或临时库。
