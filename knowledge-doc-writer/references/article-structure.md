# Article Structure

Use this file to design the document before drafting.

## Core Shape

Prefer an "encyclopedia plus tutorial" shape:

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

- It has fewer than two developed paragraphs and no example, formula, or visual.
- It only defines a term and immediately moves on.
- It could be merged into the previous section without losing meaning.

Use H2 for major learning steps. Use H3 only when a section genuinely has internal structure.

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

Before drafting, read only the headings. They should form a learning path, not a keyword list.

Weak:

- Definition
- Features
- Advantages
- Applications
- Summary

Stronger:

- Why sequential models struggle with long-distance dependencies
- Attention as direct information retrieval
- Q, K, and V: three roles from one input
- Why scaled dot-product attention needs normalization
- What attention weights reveal and what they do not prove
