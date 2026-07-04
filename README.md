# Observability as Code

`observability-as-code` explores how to represent dashboards, alerts, SLOs, traces, logs, metrics, runbooks, and operational visibility primitives as version-controlled, reviewable, testable, auditable, and agent-operable source material.

## Working Definition

`Observability-as-Code` means treating dashboards, alerts, SLOs, traces, logs, metrics, runbooks, and operational visibility primitives as canonical operational state expressed through files, schemas, examples, tests, and reviewable change history.

## Goals

- Define the domain clearly.
- Collect prior art and examples.
- Provide reusable schemas and templates.
- Support human review and agent execution.
- Preserve auditability, provenance, and governance boundaries.

## Non-Goals

- This repo is not a universal standard.
- This repo is not legal, security, compliance, or operational advice.
- This repo does not canonize HUMMBL/BaseN/Ownward concepts unless explicitly marked and audited.

## Packet status

- `v0.1-draft` -> `validated-example`

## v0.1 packet locations

- Boundary: [`docs/v0.1-boundary.md`](docs/v0.1-boundary.md)
- Schema: [`schemas/observability-as-code-v0.1.json`](schemas/observability-as-code-v0.1.json)
- Example: [`examples/trace-contract-v0.1.example.json`](examples/trace-contract-v0.1.example.json)
- Fixtures: [`fixtures/valid/trace-contract-v0.1.valid.json`](fixtures/valid/trace-contract-v0.1.valid.json), [`fixtures/invalid/trace-contract-v0.1.invalid.json`](fixtures/invalid/trace-contract-v0.1.invalid.json)

## Status

Public seed repository. Initial executable packet in progress as `v0.1-draft` -> `validated-example`.
