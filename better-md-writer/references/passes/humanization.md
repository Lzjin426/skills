# Better Md Writer Pass: Humanization

Humanization is optional. Default to `off`.

When enabled, use [../../../humanizer-zh/SKILL.md](../../../humanizer-zh/SKILL.md) as the cleanup reference.

## Use when

Use this pass for:
- tutorials
- knowledge articles
- explanatory prose
- reader-facing documentation where mechanical phrasing harms readability

## Do not use when

Skip this pass for:
- RFCs and specifications
- audit or compliance writing
- meeting minutes and trace records
- citation-heavy or quote-heavy writing
- rigid templates

## Goal

The goal is not to make the text sound casual. The goal is to remove mechanical phrasing while preserving:
- exact meaning
- scope and qualifiers
- traceability
- the user's original viewpoint

## Guardrail

If cleanup weakens precision, revert the wording.
