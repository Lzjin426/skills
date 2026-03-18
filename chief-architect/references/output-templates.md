# Output Templates

## Architecture Design Document

```markdown
# Architecture Design: {System Name}

## 1. Context & Requirements

### Business Context
- Problem statement
- Business goals and success metrics

### Functional Requirements
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | ... | Must |

### Non-Functional Requirements
| Attribute | Target | Rationale |
|-----------|--------|-----------|
| Availability | 99.9% | ... |
| Latency (p99) | <200ms | ... |
| Throughput | 10k RPS | ... |
| Data retention | 7 years | ... |

### Constraints
- Budget, team size, timeline, regulatory, existing infrastructure

---

## 2. Architecture Decision

### Candidates Evaluated

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Scalability | ... | ... | ... |
| Complexity | ... | ... | ... |
| Time to market | ... | ... | ... |
| Ops cost | ... | ... | ... |

### Selected: {Option}
**Rationale**: ...
**Trade-offs accepted**: ...

---

## 3. System Architecture

### High-Level View
[Mermaid diagram: system context / C4 Level 1]

### Component View
[Mermaid diagram: component interactions / C4 Level 2]

### Data Flow
[Mermaid diagram: sequence or flow]

---

## 4. Component Specifications

### {Component Name}
- **Responsibility**: Single-sentence purpose
- **Tech stack**: Language, framework, database
- **API contract**: Key endpoints / interfaces
- **Data model**: Key entities and relationships
- **Scaling strategy**: Horizontal / vertical / auto

(Repeat for each component)

---

## 5. Tech Stack Decisions

| Layer | Choice | Alternatives Considered | Rationale | Switching Cost |
|-------|--------|------------------------|-----------|---------------|
| Language | ... | ... | ... | ... |
| Framework | ... | ... | ... | ... |
| Database | ... | ... | ... | ... |
| Messaging | ... | ... | ... | ... |
| Hosting | ... | ... | ... | ... |

---

## 6. Cross-Cutting Concerns
- Authentication & authorization strategy
- Logging & observability
- Error handling & resilience patterns
- CI/CD pipeline outline

---

## 7. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ... | High/Med/Low | High/Med/Low | ... |

---

## 8. Open Decisions

| ID | Decision | Options | Recommendation | [DECISION NEEDED] |
|----|----------|---------|----------------|-------------------|
| D-01 | ... | A, B, C | ... | Yes |
```

---

## Implementation Plan

```markdown
# Implementation Plan: {Project Name}

## 1. Current State Assessment
- Architecture summary
- Key pain points / technical debt
- What works well (preserve)

## 2. Target State
- Architecture summary
- Key improvements over current state
- Success criteria

## 3. Gap Analysis

| Area | Current | Target | Gap | Effort |
|------|---------|--------|-----|--------|
| ... | ... | ... | ... | S/M/L |

## 4. Execution Phases

### Phase 1: {Name} (Week 1-N)
**Goal**: ...
**Prerequisites**: None

#### Tasks

| # | Task | Description | Acceptance Criteria | Size | Depends On | Parallelizable |
|---|------|-------------|---------------------|------|------------|----------------|
| 1.1 | ... | ... | ... | S/M/L | - | Yes/No |
| 1.2 | ... | ... | ... | S/M/L | 1.1 | Yes/No |

#### Phase Exit Criteria
- [ ] ...

### Phase 2: {Name} (Week N-M)
(Same structure)

## 5. Dependency Graph
[Mermaid gantt or flowchart showing phase/task dependencies]

## 6. Risk Register

| Risk | Phase | Probability | Impact | Mitigation |
|------|-------|-------------|--------|------------|
| ... | ... | ... | ... | ... |

## 7. Decisions Needed

| Decision | Context | Options | Recommendation |
|----------|---------|---------|----------------|
| [DECISION NEEDED] ... | ... | ... | ... |
```

---

## Version Roadmap

```markdown
# Version Roadmap: {Product Name}

## Product Vision
- One-paragraph vision statement
- Target users
- Core value proposition

## Version Overview

| Version | Theme | Key Outcome | Graduation Criteria |
|---------|-------|-------------|---------------------|
| v0.1 (MVP) | Core loop | Validate core assumption | ... |
| v0.2 (Alpha) | ... | ... | ... |
| v1.0 (GA) | ... | ... | ... |

## Detailed Version Plans

### v0.1 — MVP
**Theme**: ...
**Timeline estimate**: ...
**Goal**: Validate that {core assumption}

#### Features
| Feature | Description | Priority | Complexity |
|---------|-------------|----------|------------|
| ... | ... | Must | S/M/L |

#### Tech Stack
| Layer | Choice | Rationale |
|-------|--------|-----------|
| ... | ... | ... |

#### Deliverables
- [ ] ...

#### Success Metrics
- ...

#### What is explicitly OUT of scope
- ...

### v0.2 — Alpha
(Same structure)

### v1.0 — GA
(Same structure)

## Technical Debt Budget
- What shortcuts are taken in MVP and when they must be addressed
```

---

## Feasibility Report

```markdown
# Feasibility Analysis: {Feature/Product}

## 1. Request Summary
- What is being asked
- Why it matters (business context)

## 2. Technical Decomposition

| Sub-Problem | Known Solution? | Complexity | Risk |
|-------------|----------------|------------|------|
| ... | Yes / Partial / No | S/M/L | Low/Med/High |

## 3. Feasibility Verdict

**Overall: {Feasible / Feasible with Risks / Not Feasible}**
**Confidence: {High / Medium / Low}**

### Rationale
...

## 4. Recommended Approach
- High-level approach description
- Key technologies
- Estimated effort (order of magnitude)

## 5. Alternative Approaches

| Approach | Pros | Cons | Effort |
|----------|------|------|--------|
| A (recommended) | ... | ... | ... |
| B | ... | ... | ... |

## 6. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ... | ... | ... | ... |

## 7. Recommendations
- Go / No-go recommendation with conditions
- If Go: immediate next steps
- If No-go: what would change the assessment
```

---

## Architecture Review Report

```markdown
# Architecture Review: {Project Name}

## 1. Review Scope
- Components reviewed
- Methodology
- Date of review

## 2. Architecture Overview
- Current architecture summary (as understood)
- [Mermaid diagram of current state]

## 3. Findings

### Critical Issues
| # | Finding | Impact | Affected Components | Fix | Effort |
|---|---------|--------|--------------------|----|--------|
| C-01 | ... | ... | ... | ... | S/M/L |

### Warnings
| # | Finding | Impact | Affected Components | Fix | Effort |
|---|---------|--------|--------------------|----|--------|
| W-01 | ... | ... | ... | ... | S/M/L |

### Suggestions
| # | Finding | Benefit | Fix | Effort |
|---|---------|---------|-----|--------|
| S-01 | ... | ... | ... | S/M/L |

## 4. Priority Matrix

[Plot findings on Impact vs Effort matrix]

| | Low Effort | High Effort |
|---|-----------|-------------|
| **High Impact** | Do First: C-01, W-02 | Plan: C-03 |
| **Low Impact** | Quick Wins: S-01 | Backlog: S-04 |

## 5. Improvement Roadmap

### Immediate (This Sprint)
- ...

### Short-term (This Quarter)
- ...

### Long-term (Next Quarter+)
- ...

## 6. Positive Observations
- What the codebase does well (acknowledge good patterns)
```
