# Style And Anti-AI Rules

Use this file before drafting or rewriting.

## Target Voice

Write Fullstop's knowledge-base documents as serious personal reference notes. This preference is established here; do not learn a new style from existing notes for each task.

- Clear, grounded, and patient.
- Terms are allowed; hand-holding is not the same as oversimplifying.
- The reader should know what to search next if they do not know a term.
- Prefer concrete nouns and verbs over broad claims.
- Use neutral, precise statements and short descriptive headings. Explain unfamiliar ideas simply without turning the saved document into a chat transcript, repeatedly addressing “你”, or inventing the user's experiences and opinions.
- Keep useful technical language and exact conditions. Seriousness comes from precision and organization, not obscure wording.

## Information Hierarchy

Make the purpose of information visible rather than presenting every kind of content as equal paragraphs:

| Information | Preferred treatment when useful |
| --- | --- |
| Definitions, mechanisms, derivations | Connected prose and explained formulas under short numbered headings |
| Key rule or conclusion | A concise note callout or restrained emphasis; keep it understandable when revisited |
| Applicability, exceptions, common mistakes | A clearly labeled warning or important-condition block near the affected claim |
| Worked example | A named example with inputs, steps, and result kept together |
| Exercise and reference answer | Separate the question from the solution; a collapsible answer can preserve the attempt |
| Quoted source or supplemental explanation | A blockquote with clear attribution when quoting; do not make author prose appear to be an external quotation |
| Important term or short phrase | Selective bold or highlight, not whole highlighted paragraphs |
| Code, commands, useful pseudocode | A fenced code block with an appropriate language label |

For Obsidian, use native callouts such as `> [!note] 核心结论`, `> [!warning] 适用条件`, and `> [!example]- 参考答案`; use `==...==` sparingly for highlights. Blank-line separation and the `>` prefix must preserve the block. In other destinations, use supported equivalents and check the saved rendering; do not emit Obsidian-only syntax into a renderer that cannot display it.

Choose forms from the content's purpose. Do not require a quota or every form in every article, wrap most paragraphs in callouts, or add code to a non-programming explanation merely for visual variety. The resulting note should make key conclusions and necessary conditions easy to find while keeping the main explanation coherent.

If a heading already clearly identifies an example or a condition, ordinary prose beneath it may be sufficient. Reserve callouts for information that deserves additional emphasis or separation; do not box every example and conclusion or repeat the same label in both a heading and a block. Check the whole-page rhythm, especially in short notes.

Do not number pictures or write “图1/图2” in ordinary knowledge notes. Introduce them with “下图” or descriptive names. Optional captions add conditions, source notes or meaningful simplifications rather than repeating the image title. This does not change numbered chapter headings; formal publication requirements or explicit user instructions may require figure numbering.

## Avoid AI Writing Habits

Remove these patterns:

- Many parallel headings with shallow content.
- Bullet lists where paragraphs should explain causality.
- Generic openings such as "In today's rapidly developing field..."
- Empty transitions such as "It is worth noting that", "In summary", "Furthermore" when they add no logic.
- Repeating the same sentence shape across sections.
- "What / Why / How / Applications / Future" as a default skeleton.
- Over-balanced lists where every item has the same length but little depth.
- Vague praise: powerful, important, widely used, efficient, robust, flexible, without evidence.
- Fake completeness: "comprehensive", "ultimate", "from zero to mastery" unless true.

## Paragraph Rules

A good paragraph should usually do one of:

- Define a concept and explain why the definition matters.
- Move from intuition to formalism.
- Explain a mechanism step by step.
- Compare two ideas and name the real difference.
- Work through an example.
- Warn about a misconception or boundary.

If a paragraph only names things, deepen it or turn it into a compact table.

## Terminology

When first introducing a term:

- Give Chinese name, English name, abbreviation, and symbol when useful.
- Say what role it plays, not only what it is called.
- Keep notation stable.

Example pattern:

`适应度函数（fitness function）不是一个附属指标，而是遗传算法判断候选解能否留下来的标准。它把一个候选解映射成可比较的分数。`

## Formula Style

Use formulas when they reduce ambiguity. After a formula:

- Explain every symbol that matters.
- Translate the formula into a sentence.
- Show what changes when an input changes.
- Add a small numeric or conceptual example when possible.

Do not stack formulas without interpretation.

## Examples

Prefer one running example over many unrelated examples. A running example helps readers see representation, operation, and evaluation change over time.

For algorithms, use a tiny example that can fit in the reader's head.

For ML concepts, use a simple sentence, graph, image grid, vector, or toy dataset before production-scale examples.

## Rewrite Pass

After drafting, run this pass:

1. Merge shallow sections.
2. Convert decorative bullet lists into explanatory prose.
3. Replace vague adjectives with evidence, examples, or remove them.
4. Add missing bridges between intuition, notation, and implementation.
5. Check whether the first 20% of the article gives a stable mental model.
6. Check whether each diagram is introduced before it appears and interpreted after it appears.
7. Check numbered chapter hierarchy, concise titles, and visual separation of conclusions, conditions, examples, and answers. Preserve this structure through polishing.

## Humanizer And Fidelity Pass

After assembling the article and resolving technical/visual defects, read and apply `humanizer-zh` to the full Chinese text. Its role here is to improve expression while preserving teaching value. Do not remove necessary beginner explanations to avoid “hand-holding,” deliberately disrupt calculation order, invent personal experiences, or replace precise technical terms with inaccurate synonyms.

Treat formulas, values, units, defined symbols, standard editions, conditions, exceptions, uncertainty, and claim-to-citation relationships as protected meaning. Keep a comparison baseline in context or an appropriate working copy; a separate file is not mandatory. After polishing, compare these items and the connected teaching steps against the baseline. Accept no unverified change of meaning. If a factual correction is necessary, verify it against evidence and repeat the affected technical check.

Apply polishing in coherent sections for a long document, with shared notation and a final whole-document read. Do not substitute polishing selected paragraphs for a claimed full-text pass. If `humanizer-zh` is unavailable, report that fact and use this file's rewrite rules without claiming the companion skill ran.
