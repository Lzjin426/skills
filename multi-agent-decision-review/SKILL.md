---
name: multi-agent-decision-review
description: Run neutral multi-agent decision reviews for product, technical, strategy, writing, research, purchasing, hiring, prioritization, or architecture choices. Use when the user asks for agent team scoring, multi-perspective review, objective evaluation, decision support, tradeoff analysis, devil's advocacy, options ranking, or wants multiple agents to assess a plan without bias.
---

# Multi-Agent Decision Review

## Overview

Use this skill to turn a fuzzy or high-stakes choice into a structured, neutral review by multiple independent perspectives. Optimize for decision quality, not consensus theater.

## Operating Rules

- Address the user in the normal conversation style, then run the review process.
- Preserve neutrality: do not tell reviewers which option the user or main agent prefers.
- Give reviewers enough decision background before asking for scores.
- Ask clarifying questions first when the missing context can change the result.
- Use subagents when available and worthwhile; otherwise simulate separate reviewer passes with explicit perspective separation.
- Prefer evidence and first principles over seniority, popularity, or majority vote.
- Treat disagreement as signal. Surface why reviewers diverge before giving the final recommendation.
- Do not use this skill for purely mechanical tasks where no meaningful decision or tradeoff exists.

## Workflow

### 1. Frame The Decision

Extract or ask for:

- Decision question: what must be chosen or judged.
- Options: candidate plans, designs, tools, vendors, strategies, or actions.
- Goal: the outcome that actually matters.
- Constraints: time, budget, quality bar, reversibility, dependencies, policies, and risk tolerance.
- Stakeholders: who benefits, pays, maintains, approves, or is exposed to failure.
- Available evidence: docs, code, screenshots, metrics, market research, prior decisions, or user notes.

If the user only gives a plan, define the implicit alternatives:

- Do nothing or defer.
- Use the simplest lower-cost path.
- Use the proposed path.
- Use one materially different path.

### 2. Decide Review Depth

Use a light review when the decision is reversible, low cost, or mostly about taste.

Use a full review when the decision affects architecture, user experience, money, reputation, hiring, data, legal/compliance exposure, or more than one week of work.

Use web research before scoring when the decision depends on current facts, products, pricing, laws, benchmarks, market norms, third-party tools, or external risks.

### 3. Select Reviewers

Choose 3-6 perspectives that match the decision. Prefer distinct failure models over job titles.

Default reviewer set:

- User/value reviewer: checks who benefits and whether the outcome matters.
- Feasibility reviewer: checks implementation realism, dependencies, and unknowns.
- Risk reviewer: checks failure modes, reversibility, security, legal, operational, or reputational exposure.
- Cost/maintenance reviewer: checks time, complexity, upkeep, and opportunity cost.
- First-principles skeptic: challenges assumptions and asks what can be removed.

Add domain reviewers only when useful, such as design, growth, finance, research methodology, architecture, compliance, or data.

### 4. Prepare Neutral Reviewer Prompts

Use `references/prompt-patterns.md` when writing prompts for subagents or internal reviewer passes.

Each reviewer prompt must include:

- The decision question.
- The options, described symmetrically.
- Relevant background and constraints.
- The reviewer's perspective.
- Required output format.
- Explicit instruction to identify missing information and avoid guessing.

Each reviewer prompt must not include:

- The user's preferred answer.
- The main agent's suspected answer.
- Language that frames one option as obviously better.
- Expected scores, intended conclusion, or hidden evaluation rubric.
- Other reviewers' conclusions before the reviewer has answered.

### 5. Score Independently

Use a 1-5 score unless the user requests another scale:

- 1: poor fit or unacceptable risk.
- 2: weak fit; major caveats.
- 3: workable; meaningful tradeoffs.
- 4: strong fit; manageable caveats.
- 5: excellent fit; clearly supports the goal.

Load `references/evaluation-framework.md` when the decision needs a detailed rubric or weighted scoring.

Ask each reviewer to provide:

- Scores by relevant dimension.
- Top reason for the score.
- Largest risk or objection.
- Information that would change the score.
- Confidence: low, medium, or high.

### 6. Synthesize

Aggregate by reasoning, not by averaging alone.

Report:

- Short answer: recommended option and confidence.
- Score table: dimensions, reviewers, and final weighted view when useful.
- Consensus: points reviewers agree on.
- Disagreement: where reviewers diverge and why.
- Critical assumptions: claims that must be true for the recommendation to hold.
- Decision triggers: what new evidence would change the recommendation.
- Next action: the lowest-cost step that reduces the most uncertainty.
- Upgrade or revisit triggers when the recommendation should be reconsidered later.

## Output Shape

Use this default structure for full reviews:

```markdown
**结论**
推荐：...
置信度：...

**评分**
| 维度 | 方案 A | 方案 B | 说明 |
| --- | ---: | ---: | --- |

**分歧**
- ...

**关键假设**
- ...

**重审触发**
- ...

**下一步**
...
```

Use shorter prose for light reviews.

## Reference Files

- Read `references/prompt-patterns.md` before writing subagent prompts or simulated reviewer prompts.
- Read `references/evaluation-framework.md` when a review needs explicit dimensions, weights, or a reusable scoring rubric.
