# Visual Policy

Use this file whenever the article needs images, diagrams, screenshots, formulas, or visual assets. Read `imagegen` before generating or editing raster illustrations.

## Visual Types

Use visuals to lower learning effort and make relationships easier to remember or revisit:

- Mechanism diagram: how information or state moves.
- Structure diagram: components and relationships.
- Transformation diagram: before/after representation.
- Flowchart: process or algorithm steps.
- Comparison table: stable differences between methods.
- Heatmap or matrix: weights, similarity, transitions, attention, correlations.
- Timeline: historical development only when history matters.
- Screenshot: tool workflow, UI, or code output.
- Function or geometric plot: slope, extrema, area, shape, or relationships between mathematical quantities.
- Trajectory or parameter comparison: how a state changes over iterations or how a parameter changes behavior.

Do not add decorative images.

## Teaching Value Before Tool Choice

For each candidate figure, identify what it makes easier to understand, remember or locate later. Fullstop prefers richer visual explanation: do not require prose to be incapable of explaining a relationship before drawing it. A diagram can usefully reinforce the same facts by showing their arrangement, sequence or contrast. Omit decoration and redundant versions that add no useful view.

When a mathematical explanation depends on geometry or change, include the relevant curves, constructions, or trajectories rather than replacing them with a workflow. For example, gradient descent benefits from showing the objective curve, slope, and update points, together with a comparison of learning-rate behavior. These jobs may share a clear multi-panel figure or use separate figures; the example does not impose a fixed count on other topics.

Actively inspect the whole explanation for worthwhile visual opportunities: component placement, transitions between states, mechanism steps, conditional comparisons and paths across systems. These are prompts for judgment, not required categories or a fixed count. Do not stop at the minimum technically necessary set; favor adding a clear, distinct view when it materially reduces mental reconstruction. A small example or table may already do that job. Revisit coverage after drafting, then apply the flexible tool preferences below.

For machinery, devices, and other physical objects, first ask whether a new reader could locate the relevant parts and working surfaces in the actual object. A circle model or process chart may explain a calculation while leaving the assembly unclear. Consider a spatial view, cutaway, or local enlargement when it would connect the object to the model. Show the chosen arrangement and its evidence; do not present one bearing mounting, material layer, or oil passage as universal. The reader should be able to relate simplified model labels to identifiable parts.

For sections about curves, extrema, parameter changes, or numerical iteration, assess those relationships again after the equations and examples are established. A qualitative envelope may teach a mechanism but does not necessarily explain the worked function. Choose a plot when it reveals the stated result, such as a peak location or a balance-point intersection. Do not invent quantitative data for a qualitative concept merely to draw a curve.

## Visual Plan

After the learning route and technical relationships are clear, make a small plan before drafting the relevant sections:

| Section and figure ID | Question the figure answers | Required relationships and exact labels | Evidence/reference | Production and dependencies | Acceptance check |
| --- | --- | --- | --- | --- | --- |

The main agent owns which figures to include and their teaching purpose. For complex, multi-system or multi-document explanations and substantial illustrated documents, obtain the visual agent's assessment before full drafting and final production briefs when delegation is authorized and available. This assessment is required even when the initial outline proposes no images; an independently justified decision to use no figures is possible, but a main-agent text-only draft does not replace assessment. Give the visual agent room to propose additions or omissions across the whole explanation instead of locking it into a single requested image. The main agent records a short reason for accepting or declining proposals, then commissions the useful figures. Keep the brief proportional to the figure: a few clear sentences are often enough, and the table is optional.

For multi-system documents, consider whether readers can see the important paths, boundaries and feedback between systems as well as each component's internal mechanism. These are candidate visual questions, not mandatory diagram categories; a small example or table may already answer them. Revisit the assessment if drafting introduces a new difficult relationship or numerical example. One finished illustration is not evidence that all relevant visual questions were considered. Do not set a figure quota or restrict the assessment to SVG/Mermaid before considering the explanation and actual tool access.

Specify stable terminology, arrows and their meaning, assumptions, and what the picture must not imply. Keep the document visually coherent without requiring different tools to look identical. Do not start generating pictures from only a broad topic name, and do not add images simply to fill a quota.

Once specifications are stable, independent figures can be produced alongside prose. A figure containing calculated values waits for verified results. Use `references/agent-coordination.md` for delegation and concurrency; an untested parallel plan is not verified parallel capability.

## External Image Rules

Default: prefer original explanatory figures built from verified relationships, using the production rules below.

Use an external image only when one condition is true:

- It has a clear license that allows the intended use.
- Permission or an applicable reuse basis has been established for the intended use; official or paper provenance and a citation alone do not establish that basis.
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

Redraw when the source image teaches a useful structure but its license is unclear. Do not trace exact layout or copy distinctive styling. Build the explanation from verified relationships and use an independently chosen layout. Cosmetic changes alone do not establish reuse permission.

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

