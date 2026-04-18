---
name: better-md-writer
description: 通过轻量级默认工作流撰写、重写和润色文档。首先选择文档类型，仅当明确能改进草稿时才启用高成本处理环节。
---

# Better Md Writer

当用户需要撰写或优化 Markdown 文档（如笔记、知识库页面、README、提案、教程、操作手册或其他结构化文档）时，请使用此技能。

核心规则很简单：**选择最轻量但仍能满足文档任务的工作流**。除非任务明确受益，否则不要默认启用繁重的研究、图表、认知框架或后处理环节。

对于知识库写作，首先优化**未来的可读性、低理解成本和专业清晰度**。避免使用密集的学术措辞和过于随意的教学口吻。将此视为全局知识库规则，而非仅适用于机器学习的写作偏好。

## 目的

此技能是一个轻量级的协调器。它帮助智能体：
- 明确文档必须完成的任务
- 选择合适的文档类型
- 仅在合理时启用可选处理环节
- 使用选定的默认设置进行草稿撰写
- 运行面向读者的检查
- 仅在相关时应用 Fullstop 的本地 Obsidian 工作流

此技能不是单一固定的流水线。它不应强制所有文档都经过相同的长篇写作流程。

## 默认工作流

1. **明确任务**
   - 当写作任务、受众或输出形式不明确时，阅读 [references/core/document-intent.md](references/core/document-intent.md)。
   - 仅询问会实质性改变草稿的缺失信息。
   - 对于 **kb-article**，在起草前确定文章子类型：概念解释、比较、结果解读或方法/流程。

2. **选择类型**
   - 从以下类型中选择一种：
     - [note](references/profiles/note.md)
     - [kb-article](references/profiles/kb-article.md)
     - [readme](references/profiles/readme.md)
     - [proposal](references/profiles/proposal.md)
     - [tutorial](references/profiles/tutorial.md)
     - [runbook](references/profiles/runbook.md)
   - 如果类型仍不明确，保持轻量级，避免将任务变成繁重的文档编写工作。

3. **决定可选处理环节**
   - 仅当内容具有时效性、涉及比较、证据密集，或用户明确要求研究时，才启用 [research](references/passes/research.md)。
   - 仅当文档需要在较长解释中构建可复用的心智模型时，才启用 [cognitive-path](references/passes/cognitive-path.md)。
   - 仅当视觉内容比纯文本更能降低理解成本时，才启用 [illustration](references/passes/illustration.md)。
   - 仅当面向人类的文本中，润色机械措辞不会损害精确性或可追溯性时，才启用 [humanization](references/passes/humanization.md)。
   - 对于 **kb-article**，倾向于使用更多视觉内容、精确的平实语言和更强的主线，除非用户明确希望采用更密集的参考风格。
   - 对于 **kb-article**，不要仅依赖主写作智能体来决定插图。
   - 如果文档是知识库解释性文章，且满足以下任一条件，则在草稿结构稳定后**必须**进行专门的插图审查：
     - 主题抽象、基于模型、基于图表、基于用户界面，或其他难以想象的内容
     - 草稿包含 2 个或更多 `IMG-CANDIDATE` 标记
     - 读者很可能会问“这实际上是什么样子？”
     - 文档比较了多种机制、流程或模型家族

4. **起草**
   - 使用选定的类型作为默认行为。
   - 使用 [references/core/structure-selection.md](references/core/structure-selection.md) 选择主要载体并构建章节。
   - 除非目标环境明确支持更具体的格式，否则优先使用标准、可移植的 Markdown。
   - 如果目标是 Fullstop 的本地知识库或 Obsidian 仓库，默认使用显式的分层标题编号，如 `1.`、`1.1` 和 `1.1.1`，除非目标文件已有既定的冲突风格。
   - 对于读者通常难以想象的概念，在解释形式区分或实现细节之前，先展示事物的外观。
   - 对于 **kb-article**，保持语气专业且克制。不要像叙述课程、视频脚本或对话式辅导那样写作。
   - 对于 **kb-article**，从稳定的子类型骨架开始，而不是为每篇文章从头创建新大纲。
   - 对于 **kb-article**，保持顶层结构紧凑。默认 `3-5` 个顶层章节，除非文档明确需要更多。
   - 对于 **kb-article**，确保文章回答一个明确的判断性问题，如“如何识别它”、“如何区分它”、“如何解读输出”或“如何将其放回当前项目中”。
   - 对于 **kb-article**，至少包含一个显式的视觉锚点，即使在决定是否将其变为真实图像之前：它看起来是什么样子、输出是什么样子、流程是什么样子，或比较的形状是什么样子。
   - 当可能需要图表时，插入显式的图像候选标记，而不是在行内做出未经审查的最终决定。

