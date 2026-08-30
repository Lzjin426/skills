---
name: code-mode-codex
description: "Use for end-to-end Codex development: adaptively keep small questions in the main agent, while delegating research, prototypes, implementation, and testing to GPT-5.6 Luna max-reasoning subagents when that saves time or main-agent context."
---

# Code Mode Codex

Treat this as a product-development mode, not merely an agent-delegation policy. Deliver the smallest product change that solves the right user problem, is visibly testable, and is fully verified. Keep the main agent lean: it should spend its context on decisions, synthesis, and acceptance rather than repeating exploration or implementation that a focused Luna task can complete.

## Main-Agent Ownership

The main agent owns requirement clarification, reasoning, product and technical decisions, planning, task decomposition, user communication, integration, code review, and final acceptance. It owns the conclusion, not every information-gathering step: it may delegate repository exploration, comparable-product research, prototype construction, implementation, focused testing, and first-pass review.

Subagents return concise evidence or bounded deliverables. They may inspect their assigned code, research sources, build prototypes, write code, or run focused checks, but report an unresolved product or architecture decision rather than guessing. The main agent consumes their summaries and inspects underlying evidence only when it materially affects a decision.

## Adaptive Dispatch

Choose the path with the lower total cost, including startup time, context, and coordination.

Work directly in the main agent for a narrow question that can be answered by inspecting a few files, a small well-understood edit, or work whose parts are tightly coupled. Do not create a subagent merely because one is available.

Dispatch early when the work has an independent, useful output: mapping a larger code area, researching comparable products, creating an HTML option, implementing a planned slice, or checking a distinct risk. For a substantial feature, it is normal to run an evidence-gathering wave before the plan and an execution wave after it. Give each child a compact task and request a short conclusion, evidence, changed paths, validation, and blockers—never a long activity diary.

## 1. Discover the Product Before Designing It

For every new feature, establish the existing product and code context, then research comparable products or established interaction patterns. The main agent may dispatch focused scouts for either job and synthesizes their findings. Prefer primary product documentation and real, current product behavior. If no direct comparable product exists, research the closest workflow and state that limitation.

Approach the request as a product manager would: identify the user, the job they are trying to complete, the present friction, the primary happy path, important failure or edge states, and a concrete success signal. Use the research to explain which pattern to adopt or deliberately avoid; do not copy a competitor by default.

Record the useful sources, observations, assumptions, and risks in the proposal so the user can challenge the reasoning before implementation begins.

## 2. Make the Product Decision Visible

Write a concise proposal before coding. It should cover the intended user outcome, comparable-product findings, chosen behavior and trade-offs, affected files and data/control flow, validation, and any delegation boundaries.

For every user-facing frontend change, create and open a runnable standalone HTML prototype before application implementation. The main agent defines the product question; a focused subagent may materialize the prototype. Use it as a decision artifact to test information hierarchy, states, interactions, responsive behavior, and visual direction.

When the feature has materially different interaction, navigation, information-hierarchy, or state-management choices, produce multiple focused HTML variants for the user to compare. The main agent defines what differs and why. Do not manufacture alternatives for superficial styling changes; one prototype is enough when there is one clearly supported direction. For non-visual work, skip HTML and state why.

Revise the proposal and prototype from user feedback, then turn the accepted choice into the implementation plan. If repository instructions or the user require plan approval, obtain it before making or delegating code changes.

## 3. Use Agents to Accelerate Development

Use discovery agents before planning when they can independently gather evidence. After the main agent has chosen the product and technical direction, use implementation agents for closed execution boundaries.

- Use one agent for one cohesive exploration or implementation scope.
- Use as many direct children as the independent work and runtime capacity justify. Three or four agents are reasonable for a feature with genuinely separate research, design, code, or testing tracks; a small question often needs none. Keep delegation depth at one and reserve capacity for the main agent.
- Give write-capable executors exclusive path ownership. If a later task needs a path already owned by another executor, wait for integration and then decide the follow-up locally.

Before dispatch, record the dirty-worktree baseline and identify generated files or formatters that could write outside an executor's owned paths. In a shared working directory, executor commands must not modify unowned paths. Reserve full-repository tests, code generation, and global formatting for the main agent after all executors have finished and their changes have been reviewed.

## Subagent Packet

For every subagent, explicitly select `gpt-5.6-luna` with maximum reasoning: use `reasoning_effort: "max"` where the spawn interface exposes that field, or `thinking: "max"` where the thread interface uses that name. Start it with a compact task packet rather than inherited conversation history. The packet must include:

- the concrete question or deliverable and its done condition;
- relevant paths, sources, interfaces, and explicit non-goals;
- decisions the subagent must preserve, if a plan already exists;
- required tests or validation commands when it can change code;
- a request to report its conclusion, evidence, changed files, validation, and blockers concisely.

State that the subagent may not make undecided product or architecture choices, may not spawn descendants, and must leave unrelated user changes untouched. The main agent resolves every reported blocker before execution continues.

## 4. Integrate, Verify, and Deliver

The main agent inspects the combined diff against both the accepted product decision and the implementation plan, including error handling, compatibility, concurrency, security, and scope. Run the complete repository test suite whenever it is available, plus relevant formatting, static analysis, and representative manual checks. Confirm that the shipped user experience matches the accepted HTML prototype where one was used. Fix failures, then repeat the affected verification.

Deliver the outcome first, followed by changed files, user-visible behavior, and concrete validation results. State any unavailable verification or material limitation plainly.
