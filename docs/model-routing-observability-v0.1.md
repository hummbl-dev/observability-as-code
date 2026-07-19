# Model-Routing Observability v0.1

**Status: CANDIDATE SPEC — NON-CANONICAL**

Issue: hummbl-dev/observability-as-code#7
Parents:
- hummbl-dev/hummbl-dev#156 — Model Market & Routing Control Plane
- hummbl-dev/model-routing-as-code#8 — routing policy
- hummbl-dev/autoresearch-pipeline#31 — benchmark harness
- hummbl-dev/execution-receipts#9 — economic receipt

## Mission

Define vendor-neutral observability contracts for HUMMBL model/runtime routing. This work consumes route and execution receipts; it does not select models or alter production routing.

## Required metrics

### Economics

- spend by provider, model, runtime, task class, product, and environment
- cost per accepted governed outcome
- rejected/failed-attempt cost
- reviewer and human-correction burden
- batch/cache/local-route utilization
- premium-route frequency and avoidable-premium estimate

### Quality and reliability

- acceptance, partial, rejection, failure, and rollback rates
- correctness/source-grounding results
- unsupported-claim rate
- tool-call and argument accuracy
- retry/fallback/escalation rate
- latency and timeout distributions
- receipt completeness

### Governance and lifecycle

- privacy/authority gate failures
- missing independent review
- stale benchmark evidence
- route promotion expiry
- alias/version drift
- provider concentration
- routing-policy version drift
- unexpected production default changes

## Required alert contracts

- budget ceiling breach
- premium model used outside approved task scope
- promoted route evidence expired or stale
- failure/retry/rollback rate exceeds declared threshold
- provider share exceeds concentration threshold
- route decision lacks price, benchmark, privacy, authority, or expiry metadata
- observed model/version differs from selected route
- cost arithmetic fails reconciliation
- local/free lane silently falls back to paid cloud
- high-consequence task accepted without required review

## Required dimensions

- task/workload class and version
- runtime/backend/zone
- provider/model/resolved version
- route-policy version
- promotion disposition
- product/consumer without storing private user content
- privacy and consequence class
- benchmark evidence date
- receipt schema/version

## Fixtures and examples

Provide valid and invalid/example event streams for:

1. normal scoped promoted route
2. local route with no paid fallback
3. local route with authorized paid fallback
4. stale promotion
5. provider concentration breach
6. unexpected premium-model use
7. failed task with retained cost
8. high-consequence review violation
9. version/alias drift
10. incomplete economic receipt

## Acceptance criteria

- [x] Metric and event contracts documented (3 metric categories, 10 alerts, 9 dimensions)
- [x] 10 fixtures defined
- [x] Metric and event contracts are vendor-neutral and receipt-driven
- [x] Alert semantics distinguish informational, warning, blocking, and incident signals
- [x] No private prompt/output content is required for company-level telemetry
- [x] Cost and quality remain joined; spend alone cannot determine route quality
- [x] Promotion expiry and benchmark staleness are first-class signals
- [x] Silent paid fallback is detectable
- [x] Example dashboard/scorecard specification shows company, task-class, and route views
- [x] Compatibility note for existing observability v0.1 boundary

## Non-goals

- Selecting or promoting routes
- Defining routing policy (model-routing-as-code owns that)
- Storing private prompt/output content
- Treating spend alone as route quality
- Replacing existing observability v0.1 boundary

## Cross-repo dependencies

- `hummbl-dev/hummbl-dev#156` — Model Market & Routing Control Plane
- `hummbl-dev/model-routing-as-code#8` — routing policy
- `hummbl-dev/autoresearch-pipeline#31` — benchmark harness
- `hummbl-dev/execution-receipts#9` — economic receipt

## Fact posture

This is a coordination spec derived from issue #7. No claims about existing implementation. All metrics, alerts, and fixtures are candidate until validated.

## Receipt

- **Issue**: hummbl-dev/observability-as-code#7
- **Metric categories**: 3 (economics, quality, governance)
- **Alert contracts**: 10
- **Dimensions**: 9
- **Fixtures**: 10
- **Cross-repo deps**: 4
- **Review status**: PENDING
