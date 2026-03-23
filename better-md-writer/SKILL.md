---
name: better-md-writer
description: Write, rewrite, and polish documents with a lightweight default workflow. Choose a document profile first, then enable higher-cost passes only when they clearly improve the draft.
---

# Better Md Writer

Use this skill when the user needs to write or refine Markdown documents such as notes, knowledge-base pages, READMEs, proposals, tutorials, runbooks, or other structured documentation.

The core rule is simple: **choose the lightest workflow that still fits the document's job**. Do not default to heavy research, diagrams, cognitive scaffolding, or post-processing unless the task clearly benefits from them.

For knowledge-base writing, optimize first for **future readability, low understanding cost, and professional clarity**. Avoid both dense academic phrasing and overly casual teaching tone. Treat this as a global knowledge-base rule, not as a machine-learning-only writing preference.

## Purpose

This skill is a thin orchestrator. It helps the agent:
- clarify what the document must do
- choose the right document profile
- enable optional passes only when justified
- draft with the selected defaults
- run a reader-oriented check
- apply Fullstop's local Obsidian workflow only when relevant

This skill is not a single fixed pipeline. It should not force every document through the same long-form writing process.

## Default Workflow

1. **Clarify job**
   - Read [references/core/document-intent.md](references/core/document-intent.md) when the writing task, audience, or output shape is unclear.
   - Ask only for missing information that would materially change the draft.
   - For **kb-article**, identify the article subtype before drafting: concept explanation, comparison, result interpretation, or method/process.

2. **Choose profile**
   - Select one profile from:
     - [note](references/profiles/note.md)
     - [kb-article](references/profiles/kb-article.md)
     - [readme](references/profiles/readme.md)
     - [proposal](references/profiles/proposal.md)
     - [tutorial](references/profiles/tutorial.md)
     - [runbook](references/profiles/runbook.md)
   - If the type is still ambiguous, stay lightweight and avoid turning the task into a heavy documentation exercise.

3. **Decide optional passes**
   - Enable [research](references/passes/research.md) only when the content is time-sensitive, comparative, evidence-heavy, or the user explicitly asks for research.
   - Enable [cognitive-path](references/passes/cognitive-path.md) only when the document needs to build a reusable mental model across a longer explanation.
   - Enable [illustration](references/passes/illustration.md) only when a visual will reduce understanding cost more than prose alone.
   - Enable [humanization](references/passes/humanization.md) only for human-facing prose where smoothing mechanical phrasing will not damage precision or traceability.
   - For **kb-article**, bias toward more visuals, precise plain language, and a stronger through-line unless the user clearly wants a denser reference style.
   - For **kb-article**, do not rely only on the main writing agent to decide illustrations.
   - If the document is a knowledge-base explanation article and any of the following is true, a dedicated illustration review is **mandatory** after the draft is structurally stable:
     - the topic is abstract, model-based, graph-based, UI-based, or otherwise hard to picture
     - the draft contains 2 or more `IMG-CANDIDATE` markers
     - the reader would likely ask "what does this actually look like?"
     - the document compares multiple mechanisms, flows, or model families

4. **Draft**
   - Use the selected profile as the default behavior.
   - Use [references/core/structure-selection.md](references/core/structure-selection.md) to choose the primary carrier and shape the sections.
   - Prefer standard, portable Markdown unless the target environment clearly supports something more specific.
   - If the target is Fullstop's local knowledge base or Obsidian vault, default to explicit hierarchical heading numbers such as `1.`, `1.1`, and `1.1.1` unless the target file has an established conflicting style.
   - For concepts that readers often fail to visualize, show what the thing looks like before explaining formal distinctions or implementation details.
   - For **kb-article**, keep the tone professional and restrained. Do not write as if narrating a lesson, a video script, or a conversational coaching session.
   - For **kb-article**, start from a stable subtype skeleton instead of inventing a new outline from scratch for each article.
   - For **kb-article**, keep the top-level structure tight. `3-5` top-level sections is the default unless the document clearly needs more.
   - For **kb-article**, make sure the article answers one clear judgment question such as "how to identify it", "how to distinguish it", "how to read the output", or "how to place it back into the current project".
   - For **kb-article**, include at least one explicit visual anchor, even before deciding whether it becomes a real image: what it looks like, what the output looks like, what the flow looks like, or what the comparison shape looks like.
   - When a figure may be needed, insert an explicit image candidate marker instead of making an unreviewed final decision inline.

