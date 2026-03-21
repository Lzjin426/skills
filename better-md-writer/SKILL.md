---
name: better-md-writer
description: Write, rewrite, and polish documents when the user needs to write documentation. Trigger whenever the user wants to write a document, including notes, knowledge-base pages, README/wiki content, guides, specs, proposals, RFCs, decision docs, technical documentation, or other structured written material. Help clarify purpose, audience, structure, Markdown form, diagrams, and revision workflow so the result is clear, audience-aware, and easy to review.
---

# Better Md Writer

Write documents with a unified workflow: clarify purpose first, then decide structure, expression form, and level of detail. Use standard Markdown syntax by default.

Before drafting:
- Read [references/markdown-style.md](references/markdown-style.md) for Markdown layout rules.
- Read [references/document-intent.md](references/document-intent.md) when the user's purpose, audience, output shape, or document tone is unclear.

After completing the document:
- Open the document with **Obsidian** as the default reader. Use the `obsidian` CLI command or the Obsidian URI scheme to open files directly in the user's vault.

## Terminology

Keep the workflow platform-neutral unless the user explicitly wants platform-specific wording.

Use neutral terms such as:
- `assistant` or `agent` instead of a platform brand name.
- `sub-agent` or `fresh agent session` instead of a vendor-specific testing term.
- `available tools`, `integrations`, or `MCP tools` instead of platform-specific connector names.

If the surrounding environment clearly uses names such as Codex or Claude Code, mirror that wording locally in the output, but keep the underlying instructions generic and portable.

## Workflow

### 1. Clarify the document's job first

If the user has not made the writing goal clear, ask the minimum questions needed to determine:
- Who the document is for.
- What the document is used for.
- What the reader should understand, decide, or do after reading it.
- Whether there are format, length, tone, or template constraints.
- Whether the document needs comparison, explanation, steps, argumentation, evidence, or appendices.

Do not start by forcing the document into a preset category. Let purpose drive structure and tone.

### 2. Gather only the context that changes the draft

Step 1 established the writing goal. Now check whether anything is still missing that would change the structure or wording:
- Is there a required template, section order, or output constraint?
- What background, assumptions, dependencies, or trade-offs are easy to miss?
- Are there related documents, prior decisions, or ongoing discussions the draft should reference?

Ask only for the missing pieces. Do not re-ask questions already answered in step 1, and do not turn every writing task into a heavyweight intake interview.

### 3. Collect and handle source material

Before drafting, decide the research level, gather material, and integrate it properly.

**Research decision — three levels:**

| Level | When to use | What to do |
|---|---|---|
| **Skip** | Content is entirely from the user's first-hand information (meeting notes, personal summaries), or the document is a pure record (changelog, release notes, config steps the user already provided in full) | Do not search. Work directly from user-supplied material. |
| **Light (default)** | Most documents. Unless a skip or deep signal is present, default here. | Do one round of web research to confirm terminology, check current best practices, and gather background data or examples. Keep it brief — the goal is validation and enrichment, not exhaustive coverage. |
| **Deep** | The document compares options or makes a technical choice; it needs data, benchmarks, or authoritative sources; the topic changes rapidly (latest versions, recent policies); or the user explicitly asks to research. | Run a thorough search. Summarize findings, cite sources, and flag where information is uncertain or conflicting. |

When in doubt between skip and light, choose light. When in doubt between light and deep, ask the user.

**Handling the material you collect:**

**When the user provides only a topic, no material:**
- Ask whether existing materials are available (documents, links, notes), then proceed to the appropriate research level.
- Define what the search should fill: missing facts, data points, terminology, or context.
- Digest search results into the document's own voice. Do not paste raw findings.

**When the user provides scattered material (chat logs, meeting notes, bullet points):**
- Extract the core information points and confirm them with the user.
- Identify gaps in the material (missing conclusions, data, context) and ask targeted follow-ups.
- Preserve the user's key judgments and opinions. Do not wash out the original perspective during restructuring.

