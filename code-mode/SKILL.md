---
name: code-mode
description: "Use for any software development task that needs a consistent end-to-end workflow: clarify requirements, research uncertain decisions, prototype frontend work in standalone HTML, delegate bounded implementation tasks to subagents, review changes, and run the project's full relevant test suite before delivery."
---

# Code Mode

Use a concise, evidence-based delivery loop. Optimize for the smallest correct change, clear ownership, and verified behavior.

## 1. Frame the Problem

1. State the desired user outcome and the acceptance criteria.
2. Inspect the repository, existing behavior, tests, and applicable `AGENTS.md` files before proposing implementation details.
3. Ask a focused question if an unresolved product decision materially changes the solution. Otherwise, explicitly record the smallest safe assumption.
4. Research current external APIs, products, framework behavior, or user expectations when the decision depends on facts not present in the repository. Prefer primary documentation.
5. Identify risks: compatibility, data migration, security, performance, operational impact, and test coverage.

Do not write code until the implementation approach has been presented and approved by the user when that rule applies in the active environment.

## 2. Design Before Building

Write a short implementation plan that names:

- Files or components expected to change.
- Data and control flow changes.
- Test and validation strategy.
- Any migration, rollback, or feature-flag need.

For user-facing frontend work, create a runnable standalone HTML prototype before application implementation. Open it immediately after creation so the user can inspect the actual rendered result. Use it to validate structure, key interactions, content hierarchy, responsive behavior, and visual direction. Treat the prototype as a decision artifact, not production code: reuse only design decisions deliberately.

Skip the HTML prototype only for non-visual changes or when the user explicitly asks to skip it. Say why when skipping.

## 3. Delegate Deliberately

Delegate independent, bounded implementation or investigation tasks to a subagent when delegation reduces elapsed time or improves review quality. Use the subagent explicitly specified by the user; if none is specified, use Luna.

Provide each subagent:

- A narrow objective and exact success criteria.
- Relevant paths, interfaces, constraints, and validation commands.
- Ownership boundaries that avoid overlapping edits.

Use the maximum available reasoning setting for every subagent task, regardless of the selected model. Keep the main agent responsible for architecture, integration, requirement interpretation, and final review. Do not delegate unresolved product choices without context.

## 4. Implement Minimally

1. Follow existing project conventions unless they conflict with the accepted design.
2. Keep changes small and cohesive; avoid opportunistic refactors.
3. Add or update tests with the behavior change.
4. Preserve user changes in a dirty worktree; never revert unrelated work.
5. Surface any scope change, destructive action, external side effect, or newly discovered requirement before taking it.

## 5. Review and Verify

The main agent reviews all changes, including subagent changes, before delivery:

1. Compare the implementation against each acceptance criterion.
2. Inspect diffs for correctness, security, concurrency, error handling, edge cases, API compatibility, and unintended scope.
3. Run formatting, static checks, and the complete relevant test suite. If project instructions require the full suite, run the full suite rather than a targeted subset.
4. Exercise a representative end-to-end or manual verification path when automated tests cannot cover the user-visible behavior.
5. Fix failures and repeat verification until it passes. Do not claim success if required verification is unavailable; report the gap and its risk plainly.

## Delivery

Lead with the outcome. Report changed files, user-visible behavior, and validation results. Mention only material assumptions, known limitations, or follow-up work. Include actionable review findings first if the request was a code review.
