# Prompt Patterns

Use these patterns when prompting subagents or running separate internal reviewer passes.

## Neutral Review Prompt

```text
Use $multi-agent-decision-review to evaluate the decision below from the perspective of [REVIEWER PERSPECTIVE].

Decision question:
[QUESTION]

Options:
- Option A: [NEUTRAL DESCRIPTION]
- Option B: [NEUTRAL DESCRIPTION]

Context and constraints:
[BACKGROUND]

Your task:
1. Score each option from 1 to 5 on the dimensions relevant to your perspective.
2. Explain the strongest reason for each score.
3. Identify the biggest risk, missing information, and what evidence would change your view.
4. Give a recommendation only from your assigned perspective.

Do not assume the requester prefers any option. Do not optimize for consensus. If context is insufficient, say what is missing instead of guessing.
```

## Adversarial But Fair Prompt

```text
Use $multi-agent-decision-review to stress-test this decision as a fair skeptic.

Decision question:
[QUESTION]

Candidate approach:
[APPROACH]

Known constraints:
[CONSTRAINTS]

Evaluate:
- What assumptions must be true?
- What would fail first?
- What is the simpler or lower-cost alternative?
- What evidence would justify proceeding?
- What should be tested before committing?

Do not argue against the approach for sport. Focus on decision-relevant failure modes.
```

## Product Perspective Prompt

```text
Review this decision from the perspective of user value and product focus.

Assess whether each option solves a real user problem, improves the target workflow, avoids unnecessary scope, and creates measurable value.
Return scores, objections, missing evidence, and a recommendation from this perspective only.
```

## Technical Perspective Prompt

```text
Review this decision from the perspective of implementation feasibility and maintainability.

Assess complexity, dependencies, migration cost, operational burden, testability, reversibility, and future change cost.
Return scores, objections, missing evidence, and a recommendation from this perspective only.
```

## Risk Perspective Prompt

```text
Review this decision from the perspective of risk.

Assess security, privacy, legal/compliance, data integrity, user trust, operational failure, reputational exposure, and blast radius.
Return scores, objections, missing evidence, and a recommendation from this perspective only.
```

## Cost Perspective Prompt

```text
Review this decision from the perspective of cost and opportunity cost.

Assess build time, maintenance time, money, coordination load, cognitive overhead, vendor lock-in, and what other work this displaces.
Return scores, objections, missing evidence, and a recommendation from this perspective only.
```

## Forbidden Prompt Patterns

Avoid:

```text
The user wants to choose Option A. Please evaluate whether this is right.
```

Avoid:

```text
We think Option B is probably best. Give another perspective.
```

Avoid:

```text
Score this objectively, but focus on why the proposed plan is good.
```

Avoid:

```text
Other reviewers found Option A risky. Do you agree?
```

Use symmetric language, equal detail, and no leaked conclusion.
