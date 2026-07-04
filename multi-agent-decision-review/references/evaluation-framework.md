# Evaluation Framework

Use this file when a decision needs a repeatable rubric, weighted scoring, or clear comparison across options.

## Default Dimensions

Score each dimension from 1 to 5.

| Dimension | Ask | Notes |
| --- | --- | --- |
| Goal fit | Does this option solve the real problem? | Penalize attractive work that does not move the core outcome. |
| User value | Who benefits, and how strongly? | Include internal users, maintainers, buyers, or readers. |
| Feasibility | Can this be executed with current people, tools, access, and time? | Separate known work from unknown work. |
| Cost | What does this consume? | Include money, time, attention, opportunity cost, and future coordination. |
| Maintainability | Will this stay understandable and changeable? | Favor simpler systems unless complexity buys clear value. |
| Risk | What can fail badly? | Include security, data, legal, operational, reputation, and user trust. |
| Reversibility | Can we undo or change course cheaply? | High reversibility can justify experiments. |
| Evidence quality | How strong is the supporting evidence? | Penalize decisions based on anecdotes, stale facts, or hidden assumptions. |

## Weighting

Use equal weights only when the stakes are balanced. Otherwise choose weights from the decision context.

Recommended defaults:

| Decision Type | Higher Weight |
| --- | --- |
| Product feature | Goal fit, user value, feasibility, evidence quality |
| Architecture | Maintainability, risk, feasibility, reversibility |
| Tool/vendor purchase | Goal fit, cost, risk, switching cost, evidence quality |
| Hiring/team decision | Goal fit, risk, evidence quality, reversibility |
| Writing/research direction | Goal fit, evidence quality, audience value, cost |
| Personal workflow | Cost, reversibility, user value, maintainability |

## Scoring Discipline

- Explain what would make a score one point higher or lower.
- Distinguish "unknown" from "bad".
- Lower confidence when the evidence is thin, even if the score is high.
- Avoid false precision. Do not use decimals unless the user needs a numeric ranking.
- Do not let a low-risk option win if it fails the goal.
- Do not let a high-value option win if its failure mode is unacceptable.

## Recommendation Logic

Use this hierarchy:

1. Eliminate options that violate hard constraints.
2. Identify any option that clearly achieves the goal with acceptable risk.
3. Prefer the simplest reversible option when evidence is weak.
4. Prefer the option with better long-term maintainability when the decision is hard to reverse.
5. Recommend an experiment when uncertainty is high and a cheap test exists.

## Output Templates

Compact table:

```markdown
| 方案 | 目标匹配 | 可行性 | 成本 | 风险 | 可逆性 | 总体判断 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| A |  |  |  |  |  |  |
| B |  |  |  |  |  |  |
```

Reviewer summary:

```markdown
| Reviewer | Preferred Option | Main Reason | Main Objection | Confidence |
| --- | --- | --- | --- | --- |
```
