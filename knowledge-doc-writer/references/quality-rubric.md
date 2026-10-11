# Quality Rubric

Use this file before final delivery.

Use the dimensions below to diagnose weaknesses. Optional scores help compare revisions but cannot replace the acceptance checks.

| Dimension | 5 means | Warning signs |
| --- | --- | --- |
| Learning path | Chapter order supports understanding and later reference | Sections lack a connected purpose despite elaborate titles |
| Accuracy | Definitions, formulas, dates, and claims are source-backed | Unsourced claims or stale facts |
| Depth | Key concepts are explained where readers usually get stuck | Necessary relationships or steps are named without explanation |
| Terminology | Terms are introduced with role and context | Terms appear without explanation |
| Examples | Examples carry abstraction and show operations | Examples are decorative or unrelated |
| Visuals | Figures reduce learning effort through useful structure, geometry, steps or comparisons | Figures add no distinct visual value, leave worthwhile relationships to imagination, or lack reuse rights |
| Source use | Evidence is sufficient for the task, attributed, and compared where scope or conflicts require it | Important claims exceed the source's scope, or material conflicts are ignored |
| Anti-AI style | Prose is coherent, specific, and non-formulaic | Bullet soup, vague praise, generic transitions |
| Note style | Short numbered headings and information hierarchy match the established personal-note style | Chatty headings, a generic tutorial voice, or conclusions and conditions buried in uniform prose |
| Boundaries | Limitations and misconceptions are clear | Article sounds universally true |
| Practical value | Reader knows how to continue learning or use the concept | Ends with a generic summary |

## Document Acceptance

For a completed substantial article, verify the relevant checks below. Planning outputs and partial drafts may be delivered with explicit gaps; do not label them complete.

- **Learning task:** the lead establishes the problem and the main route enables the agreed explanation or application. Prerequisites are taught or explicitly required. Attempt a few representative questions using the saved document; record the answer/route and supporting sections. Repair steps requiring undeclared knowledge. An agent's success checks document adequacy, not the human reader's learning.
- **Connected explanation:** formulas and terms have context; symbols, units, assumptions, operating values and design limits remain distinct. For independent calculation, verify a connected example with lookup/interpolation and convergence where needed, explaining discrepancies against a stated tolerance. Across systems, trace outputs into inputs and central feedback through an update of the same example. Do not substitute an unrelated scalar iteration or imply that supplied illustrative outputs were calculated.
- **Examples and pace:** the example demonstrates the distinction under discussion. If a special case hides it, test a small contrasting case. Essential mechanisms and results remain on the main route; optional depth does not interrupt it, and necessary conditions stay near their claims. Judge section depth by missing understanding, not paragraph length.
- **Visual explanation:** inspect every final image for correctness, usefulness and agreement with the prose, and actively assess worthwhile additions separately. Favor richer coverage when placement, changing states, mechanism steps or comparisons otherwise require mental reconstruction; do not restrict figures to facts that prose cannot express. Geometry/change needs its relevant curve or construction; physical subjects need identifiable parts and working paths when these are prerequisites. Preserve good schematics and do not replace them merely to exercise generation. Generated structures match a source-supported arrangement and label meaningful simplifications.
- **Visual quality and sources:** inspect the linked export at document width for overlap, clipping, unreadable labels and missing glyphs. Exact plots retain traceable inputs and plotting source. Qualitative generated illustrations may use PNG alone; editable sources are conditional under `visual-policy.md`. Schematic illustrations do not replace empirical evidence. External images have an established reuse basis and attribution, or remain linked references.
- **Note style and fidelity:** concise numbered H1/H2/H3 headings follow Fullstop's established style unless overridden. Ordinary notes use descriptive image references without figure numbering. Conclusions, conditions and examples are distinguishable with purposeful formatting, without quotas of callouts or highlights. Apply `humanizer-zh` when available and verify that polishing preserved facts, calculations, uncertainty, citations and teaching steps; disclose a missing companion skill.
- **Evidence and saved display:** substantial articles include references; important claims have sufficient source scope, versions and locators. Resolve attachment and cross-document links. Check formulas, images, tables and links in the target renderer when available, disclosing unverified rendering. Obsidian Excalidraw figures normally use native embeds; check both the article display and opening the drawing for editing, not just a PNG export. For a set, verify shared notation, boundaries and reading order; delivering one part does not complete the set.

## Workflow Acceptance

For collaboration tests, inspect actual handoffs and activity as well as the document. A high content score does not establish a passing workflow.

- **Roles actually ran:** complex, multi-system or multi-document work received visual assessment and outline/dependency review before full drafting; substantial illustrated work also used visual production and a separate final reviewer. Keep at most two supporting agents active. A reviewer alone, planned delegation or a user-facing test chat does not establish the intended roles.
- **Visual discretion survived the handoff:** assessment covered the explanation before final production orders. Record inclusion/omission reasons. Check whether briefs added an unjustified figure count, tool choice or universal editable/reproducible-source requirement. For physical recognition, inspect whether schematic and spatial views were compared for their teaching benefit. If a visual agent recommended generation, trace it to an actual call and inspected output, or to an explicit concrete rejection; “2D can also do it” and native embedding alone do not justify an override. Tool overrides need a concrete task, accuracy, readability, capability or user-requirement reason; uniformity alone is insufficient. Readable existing figures do not by themselves establish that the selection process was appropriate. Using every tool or image generation is not itself a passing criterion.
- **Review was independent and consequential:** the reviewer chose and attempted representative learning questions, inspected actual figures, and reported specific gaps with locations. Review checks correctness, teaching value, missing visual explanations and pace separately. Record fixes and what was rechecked; recalculation alone is insufficient.
- **Fallbacks were verified and named:** check exposed tools before claiming capability absence; distinguish permission limits from a choice to work alone. Bridge main-only image generation back to the visual agent for inspection when available. Label main-agent self-checks honestly. A document may pass its substantive checks with disclosed review limitations, but a single-agent fallback cannot pass a test requiring independent agents.

Keep this process record outside the teaching article. Report document acceptance and workflow acceptance separately, with unresolved findings and checked limitations.

A document can legitimately use only schematics when those representations fit its learning questions. Test built-in image-generation capability separately when that is the goal; distinguish generation not selected, tool invocation failed, and generated output rejected. An independent probe does not prove that the author naturally selected generation or that its own session completed that path.

`scripts/outline_lint.py` can flag structural symptoms only. A passing exit code does not establish technical accuracy, learning adequacy, image correctness, or rendered acceptance.

It allows numbered H1 chapters and checks actual heading jumps and shallow/empty sections. Advisory warnings require judgment against actual content rather than automatic restructuring.

## Representative Review Questions

Choose questions from the document's learning goal rather than running a fixed exam: explain the mechanism in one sentence; identify the parts and working path; distinguish nearby quantities in a non-special case; trace a calculation or cross-system update; identify when the result does not apply. Return the attempted answer and the supporting or missing explanation. Do not supply desired answers or a desired verdict in the review brief.

## Delivery Notes

When giving the result to the user, mention:

- What sources shaped the article.
- Any uncertainty or source conflict.
- Which external images were used and why.
- Whether the article is ready for private notes, team knowledge base, or public publishing.
- Which delegated roles actually ran and what they contributed, or why the workflow fell back to one agent.
