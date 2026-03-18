# Architecture Review Checklist

Evaluate each area systematically. Rate severity: Critical / Warning / Suggestion.

## 1. Structural Health

- [ ] **Single Responsibility**: Each module/service has one clear purpose
- [ ] **Dependency Direction**: Dependencies flow inward (domain has no external deps)
- [ ] **Circular Dependencies**: No circular references between modules
- [ ] **Layer Violations**: No layer-skipping (e.g., UI directly accessing DB)
- [ ] **God Objects**: No classes/modules with too many responsibilities (>500 LOC is a smell)
- [ ] **Dead Code**: No unused exports, unreachable code paths, or zombie features

## 2. API & Interface Design

- [ ] **Consistency**: Naming conventions, error formats, response shapes are uniform
- [ ] **Versioning**: API versioning strategy exists and is followed
- [ ] **Contract Clarity**: Input/output types are explicit (TypeScript types, JSON schemas, protobuf)
- [ ] **Error Handling**: Errors are structured, categorized, and carry actionable context
- [ ] **Idempotency**: Mutating operations are idempotent where needed

## 3. Data Architecture

- [ ] **Schema Design**: Normalized appropriately, no redundant storage without justification
- [ ] **Migration Strategy**: Schema changes are versioned and reversible
- [ ] **Query Performance**: No N+1 queries, proper indexing, pagination for large sets
- [ ] **Data Boundaries**: Each service owns its data; no shared databases across services
- [ ] **Consistency Model**: Explicit choice between strong/eventual consistency per use case

## 4. Scalability & Performance

- [ ] **Bottleneck Identification**: Known bottlenecks are documented with mitigation plans
- [ ] **Caching Strategy**: Cache layers are intentional with clear invalidation rules
- [ ] **Async Processing**: Long-running tasks use queues/workers, not request threads
- [ ] **Connection Pooling**: Database and external service connections are pooled
- [ ] **Load Testing**: Performance baselines exist for critical paths

## 5. Reliability & Resilience

- [ ] **Failure Isolation**: One component failure doesn't cascade to the entire system
- [ ] **Retry Logic**: Retries use exponential backoff with jitter
- [ ] **Circuit Breakers**: External calls have circuit breaker patterns
- [ ] **Timeouts**: All external calls have explicit timeouts
- [ ] **Graceful Degradation**: System degrades gracefully under partial failure
- [ ] **Health Checks**: Each service exposes health endpoints

## 6. Security

- [ ] **Auth Architecture**: Authentication and authorization are centralized
- [ ] **Secret Management**: No hardcoded secrets; secrets are injected via env/vault
- [ ] **Input Validation**: All external input is validated at system boundaries
- [ ] **OWASP Top 10**: No obvious injection, XSS, CSRF, or insecure deserialization risks
- [ ] **Least Privilege**: Services and roles have minimal necessary permissions
- [ ] **Audit Trail**: Security-relevant actions are logged

## 7. Observability

- [ ] **Structured Logging**: Logs are structured (JSON), not free-form strings
- [ ] **Distributed Tracing**: Requests can be traced across service boundaries
- [ ] **Metrics**: Key business and system metrics are collected (latency, error rate, saturation)
- [ ] **Alerting**: Alerts exist for SLO violations with clear runbooks
- [ ] **Dashboards**: Critical system health is visible at a glance

## 8. Developer Experience

- [ ] **Setup Time**: New developer can run the system locally in <30 minutes
- [ ] **Test Coverage**: Critical paths have automated tests; test strategy is documented
- [ ] **CI/CD**: Automated build, test, deploy pipeline exists
- [ ] **Documentation**: Architecture decisions are recorded (ADRs or equivalent)
- [ ] **Code Standards**: Linting, formatting, and commit conventions are enforced

## 9. Deployment & Operations

- [ ] **Environment Parity**: Dev/staging/prod environments are structurally identical
- [ ] **Rollback Strategy**: Deployments can be rolled back quickly
- [ ] **Feature Flags**: Risky features can be toggled without redeployment
- [ ] **Database Migrations**: Migrations are backward-compatible for zero-downtime deploys
- [ ] **Infrastructure as Code**: Infrastructure is version-controlled and reproducible

## 10. Cost & Sustainability

- [ ] **Resource Efficiency**: No over-provisioned resources or wasteful patterns
- [ ] **Vendor Lock-in**: Critical dependencies have abstraction layers or exit strategies
- [ ] **Technical Debt Register**: Known debt is tracked with retirement plans
- [ ] **License Compliance**: Third-party dependencies have compatible licenses
