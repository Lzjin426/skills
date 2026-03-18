# Better Md Writer Reference: Markdown Style

This file captures Fullstop's Markdown layout rules. Use it as the default formatting baseline for all documents unless the user explicitly asks for a different convention.

## 1. Core Principle

- Let the Markdown structure serve the content.
- Keep the document clean, compact, and sharp.
- Treat the rule as a readability tool, not as decoration.

## 2. Heading Rules

### 2.1 Main Title

- Treat the external document title and the in-body heading hierarchy as separate layers.
- When the document title is already carried by the host system, the Markdown body should still begin with the first-level heading of the actual content, such as `# 1. Section`.
- Do not insert an extra in-body document title by default.
- Do not assume the external system title, note title, file list, or UI chrome can replace the body's first-level heading.
- Only omit the first-level heading when the user explicitly asks for a platform-specific template or a title-less fragment.

### 2.2 Numbered Hierarchy

- When headings need to show hierarchy, use numbered headings.
- Preferred patterns:
  - `# 1. xxx`
  - `## 1.1 xxx`
  - `### 1.1.1 xxx`

### 2.3 Avoid Mechanical Heading Expansion

- Do not force an extra heading level when the section contains only a tiny amount of content.
- If the content is only a few parallel points, steps, or short notes, use a list or short paragraph instead.

## 3. Choose Between Heading, List, and Paragraph

### 3.1 Use a Heading When

- The content is an independent module.
- The section is likely to grow later.
- The document needs a clear visual partition.

### 3.2 Use a List When

- The content is a small group of parallel points.
- The content is a sequence of steps.
- Each item is short.
- Adding a heading would make the document feel fragmented.
- The list is compressing already-understood structure, not replacing necessary explanation.

### 3.3 Use a Short Paragraph When

- One sentence or one short block already explains the point well.
- Splitting into headings or lists would add noise.

### 3.4 Prefer Paragraphs for Explanation-Heavy Writing

- In research notes, explanation-heavy documents, and principle analysis, paragraphs should usually carry the main reasoning.
- Let lists support paragraphs, not replace them.
- If a reader needs to follow a chain of ideas, prefer continuous prose before introducing lists, tables, or diagrams.

## 4. Blank Line Rules

- Use blank lines only at paragraph ends, module switches, or meaningful semantic changes.
- Do not alternate content lines and blank lines mechanically.
- Do not add meaningless blank lines between a heading and a child heading or between a heading and an immediately following code block.
- Keep one blank line between a heading and a following paragraph or list for source readability.
- When a paragraph is immediately followed by a semantically continuous list, do not add a blank line.

## 5. Standard Markdown Syntax

- Prefer standard and portable Markdown syntax.
- Apply standard forms for headings, lists, code blocks, blockquotes, links, and images.
- When formulas are needed, write them with Markdown-compatible formula syntax instead of plain text approximations.

## 6. Code Block Rules

- Use fenced code blocks for terminal commands.
- Group similar commands together when practical.
- Keep explanations after code blocks to the necessary minimum.
- Always label fenced code blocks with a language:
  - `python`
  - `bash`
  - `json`
  - `text`

## 7. Links and Images

### 7.1 Links

- Use relative paths for internal document references.
- Use standard `[text](URL)` for external links.
- Avoid meaningless link text such as "click here".

### 7.2 Images

- Store images in a nearby directory or an agreed resource directory.
- Do not scatter image files in the root directory.
- Use lowercase kebab-case names such as `gear-ratio-chart.png`.
- Add alt text when it improves understanding.
- If an image is sourced from the web, keep a note of the original source page when practical.
- Do not use images as empty decoration; each image should support comprehension, comparison, or recall.
- Prefer one useful image over several redundant ones.

## 8. Emphasis

- Use `**bold**` for key terms, major conclusions, and important cautions.
- Use `*italic*` for first-use proper terms, quotation-style phrasing, or mild emphasis.
- Use `` `inline code` `` for commands, filenames, variable names, and paths.
- Use blockquotes for quotations, short reader notes, or highlighted reminders when the rendered result stays visually clear.
- Use horizontal rules as mandatory separators between adjacent top-level sections.
- Use visual emphasis to guide reading, not to decorate the page.
- If the target Markdown environment supports color or custom callout syntax, use it only when compatibility is clear and the benefit is real.
- Prefer one strong emphasis signal over several mixed ones in the same paragraph.
- Outside the mandatory separators between top-level sections, do not overuse horizontal rules; too many extra separators will fragment the page and weaken structure.
- Avoid stacking multiple emphasis styles in the same sentence.

## 9. Tables

