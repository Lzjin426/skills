# Better Md Writer Local Defaults: Fullstop Obsidian

Apply this file only when the output is meant for Fullstop's local knowledge base or Obsidian workflow.

## Vault defaults

- If the user does not specify another location, documents, HTML files, and similar outputs should be stored in `Desktop/Fullstop_base`.
- Daily and weekly notes default to `Fullstop_base/03-note`.
- Images and attachments default to `Fullstop_base/Attachments`.

## Obsidian workflow

- Use Obsidian as the default reader and validation surface when the output belongs in the vault.
- Prefer the `obsidian` CLI as a practical way to open or inspect vault content when it fits the task.
- Obsidian-specific behavior is a local default, not a global writing rule.

## Local Markdown preferences

These are Fullstop defaults, not hard rules for every document:
- for documents written into Fullstop's vault, prefer explicit hierarchical numbering in headings by default:
  - level 1: `# 1. Heading`
  - level 2: `## 1.1 Heading`
  - level 3: `### 1.1.1 Heading`
- keep numbering continuous and structurally correct; do not mix numbered and unnumbered headings at the same depth without a clear reason
- concept-oriented knowledge-base articles should also use numbered semantic headings unless the target document already has a conflicting house style
- top-level `---` separators can be used when they improve readability in longer vault notes
- images should use stable, readable names
- frontmatter should store structural metadata, not mass link declarations
- do not use frontmatter wiki-links such as `related: [[...]]` or long `related` lists to create graph edges
- if relationship metadata is needed, prefer plain-text structural fields such as `note_type`, `layer`, `prerequisites`, and `next`
- keep actual wiki-links in body content, and only add them when they express a meaningful semantic relationship for readers

## Excalidraw embed syntax

When embedding Excalidraw content in Obsidian, use:

```markdown
![[filename.excalidraw.md|800|center]]
```

Use `center` for centered display. The default width is `800` unless the user asks otherwise.