**When the document needs citations or evidence:**
- Distinguish between documents that need source attribution and those that do not.
- Prefer inline links for most documents. Use footnotes or a references section for formal writing.
- Verify factual claims when possible. Flag uncertain claims explicitly.

### 4. Set the writing parameters from the user's need

Adjust the draft along these dimensions:
- Conclusion-first or exploration-first
- Concise or comprehensive
- Informative, persuasive, or execution-oriented
- Long-term reusable or task-specific
- Text-first or diagram-assisted

Use the answers to shape the document. Do not assume the same structure for every report, guide, or note.

Additionally, calibrate tone and style along four dimensions:

| Dimension | Low end | High end |
|---|---|---|
| **Formality** | Conversational, brief, omits background | Formal, complete sentences, states premises |
| **Term density** | Plain language, avoids jargon | Uses specialist terms, assumes reader knowledge |
| **Explanation depth** | Conclusions and key points only | Explains from principles, lays out reasoning chain |
| **Stance** | Direct, assertive | Hedged, balanced |

Common defaults by scenario:
- **Internal team memo**: conversational + high term density + key points only + direct
- **Proposal for leadership**: formal + moderate terms + conclusion-first with rationale + moderately hedged
- **Public README/Wiki**: medium formality + low term density (or defines terms) + explains from principles + direct
- **SOP/runbook**: impersonal, step-driven + high term density + no background explanation + assertive

Use these defaults as a starting point. Only ask the user about tone when the scenario is ambiguous.

### 5. Choose the primary expression carrier

Before drafting, decide what should carry the reader's understanding:
- `paragraph-led` when the document needs explanation, interpretation, conceptual buildup, or a continuous reasoning chain
- `table-led` when the core task is horizontal comparison
- `diagram-led` when the core task is understanding structure, flow, layering, or relationships
- `list-led` only when the core task is enumeration, steps, checklists, or short parallel points
- `mixed, paragraph-dominant` for most research, explanation, and analysis documents

Do not let lists replace explanation. Do not let tables replace judgment. Do not let diagrams replace definitions the reader still needs in prose.

### 6. Design the cognitive path

Before arranging sections, decide how the reader's understanding should build. A document is not a collection of topics placed side by side — it is a guided journey from not-knowing to knowing.

**6a. Extract the anchor concept**

Find the single mental model that, once understood, makes every detail in the document click into place.

- Ask: "If the reader can only remember one thing after closing this document, what should it be?"
- The anchor is not a summary sentence. It is a structural idea — a framework, a metaphor, a diagram, a distinction — that the reader can use to derive or recall the rest.
- State the anchor explicitly in the document. Mark its special status so the reader knows to hold onto it (e.g., "If you only remember one thing, remember this", or "This is the key that unlocks everything below").

Examples of good anchors:
- "Git has three spaces; almost every command moves data between them" (a structural model)
- "React shifts your thinking from 'change the DOM' to 'describe the UI'" (a paradigm distinction)
- "The entire authentication flow is a state machine with four states" (a framework)

If the document is short or purely procedural (runbook, changelog, config steps), the anchor may be implicit or unnecessary. But for any document that teaches, explains, or analyzes, the anchor must exist and be explicit.

**6b. Design the cognitive arc**

Plan the reading experience as a trajectory, not a flat outline:

1. **Orient** — Give the reader a panoramic view before any detail. What is the territory? What will they understand by the end? The anchor concept often appears here.
2. **Build** — Introduce concepts in dependency order. Each section should answer a question raised (explicitly or implicitly) by the previous section. The reader should feel momentum, not topic-switching.
3. **Close** — Return to the panoramic view. Now the reader can see everything they learned mapped back onto the opening frame. This callback is what turns information into understanding.

Do not confuse the cognitive arc with a rigid template. The three phases can overlap. A long document may have nested arcs within major parts. The point is intentional trajectory, not a formula.

**6c. Plan inter-section progression**

For each pair of adjacent sections, write down in your outline:
- What question does this section answer?
- Why does this question arise naturally from the previous section?
- What new question does this section leave, which the next section will pick up?

