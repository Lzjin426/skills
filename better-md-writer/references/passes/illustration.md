# Better Md Writer Pass: Illustration

Illustration is optional. Default to `off`.

## Trigger rule

If a visual can establish correct understanding faster or more accurately than extra prose, include one. Otherwise, do not.

For **kb-article**, lean toward including more visuals when the topic is abstract, graph-based, model-based, UI-based, or otherwise hard to picture from prose alone.

Do not make final illustration decisions only inside the main writing flow when the document is explanation-heavy. Treat illustration review as a separate cognitive task.

## Mandatory illustration review triggers

Run a separate illustration review when the document is a knowledge-base explanation article and any of these is true:
- the topic is abstract, model-based, graph-based, UI-based, or otherwise hard to picture
- the draft contains 2 or more `IMG-CANDIDATE` markers
- the reader would naturally ask "what does this actually look like?"
- the document compares multiple mechanisms, flows, or model families

If any trigger matches, the illustration review is mandatory rather than recommended.

## Good use cases

- flows, lifecycles, and branching paths
- architecture or layered relationships
- comparisons that are clearer visually than in text
- concrete screenshots or reference images that replace descriptive prose
- "what it looks like" examples before formal explanation
- annotated examples that help the reader map terminology to the actual artifact

## KB article bias

When writing a knowledge-base article, do not limit visuals to structure diagrams. Prefer a mix when useful:
- real screenshots or reference images
- example outputs
- before/after comparisons
- annotated diagrams
- process sketches
- simple visual analogies

If the topic is something the reader may ask "what does that actually look like?", answer that question visually as early as practical.

## Tool choice

- use web images for real, concrete things such as products, locations, devices, or UI screenshots
- use `excalidraw-diagram` for concepts, structures, flows, and relationships
- use `obsidian-canvas-creator` for note networks or knowledge relationships

## Workflow

1. During drafting, mark likely image positions with explicit candidate placeholders such as:
   - `<!-- IMG-CANDIDATE: excalidraw-diagram - request lifecycle -->`
   - `<!-- IMG-CANDIDATE: web - dashboard settings panel -->`
   - `<!-- IMG-CANDIDATE: example - what a typical PDP chart looks like -->`
   - `<!-- IMG-CANDIDATE: annotated - label the axes and the main curve shape -->`
2. After the draft structure is stable, run a **dedicated illustration review**.
3. Let the illustration review decide:
   - whether each candidate really needs a visual
   - what job the visual should do
   - what visual type fits best
   - whether any missing visual should be added even if the writer did not mark it
4. Produce visuals only after the review step.
5. Insert only visuals that reduce explanation cost.

## Dedicated illustration review

For explanation-heavy knowledge-base writing, prefer a separate review agent or a fresh review pass dedicated to visuals.

The reviewer should inspect the whole draft and answer:
- Where will the reader fail to picture the concept?
- Which sections are technically correct but too expensive to read without a visual?
- Does the document need a "what it looks like" visual before it needs a structure diagram?
- Is this best served by a real example, screenshot, output sample, annotated diagram, process sketch, or comparison figure?

This review step is not the same as producing images. Its job is to produce an **image plan**.

## Image plan output

The illustration review should produce a compact plan for each approved visual:
- location in the document
- why the visual is needed
- visual type
- short description of what the visual should show
- source or production path:
  - existing local image
  - web image search
  - `excalidraw-diagram`
  - `obsidian-canvas-creator`

If no visual is needed for a marked candidate, say so explicitly instead of producing one by habit.

Without this image plan, a draft that met the mandatory triggers should be treated as incomplete.

## Guardrails

- do not force a diagram quota
- do not treat illustration as a default acceptance criterion
- remove visuals that duplicate the prose instead of helping it
- for kb articles, under-illustration is often a bigger failure than one extra useful visual
- do not let the main writing agent be the only judge of image necessity for explanation-heavy knowledge-base articles
- if the mandatory triggers are met, do not skip the review step for speed
