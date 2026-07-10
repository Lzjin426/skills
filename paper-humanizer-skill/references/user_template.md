# User Template

## Task

Polish and humanize the following academic text to reduce AI-like patterns while preserving meaning and factual details.

## Parameters

- language: {{language}}
- field: {{field}}
- audience: {{audience}}
- tone: {{tone}}
- strict_factuality: {{strict_factuality}}
- keep_citations: {{keep_citations}}
- output_format: {{output_format}}
- blacklist_level: {{blacklist_level}}

## Text

<<<
{{text}}
>>>

## Stage Instructions

- **Stage 1**: Output only sections 1-3 (AI pattern analysis, optimization strategies, highlight notes) plus the next-step question. Do NOT output the full polished text yet.
- **Stage 2**: After the user confirms their preferred mode (full text, chapter by chapter, partial, or diff), deliver the polished content accordingly.

## Notes (optional)

- If the text contains tables/equations/code, keep them unchanged unless it is purely narrative phrasing.
- Do not add new references.
