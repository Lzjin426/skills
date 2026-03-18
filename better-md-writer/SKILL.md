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

### 6. Build the structure before filling the prose

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

### 7. Draft section by section

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

### 8. Apply Markdown rules

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

### 9. Write compactly, but not vaguely

Keep the document tight:
- Remove repetitive explanations.
- Avoid loose transitions and padding sentences.
- Keep adjacent related content close together.

Compactness must not remove definitions, assumptions, criteria, evidence, steps, interfaces, edge cases, or decisions that the reader depends on.

### 10. Plan and produce illustrations

**Skip illustrations entirely when any of these apply:**
- The document is under ~80 lines and consists of pure text explanation, configuration notes, or checklists.
- The document type rarely benefits from images: changelog, API reference, config doc, release notes, commit convention, short internal memo.
- The core content carrier is code blocks or tables, with text serving only as glue.
- The user explicitly says no images are needed.

When any condition above is met, skip the collect/mark/produce workflow below. Do not evaluate illustrations section by section.

For all other documents, every image must answer one question: would the reader understand this section faster with the image than without it? If the answer is "about the same", do not add the image.

**Choose the image type by what it represents:**

| Use web images | Use `excalidraw-diagram` | Use `obsidian-canvas-creator` |
|---|---|---|
| Real products, devices, UI screenshots | Free-form sketches, rough concepts, visual brainstorming | Knowledge maps, note relationships, idea networks |
| Locations, scenes, environment photos | Architecture diagrams, flowcharts, process stages | Zettelkasten-style connections, concept clusters |
| Style or mood references | Comparison maps, decision trees, dependency graphs | Hierarchical note structures, document organization |
| Existing data visualizations or chart screenshots | System topology, layered structures, feedback loops | Bidirectional linking visualization, tag networks |

Rule of thumb:
- If the image shows a **real, concrete thing** → search web images
- If the diagram explains **concepts, structures, flows, or relationships** → use `excalidraw-diagram`
- If the diagram visualizes **knowledge relationships or note connections** → use `obsidian-canvas-creator`

**Three-phase illustration workflow:**

1. **Collect phase** (during step 3, source material gathering): when useful reference images appear during research, save the link or path immediately. Do not interrupt the research flow to process them.
2. **Mark phase** (during step 7, section drafting): at each position that needs an image, insert a placeholder comment noting the image type and a short description, for example:
   - `<!-- IMG: excalidraw-diagram — deployment flow with rollback branch -->`
   - `<!-- IMG: obsidian-canvas-creator — concept map linking related notes -->`
   - `<!-- IMG: web — screenshot of the dashboard settings panel -->`
3. **Produce phase** (after the draft structure is stable): process all placeholders in batch. Search web images and generate diagrams with the appropriate skill (`excalidraw-diagram` or `obsidian-canvas-creator`) together, then insert them into the document.

**Quantity guidance:**
- Not every section needs an image. Images should earn their place by reducing reading cost.
- For a typical 200–300 line document, roughly 2–5 images is usually sufficient.
- Too many images fragment reading rhythm, just like too many headings.
- Diminishing returns apply: prefer one clear image over several overlapping ones.

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
- Use for diagrams needing hand-drawn aesthetics or custom layouts.
- Prefer when the visual style should feel informal or sketch-like.
- Suitable for flowcharts, architecture diagrams, process stages, and system topology.
- Keep elements aligned enough to read clearly, but loose enough to feel organic.

*`obsidian-canvas-creator` specific:*
- Use when visualizing relationships between notes, concepts, or ideas.
- Keep node labels concise; use the Markdown document for detailed explanations.
- Leverage bidirectional linking to show connection strength and direction.

### 11. Run a reader-oriented check before finishing

Before finalizing, test whether the document works for a reader who does not share the author's context.

Check at least these questions:
- Can the reader identify the purpose quickly?
- Are key terms, assumptions, and decisions defined where needed?
- Would a new reader know what to do next?
- Is anything relying on unstated background knowledge?
- Is any section generic filler that carries no real information?
- Is the document actually advancing understanding, or only placing information into boxes?
- Does the primary expression carrier fit the job, or is the document over-fragmented?

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
- Illustrations were either deliberately planned or deliberately skipped, not overlooked.
- The document can survive a reader-oriented check without relying on hidden context.
