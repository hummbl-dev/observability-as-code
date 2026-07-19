# Compatibility Note: Model-Routing Observability v0.1 and Existing Observability v0.1 Boundary

**Status: CANDIDATE - NON-CANONICAL**

Issue: hummbl-dev/observability-as-code#7

## Purpose

Document how the model-routing observability v0.1 contracts relate to and
coexist with the existing observability-as-code v0.1 boundary and packet.

## Existing observability v0.1 boundary

The existing v0.1 boundary (`docs/v0.1-boundary.md`) defines:

- A general trace contract schema (`schemas/observability-as-code-v0.1.json`)
- Trace events: `request.start`, `model.select`, `policy.check`,
  `routing.choice`, `response.complete`, `error.emit`
- Alert thresholds, retention, and SLI targets
- A validated example and negative fixture

The existing packet is a **general observability contract** for agentic
runtime behavior. It is not specific to model routing.

## Model-routing observability v0.1

The model-routing observability v0.1 contracts add:

- **Vendor-neutral, receipt-driven** metric and alert contracts specifically
  for model/runtime routing
- **3 metric categories** (economics, quality/reliability, governance/lifecycle)
- **10 alert contracts** with severity levels (informational, warning,
  blocking, incident)
- **9 dimensions** including promotion disposition, benchmark evidence date,
  and receipt schema version
- **10 event stream fixtures** covering normal and adversarial scenarios
- **Dashboard/scorecard specification** with company, task-class, and route
  views

## Compatibility

The two contracts are **additive and compatible**:

1. **Shared event vocabulary**: The model-routing event streams reuse the
   same event types (`request.start`, `model.select`, `policy.check`,
   `routing.choice`, `response.complete`) from the existing v0.1 trace
   contract. No new event types are introduced.

2. **No replacement**: The model-routing contracts do not replace the
   existing v0.1 boundary. The existing boundary remains the general
   observability contract; the model-routing contracts are a
   domain-specific profile.

3. **Receipt-driven, not vendor-driven**: The model-routing contracts
   require all metrics and alerts to be `receiptDriven: true`. The existing
   v0.1 contract does not impose this constraint. Both can coexist; the
   model-routing layer is stricter.

4. **No private content**: Both contracts prohibit private prompt/output
   content. The model-routing contracts add explicit `noPrivateContent`
   flags on dimensions that might tempted to store user content.

5. **Cost and quality joined**: The model-routing dashboard specification
   requires `costQualityJoined: true` on panels that show spend, preventing
   spend-alone from determining route quality. The existing v0.1 contract
   does not have this constraint.

6. **Promotion expiry and benchmark staleness**: The model-routing contracts
   make these first-class governance signals. The existing v0.1 contract
   does not cover route promotion lifecycle.

7. **Silent paid fallback detection**: The model-routing contracts require
   a `silent-paid-fallback` alert. The existing v0.1 contract has no
   equivalent.

## Non-goals

- This note does not modify the existing v0.1 boundary.
- This note does not merge the two contracts into one.
- This note does not claim the model-routing contracts supersede the
  general observability contract.
- This note does not authorize CI enforcement.

## Confirmation

This repo neither chooses nor promotes routes. The observability contracts
consume route and execution receipts; they do not select models, alter
production routing, or infer route promotion.
