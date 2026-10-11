# Article Structure

Use this file to design the document before drafting.

## Core Shape

Use the following teaching moves to build a serious reference note. They describe the learning route, not mandatory section names:

1. Lead: what it is, what problem it solves, where it is used.
2. Context: why the concept exists and what older/simple approach fails.
3. Core mechanism: the smallest working mental model.
4. Formal definition: terms, notation, formulas, or data structures.
5. Worked example: one concrete example carried through the explanation.
6. Variants or extensions: only after the core is stable.
7. Applications and limitations: where it works, where it does not.
8. Implementation or practical use: code, steps, tools, or workflow when relevant.
9. Misconceptions and further reading.

Do not force every article to use every item. Choose what the concept needs.

## Good Lead

The lead should stand alone. It should answer:

- What is this?
- What does it help us do?
- What is the key idea in plain language?
- What terms will the reader see later?

Bad lead: "This article will introduce X from definition, features, applications..."  
Good lead: "X is a way to solve Y when Z breaks. Its key move is..."

## Section Design

Each major section should teach one complete idea. A section is probably too shallow if:

- It names an idea without explaining the relationship, operation or distinction needed for the learning task.
- It only defines a term and immediately moves on.
- It could be merged into the previous section without losing meaning.

For Fullstop's notes, use numbered H1 chapters, H2 subchapters, and H3 for deeper topics only when needed. Use the filename or page title as the document name. Keep heading levels continuous and numbering consistent. A different destination's explicit convention can override this default.

Headings name the subject or purpose concisely; the paragraphs carry the explanation. Prefer “基本概念”, “更新原理”, “计算示例”, “学习率对比”, and “适用条件” to “从求导走到找一个更好的位置” or “自己做一次，再检查理解有没有断点”. Short headings are not evidence of shallow teaching.

## Structure Patterns

### Concept or Theory

- Problem background
- Intuitive explanation
- Formal definition
- Example
- Properties
- Applications
- Misconceptions

### Algorithm

- What problem it solves
- Search/optimization/state space intuition
- Data representation
- Step-by-step process
- Worked example
- Complexity and parameters
- Failure modes and variants
- Implementation notes

### Model or Architecture

- Why previous approach fails
- Input/output and representation
- Core operation
- Training/inference flow
- Visualization of data flow
- Strengths, limitations, and use cases
- Minimal code or pseudo-code

### Tool or Library

- When to use it
- Mental model
- Installation/setup only if needed
- Core workflow
- Practical examples
- Configuration and pitfalls
- Links to official docs

### Paper or Method Review

- Problem and prior limitation
- Main contribution
- Method
- Experiment/evidence
- Limitations
- How to use or extend it

## Depth Allocation

Spend words where understanding usually breaks:

- Representation changes: real-world object to vector/matrix/tree/graph/state.
- Boundary conditions: when the definition does not apply.
- Hidden assumptions: independence, differentiability, stationarity, linearity, distribution.
- Operators: what operation changes what object.
- Evaluation: how we know the result is good.

Skip or compress:

- Historical trivia unless it explains the concept.
- Exhaustive application lists.
- Repeated definitions after the term is stable.
- Generic benefits that apply to almost every method.

## Outline Test

Before drafting, check two things separately: whether the chapter order supports understanding, and whether the titles are short, formal, and easy to locate in an outline.

For example, a gradient-descent note might use:

- `# 1. 基本概念`, with `## 1.1 目标函数与梯度` and `## 1.2 更新规则`.
- `# 2. 计算示例`.
- `# 3. 学习率对比`, with subchapters for convergence and divergence where useful.
- `# 4. 适用条件`.
- `# 5. 练习与参考`.

This is an example, not a required skeleton or chapter count. “概念、举例、对比” can be excellent headings when their contents form a connected explanation. A mechanically filled list of definitions and advantages remains weak regardless of how elaborate the titles sound.
