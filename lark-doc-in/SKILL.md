---
name: lark-doc-in
description: Use when the user sends screenshots, a Lark or Feishu document link, a web or AI conversation link, or a Markdown file/link and wants the content written into a Lark document. Transcribe image-based text into editable content, integrate it with the document context, delete successfully transcribed in-document screenshots, and create a new document in Inbox when no target document is supplied.
---

# Screenshot, Link, And Markdown To Lark Doc

Convert screenshots, links, and Markdown into an editable Lark document without unnecessary confirmation. Preserve the source's meaning and structure, integrate it with useful surrounding context, and verify the saved result.

**REQUIRED SUB-SKILLS:** Before any Lark operation, invoke `lark-doc` and follow its required authentication, fetch, XML/Markdown, style, and update references. When creating or locating an Inbox destination, invoke `lark-drive`. For a native Drive Markdown file, invoke `lark-markdown` to fetch it.

## Autopilot Defaults

Apply these defaults unless the user explicitly gives different instructions:

1. A Lark document URL is the destination. Write directly into that document; do not ask whether to create a new document, preserve it separately, or where to insert content.
2. If the destination document itself contains screenshots, transcribe those screenshots in place and delete each successfully transcribed screenshot block after verification.
3. If the user supplies screenshots, a web link, an AI conversation link, or Markdown without a Lark document URL, create a new editable Lark document in the user's configured `Inbox` folder. Do not ask for a destination.
4. If a Lark document URL accompanies external sources, use that document as the destination. With several Lark document URLs, use the first one as the destination and treat later URLs as sources unless the user labels them otherwise.
5. Preserve unrelated existing content. Insert external sources into the best matching section; when no match is clear, append a new top-level section instead of asking.
6. Ask only when the source cannot be read reliably, access is unavailable, or executing the request would delete or overwrite non-source content. Do not ask about routine layout, title, placement, or numbering choices.

## Source Routing

Choose the first applicable source route:

| Source | Route |
|---|---|
| Lark document link containing screenshot blocks | Download the image blocks in document order, transcribe them, replace them in place, then delete the verified source blocks. |
| Chat-uploaded screenshots, clipboard images, or local image paths | Transcribe in supplied order and integrate them into the explicit destination or a new Inbox document. |
| Web page or AI conversation share link | Fetch the rendered content, preserve its meaningful structure, and integrate it into the destination or a new Inbox document. |
| Local `.md` file, Drive Markdown file, or Markdown URL | Read the Markdown and convert headings, text, lists, tables, code, formulas, and embedded text-bearing images into editable Lark content. |

For a page that is JavaScript-rendered, login-walled, or incomplete through `WebFetch`, invoke `kimi-webbridge` and read the rendered page in the user's browser. Do not transcribe an empty or broken fetch.

## Model Without Vision: OCR Fallback

When the active model cannot read images directly (the `Read` tool fails with "model does not support image input"), do not stall or repeatedly retry `Read` — switch to an OCR toolchain:

1. **Download first**: image blocks carry a direct `href` URL (`<img href="...">`); `curl -sL` them into a temp directory in document order. If no URL is present, use `docs +media-download --token <src token>`.
2. **Two-tool OCR strategy**:
   - **macOS local Vision OCR** (fast, free, strong `zh-Hans`): compile once with Swift + Vision framework (`VNRecognizeTextRequest`, `.accurate`, `recognitionLanguages = ["zh-Hans", "en-US"]`, output lines sorted by y coordinate). Best for paragraphs, lists, and table text.
   - **`mineru-open-api flash-extract <img>`** (free, no auth): best for formulas (LaTeX) and table structure. Each call takes 1–3 minutes — budget time accordingly.
3. **Parallelize aggressively**: batch remaining images to a subagent (e.g. `general` / `deepseek-v4-flash`) that runs the OCR commands and returns raw output; run your own batch in parallel. Serial per-image verification is the main time sink — avoid it.
4. **Cross-validate ambiguities**: when the two OCR tools disagree on a formula symbol, table cell, unit, or exponent, crop + upscale the region first (PIL: crop → resize ×6–8 → `autocontrast` → `Contrast(2.0)`) and re-run both tools. If still conflicting, use the majority of ≥3 consistent reads; otherwise mark `[Source content is incomplete or unreadable]` and keep the source image.
5. **Known pitfalls**:
   - Never ask a vision-less subagent to "look at" images — it returns empty output. Give it exact commands to run instead.
   - Repair only unambiguous OCR noise (e.g. 计草→计算, 工祝→工况); never guess unreadable symbols.
   - Table rows misalign easily across OCR tools: verify row-by-row (symbol / definition / unit) on magnified table crops.