### Common Quality And Conditional Sources

Every figure must answer a useful teaching question, preserve verified facts and relationships, agree with the prose, and remain readable at the intended document width. Inspect the actual linked image; a successful generation or valid source file is insufficient.

Apply source requirements according to the figure's job:

| Figure need | Required evidence or source | Delivery |
| --- | --- | --- |
| Exact curves, data or calculated trajectories | Traceable functions/data, assumptions and runnable computation or plotting source | A readable export; retain source/data in `附件/` |
| Qualitative structure, spatial view, cutaway or working scene | Verified parts/relationships and inspected output; label meaningful simplifications | A generated PNG can be sufficient; vector or editable source is not universally required |
| User requests later editing, or the figure is expected to be maintained | An appropriate editable source within actual capabilities | Keep that source and the document-facing export |

Reproducibility of calculations and editability of drawing objects are different needs. Do not apply a quantitative-plot requirement to every illustration or turn an optional SVG export into a restriction on production tools. Keep naturally available sources, but do not reconstruct a generated image as vectors merely to meet an invented universal rule.

### Tool Choice

Choose what the reader needs to see before choosing a tool. Fullstop prefers:

| Teaching purpose | Usual production choice |
| --- | --- |
| Clear boundaries, directions, correspondence, steps or changing states | Excalidraw or a precise programmatic schematic |
| Exact curves, data, ratios or numerical trajectories | Python/Matplotlib or another accurate plotting tool |
| Recognizing appearance, complex spatial form, material or a working scene | Consider built-in `imagegen` first when these details improve understanding |

Judge the particular figure, not its subject label. For physical recognition, compare the learning value of a spatial illustration and a clean schematic: can the reader recognize the actual part shape, depth, assembly or working surface, and can they trace the relevant relationships? Both may be useful for different questions. A clear membrane cross-section can remain schematic when spatial detail adds little; an object-recognition view can benefit from generation even when its mechanism is already explained by a good diagram. Do not require a schematic to fail before considering generation, or require generation to be indispensable while a schematic only needs to be adequate. Respect an explicitly requested format or existing editable source. There is no quota of generated images or tools, and more useful figures does not mean more generated figures.

Do not rule out generation merely because Chinese labels are needed, plotting code is authorized, or the destination supports native diagrams. Keep essential labels short, or add accurate labels separately when appropriate; an appearance view need not carry every precise arrow and calculation from a separate mechanism diagram. When generation is selected, execute it and inspect the returned pixels; a planned prompt is not a delivered figure. Record a meaningful tool-choice reason briefly, rather than adding a long per-figure justification.

SVG and PNG are output formats. A Python plot can export either; do not equate SVG with manually authored paths and fixed text coordinates. Prefer a plotting library for quantitative axes, ticks, curves, panels, and legends rather than reconstructing that machinery by hand.

For image generation, use one prompt per distinct figure and specify the correct relationships and necessary labels. Never treat plausible-looking generated geometry, equations, or numbers as verified content. Quantitative illustrations may also use image generation, but check all displayed values and the relationships they imply against verified inputs. When exact data cannot be faithfully represented and checked, use reproducible plotting or accurate overlays as needed. Evidence images remain tied to their actual source, not replaced by imagined results. Explain a tool choice only when it materially affects delivery.

Before generating a physical illustration, establish the relevant assembly and working path from reliable material, then specify the visible parts, interfaces, motion, and flow that the picture must convey. Inspect the output for impossible assembly, disconnected oil passages, incorrect moving surfaces, misleading layers, and ambiguous labels. Mark teaching simplifications where needed. If a subagent lacks image generation, use the main-agent bridge in `agent-coordination.md`; do not substitute a less useful diagram without reassessing the teaching need. Code approval and image-generation access are separate questions.

### Exact Mathematical Plots

Use verified functions or data to compute plotted points and trajectories. For Python plots, keep the runnable source and required data in the attachment directory alongside the final export; respect the session's code-writing authorization. Prefer an existing suitable runtime and check available fonts rather than installing dependencies without authorization.

Use the plotting library's layout support, such as Matplotlib's constrained layout, to help manage axes, ticks, and legends. It does not guarantee that arbitrary annotations avoid curves or other labels. Arrange annotations, comparison panels, and legends for the actual display width, then open the exported figure and inspect it again in the document. Check Chinese glyphs, mathematical text, clipping, labels covering data, ambiguous arrows, and label/legend collisions; revise defects before delivery. A numerical check alone cannot establish a readable plot.

Preserve an editable SVG or other requested export when useful, and provide a directly viewable PNG where the destination needs one. Inspect the export actually linked by the document. A system thumbnail that crops the figure is not a substitute for a verified export.

