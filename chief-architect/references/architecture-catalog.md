# Architecture Pattern Catalog

Quick reference for common architecture patterns. Use to match project requirements to proven solutions.

## System Architecture Patterns

### Monolith
**When**: Early-stage product, small team (<8), rapid iteration needed, domain boundaries unclear
**Strengths**: Simple deployment, easy debugging, low latency between components, fast development
**Risks**: Scaling bottlenecks, deployment coupling, team contention at scale
**Evolution path**: Monolith → Modular monolith → Microservices (when needed)

### Modular Monolith
**When**: Growing team, clear domain boundaries emerging, want monolith simplicity with better organization
**Strengths**: Module isolation within single deployment, refactoring safety, clear ownership
**Risks**: Module boundary violations if not enforced, still single deployment
**Key rule**: Modules communicate through defined interfaces, never direct DB access

### Microservices
**When**: Large teams (>20), independent deployment needed, different scaling requirements per domain, polyglot tech stack
**Strengths**: Independent scaling, team autonomy, fault isolation, tech flexibility
**Risks**: Distributed system complexity, data consistency, network latency, operational overhead
**Prerequisites**: CI/CD maturity, observability, team org alignment (Conway's Law)

### Event-Driven / Event Sourcing
**When**: Audit trails critical, temporal queries needed, complex workflows, decoupled integrations
**Strengths**: Temporal queries, complete audit log, loose coupling, replay capability
**Risks**: Eventual consistency complexity, event schema evolution, debugging difficulty
**Good fit**: Financial systems, order processing, IoT data pipelines

### CQRS (Command Query Responsibility Segregation)
**When**: Read and write patterns diverge significantly, complex read models, high read:write ratio
**Strengths**: Optimized read/write paths independently, scalable reads
**Risks**: Increased complexity, eventual consistency between read/write models
**Often paired with**: Event Sourcing

### Serverless / FaaS
**When**: Unpredictable traffic, event-triggered workloads, cost optimization for low-traffic services
**Strengths**: Zero idle cost, auto-scaling, reduced ops burden
**Risks**: Cold starts, vendor lock-in, debugging difficulty, stateless constraints, 15min execution limit
**Good fit**: Webhooks, scheduled jobs, image processing, simple APIs

---

## Data Architecture Patterns

### Shared Database
**When**: Single service/monolith, simple CRUD operations
**Risk**: Coupling between consumers. Avoid for multi-service architectures.

### Database per Service
**When**: Microservices that need data autonomy
**Coordination**: Saga pattern or event-driven for cross-service transactions

### CQRS with Read Replicas
**When**: High read:write ratio (>10:1), complex query requirements
**Implementation**: Write to primary DB, project to read-optimized stores (Elasticsearch, Redis, materialized views)

### Data Lake / Lakehouse
**When**: Analytics workloads, ML pipelines, heterogeneous data sources
**Pattern**: Raw → Staged → Curated (bronze/silver/gold)

---

## Communication Patterns

### Synchronous (REST / gRPC)
**REST**: Public APIs, CRUD operations, browser clients
**gRPC**: Internal service-to-service, streaming, performance-critical paths
**Risk**: Temporal coupling — caller blocked until response

### Asynchronous (Message Queue)
**When**: Decoupled processing, workload buffering, reliability needed
**Tools**: RabbitMQ (task queues), Kafka (event streaming), SQS (simple queuing)
**Pattern choice**: Point-to-point (queue) vs pub/sub (topic) based on consumer model

### GraphQL
**When**: Multiple frontend clients with different data needs, rapid frontend iteration
**Risk**: N+1 queries, complexity in authorization, caching challenges
**Mitigation**: DataLoader pattern, persisted queries, depth limiting

---

## Frontend Architecture Patterns

### SPA (Single Page Application)
**When**: Rich interactivity, desktop-like UX, authenticated apps
**Frameworks**: React, Vue, Svelte, Angular
**Trade-off**: SEO challenges, initial load time vs smooth navigation

### SSR / SSG (Server-Side Rendering / Static Generation)
**When**: SEO critical, content-heavy, fast first paint
**Frameworks**: Next.js, Nuxt, Astro, SvelteKit
**Pattern**: SSG for static content, SSR for dynamic, ISR for hybrid

### Micro-Frontends
**When**: Large teams owning different UI domains, independent deployment of frontend sections
**Risk**: Bundle size, inconsistent UX, routing complexity
**Prerequisite**: Design system / shared component library

### Islands Architecture
**When**: Mostly static content with interactive islands, performance-critical
**Framework**: Astro
**Benefit**: Minimal JS shipped, progressive hydration

---

## Resilience Patterns

| Pattern | Purpose | When to Apply |
|---------|---------|---------------|
| Circuit Breaker | Stop calling failing service | External dependencies |
| Retry with Backoff | Handle transient failures | Network calls, API requests |
| Bulkhead | Isolate failure blast radius | Shared thread pools, connection pools |
| Timeout | Prevent indefinite waiting | All external calls |
| Fallback | Provide degraded service | Non-critical features |
| Rate Limiting | Protect from overload | Public APIs, shared resources |
| Saga | Manage distributed transactions | Cross-service data consistency |

---

## Deployment Patterns

| Pattern | Description | When |
|---------|-------------|------|
| Blue-Green | Two identical environments, swap traffic | Zero-downtime, quick rollback |
| Canary | Gradual traffic shift to new version | Risk-sensitive releases |
| Rolling | Update instances incrementally | Standard deployments |
| Feature Flags | Toggle features without deployment | A/B testing, gradual rollout |
| Shadow / Dark Launch | Run new version in parallel without serving | Validate under production load |

---

## Decision Heuristics

When choosing between patterns, use these rules of thumb:

1. **Start simple, evolve when needed**: Monolith → modular → micro. Don't pre-optimize.
2. **Conway's Law**: Architecture mirrors team structure. Align both.
3. **The 3-service rule**: Don't go microservices until you have at least 3 clearly separable domains.
4. **Boring technology advantage**: Prefer proven tech unless the requirement truly demands novelty.
5. **Reversibility test**: Prefer decisions that are easy to reverse. Make irreversible decisions carefully.
6. **Data gravity**: Data is the hardest thing to move. Get data architecture right early.
7. **Buy vs build**: Build what differentiates you; buy/use SaaS for everything else.
