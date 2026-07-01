---
name: agent-acceptance-review
description: Use when an agent has produced a task version, implementation, document, plan, research result, or other deliverable that must be independently accepted, rejected, scored, or sent back for iteration.
---

# Agent Acceptance Review

## Overview

Use this skill as an acceptance gate for agent work. Review the submitted version with neutral evidence, score it on a 0-100 scale, and accept only when it reaches 90 or higher with no blocker issues.

This is not a replacement for tests, linters, builds, domain checks, or user approval. Treat deterministic verification as the first layer and judge scoring as the second layer.

## Core Rules

- Preserve reviewer independence. Do not reveal the worker agent's self-assessment, preferred conclusion, or expected score.
- Score evidence, not effort. A long attempt, many tool calls, or confident summary does not improve the score unless the result satisfies the task.
- Require concrete verification before acceptance. If expected tests or checks were not run, cap the score at 89 unless the task is clearly non-testable.
- Accept only if all are true: final score >= 90, no blocker, critical requirements satisfied, and verification evidence is adequate.
- If score < 90, return actionable iteration feedback instead of declaring completion.
- For high-risk work, prefer full mode and include `multi-agent-decision-review`.
- Never invent evaluation results from a platform, test suite, or tool that was not actually run.

## Review Modes

### Light Mode

Use light mode for small, reversible, low-risk tasks.

- Use one independent judge pass.
- Inspect the task request, relevant artifacts, changes, and verification evidence.
- Output score, blocker status, reasons, and next actions.

### Full Mode

Use full mode when the work is broad, risky, user-facing, expensive to undo, or likely to need multiple perspectives.

- Use `multi-agent-decision-review` when available.
- Ask reviewers to score independently before synthesis.
- Use 3-5 reviewer perspectives selected for failure modes, such as correctness, user value, maintainability, risk, and first-principles skepticism.
- Surface disagreements instead of averaging them away.

## Acceptance Workflow

1. Frame the submitted version:
   - Original request and acceptance criteria.
   - Claimed deliverable.
   - Changed files, created artifacts, or produced content.
   - Verification already performed.
   - Known constraints, skipped checks, or unresolved questions.

2. Run deterministic checks first:
   - Tests, build, lint, typecheck, format, smoke test, visual check, schema validation, citation check, or other task-specific checks.
   - If a check cannot be run, record why and whether this should cap the score.

3. Choose review mode:
   - Light mode for narrow, low-risk work.
   - Full mode for architecture, product behavior, user-facing UI, data, legal/compliance, security, research claims, or multi-file changes.

4. Score with the rubric:
   - Requirement satisfaction: 35
   - Correctness and verification: 25
   - Maintainability and integration: 15
   - Risk control: 15
   - Efficiency and focus: 10

5. Apply gates:
   - Any blocker means reject, regardless of numeric score.
   - Missing required verification usually caps score at 89.
   - Scope drift, fabricated evidence, or unreviewed destructive changes cap score at 79 or lower.

6. Decide:
   - `Accepted`: score >= 90 and no blockers.
   - `Needs iteration`: score 70-89 or non-blocking but material gaps remain.
   - `Rejected`: score < 70, blocker present, or result does not satisfy the core task.

7. If not accepted, give the worker the smallest useful next iteration:
   - Confirmed problems.
   - Evidence for each problem.
   - Required fixes.
   - Checks to rerun.
   - What would raise the score above 90.

## Output Shape

Use this shape for most reviews:

```markdown
**Acceptance**
Decision: Accepted | Needs iteration | Rejected
Score: NN/100
Blockers: none | ...
Confidence: low | medium | high

**Score**
| Dimension | Points | Reason |
| --- | ---: | --- |
| Requirement satisfaction | NN/35 | ... |
| Correctness and verification | NN/25 | ... |
| Maintainability and integration | NN/15 | ... |
| Risk control | NN/15 | ... |
| Efficiency and focus | NN/10 | ... |

**Evidence**
- ...

**Required Next Iteration**
- ...
```

Omit `Required Next Iteration` only when accepted.

## Reference Files

- Read `references/acceptance-prompts.md` before writing prompts for judge agents, subagents, or simulated reviewer passes.
