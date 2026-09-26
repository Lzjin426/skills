---
name: paper-humanizer
description: Academic text polisher and humanizer for Chinese and English research writing. Removes AI-like patterns while preserving factual accuracy. Use when polishing academic text, reducing AI-generated patterns in papers/theses, improving naturalness of research writing while maintaining data integrity, or enhancing scholarly tone without fabricating facts. Supports both Chinese (中文) and English academic texts with configurable tone, field-specific terminology, and strict factuality controls.
---

# Paper Humanizer

Polish and humanize academic writing to reduce AI-like patterns while preserving all factual content, data, and meaning.

## Quick Start

Apply the system prompt from `references/system_prompt.md` and use the workflow below.

## Output Format (Two-Stage)

### Stage 1: Analysis & Ask

Produce the first 3 sections and then ask the user how to proceed. **Do not output the full polished text in Stage 1.**

1. **原文 AI 特征分析** (Original Text AI Pattern Analysis)
2. **核心优化策略** (Core Optimization Strategies)
3. **优化亮点说明** (Highlight Notes - optional)
4. **下一步行动** (Next Step): Ask the user to choose one of the following options:
   - **全文输出**: Output the complete polished text at once.
   - **逐章修改**: Output the polished text chapter by chapter, pausing for confirmation after each chapter.
   - **局部修改**: Revise only the section(s) the user specifies.
   - **Diff 模式**: Show before/after snippets of key changes instead of the full text.

### Stage 2: Execute on User Choice

Only after the user replies, deliver the polished content in their chosen form.

## Core Constraints

**Non-negotiable:**
- Never fabricate facts, results, metrics, or references
- Never change numeric values, experimental settings, or data
- Preserve citation markers (e.g., [1], (Smith, 2023), \cite{...})
- Maintain all terminology and technical accuracy

**Remove AI-isms:**
- Chinese: "值得注意的是", "不难发现", "基于以上分析", "综上所述", "首先/其次/最后", "本文将"
- English: "It is worth noting that", "It can be seen that", "In summary", "Firstly, Secondly, Finally" (when overused)

See `references/phrase_blacklist.md` for complete list.

## Parameters

Configure behavior using these parameters:

- **language**: `auto` (detect) | `zh` (Chinese) | `en` (English)
- **tone**: `formal` (default) | `semi-formal` | `concise` | `persuasive`
- **strict_factuality**: `true` (default) - preserve all data/facts
- **keep_citations**: `true` (default) - preserve citation markers
- **blacklist_level**: `high` (default) | `medium` | `low`

## Workflow

1. **Analyze**: Identify 2-3 major AI pattern issues in the input text.
2. **Strategy**: Decide 3-5 targeted optimization strategies.
3. **Highlight**: (Optional) note 1-2 representative edits.
4. **Ask**: Present Stage 1 output and ask the user how they want to proceed.
5. **Execute**: Only after the user confirms, apply edits in their chosen mode (full text, chapter by chapter, partial, or diff).

## Language Handling

- Auto-detect language from input text
- Maintain same language in output (unless user requests translation)
- Keep technical terms (GAN, WGAN-GP, NSL-KDD) as-is
- Preserve field-specific terminology

## Advanced Features

For domain-specific terminology or special requirements, see:
- `references/system_prompt.md` - Complete editing principles and constraints
- `references/phrase_blacklist.md` - AI-pattern phrases to avoid
- `references/user_template.md` - Parameterized user prompt template

## Script Usage (Optional)

Use the CLI wrapper for batch processing:

```bash
# Process a text file
python3 scripts/paper_humanizer.py --text-file input.txt --language auto

# Generate composed prompt for external use
python3 scripts/paper_humanizer.py --text-file input.txt --out prompt.md
```

The script combines system prompt and user template with specified parameters.