## Standard Workflow

1. Resolve the destination using **Autopilot Defaults**. When a new document is needed, create it in `Inbox` with a short source-derived title.
2. Fetch the full destination with block IDs and identify its topic, heading hierarchy, formatting conventions, and image blocks.
3. Extract every source in order. Inspect screenshots visually; capture headings, paragraphs, lists, tables, code, emphasis, formulas, and unreadable regions. For document screenshots, distinguish text-bearing screenshots from diagrams, photos, and other non-text images.
4. Build the editable result using **Contextual Integration** and **Faithful Repair** below. Do not present a structural plan or wait for approval.
5. Update only the affected region. For screenshots already in the destination, replace each source image at its original location before deleting that block. For external sources, insert into the selected section or append a new section.
6. Refetch the affected region. Check its placement, hierarchy, completeness, tables, code, formulas, and the preservation of unrelated content.
7. Delete only the verified source screenshot blocks. Keep non-text diagrams, photos, and any image that was not successfully transcribed unless the user explicitly asks to remove it.
8. Refetch once more after deletions. Repair safe write defects before reporting success.

For an external URL, record the source URL once at the end of its inserted section. For an AI conversation, preserve user and assistant turns in original order unless the surrounding document clearly calls for them as quoted source material.

## Contextual Integration

Keep the source faithful while making the result usable as one document:

- Follow an existing document's heading depth, terminology, and list style.
- In a blank document, promote a clear source title to the document title. If none exists, derive a short neutral title from the source topic; do not invent substantive claims.
- When several screenshots form one passage, merge them in reading order and remove overlap caused by scrolling or page boundaries.
- Place content in a clearly matching section. Otherwise append a new top-level section named after the source heading or topic.
- Add only minimal, fact-free bridge text when it makes an otherwise abrupt connection with neighboring content readable. Never add explanations, conclusions, examples, or claims absent from the sources.
- Preserve tables as tables, code as code blocks, and formulas in their original inline or displayed form.
- Convert Markdown syntax to native editable document structure rather than pasting raw Markdown, except for code blocks and literal examples.

## Faithful Repair

Apply the following presentation repairs by default:

- Join a sentence or paragraph split across adjacent screenshots when the fragments clearly belong together.
- Remove duplicated overlap lines, browser chrome, repeated page headers, and other capture noise.
- Correct obvious OCR mistakes only when the intended text is unambiguous from the image or adjacent context.
- Continue an obviously continuous list across screenshots and normalize its numbering.
- In a blank document or new standalone section, normalize a clearly sequential heading or list that starts at `2` to start at `1`. Preserve labels whose number is semantic, such as an explicitly contextual "Chapter 2" or a section that is visibly part of a larger source.
- Repair artificial line breaks and spacing without changing terminology, argument order, or meaning.

Do not silently repair a possible content hole. If a cropped image, a numbering jump, or a broken sentence could represent missing source material, leave a concise `[Source content is incomplete or unreadable]` marker in place, keep the source image when present, and ask one focused question for a clearer source.

## Do Not Ask For Approval

Proceed automatically in these cases:

| Situation | Required action |
|---|---|
| No destination document | Create an editable document in `Inbox`. |
| Destination document is empty | Build its title and body from the source. |
| Several possible insertion sections | Use the closest semantic match; otherwise append a new top-level section. |
| Existing headings need local normalization | Align new content with the existing hierarchy without changing unrelated headings. |
| Screenshot sequence starts at `2` in a blank document | Renumber it to `1` when it is clearly sequential. |
| Existing document contains transcribed screenshots | Replace them in place and delete only the verified screenshot blocks. |
| Link or Markdown has no pre-existing target | Create the Inbox document and write it directly. |

Ask one focused question only for these blockers:

| Blocker | Required action |
|---|---|
| Important text, a table cell, or a formula symbol cannot be read | Mark the exact region, keep the source image, and request a clearer capture. |
| A web or AI link cannot be read after browser fallback | Report the access failure and ask for access, a screenshot, or pasted content. |
| The user supplied conflicting explicit destination instructions | Ask which named document is the destination. |
| The requested edit would overwrite or delete existing text or non-source images | Describe the affected content and ask before changing it. |

## Completion Check

Report completion only after refetch confirms all of the following:

- The editable content is in the resolved destination and follows its local structure.
- The source's text, list relationships, tables, code, and formulas are complete and not duplicated.
- Unrelated existing content was not overwritten, moved, or deleted.
- Sentence joins, numbering repairs, and bridge text did not change source meaning or conceal a content hole.
- Every deleted screenshot block was first transcribed and verified in the document.
- Any unreadable or inaccessible material remains explicitly identified with its source image or URL preserved where possible.
