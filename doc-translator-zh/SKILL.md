---
name: doc-translator-zh
description: |
  Translate documents (PDF or Markdown) into Chinese, with OCR error correction, formula standardization, image handling, and optional Feishu output.
  Use this skill whenever the user asks to translate a file/document/Paper/markdown into Chinese, localize content to Chinese, convert a PDF to Chinese markdown, fix OCR errors while translating, or mentions Chinese translation with formulas/images/figures.
  Also trigger when the user wants the result uploaded to Feishu or formatted as a Feishu document.
---

# 中文文档翻译器 (doc-translator-zh)

Translate PDF or Markdown documents into high-quality Chinese Markdown, clean up OCR errors, standardize formulas and image references, and optionally deliver the result to Feishu.

## When to use this skill

- The user wants a **PDF or Markdown file translated into Chinese**.
- The source looks like it came from **OCR** and may contain format/content errors.
- The document contains **formulas, images, tables, or technical terms** that need careful handling.
- The user mentions uploading or creating a **Feishu document** from the translated content.
- The user says things like: "翻译这个文件", "把论文转成中文", "汉化这个文档", "整理成中文 markdown", "翻译并上传飞书".

## What this skill produces

A workspace with three folders:

- `input/` — original file(s)
- `output/` — translated markdown + images
- `script/` — helper scripts and logs

And optionally a Feishu document or uploaded markdown.

## Before you start

1. This skill uses `mineru-open-api extract`, which requires a MinerU token.
   - Set the environment variable: `export MINERU_TOKEN=your_token`
   - Or ensure `mineru-open-api auth` has been run and saved the token.
2. `lark-cli` must be installed and authenticated if Feishu output is requested.
3. Decide whether to use a single-agent or multi-agent approach based on document complexity.
4. If the user provides an existing Feishu document URL/token, treat it as the target by default.
   - Modify that same document in place.
   - Do not create a new Feishu document unless the user explicitly asks for a new document.
   - If the user specifies a destination folder, move the same document there after editing.

## Workflow

Follow these steps in order.

### Step 1: Inspect the input

Ask the user for the file(s) if they haven't provided them. Acceptable inputs:

- A single PDF file
- A Markdown file (`.md`) with an optional `images/` folder
- A folder containing either of the above

### Step 2: Create the workspace

Run the workspace organizer:

```bash
python /Users/fullstop/.agents/skills/doc-translator-zh/scripts/organize_workspace.py --root ./doc-translator-workspace --git-init
```

Then copy the original input(s) into `./doc-translator-workspace/input/`.

Use this exact workspace root unless the user specifies another location.

### Step 3: Convert PDF to Markdown and page images (if needed)

If the input is a PDF, run the MinerU extractor:

```bash
python /Users/fullstop/.agents/skills/doc-translator-zh/scripts/extract_pdf.py \
  --pdf ./doc-translator-workspace/input/<file>.pdf \
  --output ./doc-translator-workspace/output/raw
```

Then render every PDF page to a 300 DPI PNG image so you (or a subagent) can verify uncertain formulas, figures, or text against the original page:

```bash
python /Users/fullstop/.agents/skills/doc-translator-zh/scripts/pdf_to_images.py \
  --pdf ./doc-translator-workspace/input/<file>.pdf \
  --output ./doc-translator-workspace/output/pdf_pages \
  --dpi 300
```

This produces:

- `output/raw/<basename>.md`
- `output/raw/images/` directory with extracted images
- `output/pdf_pages/page_001.png`, `page_002.png`, ... for every page of the PDF

If the input is already Markdown, copy it (and its images folder, if any) into `output/raw/`.

### Step 4: Decide single-agent vs agent-team

Use an **agent team** when any of the following is true:

- The document has more than ~20 pages or ~10,000 words.
- It contains more than ~50 formulas, figures, or tables.
- The user explicitly asked for thorough/careful translation.
- There are many uncertain terms that need cross-verification.
- A single pass would take too long or exceed context limits.

For **single-agent** translation, proceed directly to Step 5.

For **agent-team** translation, split the document into logical chunks (sections, chapters, or 3,000–5,000 word blocks). Dispatch one subagent per chunk with identical instructions. After all subagents return, merge their outputs in order, normalizing headings and image references.

For careful Feishu delivery, also use a **read-only review subagent** after the main merge/write step. The review subagent should not edit files or Feishu directly. It should inspect the final Markdown and/or fetched Feishu XML and report remaining pseudo-structures, formula issues, image/caption issues, heading problems, and missing native formatting.

### Step 5: Translate and clean the Markdown

Translate the raw Markdown into Chinese. Do not just translate word-by-word. Apply all of the following:

