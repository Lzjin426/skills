---
name: knowledge-doc-writer
description: Research and write Chinese knowledge-base documents for technical, scientific, academic, product, or conceptual topics. Use when the user wants a readable beginner-to-intermediate learning article, encyclopedia-style reference, tutorial-style concept document, Feishu knowledge-base draft, or a rewrite of AI-like fragmented notes into a complete reliable document with sources, diagrams, formulas, examples, and visual planning.
---

# Knowledge Doc Writer

## Core Intent

Write knowledge-base documents that a serious beginner or intermediate learner can actually learn from. Favor coherent explanation, source-backed accuracy, concept boundaries, examples, and useful visuals over generic summaries or many shallow headings.

The default output language is Chinese unless the user asks otherwise.

## Workflow

1. Clarify only if the missing answer changes the document shape: target audience, output location, document length, public/private use, or required format.
2. Research first unless the user explicitly forbids browsing or supplies enough source material. Read `references/research-workflow.md`.
3. Build a source inventory and identify 2-4 good structure/visual references. Learn from their organization and explanation strategy; do not copy their prose.
4. Choose an article shape from `references/article-structure.md`. Make fewer, deeper sections instead of many shallow ones.
5. Plan visuals before drafting. Read `references/visual-policy.md` when using external images, screenshots, diagrams, formulas, Mermaid, SVG, or Feishu media.
6. Draft in a knowledge-base style. Read `references/style-and-anti-ai.md` before long-form writing or rewriting.
7. Run quality review using `references/quality-rubric.md`. For Markdown drafts, optionally run `scripts/outline_lint.py`.
8. If the user asks to create or update a Feishu document, switch to the relevant Lark skill after the draft is ready. Ask before writing to Feishu unless the user already requested creation/update.

## Hard Rules

- Start from the real learning problem: what question does this concept answer, what was impossible or awkward before it existed, and where it fits.
- Do not make a pile of H2 headings with 2-3 lines under each. Merge sections until each section teaches one complete idea.
- Terminology, formulas, and English names are allowed. Introduce them with context and use them consistently.
- Use examples to carry abstraction. A good document often keeps one running example through several sections.
- Include source links or a source inventory for every substantial article.
- Prefer self-drawn diagrams for process, structure, comparison, and mechanism explanations.
- Do not directly embed ordinary web images by default. External images require source, author when available, license/permission status, and modification notes. If permission is unclear, link, paraphrase, or redraw.
- Separate facts from interpretation. Mark uncertain claims and current facts that may change.
- Avoid AI writing habits: generic transitions, symmetrical but empty lists, slogan-like conclusions, excessive bullets, and shallow "what/why/how/applications" templates.

## Simplicity and Concrete Explanation Rules

Use these rules especially when the user is a beginner, says they do not understand, asks for a simpler explanation, or complains that prior explanations were too abstract.

- Prefer **simple, concrete language** over formal or abstract phrasing. If a sentence sounds like it belongs in a textbook but not in a conversation with a beginner, rewrite it.
- Explain abstract ideas through **one small concrete example first**, then name the concept. Do not start with a dense definition when an example can carry the idea.
- Use the pattern: **plain sentence → tiny example → formal term**. Example: "去了又回来，就是一个完整循环。比如 `0 → 10 → 0`。在疲劳分析里，这叫一个完整循环。"
- Avoid unexplained phrases such as "机制", "本质", "映射", "状态空间", "闭合路径", "等效", "统计特性", "物理意义". If they are necessary, immediately translate them into everyday language.
- For formulas, first say what the formula is trying to calculate, then show the formula, then explain each symbol with a number example. Never leave a formula without a concrete interpretation.
- When teaching an algorithm, do not only describe rules. Walk through a **tiny sequence that fits in one line**, such as `0 → 10 → 0` or `0 → 100 → 60 → 100 → 0`.
- When a reader is confused, reduce scope instead of adding more branches. Teach the minimum working picture before mentioning exceptions, variants, standards, or edge cases.
- Prefer "你可以先这样记" summaries for early learning. Put caveats after the basic intuition is stable.
- If a section contains two consecutive abstract paragraphs, insert a concrete example, analogy, table, or diagram before continuing.
- The final draft should pass this beginner check: a reader should be able to answer "这个概念在解决什么问题？输入是什么？输出是什么？最小例子是什么？" without rereading the whole article.

## Output Modes

- **Planning mode**: source inventory, article outline, visual plan, and quality risks.
- **Draft mode**: complete article with references and visual placeholders or embedded diagrams.
- **Rewrite mode**: turn notes/AI draft into a coherent knowledge-base document while preserving factual content.
- **Feishu mode**: after drafting, use Lark document skills to create/update a Feishu doc when requested.

## Reference Routing

- Read `references/research-workflow.md` for web research, source selection, source inventory, and how to use good articles as references without copying them.
- Read `references/article-structure.md` for structure patterns and section design.
- Read `references/style-and-anti-ai.md` for prose rules and AI-writing cleanup.
- Read `references/visual-policy.md` for diagrams, image reuse, attribution, and visual planning.
- Read `references/quality-rubric.md` for final evaluation and acceptance criteria.

## Useful Command

For Markdown drafts:

```bash
python3 /Users/fullstop/.agents/skills/knowledge-doc-writer/scripts/outline_lint.py draft.md
```