5. **运行读者检查**
   - 在最终交付前使用 [references/core/reader-check.md](references/core/reader-check.md)。
   - 如果启用了任何可选处理环节，验证它是否改进了文档，而不是增加了仪式感或噪音。

6. **在相关时应用本地环境操作**
   - 如果文档用于 Fullstop 的知识库或 Obsidian 仓库，应用 [references/local/fullstop-obsidian.md](references/local/fullstop-obsidian.md)。
   - 将这些本地默认设置与通用写作逻辑分开。
   - 在为 Obsidian 知识库写作时，不要使用 frontmatter wiki-links（如 `related: [[...]]`）来批量创建图谱边；将结构元数据保留在 frontmatter 中，并将语义链接保留在正文内容中。

## 类型选择

根据文档的任务（而非仅标签）选择类型：
- **note**：快速记录、清理或内部工作记忆
- **kb-article**：为后续重用而进行的持久性知识库写作
- **readme**：仓库或项目的引导和入门
- **proposal**：包含选项、权衡和推荐的支持决策文档
- **tutorial**：教学或引导学习
- **runbook**：包含步骤、分支和验证的操作执行文档

如果文档结合了多个任务，选择主要任务，并仅从其他类型中借用最小有用的元素。

对于 **kb-article**，默认：
- 首先选择一个子类型：概念解释、比较、结果解读或方法/流程
- 在依赖术语或符号之前，用平实但精确的语言解释
- 当能降低读者困惑时，首先展示具体事物、输出或图片
- 保持清晰的进展，而不是堆叠松散相关的小节
- 保持默认的顶层结构在 `3-5` 个章节内
- 回答一个明确的判断性问题，而不仅仅是积累定义
- 在草稿早期预留至少一个视觉锚点
- 使用语义化的章节标题，而非对话式钩子
- 避免使用诸如“先记这一句”、“先别管”、“你只要记住”或类似口语风格的提示语，除非用户明确希望教程口吻
- 对于 Obsidian 目标，使用 frontmatter 存储结构字段（如笔记类型、层级、先决条件或后续步骤），而非用于批量 wiki-link 关系列表，以免污染图谱

## 处理环节选择

所有可选处理环节**默认关闭**。

### 研究

- 默认：`关闭`
- 仅当事实、术语、政策、版本或比较需要验证时开启。
- 参见 [references/passes/research.md](references/passes/research.md)。

### 认知路径

- 默认：`关闭`
- 仅当较长解释需要显式心智模型和刻意学习弧线时开启。
- 参见 [references/passes/cognitive-path.md](references/passes/cognitive-path.md)。

### 插图

- 默认：`关闭`
- 仅当图表或图像比额外文本解释更快或更准确时开启。
- 特殊情况：对于 **kb-article**，鼓励在能实质性减少困惑时使用插图，包括截图、示例、流程草图、比较和“它看起来是什么样子”的视觉内容。
- 对于解释性强的知识库文章，主写作智能体应提出候选方案，但单独的审查环节应决定实际需要哪些视觉内容及其类型。
- 如果满足强制插图审查条件，则文档在审查产生图像计划之前不算完成。
- 参见 [references/passes/illustration.md](references/passes/illustration.md)。

### 人性化

- 默认：`关闭`
- 仅当输出是面向读者的文本密集型内容，且措辞清理不会削弱确切含义时开启。
- 参见 [references/passes/humanization.md](references/passes/humanization.md)。

## 参考

### 核心

- [document-intent](references/core/document-intent.md)
- [structure-selection](references/core/structure-selection.md)
- [reader-check](references/core/reader-check.md)

### 类型

- [note](references/profiles/note.md)
- [kb-article](references/profiles/kb-article.md)
- [readme](references/profiles/readme.md)
- [proposal](references/profiles/proposal.md)
- [tutorial](references/profiles/tutorial.md)
- [runbook](references/profiles/runbook.md)

### 可选处理环节

- [research](references/passes/research.md)
- [cognitive-path](references/passes/cognitive-path.md)
- [illustration](references/passes/illustration.md)
- [humanization](references/passes/humanization.md)

### 本地默认设置

- [fullstop-obsidian](references/local/fullstop-obsidian.md)