Relevant primary documentation: [Matplotlib constrained layout](https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html) and [savefig export options](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html).

### Obsidian Native Excalidraw

When Excalidraw has been selected for a figure in Fullstop's Obsidian vault, use the installed plugin's native drawing format and embed the drawing directly in the article. This is a delivery rule for that chosen tool, not a reason to choose it for every figure. Generated illustrations and other plots can be embedded in their appropriate image format without conversion to Excalidraw. Store the native drawing under the vault's `附件/`, with a descriptive unique name such as `主题-运输路径.excalidraw.md`; the article can embed it with `![[附件/主题-运输路径.excalidraw.md]]`. The note should display the drawing and let Fullstop open the same asset for editing, without a PNG-only detour.

Use the plugin's available creation/editing facilities or a valid plugin-compatible scene file, following `excalidraw-diagram` for format guidance and the installed plugin's actual behavior. Do not require manual GUI drawing when native-file creation is reliable. Vault attachment rules override that companion skill's generic current-directory save rule. Do not change plugin settings or install dependencies merely to draw.

Verify both the native embed at article width and the drawing opened in the plugin. Native file existence or JSON validity is not rendered acceptance. Export PNG/SVG when needed for external delivery, inspection or a verified renderer fallback; keep the native drawing as the Obsidian-facing asset when it works. Read-only fallback limitations must be reported rather than silently delivering only a raster. Reference: [plugin documentation](https://github.com/zsviczian/obsidian-excalidraw-plugin).

### Local Excalidraw CLI

Fullstop has two distinct CLI entries, confirmed via their help commands on 2026-10-09:

- `excalidraw-cli`, found at `/Users/fullstop/.hermes/node/bin/excalidraw-cli`: creates editable diagrams from JSON elements with `create`. Read `excalidraw-cli create --help` for current options; use an explicit attachment output path and `--no-checkpoint` when no checkpoints are needed.
- `excalidraw`, found at `/Users/fullstop/.hermes/node/bin/excalidraw`: renders local scene JSON to PNG with `excalidraw render drawing.excalidraw --out drawing.png`. Local rendering needs an installed browser but no account/API key; unrelated workspace commands use a separate online service.

Resolve entries with `command -v` when using them rather than assuming paths never change. Consult `excalidraw-diagram` when its schema or Obsidian format guidance helps. Keep editable source and document-facing exports in `附件/` for this vault. CLI help checks confirm the command entries, not successful rendering; inspect the actual rendered diagram before delivery. Do not invoke online exports or workspace mutations merely to draw locally.

For Feishu, follow the active Lark skill's media workflow within existing user authorization. For local documents, copy selected generated assets from their returned locations into the project's attachment directory, then update and verify references. In Fullstop's Obsidian vault, use `附件/`. Preserve existing files and avoid overwriting unrelated assets.

## Diagram Quality

A good diagram:

- Has one main message.
- Adds a concrete understanding beyond the adjacent prose; for plots, shows the mathematical relationship under discussion.
- Uses labels that match article terminology.
- Can be understood at mobile width if possible.
- Is introduced before it appears.
- Is interpreted after it appears.

Ordinary knowledge notes do not use “图1/图2” or numbered figure captions. Refer to “下图” or a descriptive name tied to the adjacent section. Keep short captions only when they supply a useful condition, simplification or source; do not repeat the picture title and nearby paragraph. Internal asset IDs used for coordination need not appear in reader-facing content. Number figures only when the user or a formal publication format requires it.

Inspect every actual final figure before delivery. Check geometry and component relationships, arrow directions, exact text, symbols, units, and agreement with the prose. For mathematical plots, also check axes and scale, curve shape, marked coordinates, slopes, and trajectory or parameter comparisons against the verified function or data. Generated plots must satisfy the same checks; use reproducible plotting or accurate overlays when needed for fidelity. State when geometry is schematic rather than to scale if the distinction matters. Data plots must retain a traceable data source. A prompt or a generator's success status cannot substitute for inspecting the image.

Judge readability at the intended document width as well as full export size. Do not accept small notes simply because the source uses a large pixel font: scaling a wide illustration can make them unreadable. Move long conditions into adjacent prose, enlarge essential labels, or split overloaded panels. Prefer one clear question per figure; coherent multi-panel figures remain useful when their panels directly support that question.

Correct a failed figure and recheck it. If image-generation edits repeatedly preserve the same geometric or directional defect, reconsider the production method rather than continuing cosmetic edits; use precise editable geometry or reproducible plotting when it fits the teaching purpose. If a required figure remains unreadable or technically wrong, mark the draft incomplete; do not claim a completed illustrated document.

Avoid:

- Too many colors.
- Tiny labels.
- Generic icons.
- Flow arrows without meaning.
- A diagram that duplicates a paragraph without adding structure.
