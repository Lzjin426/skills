# Agent Coordination

Delegate only when user or applicable project instructions authorize it and tools are available; carry existing authorization forward instead of asking again. Fullstop wants actual role separation for substantial illustrated and complex documents. Do not create user-facing chats as substitute subagents.

## When To Delegate

- A short text-only answer or simple note can stay in the main agent.
- A document with substantive figures normally delegates visual planning/production and uses a separate reviewer for the integrated result. Being a single document is not a reason to skip these roles.
- A complex, multi-system, or multi-document explanation gets both visual assessment and outline/dependency review before full drafting, even if the main agent proposes no figures. This prevents a text-only draft from bypassing the assessment of whether visuals are needed. Check prerequisites, learning pace, system boundaries, interfaces, shared notation, and calculation order. A reviewer can inspect both the initial outline and final result while remaining separate from the author and visual producer.
- Use a research agent only for a bounded evidence task that benefits from separation. Do not create agents merely to fill roles.

Keep at most two supporting agents active. Reuse a visual agent across related figures and a reviewer across review stages; finish or close a research/visual role before adding a later role when necessary. The visual producer cannot count as the independent reviewer of its own figures.

## Roles And Ownership

| Role | Bounded task | Return |
| --- | --- | --- |
| Main agent | Own learning goal, evidence decisions, outline, figure inclusion and purpose, narrative, notation, integration, and delivery | One coherent document |
| Research agent | Search a defined slice, such as primary standards or Chinese teaching articles; read relevant sources | Verified links and locators, supported claims, gaps/conflicts, teaching and visual ideas with reuse status |
| Visual agent | Assess visual needs and propose useful figures; produce approved plots/illustrations, inspect exports and repair layout defects | Figure purposes, actual paths, runnable plotting source or editable source where relevant, checked data/relationships, and unresolved defects |
| Review agent | Check learning pace and dependencies before drafting when complex; independently attempt the final task and inspect technical claims, actual figures, and polished prose | Specific gaps, redundant/missing figures, readability and pacing defects, locations, and checks actually performed |

Keep prose ownership in the main agent. Avoid splitting ordinary chapters among writers who would independently invent notation, repeat prerequisites, or choose incompatible depth.

## Handoffs

Research receives the user's goal, scope, source material, and the exact research question. Instruct it to distinguish authoritative evidence from useful article structure; do not request a generic pile of links.

Visual work has two handoffs:

1. **Assessment:** give the learning goal, outline, relevant prose/relationships and stable notation. A suitable brief is: “阅读提纲和相关正文，主动评估哪些图能减少理解负担、帮助记忆或方便回看。每个建议说明帮助理解什么、放在哪里、适合什么表达方式和工具，以及需要哪些资料或计算结果。” Include established note style, actual capabilities and effective permissions. Let the visual agent assess the whole explanation, including physical parts, mathematical changes and relationships between systems where relevant. A main-agent sketch is a proposal to reconsider. Do not announce a script/SVG/all-editable production plan before assessment; permission to write plotting code is an available capability, not a tool preference. Do not add a figure quota or a predetermined tool unless a concrete user/task constraint warrants it. For a simple explicitly requested figure, use a direct brief.
2. **Production:** accept or decline proposals with a short teaching reason; supply verified functions/results, assumptions and labels. Approve the figure's purpose and factual constraints, leaving the visual agent responsible for tool and layout choice. When a supported proposal recommends generation, commission it through the available tool or bridge, or explicitly decline it with a concrete reason about learning value, accuracy, readability, capability or user requirements. “A schematic could also explain this” alone does not compare their benefits. Do not append a blanket “native Excalidraw first” or an extra “only if necessary” hurdle to an otherwise open brief. Uniform appearance, SVG export, or editability of unrelated figures alone is insufficient. Reassess the tool after a genuine production failure; preserve the teaching purpose rather than substituting a weaker picture.

Keep both handoffs proportional to the task; the small plan/check record can retain proposals and decisions without putting orchestration details in the article. Include the relevant `visual-policy.md` pointer in the visual handoff and `quality-rubric.md` in the review handoff so that a narrow brief does not remove the document's acceptance requirements. Pass the authorization actually effective in the current project/session and any remaining approval requirement to the assigned agent. Check actual tool availability. The skill does not grant image-generation access or broader coding permission.

Pass permission boundaries accurately: “plotting code requires approval” does not mean “only static SVG is available.” When an essential plot needs approval, describe that method and resolve the actual permission requirement rather than dropping the plot. If image generation is available only in the main agent, the visual agent still proposes its purpose and specification, then inspects the returned generated image. Once that proposal is accepted and authorized, the main agent executes the bridge as part of production rather than waiting for the subagent to prove generation indispensable. Revisit proposals when drafting adds a numerical example or exposes an unclear structure.

