---
name: dev-env-sync
description: |
  同步两台电脑（Mac 与 Windows）之间的开发环境配置，特别是 .agent/skills 目录下的 skill 仓库。
  当用户提到"同步 skill"、"更新 skill"、"拉取 skill"、"看看两边的 skill 有什么不一样"、
  "对比环境"、"同步开发环境"、"检查另一台电脑"、"看看 CLI 有什么不一样"等任何相关意图时，**必须**使用此 skill。
  即使只是随口提到"好像两边 skill 不同步了"或"另一台电脑的 skill 是不是更新了"，也应触发。
  此 skill 默认在 Mac 端运行，通过 ssh main-long 连接 Windows 端。
---

# 开发环境同步 Skill

## 背景

用户有两台电脑：
- **Mac（本地）**：当前运行环境，skills 位于 `~/.agent/skills`
- **Windows（远程）**：通过 `ssh main-long` 连接，skills 同样位于 `~/.agent/skills`

两边的 skills 目录均为 git 仓库，通过 GitHub 同步。此 skill 帮助用户：
1. 同步 skills 仓库（自动判断方向、拉取/推送）
2. 对比两边安装的开发工具差异（CLI、插件等）

## 核心原则

- **默认 Mac 为操作端**：所有命令优先在本地执行，远程操作通过 `ssh main-long` 完成。
- **自动判断同步方向**：比较两边的 git 提交历史，自动决定谁领先、谁落后，无需用户手动选择。
- **安全优先**：涉及写操作（push/merge）时，先向用户确认；只读检查则直接执行。
- **输出简洁**：用表格或列表清晰展示对比结果，不堆砌无用信息。

## 工具路径

| 电脑 | 路径 | 连接方式 |
|------|------|----------|
| Mac | `~/.agent/skills` | 本地 |
| Windows | `~/.agent/skills` | `ssh main-long` |

## 任务类型

### 1. Skills 仓库同步

当用户说"同步 skill"、"更新 skill"、"拉取 skill"时执行：

#### 步骤 1：检查本地状态

在 Mac 本地执行：
```bash
cd ~/.agent/skills
git status --short
git log --oneline --decorate -5
git branch -vv
git remote -v
```

记录以下信息：
- 是否有未提交的更改
- 当前分支
- 最近 5 条提交
- 分支与远程的追踪关系

#### 步骤 2：检查远程状态

通过 SSH 在 Windows 上执行相同命令：
```bash
ssh main-long "cd ~/.agent/skills && git status --short && echo '---SEP---' && git log --oneline --decorate -5 && echo '---SEP---' && git branch -vv && echo '---SEP---' && git remote -v"
```

#### 步骤 3：分析同步状态

比较两边的输出，判断属于以下哪种情况：

| 情况 | 判断依据 | 操作 |
|------|----------|------|
| A. 完全同步 | 最新 commit hash 相同，且无未提交更改 | 告知用户已同步 |
| B. Mac 领先 | Mac 有 Windows 没有的提交，Windows 无本地更改 | 询问用户是否 push 到远程，或在 Windows 端 pull |
| C. Windows 领先 | Windows 有 Mac 没有的提交，Mac 无本地更改 | 在 Mac 端执行 `git pull` |
| D. 双向分叉 | 两边都有对方没有的提交 | 询问用户策略：merge、rebase 或手动处理 |
| E. 本地有未提交更改 | 任一边有未 staged/uncommitted 文件 | 先提醒用户提交或暂存 |

#### 步骤 4：执行同步

根据分析结果执行：

- **情况 C**：直接在 Mac 端 `git pull`
- **情况 B**：询问用户 "Mac 领先，要推送到远程让 Windows 拉取吗？" 或 "直接在 Windows 上拉取吗？"
- **情况 D**：向用户展示分叉的提交历史，请用户决定
- **情况 E**：列出未提交文件，请用户处理

如果需要在 Windows 端执行 pull：
```bash
ssh main-long "cd ~/.agent/skills && git pull"
```

如果需要在 Mac 端 push：
```bash
cd ~/.agent/skills && git push
```

#### 步骤 5：验证同步结果

再次检查两边的最新 commit hash，确认一致。

### 2. 开发环境对比

当用户说"对比环境"、"看看两边装了什么"、"检查开发工具"、"CLI 有什么不一样"时执行：

