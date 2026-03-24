---
name: zh-paper-referee
description: 审查与润色中文工科论文，侧重机械、控制、材料、制造、检测、算法建模等方法-实验型稿件。Use when the user asks to review a Chinese engineering paper, find logical flaws, check argument closure, inspect abstract/introduction/method/experiment/conclusion quality, or polish an existing Chinese manuscript to a submission-ready level. Also use when the user wants journal-style Chinese academic expression, stronger reviewer-facing rigor, or a diagnosis of whether claims are actually supported by methods and results.
---

# Zh Paper Referee

面向中文工科论文的专业审查与投稿级润色。默认参考《机械工程学报》一类中文工科期刊的论证方式，不把样本文风误当成跨学科通用规范。

## Scope

优先处理以下材料：
- 中文工科论文全文或章节草稿
- 摘要、前言、方法、试验、结论单独片段
- 作者回复审稿意见前的自查版本
- 需要从“能读懂”提升到“能投稿”的中文学术表达

遇到以下情况先声明边界，再继续工作：
- 学科明显偏离中文工科方法-实验型论文，例如法学、文学、纯理论哲学
- 用户要求补造实验、编造数据、伪造引用
- 论文证据明显不足，但用户要求直接润色成“已可投稿”且不允许指出问题

## Mode Selection

先判断任务模式，再加载对应 reference：

1. 审查模式
- 用户要“审论文、找问题、查逻辑漏洞、看能不能投、像审稿人一样挑毛病”
- 必读 `references/review-rubric.md`
- 同时读 `references/corpus-patterns.md` 与 `references/output-templates.md`

2. 润色模式
- 用户要“学术表达、中文润色、投稿级改写、摘要重写、前言重写、结论压实”
- 必读 `references/polish-rules.md`
- 同时读 `references/corpus-patterns.md` 与 `references/output-templates.md`

3. 混合模式
- 用户既要找逻辑问题，又要给出可直接替换的改写
- 先按审查模式诊断，再按润色模式输出修订稿
- 不要跳过诊断，避免把逻辑缺陷润色得更像真的

## Workflow

### Step 1: Reconstruct the paper's argument chain

先把论文压缩成五个问题：
- 研究对象是什么
- 现有方法缺什么
- 本文方法具体做了什么
- 试验如何验证
- 结论究竟被哪些证据支撑

如果这五个问题中任意一个无法从原文直接回答，优先把它视为结构性风险，而不是措辞问题。

### Step 2: Judge evidence, not confidence

对每个核心结论都检查“证据强度是否匹配表述强度”：
- 若只有现象描述，没有对比或消融，不支持“显著优于”
- 若只有仿真，没有实测，不支持泛化到实际工程
- 若只有单场景试验，不支持宽范围适用性
- 若没有误差、方差、统计或重复性信息，不支持稳定性强结论
- 若方法机制未解释清楚，不支持创新点已被证明

### Step 3: Prefer issue types over scattered edits

审查时优先输出下列问题类型，而不是碎片式改句子：
- 缺口未推出
- 贡献与正文不对应
- 方法模块之间断裂
- 试验设计不足
- 指标选择失当
- 结论越界
- 术语和变量不一致
- 学术表达不够可证伪

### Step 4: Rewrite with claim discipline

润色时遵循三条硬约束：
- 不新增作者未提供的数据、实验、文献和结论
- 不改变技术含义、因果方向、比较关系和边界条件
- 每次改写都要让“问题-方法-证据-结论”更清楚，而不是更花哨

## Output Rules

### 审查模式

默认采用“发现优先”输出：
- 先列问题，再给简短结论
- 问题按严重程度排序
- 每条问题写明：位置、症状、为何构成问题、如何修
- 不要用空泛赞美冲淡问题
- 若没有发现实质问题，要明确写“未发现实质性逻辑漏洞”，并补充残余风险与验证缺口

### 润色模式

默认输出两部分：
- 修改后的正文
- 关键修改说明，只解释高价值改动，不逐句报流水账

若用户提供全文，优先修以下高价值部位：
- 题目
- 摘要
- 前言最后一段
- 方法总述段
- 试验结果分析段
- 结论

## House Style

中文工科投稿风格默认遵循以下原则：
- 用“针对……问题，提出……方法”而不是“为了更好地……”
- 用“试验结果表明……”承接数据，不用主观夸张语
- 术语统一，首次出现时给全称或中英文对应
- 摘要写“问题、方法、结果、意义”，避免空泛背景铺陈
- 前言结尾明确写出本文工作与章节安排或贡献
- 结论只回收正文已证明内容，可写有限展望，但不能引入新发现

## References

- `references/corpus-patterns.md`: 五篇中文工科样本提炼出的结构与表达共性
- `references/review-rubric.md`: 审查量表、严重度定义、常见硬伤
- `references/polish-rules.md`: 投稿级中文润色规则与禁区
- `references/output-templates.md`: 审查报告与润色交付模板
