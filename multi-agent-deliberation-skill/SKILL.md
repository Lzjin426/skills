---
name: multi-agent-deliberation
description: Run multi-agent deliberation when a task has arguable alternatives, testable evaluation criteria, and a falsifiable evidence chain. Use this skill to improve final answer quality and robustness via proposer/critic/checker/judge workflow with structured verdict, confidence, evidence map, residual risks, and verification steps.
---

# Multi-Agent Deliberation (v1.1)

## Overview

Use this skill to run a structured multi-agent deliberation workflow for quality-first answers.

Prioritize this skill only when debate adds value. Do not use it for simple factual queries or low-stakes prompts where a single agent is sufficient.

## Workflow Decision Tree

1. Validate activation gate.
2. Define the decision target and testable criteria.
3. Instantiate debate roles.
4. Run bounded rounds with evidence constraints.
5. Judge with fixed rubric.
6. Emit final answer with structured state and risk controls.

## Step 1: Validate Activation Gate

Require all three conditions before using multi-agent debate:

1. Confirm arguable space.
2. Confirm testable criteria.
3. Confirm a falsifiable evidence chain.

If any condition is missing, do not spawn debate roles. Use a fallback single-agent response with `STATUS=GATE_FAILED` and list missing conditions.

Load `references/gate_and_controls.md` for the gate checklist and fallback schema.

## Step 2: Define Evaluation Contract

Set these items before spawning roles:

1. Define `QUESTION` and explicit `CONSTRAINTS`.
2. Define acceptance metrics.
3. Define source quality policy.
4. Define budget limits (rounds, token, latency).

Use this default rubric unless the user specifies otherwise:

- Accuracy: 40%
- Completeness: 25%
- Traceability: 20%
- Robustness after rebuttal: 15%

Default source policy:

- Tier A: primary sources (official docs, standards, original papers, authoritative datasets).
- Tier B: reliable secondary synthesis.
- Tier C: opinion/unverified content.
- `critical claim` means a claim that can change conclusion direction, risk level, or recommended actions.
- Critical claims require at least one Tier A source (high-stakes: two independent high-quality sources).

## Step 3: Instantiate Debate Roles

Create exactly five roles by default:

1. `Proposer-A`: deliver candidate answer A with evidence map.
2. `Proposer-B`: deliver independent candidate answer B with evidence map.
3. `Critic`: attack both candidates and expose hidden assumptions.
4. `Evidence-Checker`: verify claim-source consistency and mark unsupported claims.
5. `Judge`: score and decide with fixed rubric.

Isolation rule:

- A/B must generate first drafts in isolated contexts.
- No cross-read of draft reasoning before Round 1 starts.

Load `references/debate_playbook.md` for reusable prompt blocks.

## Step 4: Run Bounded Deliberation

Run phases with explicit counting:

1. Phase 0 (not counted as a debate round): independent proposals (A/B).
2. Round 1: critic cross-examination.
3. Round 2: targeted rebuttal and evidence updates.
4. Optional Round 3: only if new evidence appears or core factual disagreement remains unresolved.

Round budget definition:

- Default debate rounds: 2 (Round 1-2).
- Maximum debate rounds: 3.
- Phase 0 is mandatory and excluded from round budget.

Stop rule:

- Judge outputs total score on 0-100 scale each round.
- `score_gain = current_total_score - previous_total_score`.
- Stop when score gain is < 1 point for two consecutive rounds, or no new evidence appears.

## Step 5: Judge and Decide

Force structured decision output:

1. Provide `SCORE_A` and `SCORE_B`.
2. Select winner or merged final with explicit merge rationale.
3. Emit final answer with confidence and residual risks.
4. Emit what evidence would change the decision.
5. Emit unsupported claim disposition (`dropped`, `pending_evidence`, or `accepted_with_uncertainty`).

Never force consensus if evidence is weak.

## Step 6: Output Contract

Always output this structure:

```text
[STATUS]
DECIDED | MERGED | INSUFFICIENT_EVIDENCE | GATE_FAILED

[FINAL_ANSWER]
...

[SCORES]
SCORE_A: ...
SCORE_B: ...
SCORE_DELTA: ...

[CONFIDENCE_0_TO_100]
...

[KEY_EVIDENCE_MAP]
- claim_id -> source_id
...

[UNSUPPORTED_CLAIMS]
- claim_id
...

[DISPOSITION]
- claim_id: dropped | pending_evidence | accepted_with_uncertainty
...

[OPEN_RISKS]
...

[WHAT_WOULD_CHANGE_THE_ANSWER]
...

[NEXT_VERIFICATION_STEPS]
...
```

## Operating Controls

1. Cap debate rounds at 2 by default; max 3 (excluding Phase 0).
2. Cap per-role response length to avoid verbosity bias.
3. Require source IDs for all critical claims.
4. Reject unsupported critical claims unless explicitly marked `accepted_with_uncertainty`.
5. Enforce human review for all high-stakes tasks before release.

Load `references/gate_and_controls.md` for failure modes and mitigation rules.

## Resource Loading Guide

Load only what is needed:

1. Load `references/research_findings_2026-02-25.md` when deciding whether debate is justified and for parameter defaults.
2. Load `references/debate_playbook.md` when you need role prompts or output templates.
3. Load `references/gate_and_controls.md` when you need activation checks, stop rules, and risk governance.