1. **Terminology accuracy**: Use industry-standard Chinese terms. For ambiguous technical terms, search the web or cross-check with authoritative sources.
2. **OCR error correction**: Be skeptical of the source. Fix:
   - Missing or duplicated formula numbers (e.g., "式1" and "式3" but no "式2").
   - Broken heading levels.
   - Misplaced line breaks inside paragraphs or formulas.
   - Garbled characters or wrong punctuation.
   - Repeated page headers, footers, or watermarks.
3. **Verify against PDF page images**: When you encounter any of the following, open the corresponding `output/pdf_pages/page_XXX.png` and compare with the extracted Markdown:
   - A formula that looks suspicious, has unbalanced delimiters, or whose numbering conflicts with the text.
   - A figure, table, or diagram whose caption or content seems unclear.
   - Any text that appears garbled or inconsistent with surrounding context.
   - A claim that contradicts what you see in the rendered page.
   Fix the Markdown based on what you see in the page image.
4. **Formula standardization**:
   - Use standard Markdown math syntax.
   - Inline math: `$...$`
   - Block math: `$$...$$`
   - Ensure every displayed formula that should be numbered actually has a correct number.
   - Fix OCR-induced LaTeX errors (e.g., `\alpha` becoming `a`, missing backslashes, unbalanced braces).
   - Never wrap mathematical formulas in fenced math code blocks or in Feishu `<pre><code>...</code></pre>`.
   - Keep formula numbers attached to the formula body; do not leave `\tag{...}` or equation numbers as separate paragraphs.
5. **Image handling**:
   - Preserve all image references exactly as they appear, including the relative path (e.g., keep `images/fig1.png`, do not rewrite it to `fig1.png`).
   - Make paths relative to the Markdown file.
   - Verify that every referenced image file exists.
   - In Feishu output, ensure images are centered and sized appropriately.
   - Copy images so that the original relative structure still resolves.
   - In Feishu output, do not leave importer residue such as `图像 N. images/...` or redundant captions like `图像 N. 图 X.`.
6. **Heading hierarchy**:
   - Start with `#` for the document title.
   - Use `##` for major sections, `###` for subsections, etc.
   - Do not skip levels (e.g., do not jump from `##` to `####`).
7. **Remove OCR clutter**: Delete page numbers, repeated headers/footers, stray watermark text, and meaningless separator lines.
8. **Standard Markdown**: Do not use HTML for images, formulas, or layout unless necessary for Feishu compatibility.

Write the translated result to:

```
./doc-translator-workspace/output/<basename>_zh.md
```

Copy the images folder next to it:

```
./doc-translator-workspace/output/images/
```

### Step 6: Automated review

Run the reviewer script:

```bash
python /Users/fullstop/.agents/skills/doc-translator-zh/scripts/review_md.py \
  --md ./doc-translator-workspace/output/<basename>_zh.md \
  --images ./doc-translator-workspace/output/images
```

Address every issue reported. Common fixes:

- Broken image paths → update references or move images.
- Heading level skips → re-level headings.
- Unbalanced math delimiters → fix `$` / `$$` pairs.
- Missing formula numbers → insert or renumber.
- Detected OCR noise → remove it.

If a reported issue involves a formula or figure, cross-check the relevant `output/pdf_pages/page_XXX.png` before deciding on the fix.

### Step 7: Ask about Feishu output

If the user has not already specified, ask:

> 你想把结果怎么处理？
> 1. 生成飞书文档（推荐，图片和公式渲染更稳定）
> 2. 上传原始 Markdown 文件到飞书
> 3. 不要飞书，只要本地文件

#### Option 1: 生成飞书文档

When creating a Feishu document, the output must follow Feishu-native formatting. Read `references/feishu-formatting.md` first, then prepare the content.

Also read `references/feishu-config.md` for the default output folder. Unless the user explicitly asks for a different location, create the Feishu document in the default folder:

- **Default folder**: `标准&论文`
- **Folder token**: `BXaMfawkhlGHfTdIkaNcQhlRnWc`

Key rules:

1. **Document title**: Must be the only top-level heading at the very start (`# 标题` in Markdown or `<title>标题</title>` in XML).
2. **Heading numbering**: Add explicit numbering to all section headings (e.g., `## 1 引言`, `### 1.1 背景`). Do not rely on Feishu's auto-numbering toggle.
3. **Lists**: Use `-` for unordered lists and explicit `1. 2. 3.` for ordered lists.
4. **Formulas**: Keep standard Markdown math (`$...$` / `$$...$$`); do not convert formulas to images.
   - Do not convert formulas to code blocks.
   - When writing Feishu XML, inline/table-cell formulas should use `<latex>...</latex>` rather than raw `$...$`.
5. **Images**: Center them and set a reasonable width. Prefer XML `<p align="center"><img .../></p>` when precise control is needed.
   - When fixing a Feishu image caption, remember that the caption is an `<img>` attribute, not ordinary paragraph text. `str_replace` may not update it.
   - To fix a caption, preserve the image resource attributes (`src`, `href`, `name`, `width`, `height`, etc.) and use a targeted `block_replace` for that image block.