- Use tables for structured comparison or parameter information.
- Do not use tables as a substitute for ordinary lists.
- Keep headers concise and alignment readable.
- If a table grows beyond five columns or becomes too verbose, split it or switch format.
- Introduce a table with a framing sentence so the reader knows what to compare and why.

## 10. File Naming

- Use either Chinese or English names, but keep style consistent within the same category.
- Keep file names as short as possible while still expressing the topic clearly.
- Avoid special characters such as `/`, `\\`, `:`, `*`, and `?`.

## 11. Common Failure Modes

- Heading density is higher than content density.
- The document sacrifices readability for a fake sense of formality.
- The writer over-formats instead of improving content.
- The Markdown source becomes visually noisy because of excessive blank lines.
- The document becomes a stack of cards instead of a continuous explanation.
- Several short lists appear back-to-back where one connected paragraph would read better.
- Tables or diagrams are inserted without enough prose to explain their role.

## 12. Extended Syntax

Use extended Markdown syntax when the target environment supports it and the benefit is clear.

### 12.1 Callouts and Admonitions

When the environment supports GitHub-style, Obsidian-style, or similar callout syntax:

```
> [!NOTE] Useful information
> > [!TIP] Practical suggestion
> > [!WARNING] Warning
> > [!CAUTION] Important caution
> > [!IMPORTANT] Critical information
```

Use callouts sparingly. Not every paragraph needs a colored box.

### 12.2 Highlights

When supported (e.g., Obsidian's `==highlight==` syntax), use highlights for:
- Key phrases in long summaries
- Critical warnings in configuration sections
- Temporary markers for content that needs review

Do not highlight more than 5% of the text.

### 12.3 Task Lists

Use task lists for checklists, action items, or verification steps:

```markdown
- [ ] Todo item
- [x] Completed item
- [ ] Sub-item
```

Use for practical tasks, not for general content.

### 12.4 Color and Custom Styling

Use color or custom styling only when:
- Compatibility with the target environment is guaranteed
- The styling serves a clear functional purpose (warnings, categories, status)
- The benefit outweighs the portability cost

Avoid using non-standard syntax in documents that may be viewed in multiple Markdown renderers.

## 13. Reading Rhythm

Design the document's visual flow to guide the reader through the content naturally.

### 13.1 Section Separators

Use horizontal rules (`---`) between every adjacent pair of top-level sections as a default hard rule.

This means:
- After each completed top-level section, insert `---` before the next top-level section.
- Apply this rule even in shorter documents.
- Do not add extra horizontal rules inside a top-level section unless there is a strong readability reason.

### 13.2 Pacing with Content Density

Alternate between dense and light content:
- Follow a long, dense paragraph with a short paragraph or list
- Follow a complex explanation with a concrete example
- Follow multiple lists with a connecting paragraph
- Follow a table or diagram with a brief summary

Let the document breathe. Do not pack everything tightly.

### 13.3 Semantic List Usage

Choose list types based on meaning:

- **Ordered lists**: Sequential steps, prioritized items, ranked criteria
- **Unordered lists**: Parallel points, features, options without order
- **Nested lists**: Hierarchical relationships (maximum 3 levels)
- **Task lists**: Action items, verification steps, checklists

Do not use numbered lists when order does not matter. Do not use bullet points for sequential steps.

### 13.4 Code Block Context

Provide context for code blocks:

- **Before**: One sentence explaining what the code does or why it's needed
- **After**: Key caveats, expected output, or dependencies (if non-obvious)
- **Inside**: Inline comments for complex logic

Avoid uncommented code blocks in explanation-heavy documents.

### 13.5 Link Usability

Make links reader-friendly:

- Use descriptive link text, not bare URLs
- For external links, consider adding an icon or prefix (📎, 🔗, 📖) when appropriate
- Group related links together instead of scattering them
- For important destinations, repeat the link in context

Example:
```markdown
See the [API documentation](https://example.com/api) for details.
```

Not:
```markdown
Click https://example.com/api for details.
```

### 13.6 Table Readability

Keep tables accessible and scannable:

- Use **bold** for headers to distinguish them from content
- Keep column width reasonable; split wide tables
- Add a framing sentence before the table explaining what to compare
- For complex data, consider whether a diagram would be clearer

### 13.7 Paragraph Length

Keep paragraphs focused:

- **Ideal**: 3-5 sentences for most paragraphs
- **Maximum**: 8 sentences for complex explanations
- **Break**: When shifting to a new subtopic
- **Connect**: Use transition phrases between paragraphs

If a paragraph exceeds 10 lines, consider splitting it.
