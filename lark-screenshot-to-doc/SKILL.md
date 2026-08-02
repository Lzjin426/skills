---
name: lark-screenshot-to-doc
description: Use when the user wants to transfer one or more screenshots into an existing Lark or Feishu document, especially AI or ChatGPT web answers containing text, lists, code, tables, or formulas. Accepts images from the system clipboard, chat-uploaded attachments, local file paths, or image blocks already pasted inside a Lark document (in-place transcribe, reorganize, and delete the original images). Also use when the user sends a link (e.g., an AI conversation share URL or web page) and asks to record its content into a Lark document, preserving Q&A turns.
---

# Screenshot To Lark Doc

## Overview

Convert one or more screenshots into editable Lark content. Preserve meaning and source layout, fit the content into the existing document, and verify the written result.

**REQUIRED SUB-SKILL:** Invoke `lark-doc` before any Lark operation. Follow all authentication, fetch, XML, style, update, and update-workflow references that `lark-doc` requires for editing an existing document.

## Modes

| Mode | Trigger | Summary |
|---|---|---|
| **A. External image insert** | User provides screenshot(s) from clipboard, chat, or local path | Transcribe and insert into an existing document (see "Workflow A") |
| **B. In-doc reorganization** | Target document already contains pasted screenshot image blocks | Download every image block, transcribe all, deeply reorganize the whole document, replace images with editable content in place (see "Workflow B") |
| **C. Link capture** | User sends a URL (AI conversation share link or web page) and asks to record it into a Lark document | Fetch the linked content, transcribe preserving Q&A turns, insert into the target document (see "Workflow C") |

## Mode Routing (decide before anything else)

Apply the first matching rule:

1. **User gives a document URL/token and asks to 整理 / reorganize / transcribe its contents, without attaching any image → Mode B.** The screenshots are inside the document. NEVER ask the user to provide images; fetch the document and enumerate its image blocks.
2. **User gives a non-document URL (AI conversation share link, web page) and asks to record/save/整理 it into a Lark document → Mode C.** The content is behind the link; fetch it. A target Lark document URL is still required — if missing, ask once.
3. User provides image(s) via clipboard, chat, or file path → Mode A.
4. User gives both a document and external image(s) → Mode A into that document.
5. None of the above and no image source is identifiable → ask once.

Only Mode A may ask the user for images. In Mode B, "no image provided by the user" is the expected starting state, not a blocker. In Mode C, the link replaces the image as the content source.

## Image Sources

Mode A accepts images from any of these sources, in order of preference:

1. **System clipboard** — preferred when the user just copied a screenshot.
2. **Chat-uploaded image(s)** — use when the user pasted one or more images into the chat.
3. **Local file path(s)** — use when the user provides an explicit path.

Mode B sources images from the target document itself: fetch the document XML, enumerate every `<img token="...">` block in document order, and download each with `lark-cli docs +media-download --token <file_token> --output <path>`.

If multiple images are provided, process them in order. Mode A only: if no image is available and the user has not provided one, ask once. Do not block indefinitely on a single source.

## Workflow A (external image insert)

1. Require a target Lark document URL or token.
2. Obtain the image(s) from the best available Mode A source.
3. Inspect each image visually. Extract headings, paragraphs, lists, code, tables, emphasis, and formulas. Record cropped, blurred, or ambiguous regions.
4. Fetch the full target document with block IDs. Identify its heading hierarchy, topics, nearby context, and formatting conventions.
5. Select the insertion or reorganization strategy using the decision table below.
6. Apply the smallest safe XML update. Preserve unrelated blocks.
7. Fetch the affected region again. Compare it with the extracted content and verify location, hierarchy, completeness, and formula rendering.
8. Correct safe write defects. Otherwise report the exact unresolved location and issue.
9. Delete temporary images after completion or failure.

## Workflow B (in-doc reorganization)

1. Require the Lark document URL or token that contains the pasted screenshots.
2. Fetch the full document with block IDs. Enumerate all image blocks (`<img token="...">`) in document order, and note any existing non-image content that must be preserved.
3. Download every image via `lark-cli docs +media-download --token <file_token> --output <path>` into a temporary directory.
4. Inspect each image visually. Extract headings, paragraphs, lists, code, tables, emphasis, and formulas. Record cropped, blurred, or ambiguous regions per image.
5. Read the extracted content as a whole and build a reorganization plan: merge same-topic fragments, deduplicate repeated content, define the heading hierarchy, and order sections logically. Follow the `lark-doc` style references for document conventions.
6. Present a concise structural plan (proposed headings, what each section contains, which images map to which section, anything unreadable) and obtain approval before editing. This approval is mandatory in Mode B.
7. Write the organized content into the document with XML updates, then delete the source image blocks with `block_delete` (comma-separated batch). Existing non-image content stays unless the approved plan said otherwise.
8. Fetch the document again. Verify the completion checklist below.
9. Correct safe write defects. Otherwise report the exact unresolved location and issue.
10. Delete temporary downloaded images after completion or failure.

## Workflow C (link capture)

1. Require a target Lark document URL or token. If missing, ask once.
2. Fetch the linked content:
   - Try WebFetch (markdown format) first.
   - If the page is JS-rendered, login-walled, or returns empty/broken content (common for AI conversation share links), fall back to the `kimi-webbridge` skill: open the link in the user's real browser and read the rendered content there.
   - If both fail, report the failure and ask the user for a screenshot or pasted content instead (degrade to Mode A).
