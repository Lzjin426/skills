# Learning Goal And Teaching Route

Read `guided-learning` when designing the learning route. Use its goal adaptation, prerequisite diagnosis, and document-anchored teaching; do not copy its entire conversational template into every article. Locate companion skills through the available skill catalog; Fullstop's personal skill source is `~/.skillsbase/skills`, not the deprecated `~/.agents/skills`.

Within this document workflow, use encyclopedia checks when names, scope, or prerequisites need clarification. Sufficient supplied material does not require extra Wikipedia/Baidu searches merely to fill a checklist. Follow the user's browsing constraints; verify current or uncertain claims when required. This adapts the companion skill's encyclopedia-baseline routine without weakening technical source checks.

## Establish The Finish Line

Infer known context first. If the learning goal is missing and changes the document, ask one concrete question, for example: “这次希望读完能解释基本概念、理清整套计算关系，还是独立完成一次计算并判断结果？” Adapt the choices to the actual topic.

Use outcomes rather than length or labels such as “comprehensive”:

| Outcome | What the document must enable | Possible check |
| --- | --- | --- |
| Understand a concept | Explain the problem, intuition, necessary terms, and one example | Explain the idea in the reader's own words and distinguish a nearby concept |
| Follow a method | Trace known inputs through intermediate steps to outputs, with reasons for the order | Explain where each input comes from and why an iteration or branch is needed |
| Apply independently | Choose applicable conditions, perform the method, and interpret the result | Complete a worked task and identify a case where the method should not be used |

These are flexible outcomes, not mandatory tiers. The user may need one difficult step explained deeply and the rest only mapped. If the goal is already explicit, summarize the inferred boundary briefly and proceed without another intake question.

Before drafting, keep a compact internal brief: target task, current knowledge, prerequisites required now, scope deferred, and how completion will be checked. Do not force the user to approve a formal brief unless they requested a planning checkpoint.

## Choose Document Boundaries And Reading Order

Before drafting, the main agent decides whether one document is enough or a connected set would be easier to learn from and revisit. Respect an explicit request for a single document or a fixed scope. A narrow concept or tightly connected task usually stays together; split when there are distinct learning questions, prerequisite levels, or independently useful reference topics. Do not split by fixed word counts, heading counts, source-file boundaries, or the number of agents.

For a set, briefly tell the user the estimated document count, each document's core question or outcome, and the recommended reading order. Use a short paragraph or compact list, not a mandatory planning form. This is a working estimate, not a quota: revise it when research reveals a better boundary, and briefly explain a material change. Do not add an approval checkpoint unless the user requested one.

Each document should teach a connected unit and state any prerequisite reading. Keep shared terminology, notation, and a running example consistent across the set. Put the main explanation in one place and cross-link it where needed, with enough local context to avoid needless back-and-forth. Do not scatter a calculation chain so widely that readers must reconstruct its order; preserve an overview and at least one connected worked path when the goal requires it. An overview may live in the first document; a separate index is optional.

Set the pace from the reader's starting knowledge: establish the overall picture, explain needed concepts, then develop the method and application where relevant. These are flexible teaching moves, not required separate documents. Slow down at difficult transitions and defer optional branches. The document count follows the learning route, rather than determining it.

## Teach A Connected Unit

Start with the problem and the smallest useful picture. Introduce abstract terms through a concrete example, then explain the method before expecting a numerical example to make sense. Keep one running example where it helps.

Choose the running example for the distinction it reveals, not just convenient arithmetic. Symmetry, equal magnitudes or another special case can conceal why two quantities or methods differ. Add a small contrasting case when that distinction matters; do not multiply examples when the existing one already exposes it. Review should test the distinction, not merely recalculate the chosen numbers.

For each learning step, explain what question it answers, what the reader already knows, what changes, and why the next step follows. Spend detail at the likely blocker rather than distributing equal space to every heading. Defer side branches, but retain conditions whose omission would make the explanation misleading.

For a physical mechanism, establish what the relevant object and parts are before expecting the reader to interpret an abstract section or equation. For a mathematically dense explanation, keep the mechanism, essential equation and interpreted result on the main route; place optional derivations in a clearly marked advanced section, appendix, or supported collapsible block. This is a pacing choice, not a fixed chapter template. Keep important conditions near the affected claim and consolidate repeated general warnings without deleting necessary distinctions.

Apply the established note style in `SKILL.md` directly; existing notes are not required to infer style anew. Read supplied or relevant notes when they contain task material, known prerequisites, or gaps in understanding. They are not an authority for technical claims; check suspicious wording or arithmetic against the source before adopting it.

## Standards And Calculation Chains

Read the actual supplied standard, relevant parts, edition, and example before transferring formulas. Do not reconstruct inaccessible normative content from search snippets or memory. If critical source pages are unavailable, teach the verified portion and state what is needed to complete the chain.

Map the chain before individual equations:

- Given geometry, loads, operating conditions, and material properties.
- Trial assumptions, derived operating values, and values looked up from tables.
- Sequential dependencies and parallel branches.
- Iterations: why an initial guess is needed, what is recomputed, the update rule, and a justified stopping tolerance.
- Final outputs and the separate applicable limits used to judge them.

When feedback between systems is central to the learning goal, carry the same example through at least one update: show what output changes which input, which relationships must be recomputed, and how the new result returns to the preceding system. State whether intermediate values were calculated, looked up, measured, or supplied as illustrative model outputs. A separate simplified iteration can teach numerical updating, but does not by itself demonstrate the original coupled mechanism. Do not invent a solver or unverified values to close the example; identify the needed model or supplied inputs and match the claim to the demonstrated scope.

For each formula, make its purpose, symbols, units, assumptions, and source locator identifiable. Define shared notation once and use a connected example to interpret related equations; avoid repeating the same symbol glossary and numerical demonstration at every formula. Explain table selection and interpolation rather than merely saying “look up the coefficient.” Define subscripts and primes that change the meaning. Distinguish numerical convergence from passing a design check.

For a document teaching independent calculation, verify at least one connected worked example. Use supplied data or clearly labeled teaching assumptions, choose a rounding/interpolation tolerance before comparing results, and show discrepancies rather than adjusting numbers to match a claimed answer. A narrower explanation can verify only its current calculation stage and must not imply the full method was validated.

## Check Learning Without Forcing An Exam

Include a small task with a reference answer or solution criteria when it helps the goal. Do not repeatedly interrupt drafting to demand answers from the user.

During review, attempt the agreed task using only the document and its explicitly required inputs. If a necessary definition, coefficient source, step, or interpretation must be invented, repair that gap or mark the output incomplete. An agent completing the task is a document adequacy check; it does not prove the human reader has learned it.