5. **Run reader check**
   - Use [references/core/reader-check.md](references/core/reader-check.md) before final delivery.
   - If any optional pass was enabled, verify that it improved the document instead of adding ritual or noise.

6. **Apply local environment actions when relevant**
   - If the document is meant for Fullstop's knowledge base or Obsidian vault, apply [references/local/fullstop-obsidian.md](references/local/fullstop-obsidian.md).
   - Keep these local defaults out of the generic writing logic.

## Profile Selection

Use the document's job, not the label alone, to choose the profile:
- **note**: quick capture, cleanup, or internal working memory
- **kb-article**: durable knowledge-base writing for later reuse
- **readme**: orientation and onboarding for a repo or project
- **proposal**: decision support with options, trade-offs, and recommendation
- **tutorial**: teaching or guided learning
- **runbook**: operational execution with steps, branches, and verification

If a document combines multiple jobs, choose the primary one and borrow only the minimum useful elements from another profile.

For **kb-article**, default to:
- choose one subtype first: concept explanation, comparison, result interpretation, or method/process
- explain in plain but precise language before leaning on terms or symbols
- show the concrete thing, output, or picture first when that lowers reader confusion
- keep a clear progression instead of stacking loosely related mini-sections
- keep the default top-level structure within `3-5` sections
- answer one explicit judgment question, not just accumulate definitions
- reserve at least one visual anchor early in the draft
- use semantic section titles, not conversational hooks
- avoid lines such as "先记这一句", "先别管", "你只要记住", or similar spoken-style prompting unless the user explicitly wants a tutorial voice

## Pass Selection

All optional passes are **off by default**.

### Research

- Default: `off`
- Turn on only when facts, terminology, policy, versions, or comparisons need validation.
- See [references/passes/research.md](references/passes/research.md).

### Cognitive Path

- Default: `off`
- Turn on only when a longer explanation needs an explicit mental model and a deliberate learning arc.
- See [references/passes/cognitive-path.md](references/passes/cognitive-path.md).

### Illustration

- Default: `off`
- Turn on only when a diagram or image will explain faster or more accurately than extra prose.
- Special case: for **kb-article**, illustrations are encouraged whenever they materially reduce confusion, including screenshots, examples, process sketches, comparisons, and "what it looks like" visuals.
- For explanation-heavy knowledge-base articles, the main writing agent should propose candidates, but a separate review pass should decide which visuals are actually needed and what kind they should be.
- If the mandatory illustration-review conditions are met, the document is not complete until that review has produced an image plan.
- See [references/passes/illustration.md](references/passes/illustration.md).

### Humanization

- Default: `off`
- Turn on only when the output is prose-heavy and reader-facing, and when wording cleanup will not weaken exact meaning.
- See [references/passes/humanization.md](references/passes/humanization.md).

## References

### Core

- [document-intent](references/core/document-intent.md)
- [structure-selection](references/core/structure-selection.md)
- [reader-check](references/core/reader-check.md)

### Profiles

- [note](references/profiles/note.md)
- [kb-article](references/profiles/kb-article.md)
- [readme](references/profiles/readme.md)
- [proposal](references/profiles/proposal.md)
- [tutorial](references/profiles/tutorial.md)
- [runbook](references/profiles/runbook.md)

### Optional Passes

- [research](references/passes/research.md)
- [cognitive-path](references/passes/cognitive-path.md)
- [illustration](references/passes/illustration.md)
- [humanization](references/passes/humanization.md)

### Local Defaults

- [fullstop-obsidian](references/local/fullstop-obsidian.md)
