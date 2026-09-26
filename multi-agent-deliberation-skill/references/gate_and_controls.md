# Gate And Controls (v1.1)

## 1) Activation Gate Checklist

Enable debate only if all 3 conditions are true:

1. Arguable alternatives exist.
2. Testable evaluation criteria exist.
3. A falsifiable evidence chain exists.

If gate score < 3/3, do not start multi-agent debate.
Return fallback schema with `STATUS=GATE_FAILED`.

Fallback template:

```text
[STATUS]
GATE_FAILED

[GATE_SCORE]
x/3

[MISSING_CONDITIONS]
- ...

[SINGLE_AGENT_ANSWER]
...

[WHAT_EVIDENCE_IS_NEEDED_TO_ACTIVATE_DEBATE]
...
```

## 2) Budget Controls

1. Default debate rounds: 2.
2. Max debate rounds: 3.
3. Phase 0 is mandatory but excluded from round count.
4. Cap per-role response length and total token budget per task.
5. If budget is exceeded, stop and output current-best answer with explicit risk flags.

## 3) Stop Rules

1. Judge produces a 0-100 total score at each round end.
2. `score_gain = current_total_score - previous_total_score`.
3. Stop if score_gain < 1 point for two consecutive rounds.
4. Stop if no new evidence is added.
5. If disagreement is value-based (not factual), escalate to human decision.

## 4) Failure Modes And Mitigations

1. Shared-bias amplification:
- Keep A/B isolated in Phase 0.
- Require independent evidence checks.
- Force counterexample slots.

2. Role collapse:
- Enforce role-specific outputs.
- Prevent early cross-read.

3. Confident but wrong consensus:
- Judge must rely on evidence map, not agreement rate.

4. Debate loops:
- Enforce round caps and stop rules.

## 5) High-Stakes Escalation

For medical, legal, financial, safety, or major-loss scenarios:

1. Human-in-the-loop review is mandatory before release.
2. If unresolved or under-supported, output `STATUS=INSUFFICIENT_EVIDENCE`.
3. Provide a concrete verification plan.