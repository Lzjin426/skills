---
name: code-mode-codex
description: "Use for end-to-end Codex feature development: research comparable products, make product and technical decisions, prototype frontend choices in HTML, then use GPT-5.6 Luna max-reasoning subagents for bounded implementation when helpful."
---

# Code Mode Codex

Treat this as a product-development mode, not merely an agent-delegation policy. Deliver the smallest product change that solves the right user problem, is visibly testable, and is fully verified.

## Main-Agent Ownership

The main agent personally performs requirement clarification, repository investigation, external research, reasoning, design, planning, task decomposition, user communication, integration, code review, and final acceptance. Do not create planner, researcher, explorer, architect, or reviewer subagents.

Executors accelerate a decision that is already made. They may inspect the explicitly relevant local code and tests to implement their packet, but report an unresolved decision or blocker rather than guessing.

## 1. Discover the Product Before Designing It

For every new feature, the main agent first inspects the existing product and code, then researches comparable products or established interaction patterns. Prefer primary product documentation and real, current product behavior. If no direct comparable product exists, research the closest workflow and state that limitation.

Approach the request as a product manager would: identify the user, the job they are trying to complete, the present friction, the primary happy path, important failure or edge states, and a concrete success signal. Use the research to explain which pattern to adopt or deliberately avoid; do not copy a competitor by default.

Record the useful sources, observations, assumptions, and risks in the proposal so the user can challenge the reasoning before implementation begins.

## 2. Make the Product Decision Visible

Write a concise proposal before coding. It should cover the intended user outcome, comparable-product findings, chosen behavior and trade-offs, affected files and data/control flow, validation, and any delegation boundaries.

For every user-facing frontend change, create and open a runnable standalone HTML prototype before application implementation. Use it as a decision artifact to test information hierarchy, states, interactions, responsive behavior, and visual direction.

When the feature has materially different interaction, navigation, information-hierarchy, or state-management choices, produce multiple focused HTML variants for the user to compare. The main agent defines what differs and why. Do not manufacture alternatives for superficial styling changes; one prototype is enough when there is one clearly supported direction. For non-visual work, skip HTML and state why.

Revise the proposal and prototype from user feedback, then turn the accepted choice into the implementation plan. If repository instructions or the user require plan approval, obtain it before making or delegating code changes.

## 3. Use Agents to Accelerate Execution

Delegate only after the plan is settled and only when the task has a closed execution boundary.

- Use one executor for one cohesive implementation scope.
- Use an agent team when several independent work packages can proceed without touching the same files. Choose the smallest useful team; three or four executors are appropriate when the work genuinely supports it and the runtime has capacity. Keep delegation depth at one and reserve capacity for the main agent.
- Do not split a change merely to create parallelism. Keep discovery, product decisions, planning, integration, and final review in the main thread.
- Give each executor exclusive path ownership. If a later task needs a path already owned by another executor, wait for integration and then decide the follow-up locally.

Before dispatch, record the dirty-worktree baseline and identify generated files or formatters that could write outside an executor's owned paths. In a shared working directory, executor commands must not modify unowned paths. Reserve full-repository tests, code generation, and global formatting for the main agent after all executors have finished and their changes have been reviewed.

## Executor Packet

For every executor, explicitly select `gpt-5.6-luna` with maximum reasoning: use `reasoning_effort: "max"` where the spawn interface exposes that field, or `thinking: "max"` where the thread interface uses that name. Start it with a compact task packet rather than inherited conversation history. The packet must include:

- the already-decided objective and acceptance criteria;
- exact owned paths, relevant interfaces, and explicit non-goals;
- decisions the executor must preserve;
- required tests or validation commands;
- a request to report changed files, validation evidence, and blockers.

State that the executor is execution-only, may not make undecided product or architecture choices, may not spawn descendants, and must leave unrelated user changes untouched. The main agent resolves every reported blocker before execution continues.

## 4. Integrate, Verify, and Deliver

The main agent inspects the combined diff against both the accepted product decision and the implementation plan, including error handling, compatibility, concurrency, security, and scope. Run the complete repository test suite whenever it is available, plus relevant formatting, static analysis, and representative manual checks. Confirm that the shipped user experience matches the accepted HTML prototype where one was used. Fix failures, then repeat the affected verification.

Deliver the outcome first, followed by changed files, user-visible behavior, and concrete validation results. State any unavailable verification or material limitation plainly.