If a section can be moved to a different position without the reader noticing, the progression is too weak. Strengthen it by adding a bridging insight or reordering.

### 7. Build the structure before filling the prose

Start from the section layout, not from sentence-level polishing.

When the structure is unclear:
- Propose a compact outline.
- Start with the section that carries the main value, the main uncertainty, or the main decision.
- Leave summaries and introductions until the core is stable.

When refining an existing document:
- Preserve the useful structure.
- Replace only the sections that are weak, unclear, or too loose.

For long documents, apply these structural rules:

**When to split into multiple documents:**
- Consider splitting when a single document exceeds roughly 500 lines or contains 2 or more independently readable topics.
- Each resulting document should be self-contained, not dependent on reading other parts first.
- Use an index document to connect a document series.

**Cross-referencing between documents:**
- Use relative links to reference sibling documents.
- Include a one-sentence description of what the linked document covers. Do not leave bare links.
- Avoid circular dependencies between documents.

**Navigation aids:**
- In long documents, consider adding a "back to top" anchor at the end of major sections.
- Open each major section with one sentence stating the problem or question it addresses.

### 8. Draft section by section

Decide the structure before writing:
- Use headings for independent modules, clear sections, or content that will likely expand.
- Use lists for parallel points, short steps, or compact grouped information.
- Use a short paragraph when one small block is enough.
- Use tables for cross-option comparison.
- Use diagrams for flows, layers, relationships, and route maps.
- Use paragraphs as the default carrier for explanation-heavy writing.

For high-uncertainty sections, refine in this order:
- Ask a few targeted clarifying questions.
- Offer candidate angles, points, or section contents when needed.
- Draft the section.
- Iterate with focused edits instead of rewriting the whole document each time.

Do not create headings only to make the document look formal. If a heading would contain only a tiny amount of content, collapse it into a list item or paragraph.

For research, explanation, and principle-heavy writing, each major section should usually begin with a continuous orienting paragraph before lists or tables appear.

**Connecting sections to the cognitive path (from step 6):**

- Each major section should open by connecting to what came before — why this topic matters now, what question it answers, or what gap it fills. Do not drop the reader into a new topic without a bridge.
- If the document has an anchor concept (step 6a), refer back to it when introducing new material. The reader should see how each new idea relates to the central model, not just to the previous section.
- End major sections with a forward-pointing hook when natural — a question raised, a gap acknowledged, or a preview of what comes next. This creates momentum rather than a sequence of standalone blocks.

**Using analogies and metaphors:**

- A good analogy maps precisely to the technical concept. Every element in the analogy should correspond to something real. If parts of the analogy do not map, either trim the analogy or acknowledge the limits.
- Avoid "atmosphere analogies" that sound approachable but do not actually help the reader think. "It's like building a house" is too vague. "The staging area is like a packing table — you lay out exactly which items go into the box before sealing it" is precise.
- One strong, well-developed analogy per major concept is better than scattered metaphors. Let the analogy do real work, then move on.
- If the document has a technical audience that does not need analogies, skip them. Analogies are teaching tools, not decoration.

### 9. Apply Markdown rules

See [markdown-style.md](references/markdown-style.md) for the complete reference.

**Structure:**
- **Headings**: External title ≠ in-body hierarchy. Start with `# 1. Section`. Use numbered headings (`# 1.`, `## 1.1`, `### 1.1.1`) when hierarchy is needed.
- **Top-level separators**: After every top-level section, add a horizontal rule `---` before the next top-level section. Treat this as a hard rule for this skill, including shorter documents.
- **Spacing**: Use blank lines only at paragraph ends, module switches, or semantic changes. Do not insert empty lines mechanically.
- **Elements**: Choose appropriately between headings, lists, and paragraphs based on content function.

