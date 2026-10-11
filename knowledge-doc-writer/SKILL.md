---
name: knowledge-doc-writer
description: Research, write, and revise Chinese learning documents matched to what the reader needs to understand or do. Use for knowledge-base articles, unfamiliar concepts, standards and calculation-chain explanations, worked tutorials, or turning rough notes into reliable learning documents with sources and reviewed visuals.
---

# Knowledge Doc Writer

## Core Intent

Write knowledge-base documents that a serious beginner or intermediate learner can actually learn from. Favor coherent explanation, source-backed accuracy, concept boundaries, examples, and useful visuals over generic summaries or many shallow headings.

The default output language is Chinese unless the user asks otherwise. For a small conversational explanation without a requested document, use `guided-learning` directly rather than expanding it into a long article.

## Fullstop's Default Note Style

Apply this established style directly to Fullstop's knowledge-base documents. Do not search existing notes or ask for examples merely to relearn it. A new explicit user instruction or required destination format takes precedence.

- Write as a serious personal reference note: concise, precise, easy to understand, and useful to revisit. Keep explanations accessible without making headings conversational, inventing personal experiences, or addressing the reader throughout as a tutor.
- Use short descriptive Chinese headings, such as “基本概念”, “计算示例”, “参数对比”, and “适用条件”. Main chapters use numbered H1 (`# 1. 基本概念`), subchapters H2 (`## 1.1 目标函数`), and deeper topics H3 where needed. The filename or page title names the document; do not add a redundant unnumbered H1 title above the chapters. Adapt chapter names and depth to the topic rather than copying a fixed outline.
- Distinguish definitions, key conclusions, conditions, examples, and answers visually. Use restrained highlights, quotations, and purposeful callouts; code blocks only when code, commands, or pseudocode help. Read `references/style-and-anti-ai.md` for the information hierarchy and destination-specific syntax.
- Use figures to make relationships easier to see and learn. For physical objects, assess whether the reader can identify the parts, their placement, and the working surfaces before teaching an abstract model. Mathematical geometry or change usually needs curves, geometric constructions, or trajectories; a text-and-arrow flowchart does not substitute for these. Choose tools flexibly and verify the actual figures.
- Be generous with useful visuals: a figure is worthwhile when it reduces explanation effort, supports memory or makes later reference easier, even if prose could express the same facts. Actively consider missing views, steps and comparisons without imposing a figure count. Ordinary notes use descriptive image references rather than “图1/图2” numbering; captions contain only useful conditions, source notes or simplifications.

## Workflow

1. Establish the learning task and prerequisites from the request and supplied material. Apply Fullstop's established style directly; ask only when missing information changes the route. Research an authoritative backbone using `references/research-workflow.md` unless sufficient material is supplied or browsing is forbidden.
2. Plan a connected explanation using `references/learning-workflow.md` and `references/article-structure.md`. Decide document boundaries from learning questions. For a set, state the estimated count and reading order; for calculations, map dependencies before individual formulas.
3. For complex, multi-system, multi-document or substantial illustrated work, use two separate supporting roles when authorized and available: visual assessment/production and outline/final review. Keep at most two supporting agents active. Read `references/agent-coordination.md` before briefing them. Obtain visual proposals and dependency review before full drafting, even if the initial outline has no images. The main agent owns narrative and inclusion; the visual agent proposes tools and layouts. Approve teaching purposes without adding blanket figure-count, tool or editable-source requirements.
4. Draft the main learning route and produce stable figures alongside it. Read `references/visual-policy.md` before visual work and apply its common quality checks and conditional source requirements. Results-dependent figures wait for verified calculations. Resolve technical and visual findings before applying `humanizer-zh` to the assembled text, then check factual fidelity.
5. Review the saved document using `references/quality-rubric.md`. The independent reviewer attempts representative learning questions and inspects actual final images; repair findings and recheck affected parts. Record document acceptance and workflow acceptance separately. Verify links, formulas, tables and images in the target renderer when available; disclose unchecked rendering or unavailable capabilities. A plan or draft can carry labeled gaps; a completed document cannot hide them.
6. Deliver only to an authorized destination or applicable user/project default. Create/update Feishu only when requested, using the relevant Lark skills and verifying the saved result. Do not infer publication permission from a writing request. In Fullstop's vault, all attachments belong in `附件/` and formulas use `$...$` or standalone `$$` blocks.

