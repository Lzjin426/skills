# Visual Policy

Use this file whenever the article needs images, diagrams, screenshots, formulas, or visual assets.

## Visual Types

Use visuals for jobs text does poorly:

- Mechanism diagram: how information or state moves.
- Structure diagram: components and relationships.
- Transformation diagram: before/after representation.
- Flowchart: process or algorithm steps.
- Comparison table: stable differences between methods.
- Heatmap or matrix: weights, similarity, transitions, attention, correlations.
- Timeline: historical development only when history matters.
- Screenshot: tool workflow, UI, or code output.

Do not add decorative images.

## Visual Plan

Before drafting, make a small plan:

| Section | Visual | Purpose | Source | Reuse status |
| --- | --- | --- | --- | --- |

`Source` can be self-drawn, Mermaid, SVG, screenshot, official image, Wikimedia, paper figure, or external article image.

## External Image Rules

Default: prefer self-drawn diagrams or redrawn explanatory figures.

Use an external image only when one condition is true:

- It has a clear license that allows the intended use.
- It is from official docs or a paper and the document will cite/link it in a context that allows use.
- The user explicitly says the output is private personal notes and accepts the risk.
- The image is linked as a reference rather than embedded.

For each embedded external image, record:

- Title or description.
- Author or organization when available.
- Source URL.
- License or permission status.
- Whether modified.
- Access date.

Use a TASL-style note when possible: Title, Author, Source, License.

If license is unclear, do not embed by default. Link, summarize, or redraw.

## Redrawing

Redraw when the source image teaches a useful structure but its license is unclear. Do not trace exact layout or copy distinctive styling. Change the structure enough that the new diagram expresses your own explanation.

Good redraw targets:

- Process diagrams.
- Concept maps.
- Data-flow diagrams.
- Simple architecture diagrams.
- Toy examples.

Bad redraw targets:

- Photographs.
- Complex original illustrations.
- Proprietary UI screenshots.
- Experimental figures where the exact image is the evidence.

## Diagram Format

Use Mermaid for simple flowcharts and state diagrams. Use SVG for precise visual explanation, matrices, comparison layouts, or when the diagram needs careful labels.

For Feishu documents, use formats supported by the active Lark skill. When in doubt, create a local image/SVG and insert it through the document media workflow after user approval.

## Diagram Quality

A good diagram:

- Has one main message.
- Uses labels that match article terminology.
- Can be understood at mobile width if possible.
- Is introduced before it appears.
- Is interpreted after it appears.

Avoid:

- Too many colors.
- Tiny labels.
- Generic icons.
- Flow arrows without meaning.
- A diagram that duplicates a paragraph without adding structure.