#### 步骤 1：对比 ~/.agent/ 目录结构

skills 之外，检查 ~/.agent/ 下还有哪些工具目录：

**Mac 本地**：
```bash
ls -la ~/.agent/
```

**Windows 远程**：
```bash
ssh main-long "ls -la ~/.agent/"
```

找出哪边有独有的目录或文件。

#### 步骤 2：对比全局 CLI 工具

通过 `compgen -c` 列出所有可执行命令，过滤出常见的 CLI 工具模式：

**Mac 本地**：
```bash
# 列出所有包含 "-cli"、"-tool" 或常见工具名的命令
compgen -c | grep -E '\-(cli|tool)|^(lark|mineru|codex|claude|cursor|npm|pip|uv|pnpm|yarn|cargo|brew|gh|git|docker|kubectl|terraform|ansible|vagrant|flyctl|vercel|netlify|supabase)$' | sort -u
```

**Windows 远程**：
```bash
ssh main-long "compgen -c | grep -E '\\-(cli|tool)|^(lark|mineru|codex|claude|cursor|npm|pip|uv|pnpm|yarn|cargo|brew|gh|git|docker|kubectl|terraform|ansible|vagrant|flyctl|vercel|netlify|supabase)$' | sort -u"
```

> 如果某些工具名不在上述正则中但用户经常提到，主动将其加入过滤模式。

#### 步骤 3：检查包管理器全局安装列表

**npm global**：
```bash
npm list -g --depth=0 2>/dev/null
ssh main-long "npm list -g --depth=0 2>/dev/null"
```

**pip global**（如果安装了 pip）：
```bash
pip list --format=freeze 2>/dev/null | head -50
ssh main-long "pip list --format=freeze 2>/dev/null | head -50"
```

#### 步骤 4：检查 ~/bin/ 和 ~/.local/bin/

很多自定义 CLI 会安装在这里：

```bash
ls -la ~/bin/ 2>/dev/null
ls -la ~/.local/bin/ 2>/dev/null

ssh main-long "ls -la ~/bin/ 2>/dev/null; ls -la ~/.local/bin/ 2>/dev/null"
```

#### 步骤 5：汇总输出

用表格展示对比结果，分为几个区块：

```
## ~/.agent/ 目录对比

| 项目 | Mac | Windows | 状态 |
|------|-----|---------|------|
| skills | 有 | 有 | 已同步 |
| lark-cli | 有 | 无 | 仅 Mac 有 |
| mineru | 无 | 有 | 仅 Windows 有 |

## CLI 工具对比

| 工具 | Mac | Windows | 状态 |
|------|-----|---------|------|
| lark-cli | v1.2.0 | 未安装 | 仅 Mac 有 |
| mineru-cli | 未安装 | v0.5.0 | 仅 Windows 有 |
| codex | v2.1.0 | v2.1.0 | 一致 |
```

### 3. 综合检查（默认模式）

如果用户只是笼统地说"同步一下"或"检查环境"，**同时执行**任务 1 和任务 2，先同步 skills，再对比环境差异。

## 输出格式

所有输出使用中文，结构如下：

```
## Skills 同步状态

- Mac 最新提交: abc1234 (添加 xxx skill)
- Windows 最新提交: def5678 (修改 yyy)
- 状态: Windows 领先，正在拉取...
- 结果: 同步完成，两边现在都是 abc1234

## ~/.agent/ 目录对比
（表格）

## CLI 工具对比
（表格）

## 建议

（如果有版本差异或遗漏的工具，给出安装建议）
```

## 常见 SSH 问题处理

如果 `ssh main-long` 失败：
1. 检查 SSH 配置是否存在：`cat ~/.ssh/config | grep -A 5 "Host main-long"`
2. 如果连接超时，提示用户检查 Windows 电脑是否开机、网络是否正常
3. 如果权限 denied，提示用户检查 SSH 密钥

## 边界情况

- **Windows 不在线**：记录为"Windows 不可达"，仅展示 Mac 端状态
- **skills 目录不是 git 仓库**：提示用户初始化或检查路径
- **未配置 git remote**：提示用户设置远程仓库
- **网络问题导致 GitHub 无法访问**：提示用户稍后重试或手动同步
- **~/.agent/ 目录不存在**：提示用户检查安装路径