## Hard Rules

- Respect effective project/session permissions and pass them accurately into handoffs. Carry existing authorization forward; when per-task code approval is still required, describe the plotting method and obtain it. This skill grants no coding, installation, publication or paid-service permission. Do not replace an essential exact plot with an unsuitable illustration to avoid resolving permission.
- Start from the real learning problem: what question does this concept answer, what was impossible or awkward before it existed, and where it fits.
- Do not fragment the explanation into many shallow sections. Each chapter or subchapter should serve a clear learning or reference purpose; short descriptive headings are welcome when the content is developed.
- Terminology, formulas, and English names are allowed. Introduce them with context and use them consistently.
- Use examples to carry abstraction. A good document often keeps one running example through several sections.
- Include source links or a source inventory for every substantial article.
- Choose the visual representation before the tool: clear schematics for relationships/steps, Python for exact curves/data, and built-in `imagegen` when appearance, spatial form or a working scene contributes to understanding. For physical recognition, compare what a spatial illustration and a schematic would each teach; a usable schematic alone does not settle that choice. Preserve effective diagrams and do not impose a tool quota. If Excalidraw is selected for an Obsidian note, embed its native drawing; this delivery rule does not favor Excalidraw over other tools. See `references/visual-policy.md` for production and conditional source requirements.
- Do not directly embed ordinary web images by default. External images require source, author when available, license/permission status, and modification notes. If permission is unclear, link, paraphrase, or redraw.
- Separate facts from interpretation. Mark uncertain claims and current facts that may change.
- Avoid AI writing habits: generic transitions, symmetrical but empty lists, slogan-like conclusions, excessive bullets, and shallow "what/why/how/applications" templates.

## Explanation And Pace

- Use concrete language and introduce necessary terms with their role. Explain the object and problem before expecting a reader to interpret a model.
- Keep the mechanism, essential equations and a connected example on the main route. Explain symbols, units and applicable conditions; a shared example can interpret a related group of formulas without repeating a numerical demonstration for each symbol.
- Spend detail where understanding is likely to break. Put optional derivations and side branches in clearly marked supplements when helpful; keep essential conditions near their claims and consolidate repeated general warnings.
- Choose examples that expose the distinction being taught. If a convenient special case hides it, add a small contrasting case. Algorithms need observable steps, not just a list of rules.
- Use a figure, table, analogy or callout because it resolves a specific difficulty, not at a fixed interval. Judge depth by what the reader can explain or do, not paragraph counts or uniform section lengths.

## Output Modes

- **Planning mode**: learning outcome, scope, one-document or multi-document plan, source inventory, connected outline, visual plan, and quality risks. Do not execute image generation or publish a document merely to plan it.
- **Draft mode**: article with references and reviewed figures, or explicitly labeled missing assets and unresolved points. A draft with placeholders is not a completed illustrated document.
- **Rewrite mode**: turn notes/AI draft into a coherent knowledge-base document while preserving factual content.
- **Feishu mode**: after drafting, use Lark document skills to create/update a Feishu doc when requested.

## Reference Routing

- Read `references/learning-workflow.md` for learning depth, document count and reading order, prerequisite repair, standards/calculation teaching, and task-based acceptance.
- Read `references/agent-coordination.md` for role boundaries, handoffs, concurrency, and tool-unavailable fallbacks.
- Read `references/research-workflow.md` for web research, source selection, source inventory, and how to use good articles as references without copying them.
- Read `references/article-structure.md` for structure patterns and section design.
- Read `references/style-and-anti-ai.md` for prose rules and AI-writing cleanup.
- Read `references/visual-policy.md` for diagrams, image reuse, attribution, and visual planning.
- Read `references/quality-rubric.md` for final evaluation and acceptance criteria.

## Useful Command

For Markdown drafts:

```bash
python3 /Users/fullstop/.skillsbase/skills/knowledge-doc-writer/scripts/outline_lint.py draft.md
```

The linter allows numbered H1 chapters and checks heading jumps, empty or shallow sections, and other structural symptoms. Advisory warnings require judgment against actual hierarchy and substance; do not restructure a sound note merely to silence them.
