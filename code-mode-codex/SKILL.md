---
name: code-mode-codex
description: "Use for end-to-end Codex development: delegate independently verifiable research, implementation, and testing units to GPT-5.6 Luna Max subagents, while the main agent makes decisions and accepts the integrated result."
---

# Code Mode Codex — Delegation-First Development

Treat this as a product-development mode with a delegation-first execution model. Deliver the smallest product change that solves the right user problem, is visibly testable, and is fully verified. The main agent is accountable for the result, but it must not become the default explorer, implementer, or first-pass tester when a child can own a bounded deliverable.

Delegate a **complete, independently verifiable unit of work**, not a sequence of tiny assistant chores. A good child assignment owns enough context to reach a conclusion or produce a tested change without asking the main agent to repeat its exploration. Prefer one child that can inspect a module, implement its slice, and run focused validation over separate children for discovery, coding, and unit testing of the same slice.

## Main-Agent Ownership

The main agent owns only work that genuinely requires central authority: material requirement clarification, unresolved product and architecture decisions, decomposition, user communication, cross-boundary integration, and final acceptance. It owns the conclusion, not the default exploration, implementation, or focused testing.

Subagents return concise evidence or bounded deliverables. They may inspect their assigned code, research sources, build prototypes, write code, and run focused checks, but report an unresolved product or architecture decision rather than guessing. The main agent consumes their summaries and inspects underlying evidence only when it materially affects a decision, conflicts with another result, or needs integration review. It must not re-map code that a child has mapped, re-implement a child's closed slice, or repeat a child's focused validation without a specific reason.

## Adaptive Dispatch

Choose the path with the lower total cost, including startup time, context, coordination, and duplicated thinking.

Work directly in the main agent only for a narrow question answerable from a few files, a tiny well-understood edit, or work whose parts are inseparably coupled. Do not create a subagent ceremonially. Once delegation is justified, dispatch early and let the child do the substantive work.

Dispatch a child when it can own a complete, independently verifiable unit: mapping a larger code area, answering a concrete research question, creating a prototype, implementing a planned slice, investigating a bug, or adding focused tests. Do not split the same boundary by workflow phase—one agent for inspection, one for coding, and one for testing—when one executor can own it end-to-end. For a substantial feature, an evidence wave before the decision and an execution wave after it are appropriate only when the waves answer distinct questions. Give each child a compact task and request a short conclusion, evidence, changed paths, validation, and blockers—never a long activity diary.

## 1. Discover the Product Before Designing It

For a new feature with material product, UX, or workflow choices, establish the needed product and code context, then research comparable products or established interaction patterns. The main agent may dispatch focused scouts for either job and uses their findings rather than recreating them. Prefer primary product documentation and real, current product behavior. If no direct comparable product exists, research the closest workflow and state that limitation. Skip external research for a clear local implementation, bug fix, internal refactor, or established pattern.

Approach the request as a product manager would: identify the user, the job they are trying to complete, the present friction, the primary happy path, important failure or edge states, and a concrete success signal. Use the research to explain which pattern to adopt or deliberately avoid; do not copy a competitor by default.

Record the useful sources, observations, assumptions, and risks in the proposal so the user can challenge the reasoning before implementation begins.

## 2. Make the Product Decision Visible

Write a concise proposal before coding only for a consequential product or architecture decision, or when repository instructions require plan approval. It should cover the intended user outcome, relevant findings, chosen behavior and trade-offs, affected boundaries, validation, and any delegation boundaries. Do not create proposal ceremony for an obvious, bounded implementation.

For a user-facing frontend change with uncertain interaction, navigation, information hierarchy, or visual direction, create and open a runnable standalone HTML prototype before application implementation. The main agent defines the product question; a focused subagent may materialize the prototype. Use it as a decision artifact to test information hierarchy, states, interactions, responsive behavior, and visual direction. Skip a prototype for non-visual work or an already-specified UI change, and state why.

When the feature has materially different interaction, navigation, information-hierarchy, or state-management choices, produce multiple focused HTML variants for the user to compare. The main agent defines what differs and why. Do not manufacture alternatives for superficial styling changes; one prototype is enough when there is one clearly supported direction. For non-visual work, skip HTML and state why.

Revise the proposal and prototype from user feedback, then turn the accepted choice into the implementation plan. If repository instructions or the user require plan approval, obtain it before making or delegating code changes.

## 3. Use Agents to Accelerate Development

Use discovery agents before planning only when they can independently remove a concrete uncertainty. After the main agent has chosen the product and technical direction, use implementation agents for closed execution boundaries. Prefer one end-to-end executor for a boundary over a chain of scout, implementer, and tester agents.

- Use one agent for one cohesive, independently verifiable exploration or implementation scope.
- Use as many direct children as the independent work and runtime capacity justify. Three or four agents are reasonable for a feature with genuinely separate research, design, code, or testing tracks; a small question often needs none. Keep delegation depth at one and reserve capacity for the main agent.
- Give write-capable executors exclusive path ownership. If a later task needs a path already owned by another executor, wait for integration and then decide the follow-up locally.

Do not dispatch agents whose output is a generic recommendation, a duplicate summary, or evidence that the main agent would need to reproduce before acting. The main agent resolves only reported blockers and cross-boundary decisions; it otherwise accepts completed child units and moves to integration.

Before dispatch, record the dirty-worktree baseline and identify generated files or formatters that could write outside an executor's owned paths. In a shared working directory, executor commands must not modify unowned paths. Reserve full-repository tests, code generation, and global formatting for the main agent after all executors have finished and their changes have been reviewed.

## Subagent Packet

For every subagent, explicitly select `gpt-5.6-luna` with maximum reasoning: set `model: "gpt-5.6-luna"` and `reasoning_effort: "max"` where the spawn interface exposes those fields, or `thinking: "max"` where the thread interface uses that name. Start it with a compact, standalone task packet rather than inherited conversation history. The packet must include:

- the concrete question or deliverable and its done condition;
- relevant paths, sources, interfaces, and explicit non-goals;
- decisions the subagent must preserve, if a plan already exists;
- required tests or validation commands when it can change code;
- a request to report its conclusion, evidence, changed files, validation, and blockers concisely.

State that the subagent may not make undecided product or architecture choices, may not spawn descendants, and must leave unrelated user changes untouched. The main agent resolves every reported blocker before execution continues.

## 4. Integrate, Verify, and Deliver

The main agent reviews child summaries and the combined diff against the accepted product decision and implementation plan. Inspect changed code at integration boundaries and validate the remaining risks: error handling, compatibility, concurrency, security, scope, and interactions between slices. Do not recreate completed child exploration or focused validation without a specific risk. Run the complete repository test suite whenever it is available, plus relevant formatting, static analysis, and representative manual checks. Confirm that the shipped user experience matches the accepted HTML prototype where one was used. Fix failures, then repeat the affected verification.

Deliver the outcome first, followed by changed files, user-visible behavior, and concrete validation results. State any unavailable verification or material limitation plainly.