For early review, supply the learning goal, reader's starting knowledge, proposed document boundaries, outline, notation and dependency map. For final review, supply the assembled draft, actual final images, and relevant sources. Ask the reviewer to independently choose a few representative explanation/application questions and attempt them using the document and stated prerequisites. Include a cross-system question where relevant. Return the answers or calculation route, where the document supports them, and any step that required unstated knowledge. Do not feed it desired answers or a desired verdict. Formula recalculation alone does not establish that the explanation is connected.

Review figure correctness, usefulness and coverage separately: an existing figure may be correct while another central relationship still needs a plot, construction or diagram. Missing-figure findings must name the relationship and explain what a visual would reveal beyond prose; do not demand a count. Check prerequisite jumps, awkward pace and fragmented calculation chains as well as label/legend overlap. A renderer screenshot or actual exported image is needed for layout judgment; source/XML validity is insufficient. Do not let a reviewer silently rewrite the same file while the main agent is polishing it.

Also look for worthwhile visual additions where prose is accurate but readers must mentally reconstruct placement, successive steps or a comparison. Coverage review is not limited to essential omissions. For physical-recognition tasks, assess whether the chosen view actually helps identify the object and its working parts; correct arrows in an abstract diagram do not establish this. Preserve good schematics; do not request generation just to prove a tool was used. When native Obsidian Excalidraw is selected, production returns the plugin drawing path and the article embeds that asset directly.

For cross-system gaps, return the affected chapters/figures, the missing input/output relationship or prerequisite, and the needed bridge, assumption, unit, boundary condition, or feedback/iteration explanation. The main agent repairs concrete gaps; the reviewer records what was rechecked and whether the issue is resolved. “Improve the pace” alone is not actionable review feedback.

For physical topics, include a question that requires identifying the parts, their placement, and the motion or working path using the saved document. Where coupled iteration is central, trace at least one update from the same example through the affected parameters and back to the original system. Check whether a special-case example conceals an important distinction; use a contrasting question when needed. Merely reciting the flowchart or verifying an unrelated scalar iteration is insufficient. Distinguish an adequately explained concept from a complete numerical design; do not demand a full solver for a conceptual task.

## Sequence And Concurrency

1. The main agent establishes the learning goal and reads the supplied material.
2. If a bounded evidence task needs research help, delegate that slice while the main agent examines the backbone source or task material. Otherwise continue without a research agent.
3. Reconcile evidence and build the connected outline and shared notation. For complex documents, review the outline and dependency map before full drafting. Obtain the visual agent's assessment of the explanation before ordering final figures, and decide on its proposals. Do not let a successful first figure end this assessment.
4. Draft prose while the visual agent produces stable independent figures. Figures using calculated results wait for those results; figures depending on another figure's design wait for that design.
5. Integrate the text and figures, polish with `humanizer-zh`, and check fidelity/display. Have the independent reviewer inspect the assembled result, resolve findings, and recheck affected meaning and rendering after revisions.

Start with at most two active supporting agents, normally research plus visuals or review as the phase changes. Reuse or close agents when their task ends. The main agent should do useful non-overlapping work while delegated work runs.

Multiple images need distinct prompts and deliverables. Try a small pair of independent built-in image calls concurrently only if the active tool permits it; otherwise use sequential calls. Do not claim parallel support from a theoretical plan, tool metadata, or merely spawning two agents. Do not switch to an external image API or CLI to gain concurrency without user authorization.

## Fallbacks

- Establish a capability limitation from the tools actually exposed to the session or its available tool registry. Record what was checked before claiming no delegation tools. An unattempted call, a speculative opening statement or choosing to work alone is not evidence of tool absence. An approval or permission restriction is a different limitation and must be named accurately.
- No delegation tools or authorization: perform visual assessment and task-question checks sequentially in the main agent, state that these were self-checks, and do not claim independent review or a verified multi-agent workflow. A document can still be delivered when its substantive checks pass, with that review limitation stated; it cannot pass a workflow test specifically requiring independent agents.
- No image-generation tools on a subagent: it still owns visual proposals and can produce exact plots with an authorized available plotting runtime. For generated illustrations, let it prepare the specification; generate in the main agent, then return the actual output for its inspection. Do not silently drop the visual role.
- No built-in image generation for an essential generated illustration: report the missing capability and preserve its specification. Available Python plotting or Excalidraw can still complete their appropriate figures. Do not silently install dependencies or use another paid service. Return a clearly incomplete draft only if a required figure remains unproduced, and ask for a delivery change only when needed.
- Review finds an evidence gap: repair it from available sources or narrow the claim; additional agents cannot replace missing evidence.

## Report What Actually Ran

Keep a small check record outside the article: actual roles and handoffs, visual proposals and decisions, any tool override and its reason, attempted learning questions and resolved findings, and capability limitations. Review the briefs as well as the result: did the main agent impose an unjustified count, tool or universal source-format constraint? A delegation plan, CLI subprocess, humanizer invocation or new user-facing test chat is not evidence that supporting agents ran. Report document acceptance and workflow acceptance separately under `quality-rubric.md`; a good document does not establish that the intended collaboration occurred.
