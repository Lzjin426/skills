---
name: code-mode
description: "Use for end-to-end software development that should begin with project understanding and current external calibration, then choose the implementation, model, and any delegation adaptively to minimize total time, usage, and rework."
---

# Code Mode

Deliver the smallest product change that solves the user's actual problem and passes complete verification. Optimize for total completion time, total usage, and first-pass quality rather than model price, agent count, or activity volume.

## Main-Agent Ownership

The main agent owns requirement clarification, product and technical decisions, planning, user communication, integration, code review, and final acceptance. Keep work in the main agent whenever continuous understanding of the product, repository, and prior decisions is likely to improve speed or correctness.

Subagents may collect evidence or execute bounded work, but they do not decide unresolved product or architecture questions. The main agent remains responsible for every conclusion and inspects the underlying evidence whenever it materially affects a decision.

## 1. Understand the Problem and Project

Before proposing an implementation:

- identify the user outcome, current friction, acceptance criteria, and important failure states;
- inspect the applicable `AGENTS.md`, repository structure, existing behavior, tests, dependencies, conventions, reusable components, and prior decisions;
- distinguish a missing feature from a symptom of a deeper product or technical problem;
- prefer the smallest solution that fits the existing system unless current evidence justifies a larger change.

Ask a focused question only when the missing answer would materially change the result. Otherwise state the smallest safe assumption.

## 2. Calibrate Against the Outside World

For a new feature, perform external calibration before choosing the solution whenever there is a meaningful technology, architecture, dependency, API, security, or user-experience decision.

Check the most decision-relevant current evidence:

- official documentation, release notes, compatibility limits, deprecations, and security guidance;
- maintained open-source implementations of the same technical problem;
- current behavior of comparable products that solve the same user problem;
- established architecture or interaction patterns, including known failure modes.

Separate product references from implementation references. A comparable product may inform behavior without determining the project's technical architecture. Prefer primary sources and real current behavior; treat blog posts, examples, benchmarks, and popularity as supporting evidence rather than authority.

Compare the smallest solution compatible with the current project against credible alternatives. Judge them by project fit, maturity, maintainability, migration cost, performance, security, reversibility, and ecosystem health. Novelty alone is not a reason to adopt a technology, and familiarity alone is not a reason to keep an inferior approach.

Keep research proportional to the decision. A localized fix or mechanical edit with no meaningful product or technical choice does not need broad external research. Stop when enough current evidence supports a decision; do not search merely to accumulate links.

## 3. Make the Decision Visible

Before writing or delegating code, present a concise proposal and wait for user approval. Include:

- the intended user outcome and acceptance criteria;
- what the project already provides and constrains;
- the useful external findings and their sources;
- serious alternatives considered, the selected direction, and its trade-offs;
- affected files or components, data or control flow, and validation;
- any proposed delegation boundary.

For user-facing frontend work, create and open a runnable standalone HTML prototype when interaction, navigation, information hierarchy, responsive behavior, or state handling needs a product decision. Produce multiple variants only when they represent materially different choices. Skip the prototype for non-visual or already-decided changes and state why.

## 4. Choose Execution Adaptively

Do not fix the main-agent model, subagent model, reasoning effort, or agent count in this skill. Follow explicit user choices; otherwise select them from the current environment according to task difficulty, cost of error, context needs, speed, and verifiability.

Use a subagent only when all of these are true:

- the work has an independent useful output;
- its input, boundaries, and done condition can be stated precisely;
- its result can be verified cheaply;
- delegation is expected to reduce total elapsed time or context cost after startup, coordination, review, and likely rework are included.

Use the fewest agents needed. Parallelize only genuinely independent work, keep delegation one level deep, and do not create agents merely because capacity is available. If an agent's work fails or creates substantial integration cost, reassess the task boundary or model instead of repeating the same dispatch pattern.

Before write-capable delegation, record the dirty-worktree baseline and give each executor exclusive path ownership. Reserve full-repository tests, code generation, and global formatting for main-agent integration.

Give each subagent a compact packet containing the objective, done condition, relevant paths and interfaces, preserved decisions, non-goals, owned paths, required validation, and a request for concise evidence, changed files, results, and blockers. Use fresh context when the packet is sufficient and the interface supports it; inherit conversation history only when the task truly depends on that history. State that the subagent may not spawn descendants, make undecided product or architecture choices, or modify unrelated user work.

## 5. Implement, Integrate, and Verify

Follow the accepted proposal and existing project conventions. Keep changes cohesive, avoid opportunistic refactors, and surface any newly discovered requirement or scope change before expanding the implementation.

The main agent reviews the combined diff against the approved outcome and plan, including error handling, compatibility, concurrency, security, and unintended scope. After every feature or bug fix, run the complete project test suite plus applicable formatting, static analysis, build checks, and representative manual or end-to-end verification. Fix failures and repeat the affected checks. When a prototype was approved, confirm that the shipped experience matches its decisions.

Deliver the outcome first, followed by changed files, user-visible behavior, and concrete validation results. State unavailable verification or material limitations plainly.
