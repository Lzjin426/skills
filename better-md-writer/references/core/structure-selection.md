# Better Md Writer Core: Structure Selection

Use this file after the document job is clear and the profile has been chosen.

## 1. Choose the primary carrier

Pick the main form that should carry understanding:
- **paragraph-led** for explanation, reasoning, and continuous interpretation
- **list-led** for short parallel points, steps, or checklists
- **table-led** for stable side-by-side comparison
- **diagram-led** only when a visual truly explains faster than prose
- **mixed** when one main carrier needs light support from another

Do not let lists replace explanation or let tables replace judgment.

## 2. Structure before sentences

Draft the outline before polishing prose:
- Decide the major sections first.
- Put the highest-value or highest-uncertainty section early.
- Leave introductions and summaries until the core is stable if needed.
- Keep related ideas close together.

If the structure is right, sentence-level editing becomes much easier. If the structure is wrong, sentence polish will not save the document.

For knowledge-base writing, do not begin from heading wording alone. First decide:
- what subtype this article belongs to
- what judgment question the article must answer
- what visual anchor the reader will need

## 3. Optimize for comprehension first

When the topic is technical or abstract:
- explain the idea in plain but precise language before leaning on terminology
- introduce symbols, variable names, API names, or code identifiers only after the reader knows what role they play
- show the concrete artifact, output, or visual shape early when it reduces confusion

Use plain but precise language. Avoid both unexplained jargon and overly casual teaching tone.

## 4. Use the simplest shape that fits

Choose based on content function:
- Use a **heading** for a real module that can stand on its own.
- Use a **short paragraph** when one compact block already does the job.
- Use a **list** when items are parallel and brief.
- Use a **table** when the reader must compare across the same dimensions.
- Use a **diagram** only when it materially lowers explanation cost.

Avoid fragmenting the page with decorative headings or stacks of tiny lists.

For knowledge-base writing:
- use semantic section titles that describe content, not spoken hooks
- avoid headings that read like narration, coaching, or presentation copy
- prefer a short orienting paragraph over a highlighted slogan when opening a section

## 5. Keep a through-line

Each section should answer one natural question raised by the previous section.

For explanation-heavy writing:
- start with the reader's most immediate question
- move from "what is it" to "what does it look like" to "how do I read it" to "how does it work" when that order lowers friction
- collapse thin sections instead of producing many top-level headings with very little content

For medium-length knowledge-base articles, `3-5` top-level sections is usually a better default than `8-10` tiny ones.

Every knowledge-base article should answer at least one judgment question, such as:
- how do I identify this thing?
- how do I distinguish it from nearby concepts?
- how do I read this output correctly?
- how do I place this back into the current project or workflow?

Every knowledge-base article should also establish at least one visual anchor, even if the visual is later represented only as a candidate marker.

Low understanding cost does not mean casual wording. A knowledge-base article should read like a clear internal reference, not a spoken lesson transcript.

## 6. Keep Markdown portable

Default to standard Markdown:
- use clear headings only when needed
- use fenced code blocks with language tags
- use meaningful link text
- use emphasis sparingly and intentionally
- use environment-specific syntax only when compatibility is clear

Style rules such as numbered headings or top-level separators belong to the selected profile or local environment defaults, not to every document automatically.

When the target is Fullstop's knowledge base or Obsidian vault, prefer explicit hierarchical heading numbers such as:
- `# 1. ...`
- `## 1.1 ...`
- `### 1.1.1 ...`

Keep the numbering aligned with the actual outline. If the numbering becomes awkward, the outline is usually wrong and should be simplified before drafting further.

## 7. Split only when it helps

Consider splitting into multiple documents when:
- the content contains multiple independently readable topics
- one file is becoming hard to scan or maintain
- different readers need different slices of the material

When splitting:
- make each document self-contained
- use relative links between documents
- give each link a short explanation of what it contains
