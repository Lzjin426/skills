# Style And Anti-AI Rules

Use this file before drafting or rewriting.

## Target Voice

Write like a knowledgeable teacher building a reference note:

- Clear, grounded, and patient.
- Terms are allowed; hand-holding is not the same as oversimplifying.
- The reader should know what to search next if they do not know a term.
- Prefer concrete nouns and verbs over broad claims.

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