**Inline syntax and assets:**
- Use fenced code blocks with language tags (`bash`, `python`, `json`, `text`). Group similar commands together.
- Use `**bold**` for key terms and warnings, `*italic*` for first-use terms, `` `inline code` `` for technical strings.
- Use relative paths for internal links, `[text](URL)` for external links.
- Store images in resource directories, use lowercase kebab-case filenames, add alt text when helpful.

### 10. Write compactly, but not vaguely

Keep the document tight:
- Remove repetitive explanations.
- Avoid loose transitions and padding sentences.
- Keep adjacent related content close together.

Compactness must not remove definitions, assumptions, criteria, evidence, steps, interfaces, edge cases, or decisions that the reader depends on.

### 11. Plan and produce illustrations

**Default: illustrations are expected.** For any document that teaches, explains, analyzes, or compares, plan illustrations proactively as part of the drafting process. Do not wait for the user to ask. A well-placed diagram often does more work than three paragraphs of prose.

**Mandatory illustration triggers — always produce at least one diagram when any of these apply:**
- The document has an anchor concept (step 6a) — the anchor almost always deserves a visual representation. If the reader can "see" the model, it sticks.
- The document has an orient phase (step 6b) — the panoramic opening view is a natural candidate for a diagram.
- The document explains a process, flow, lifecycle, or multi-step sequence.
- The document compares options, layers, or architectures.
- The document describes relationships, dependencies, or hierarchies.

**Skip illustrations only when ALL of these apply:**
- The document is under ~80 lines, AND
- The document type is inherently text-and-code (changelog, API reference, config doc, release notes, commit convention, runbook, short internal memo), AND
- The user has not asked for images.

If you are unsure whether to include illustrations, include them. It is easier to remove an unnecessary diagram than to retroactively realize the document needed one.

**Choose the image type by what it represents:**

| Use web images | Use `excalidraw-diagram` (default) | Use `obsidian-canvas-creator` |
|---|---|---|
| Real products, devices, UI screenshots | Free-form sketches, rough concepts, visual brainstorming | Knowledge maps, note relationships, idea networks |
| Locations, scenes, environment photos | Architecture diagrams, flowcharts, process stages, sequence diagrams, structural views | Zettelkasten-style connections, concept clusters |
| Style or mood references | Comparison maps, decision trees, dependency graphs | Hierarchical note structures, document organization |
| Existing data visualizations or chart screenshots | System topology, layered structures, feedback loops | Bidirectional linking visualization, tag networks |

Rule of thumb:
- If the image shows a **real, concrete thing** → search web images
- If the diagram explains **concepts, structures, flows, or relationships** → use `excalidraw-diagram`
- If the diagram visualizes **knowledge relationships or note connections** → use `obsidian-canvas-creator`

**Three-phase illustration workflow:**

1. **Collect phase** (during step 3, source material gathering): when useful reference images appear during research, save the link or path immediately. Do not interrupt the research flow to process them.
2. **Mark phase** (during step 8, section drafting): at each position that needs an image, insert a placeholder comment noting the image type and a short description, for example:
   - `<!-- IMG: excalidraw-diagram — deployment flow with rollback branch -->`
   - `<!-- IMG: excalidraw-diagram — request lifecycle overview -->`
   - `<!-- IMG: obsidian-canvas-creator — concept map linking related notes -->`
   - `<!-- IMG: web — screenshot of the dashboard settings panel -->`
3. **Produce phase** (after the draft structure is stable): process all placeholders in batch. Search web images and generate diagrams with `excalidraw-diagram` or `obsidian-canvas-creator` skill as needed, then insert them into the document.

**Quantity guidance:**
- For a teaching, explanation, or analysis document of 100–200 lines, plan at least 1–2 diagrams. For 200–400 lines, plan 3–6. These are minimums, not ceilings.
- The anchor concept diagram and the panoramic overview diagram (if the document has an orient phase) count toward this minimum but should not be the only illustrations.
- Not every section needs its own image, but a document with zero images almost always means the illustration step was skipped, not that no diagram was warranted.
- Too many images fragment reading rhythm, just like too many headings. Diminishing returns apply: prefer one clear image over several overlapping ones.

