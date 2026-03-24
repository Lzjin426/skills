---
name: zh-lit-review-citation
description: Rewrite and strengthen Chinese engineering-paper literature reviews and in-paragraph citations for already-drafted manuscripts. Use when revising introductions, related work, research-status sections, method-motivation paragraphs, experiment-baseline paragraphs, or checking where/how many references to cite in Chinese academic writing, especially methods-plus-experiments papers. Classify the paragraph type first, then rewrite only with evidence-backed citations from the user's existing bibliography; never invent references.
---

# Zh Lit Review Citation

先判断任务属于哪一类，再决定引用密度和句内位置。不要把所有段落都写成“高密度综述段”，也不要把整段只在句末补一个大括号式引用。

## Workflow

1. 识别输入材料

- 优先读取用户已有稿件、参考文献表、文献管理导出、已给出的 PDF/Markdown 论文。
- 如果只有草稿、没有可用参考文献，停止改写，只输出“缺文献支撑点清单”。
- 严禁补造不存在的文献、作者、年份、卷期页码。

2. 判断段落类型

- `综述型综述段`：用于“研究现状/国内外研究进展/相关工作”主体段落。
- `方法型引言综述段`：用于方法论文引言中的“背景-路线-缺口-本文”。
- `方法章节局部补引段`：用于方法原理、经典理论、模块动机、算法来源。
- `实验章节补引段`：用于基线模型、数据集、评价指标、对比设置。
- `本文贡献/结论段`：默认不做高密度补引，除非句子明确在复述外部工作。

3. 建立证据表

对每个待写句子，先在心里建立一张简表：

- 这句话是不是事实判断、现状判断、性能判断、路线分类、代表工作描述？
- 这句话的证据来自哪几篇已有文献？
- 这句话是不是作者自己的设计、实验结果、总结判断？

只有前两类需要外部引用。第三类通常不引。

4. 按段落类型改写

- 综述型综述段：先总述，再分型，再点代表工作，再收束到瓶颈。
- 方法型引言综述段：先背景与任务价值，再写已有路线，再写关键不足，最后自然过渡到“本文”。
- 方法章节局部补引段：只给理论来源、对比对象、设计动机补引，不要把公式推导段写成综述。
- 实验章节补引段：给基线、数据集、指标补引；对本文实验结果的分析一般不补引。

5. 校验

- 检查是否存在“明显判断但无引文”。
- 检查是否存在“整段最后一次性补引，前文多个判断无对应证据”。
- 检查是否存在“本文提出/本文设计/实验结果表明”后机械补引。
- 检查段落是否把“已有工作不足”写成空泛批评。

## Reference Guide

按需读取：

- `references/corpus-patterns.md`
作用：查看五篇中文论文抽取出的文体模式和综述结构。
- `references/citation-rules.md`
作用：查看段内引用位置、每段大致引多少、什么时候合并引用。
- `references/rewrite-workflow.md`
作用：按段落类型执行改写与终检。

## Hard Rules

- 只使用用户现有参考文献或用户明确提供的文献。
- 不把一个引用簇放在整段最后，试图覆盖整段所有判断。
- 不把“本文工作、本文实验结果、本文结论”伪装成外部文献共识。
- 不因为用户要求“多引几篇”就堆砌无关文献。
- 不把综述型文章的高密度写法直接套到方法论文的每一段。
- 遇到证据不足时，宁可删弱判断，也不要强写强引。

## Use The Audit Script

如需先做机械排查，再进行人工改写，运行：

```bash
python scripts/review_citation_audit.py path/to/draft.md
```

该脚本只做启发式排查，不能代替人工学术判断。它适合先定位：

- 疑似缺引用段
- 疑似整段末尾堆引段
- 疑似“本文句”误引段
