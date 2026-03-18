# Better Md Writer Reference: Document Intent

Use this file when the user's request is to "write a document" but the intended use is still unclear. The goal is not to classify documents mechanically. The goal is to infer what the document needs to accomplish, then shape the writing around that need.

## 1. Ask for the Missing Purpose

If the request is underspecified, ask only the smallest set of questions that changes the draft:
- Who is the audience?
- What is the document for?
- What should the reader understand, decide, or do afterward?
- Is the document mainly for explanation, decision support, execution, archival, or persuasion?
- Are there format, length, tone, or template constraints?

Do not ask all of these if the answer is already obvious from context.

## 2. Derive Writing Parameters Instead of Forcing a Category

Infer the document's shape from a few dimensions:
- `Purpose`: explain, compare, decide, persuade, record, instruct
- `Audience familiarity`: expert, mixed, newcomer
- `Actionability`: informational, decision-supporting, execution-driving
- `Depth`: concise overview, balanced summary, full detail
- `Durability`: temporary working draft, reusable note, long-lived reference
- `Evidence load`: light rationale, comparative evidence, explicit sources and assumptions

These dimensions matter more than a rigid label such as "knowledge base" or "technical doc".

## 3. Map Purpose to Structure

Use purpose to choose the backbone:
- If the reader needs a quick answer, lead with the conclusion or summary.
- If the reader needs to understand trade-offs, include comparisons, options, and a judgment.
- If the reader needs to execute work, include prerequisites, steps, decision points, and failure handling.
- If the reader needs a durable reference, keep scope tight, naming stable, and structure easy to scan later.
- If the reader needs confidence in a claim, include method, evidence, assumptions, and limits.

One document can combine several of these. Use the minimum structure that makes the task clear.

## 4. Map Purpose to Expression Form

Choose the dominant expression form from the document's actual job:
- Use **paragraph-led writing** when the goal is to explain mechanisms, teach concepts, compare underlying ideas, or walk the reader through a reasoning chain.
- Use **table-led sections** when the goal is side-by-side comparison across stable dimensions.
- Use **diagram-led sections** when the goal is to show flow, layering, route maps, dependency structure, or spatial relationships.
- Use **list-led sections** when the goal is to enumerate items, summarize short parallel points, or present step sequences.

For most research notes, technical explanations, and route-analysis documents, default to **paragraph-dominant writing with selective tables and diagrams**.

Do not treat “clear structure” as permission to over-fragment the page. A document can be structurally clear and still read badly if every idea is broken into mini lists.

## 5. Typical Clarifying Signals

Different user intents usually imply different emphases:
- "Help me write a proposal" often needs recommendation, rationale, and trade-offs.
- "Help me write a report" often needs purpose, findings, evidence, and conclusion.
- "Help me document this system" often needs definitions, interfaces, boundaries, and operational details.
- "Help me整理成文档" often needs cleanup, structure tightening, and stronger reader orientation.
- "Help me understand X and write it down" often needs explanation first, then a reusable structure.

Treat these as signals, not strict categories.

## 6. Decide Whether the Document Needs Illustrations

Ask: would the reader understand the content meaningfully faster with an image than without one? If no section clearly benefits, skip illustrations entirely.

Quick signals that illustrations will help:
- The prose is really a hidden flowchart, architecture, or dependency map.
- A comparison depends on spatial relationships or branching that tables cannot show.
- A concrete visual example (product, UI, device) would replace a paragraph of description.

Quick signals to skip illustrations:
- The document is short (<~80 lines), a changelog, API reference, config doc, or similar text-and-code format.
- The core content carrier is already code blocks or tables.

For the full illustration workflow — image type selection, three-phase process, quantity guidance, and sub-agent delegation — see SKILL.md step 11.

## 7. Anti-Fragmentation Check

For research, explanation, analysis, and principle-heavy writing, check whether the document has become too card-like:
- Too many short lists in a row usually means missing connective prose.
- If the reader must reconstruct the logic between blocks, the document is under-explained.
- If a section contains several lists but no orienting paragraph, it probably needs a paragraph-first rewrite.
- If a table or diagram appears without a framing paragraph, the reader may not know why it matters.

Use lists to compress information, not to replace thinking.

## 8. Reader-Oriented Revision

Before finalizing, ask:
- Would the intended reader understand why this document exists?
- Is the main value obvious in the first screenful?
- Is anything important assumed but unstated?
- Does the structure match the user's goal, or just imitate a generic template?
- Can anything be removed without reducing usefulness?
- Is the document easy to follow linearly, not just easy to scan?

If tools allow, use a fresh agent or sub-agent for a blind-reader check. Otherwise, simulate the same review manually.
