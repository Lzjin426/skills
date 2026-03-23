# Better Md Writer Pass: Cognitive Path

Cognitive path design is optional. Default to `off`.

Enable it only when the document needs to build a reusable mental model across a longer explanation.

## Use when

Use this pass for longer explanations, tutorials, or analysis where the reader needs more than isolated facts.

## Skip when

Skip this pass for:
- notes and records
- config docs and runbooks
- short documents
- scan-oriented reference material

## What to add when enabled

### Anchor concept

Identify the one mental model that helps the rest of the document click into place. Make it explicit in the draft.

### Cognitive arc

Shape the draft as:
- **orient**: show the territory and what the reader will understand
- **build**: add detail in dependency order
- **close**: return to the opening frame so the reader can verify understanding

### Inter-section progression

Make adjacent sections feel connected:
- each section should answer a question raised by the previous one
- if sections can be swapped freely, the progression is too weak

## Guardrail

Do not enable this pass just because a topic is technical. Use it only when the reader truly benefits from an explicit learning path.