6. **Tables**: Use standard GFM tables or XML tables.

#### Feishu native structure QA

After creating or updating a Feishu document, fetch the final XML and audit native structure:

```bash
lark-cli docs +fetch --api-version v2 \
  --doc <doc_token_or_url> \
  --detail with-ids \
  --doc-format xml \
  --json > ./doc-translator-workspace/script/final_feishu_fetch.json
```

Check and fix all of the following before final delivery:

- **No formula code blocks**: `<pre>` should be `0` unless the original document truly contains code.
- **Images**: Image count should match expectations; no caption should contain `images/...`, `图像 N. images/...`, or redundant `图像 N. 图 X.` prefixes.
- **Lists**: Real lists should be `<ul>/<ol>/<li>`, not paragraphs beginning with `- `, `\- `, or `• `.
- **Tables**: Row/column data such as acknowledgements, abbreviation lists, table/figure lists, and tables of contents should be native `<table>`, not dot leaders (`.....`) or many `<br/>` lines in a paragraph.
- **Formulas in tables**: Table cells should not contain raw `$...$`; convert them to `<latex>...</latex>`.
- **Empty containers**: Remove empty `<blockquote>`, placeholder image paragraphs, and temporary appendices.
- **Headings**: Verify heading levels and remove accidental outline pollution from low-level calculation labels. Keep explicit chapter numbers in heading text unless the user explicitly asks otherwise.

If a read-only review subagent was used, compare its report against this checklist and resolve every confirmed issue.

Prepare the Feishu-ready content with the helper script:

```bash
python /Users/fullstop/.agents/skills/doc-translator-zh/scripts/feishu_output.py \
  --md ./doc-translator-workspace/output/<basename>_zh.md \
  --images ./doc-translator-workspace/output/images \
  --mode create_doc \
  --number-headings
```

The script produces a self-contained folder under `output/feishu_ready/` with numbered headings and resolved image paths. Then invoke the `lark-doc` skill to create the Feishu document from the prepared content, using the default folder token:

```bash
lark-cli docs +create --api-version v2 \
  --parent-token BXaMfawkhlGHfTdIkaNcQhlRnWc \
  --doc-format markdown \
  --content "$(cat ./doc-translator-workspace/output/feishu_ready/<basename>_zh.md)"
```

> Note: The exact `lark-doc` invocation may vary; pass `--parent-token BXaMfawkhlGHfTdIkaNcQhlRnWc` to place the document in the default folder.

#### Option 2: 上传原始 Markdown 到飞书

For raw Markdown upload, still run `feishu_output.py` without `--number-headings` to ensure image paths are valid and images are collected in one place. Then upload the prepared folder.

#### Option 3: 不要飞书

Skip Feishu output and finalize the local workspace.

### Step 8: Clean up intermediate files

After translation, review, and Feishu output are all complete, clean up intermediate files to save disk space:

```bash
python /Users/fullstop/.agents/skills/doc-translator-zh/scripts/cleanup_intermediates.py \
  --workspace ./doc-translator-workspace
```

This removes:

- `output/raw/` — raw MinerU extraction output
- `output/pdf_pages/` — temporary PDF page images used for verification
- obvious temporary files in `script/` (`*.log`, `temp_*`, `chunk_*`, etc.)

It keeps:

- `input/` — original source files
- `output/<basename>_zh.md` — final translated Markdown
- `output/images/` — extracted/used images
- `output/feishu_ready/` — prepared Feishu output (if created)
- `script/summary.txt` and other non-temp files

Use `--dry-run` first if you want to see what would be deleted:

```bash
python /Users/fullstop/.agents/skills/doc-translator-zh/scripts/cleanup_intermediates.py \
  --workspace ./doc-translator-workspace --dry-run
```

### Step 9: Finalize the workspace

Ensure the workspace contains:

- `input/` — original files
- `output/` — final Chinese markdown + images (and Feishu-ready folder if requested)
- `script/` — final logs, summaries, and reports

The `output/raw/` and `output/pdf_pages/` directories should have been removed by the cleanup step.

Report to the user:

- Path to the final Markdown file
- Path to the images folder
- Any OCR issues found and fixed
- Feishu link (if created)
- Whether the Feishu document was created or an existing document was modified in place
- Destination folder or confirmation that the document was moved, if applicable
- Final Feishu QA counts when Feishu output was requested:
  - image count
  - table count
  - list count
  - formula/latex count
  - code block (`pre`) count
  - remaining pseudo-structure count (`.....`, long `<br/>` paragraphs, raw table `$...$`, image caption residue)
- Any remaining ambiguities the user should review

## Bundled scripts

