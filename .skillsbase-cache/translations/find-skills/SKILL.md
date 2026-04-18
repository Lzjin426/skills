---
name: find-skills
description: 当用户提出诸如“如何做X”、“查找用于X的技能”、“有没有能……的技能”等问题，或表达扩展能力的兴趣时，帮助用户发现并安装智能体技能。当用户寻找可能以可安装技能形式存在的功能时，应使用此技能。
---

# 查找技能

此技能帮助您从开放的智能体技能生态系统中发现并安装技能。

## 何时使用此技能

当用户出现以下情况时使用此技能：

- 询问“如何做X”，而X可能是已有技能能处理的常见任务
- 说“查找用于X的技能”或“有没有用于X的技能”
- 询问“你能做X吗”，而X是一项专业能力
- 表达扩展智能体能力的兴趣
- 想要搜索工具、模板或工作流
- 提到希望获得特定领域（设计、测试、部署等）的帮助

## 什么是技能 CLI？

技能 CLI（`npx skills`）是开放智能体技能生态系统的包管理器。技能是模块化包，通过专业知识、工作流和工具扩展智能体的能力。

**关键命令：**

- `npx skills find [查询词]` - 通过关键词交互式搜索技能
- `npx skills add <包名>` - 从 GitHub 或其他来源安装技能
- `npx skills check` - 检查技能更新
- `npx skills update` - 更新所有已安装技能

**浏览技能请访问：** https://skills.sh/

## 如何帮助用户查找技能

### 步骤 1：理解用户需求

当用户寻求帮助时，请确定：

1. 领域（例如：React、测试、设计、部署）
2. 具体任务（例如：编写测试、创建动画、审查 PR）
3. 该任务是否常见到很可能已有对应技能存在

### 步骤 2：搜索技能

使用相关查询词运行查找命令：

```bash
npx skills find [查询词]
```

例如：

- 用户问“如何让我的 React 应用更快？” → `npx skills find react performance`
- 用户问“你能帮我审查 PR 吗？” → `npx skills find pr review`
- 用户问“我需要创建更新日志” → `npx skills find changelog`

该命令将返回类似以下结果：

```
使用 npx skills add <所有者/仓库@技能名> 安装

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### 步骤 3：向用户展示选项

找到相关技能后，向用户展示：

1. 技能名称及其功能
2. 可运行的安装命令
3. 在 skills.sh 上了解更多信息的链接

示例回复：

```
我找到了一个可能对您有帮助的技能！“vercel-react-best-practices”技能提供了来自 Vercel Engineering 的 React 和 Next.js 性能优化指南。

安装命令：
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

了解更多：https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### 步骤 4：提供安装帮助

如果用户希望继续，您可以为其安装技能：

```bash
npx skills add <所有者/仓库@技能名> -g -y
```

`-g` 标志表示全局安装（用户级别），`-y` 标志跳过确认提示。

## 常见技能类别

搜索时，可考虑以下常见类别：

| 类别           | 示例查询词                               |
| -------------- | ---------------------------------------- |
| 网页开发       | react, nextjs, typescript, css, tailwind |
| 测试           | testing, jest, playwright, e2e           |
| DevOps         | deploy, docker, kubernetes, ci-cd        |
| 文档           | docs, readme, changelog, api-docs        |
| 代码质量       | review, lint, refactor, best-practices   |
| 设计           | ui, ux, design-system, accessibility     |
| 生产力         | workflow, automation, git                |

## 高效搜索技巧

1.  **使用具体关键词**：“react testing”比仅用“testing”更好
2.  **尝试替代术语**：如果“deploy”无效，试试“deployment”或“ci-cd”
3.  **查看热门来源**：许多技能来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`

## 未找到技能时

如果未找到相关技能：

1.  告知用户未找到现有技能
2.  提供使用您的通用能力直接帮助完成任务的选项
3.  建议用户可以使用 `npx skills init` 创建自己的技能

示例：

```
我搜索了与“xyz”相关的技能，但没有找到匹配项。
我仍然可以直接帮助您完成此任务！您希望我继续吗？

如果这是您经常做的事情，您可以创建自己的技能：
npx skills init my-xyz-skill
```