**Sub-agent delegation:**

When sub-agents are available, illustration work is naturally parallelizable:
- The main agent writes the document and produces the placeholder list.
- A sub-agent searches the web for reference images based on the placeholder descriptions.
- A sub-agent creates diagrams with `excalidraw-diagram` skill for flowcharts, architecture diagrams, and visual explanations.
- A sub-agent builds knowledge maps with `obsidian-canvas-creator` skill for note relationships and concept networks.
- The main agent reviews the results and inserts them into the final document.

If sub-agents are not available, handle the produce phase sequentially after the draft is stable.

**Diagram tool best practices:**

*General principles (all tools):*
- Keep diagrams focused on logic, not decoration.
- Make labels short and consistent with the Markdown terminology.
- Place the diagram where it reduces reading cost instead of duplicating the full text.

*`excalidraw-diagram` specific:*
- Treat this as the default diagram tool for all explanatory documents.
- Use for diagrams needing hand-drawn aesthetics or custom layouts.
- Suitable for flowcharts, architecture diagrams, process stages, sequence diagrams, system topology, and structural overviews.
- Keep elements aligned enough to read clearly, but loose enough to feel organic.

*`obsidian-canvas-creator` specific:*
- Use when visualizing relationships between notes, concepts, or ideas.
- Keep node labels concise; use the Markdown document for detailed explanations.
- Leverage bidirectional linking to show connection strength and direction.

### 12. Run a reader-oriented check before finishing

Before finalizing, test whether the document works for a reader who does not share the author's context.

Check at least these questions:
- Can the reader identify the purpose quickly?
- Are key terms, assumptions, and decisions defined where needed?
- Would a new reader know what to do next?
- Is anything relying on unstated background knowledge?
- Is any section generic filler that carries no real information?
- Is the document actually advancing understanding, or only placing information into boxes?
- Does the primary expression carrier fit the job, or is the document over-fragmented?

**Cognitive arc verification (from step 6):**

- After closing the document, what stays in the reader's head — a usable mental model, or a list of facts? If it is only facts, the anchor concept is missing or too weak.
- Does the ending connect back to the opening frame? The reader should feel closure, not a trail-off. For teaching and explanation documents, the last section should let the reader verify their own understanding against the opening panorama.
- Can any two adjacent sections be swapped without the reader noticing? If yes, the inter-section progression is too weak — add bridges or reorder.
- Are analogies precise and load-bearing, or decorative? Remove any analogy that does not help the reader think about the concept differently.

If sub-agents or fresh-agent testing are available, use them as a blind-reader check. If not, simulate the same review manually and tighten the weak sections.

## Final Check

Before finishing, verify:
- The document purpose, audience, and expected outcome are clear enough to justify the chosen structure.
- Source material was collected with a clear purpose and integrated into the document's own voice, not pasted raw.
- Tone and style match the intended audience and scenario.
- The terminology stays platform-neutral unless the user wants platform-specific wording.
- The primary expression carrier was chosen deliberately.
- The most uncertain sections were clarified before drafting.
- The structure serves the content instead of showing off structure.
- Long documents have appropriate splitting, cross-references, and navigation aids.
- Research and explanation sections are not fragmented into avoidable card-like chunks.
- Headings, lists, tables, spacing, code blocks, links, images, and emphasis follow [markdown-style.md](references/markdown-style.md) conventions.
- Illustrations were proactively planned for teaching/explanation/analysis documents. If the document has zero diagrams, confirm that ALL skip conditions are met (under 80 lines AND inherently text-and-code type AND user did not ask for images). A missing illustration in a 200+ line explanation document is a defect, not a style choice.
- The document can survive a reader-oriented check without relying on hidden context.
- For teaching, explanation, and analysis documents: an anchor concept exists and is explicitly marked; the cognitive arc has orient → build → close phases; sections have inter-section progression (not interchangeable order); the ending connects back to the opening frame.
- Analogies are precise and structurally mapped, not decorative. Any analogy that does not help the reader reason about the concept has been removed.