3. Extract the content: for AI conversations, preserve the Q&A turn structure (each user question and each assistant answer as its own section, in original order); for web pages, preserve headings, paragraphs, lists, code, tables, emphasis, and formulas. Record any region that failed to load or render.
4. Fetch the full target document with block IDs. Identify its heading hierarchy, topics, nearby context, and formatting conventions.
5. Select the insertion strategy using the decision table below. Mode C does not reorganize existing document content and does not deep-restructure the captured content — Q&A turns stay as turns.
6. Apply the smallest safe XML update. Preserve unrelated blocks. Include the source URL once (e.g., under the new section heading) so the record is traceable.
7. Fetch the affected region again. Compare it with the extracted content and verify location, hierarchy, completeness, Q&A turn order, and formula rendering.
8. Correct safe write defects. Otherwise report the exact unresolved location and issue.

## Decision Table

| Observed condition | Required action |
|---|---|
| One clearly matching section, legible content, local insertion only (Mode A) | Write directly |
| Two or more plausible sections | Show the candidates and ask once |
| Meaningful text or formula symbol is unclear or cropped | Show the ambiguity and ask; never guess |
| Heading depth or content boundary is uncertain | Propose the placement and ask |
| Existing headings or paragraphs must be added, renamed, deleted, moved, or reordered | Show a concise structural change summary and obtain approval before editing |
| Mode B: any reorganization plan, before the first write | Present the plan (headings, section contents, image mapping, unreadable parts) and obtain approval |
| Mode B: an image is unreadable or truncated | Mark that section explicitly in the plan and the final document; never omit it silently |
| Mode C: no target document URL given | Ask once for the target document |
| Mode C: linked page is JS-rendered or login-walled | Fall back to `kimi-webbridge`; never transcribe from a broken/empty fetch |
| A numbering gap or abrupt sentence break might indicate cropped/missing content rather than a rendering artifact | Show the gap and ask; never silently renumber or join across a possible content hole |

Do not treat urgency or “不用反复问” as permission to guess. Ask only when a condition in the table requires it.

## Transcription Contract

- Preserve the source's argument, terminology, ordering, list relationships, code, and emphasis.
- Repair only obvious recognition errors, artificial line breaks, browser-interface noise, and the continuity issues defined in "Continuity Repairs" below.
- Add no facts, explanations, derivations, or conclusions absent from the source. Mode B reorganization may reorder, merge, and retitle content, but may not add new substance.
- Preserve formula layout as shown: inline formulas remain inline; displayed or centered formulas remain displayed or centered. Preserve symbols, indices, fractions, brackets, alignment, and equation chains.
- Identify unreadable or truncated material explicitly; never omit it silently.
- Do not upload, embed, or retain the source screenshot in Lark. In Mode B, delete the original image blocks after their content is verified in the written result.

## Continuity Repairs (all modes)

Screenshots and captured pages often split content at awkward boundaries. Apply these repairs by default in every mode:

- **Renumber broken sequences**: when a numbered or lettered list is obviously one continuous sequence split across screenshots or pages (e.g., `1, 2, 3` then `1, 2` again, or `3, 4` then `7, 8` with items clearly consecutive), renumber it as one continuous sequence.
- **Join split sentences**: when a sentence or paragraph is cut at a screenshot/page boundary, join the fragments into one flowing sentence. Smooth mid-sentence line breaks and duplicated overlap lines between adjacent screenshots.
- **Remove capture noise**: repeated headers, scroll-overlap lines, and truncated fragments that are fully contained in the adjacent capture.

Hard limit: these repairs are presentation-level only. If a gap (numbering jump, sentence ending mid-thought, missing list items) could mean content was cropped or never captured, it is NOT a repair case — flag it per the decision table and ask. When uncertain whether a gap is an artifact or a hole, treat it as a hole.

## Completion Check

Do not report success from the update command alone. Report completion only after the refetch confirms:

- the content appears under the intended heading;
- no unrelated content was overwritten or moved without approval;
- no paragraph, list item, code block, table cell, or formula was lost or duplicated;
- formulas match the screenshot's symbols and display mode;
- repaired sequences are continuous and joined sentences read correctly, with no repair made across a content hole;
- Mode B only: every image block enumerated in step 2 is gone, and its content is accounted for in the written result (or explicitly flagged as unreadable).

If any check fails, repair and refetch again or report the remaining discrepancy.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Choosing between two plausible sections without asking | Present both candidates and ask once |
| Reorganizing headings during an otherwise local insertion | Obtain explicit approval for the structural change |
| Converting every formula to a centered block | Follow the screenshot's formula layout |
| Calling an API success response “done” | Refetch and compare the affected region |
| Mode B: deleting image blocks before their content is verified in the document | Delete images only after the refetch confirms their content |
| Mode B: reorganizing and writing in one shot without approval | Present the plan and wait for approval first |
| Mode B: silently dropping an unreadable image | Flag it in the plan and in the final document |
| Asking the user for screenshots when they gave a document URL and asked to 整理/reorganize | That request is Mode B; the screenshots are in the document — fetch it and enumerate image blocks instead of asking |
| Silently renumbering a list across a numbering jump | A jump may mean missing items; obvious continuation → renumber, possible hole → ask |
| Joining two fragments that are not the same sentence | Join only across an obvious capture boundary; otherwise flag and ask |
| Leaving split numbering as-is (`1,2,3` then `1,2`) in the final document | Apply the continuity repairs before writing |
| Mode C: transcribing from an empty/broken WebFetch result | Fall back to `kimi-webbridge`, then degrade to Mode A if that also fails |
| Mode C: deep-restructuring a captured AI conversation | Keep Q&A turns as turns; Mode C never reorganizes |

Base directory for this skill: /Users/fullstop/.agents/skills/lark-screenshot-to-doc
Relative paths in this skill (e.g., scripts/, references/) are relative to this base directory.