| Script | Purpose |
|--------|---------|
| `scripts/organize_workspace.py` | Create `input/`, `output/`, `script/` folders; optionally init git |
| `scripts/extract_pdf.py` | Call `mineru-open-api extract` on a PDF |
| `scripts/pdf_to_images.py` | Render every PDF page to a 300 DPI PNG image |
| `scripts/review_md.py` | Automated checks for headings, images, formulas, OCR noise |
| `scripts/feishu_output.py` | Prepare Markdown + images for Feishu create or upload |
| `scripts/cleanup_pdf_pages.py` | Remove temporary PDF page images |
| `scripts/cleanup_intermediates.py` | Remove all intermediate files after task completion |

## Quality principles

- **Suspect the source**: OCR output is often wrong. Verify structure and content against the rendered PDF page images or your own reasoning.
- **Verify visually**: When a formula, figure, or paragraph looks suspicious, open the corresponding `output/pdf_pages/page_XXX.png` and compare it with the extracted Markdown.
- **Be consistent**: Maintain a terminology glossary for repeated terms, especially technical ones.
- **Preserve structure**: Keep the original document's logical structure; do not flatten headings or reorder sections without reason.
- **Make formulas render**: A formula that looks wrong in the source must be fixed so it renders correctly.
- **Images must work**: Every image reference must resolve, both locally and in Feishu output.

## Example

**User**: "帮我把这篇论文 PDF 翻译成中文，然后传到飞书上。"

**Your actions**:

1. Create `./doc-translator-workspace/` with `input/`, `output/`, `script/` and run `git init`.
2. Copy the PDF to `input/`.
3. Run `extract_pdf.py` to get `output/raw/paper.md` and `output/raw/images/`.
4. Run `pdf_to_images.py --dpi 300` to create `output/pdf_pages/page_001.png`, etc.
5. Because the paper is long and has many formulas, dispatch 3 subagents to translate sections in parallel.
6. When a subagent finds an uncertain formula, it opens the relevant `output/pdf_pages/page_XXX.png` to verify.
7. Merge results into `output/paper_zh.md` and copy images to `output/images/`.
8. Run `review_md.py`, fix 2 broken image paths and 1 missing formula number.
9. Ask the user: "生成飞书文档还是上传 md？" User chooses "生成飞书文档".
10. Run `feishu_output.py --mode create_doc --number-headings`, then use `lark-doc` with `--parent-token BXaMfawkhlGHfTdIkaNcQhlRnWc` to create the Feishu document in the default folder.
11. Run `cleanup_intermediates.py` to remove `output/raw/`, `output/pdf_pages/`, and temporary files in `script/`.
12. Report the final file paths and Feishu link.

## Troubleshooting

- `mineru-open-api extract` fails with auth error → remind the user to set `MINERU_TOKEN` or run `mineru-open-api auth`.
- Images are missing after MinerU extraction → check `output/raw/images/` and update Markdown references to relative paths.
- Review reports unbalanced math → fix delimiter pairs before continuing.
- Feishu upload fails → verify `lark-cli` authentication and image file sizes.

## Feishu upload optimization

When uploading to Feishu, prefer fast, parallel, token-based workflows.

### Do this

1. **Upload images in parallel**
   - Use `dispatching-parallel-agents` or multiple `Task` calls to upload images to the target Feishu Drive folder at the same time.
   - Collect `file_token` for each image into a single `image_token_map.json`.

2. **Replace all image references at once**
   - After upload, run one regex pass over the Feishu-ready Markdown:
     - Replace `src="images/xxx.jpg"` with `src="FILE_TOKEN"`.
     - Replace `](images/xxx.jpg)` with `](https://my.feishu.cn/file/FILE_TOKEN)` if using Markdown-style links.
   - Validate that no local `images/` paths remain.

3. **Pre-validate locally before overwrite**
   - Run `review_md.py` on the Feishu-ready Markdown before calling `lark-cli`.
   - Check: every image has a token, headings are intact, formulas are balanced, tables have separators.

4. **Use file tokens, not public URLs**
   - Use `<img src="FILE_TOKEN"/>` in Markdown/XML.
   - Do **not** use `https://my.feishu.cn/file/FILE_TOKEN`; Feishu document servers reject these with HTTP 444.

5. **Prefer XML format for complex documents**
   - If the document has many images, tables, formulas, or needs precise layout, create/update with `--doc-format xml`.
   - This avoids Markdown-to-Feishu round-trip ambiguities.

6. **Use incremental updates when possible**
   - If only images or a single section changed, use `docs +update --command append` or `block_replace` instead of `overwrite`.
   - Overwrite only for the final full draft.

### Avoid this

- Fixing image paths one by one in the editor.
- Fetching the document repeatedly after every small change.
- Uploading images serially in a loop.
- Creating a new Feishu document when the user gave you an existing URL/token; modify in place instead.
