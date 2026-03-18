# Research Findings (2026-02-25)

Source baseline: `Desktop/Fullstop_base/multi_agent_debate_deliberation_research_2026-02-25.html`

## 1) Applicability Boundary

Enable debate-style multi-agent deliberation only when all three conditions hold:

1. Arguable space exists.
2. Testable criteria exist.
3. A falsifiable evidence chain exists.

If not, debate often increases cost without improving quality.

## 2) Key Evidence Summary

1. MAD (Du et al., 2023): Significant gains over single-agent on multiple tasks.
2. Sparse Topology (Li et al., 2024): In some tasks, maintains or improves quality while reducing token cost (reported 40%+ in selected settings).
3. ChatEval (Chan et al., 2023): Multi-agent discussion improves agreement with human evaluation in review tasks.
4. BioNLP 2025 medical setting: Debate framework outperforms some baselines but with significantly higher cost.
5. EMNLP Findings 2025: Debate can amplify bias without explicit controls.

## 3) Actionable Implications

1. Default to 2 rounds, max 3.
2. Enforce Evidence-Checker to reduce confident mistakes.
3. Use fixed rubric in Judge stage.
4. Set budget and stop thresholds to prevent unbounded loops.

## 4) Suggested Defaults

1. Roles: 2 proposers + 1 critic + 1 evidence-checker + 1 judge.
2. Rounds: 2 (optional 3rd with strict gate).
3. Stop rule: gain <1% for two checkpoints or no new evidence.
4. High-stakes tasks: allow "insufficient evidence" as final state.

## 5) Residual Risks

1. Shared-model bias can create confident but wrong consensus.
2. Role collapse can weaken debate value.
3. Poor citation discipline can create false robustness.

Always run gate checks before activating this skill.