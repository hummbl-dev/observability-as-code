# Prior Art and Adjacent Ecosystem References

This document collects public prior art, adjacent ecosystem projects, vocabulary references, and key concepts that inform the `observability-as-code` domain.

> **Note: These are references, NOT adopted canon.**
>
> Nothing in this document is adopted as operating canon for this repository. These entries are collected to orient contributors, clarify vocabulary, and surface adjacent work. They are public, independent projects with their own licenses, governance, and communities. Referencing them here does not imply endorsement, integration, or that their definitions override this repository's own schemas, examples, or boundary.
>
> See [`docs/principles.md`](principles.md) ("Separate examples from adopted operating canon") and [`docs/definition.md`](definition.md) ("It is not ... adopted HUMMBL canon").

---

## Public Prior Art

These are widely used public projects and platforms in the observability space. They are referenced for context only.

### OpenTelemetry

- **What it does:** A vendor-neutral specification, SDKs, and tooling for generating, collecting, and exporting telemetry (metrics, logs, traces) from instrumented applications.
- **Relevance to this repo:** Defines the most widely adopted vocabulary and data model for telemetry primitives (traces, spans, metrics, logs, resource attributes). Its instrumentation model is a primary input for what an observability-as-code repository would express and govern.
- **Docs:** https://opentelemetry.io/docs/

### Prometheus

- **What it does:** A time-series database and monitoring system with a pull-based metrics collection model, PromQL query language, and alerting rules.
- **Relevance to this repo:** Establishishes the dominant model for metrics collection, recording rules, and alert rule definitions expressed as code (rule files). Alert rule files are a canonical example of observability primitives expressed as versioned source.
- **Docs:** https://prometheus.io/docs/introduction/overview/

### Grafana

- **What it does:** An open-source visualization and analytics platform that queries multiple data sources to build dashboards and panels.
- **Relevance to this repo:** Demonstrates dashboards-as-code through provisioning, JSON dashboard models, and Terraform/Ansible-style export. A key reference for how dashboards can be represented, reviewed, and versioned as files.
- **Docs:** https://grafana.com/docs/grafana/latest/

### Datadog

- **What it does:** A commercial observability platform providing metrics, traces, logs, dashboards, monitors, and SLO tracking as a managed service.
- **Relevance to this repo:** Illustrates a unified commercial model for metrics, traces, logs, monitors, and SLOs, plus infrastructure-as-code tooling (Terraform provider). A reference for how an integrated vendor models these primitives and exposes them as code.
- **Docs:** https://docs.datadoghq.com/

### Honeycomb

- **What it does:** A commercial observability platform focused on high-cardinality event analysis, tracing, and interactive query of production behavior.
- **Relevance to this repo:** Demonstrates an event-/trace-centric, high-cardinality model of observability distinct from metric-centric tooling. A reference for how telemetry is modeled as wide events and queried interactively.
- **Docs:** https://docs.honeycomb.io/

### Jaeger

- **What it does:** An open-source distributed tracing platform for monitoring and troubleshooting distributed transactions.
- **Relevance to this repo:** A reference implementation for distributed trace storage, query, and visualization. Illustrates how trace data is stored, sampled, and surfaced, informing how trace contracts could be expressed as code.
- **Docs:** https://www.jaegertracing.io/docs/

### Tempo

- **What it does:** An open-source, highly scalable distributed tracing backend by Grafana Labs that stores traces and indexes them by trace ID.
- **Relevance to this repo:** A reference for trace storage and retrieval at scale, integrated with metrics and logs. Informs how trace backends fit into a broader observability-as-code topology.
- **Docs:** https://grafana.com/docs/tempo/latest/

### Loki

- **What it does:** An open-source log aggregation system by Grafana Labs designed for cost-effective storage and querying of logs.
- **Relevance to this repo:** A reference for log storage and query. Informs how log primitives (labels, streams, queries) can be modeled alongside metrics and traces in an observability-as-code repository.
- **Docs:** https://grafana.com/docs/loki/latest/

---

## Adjacent Ecosystem

These projects are adjacent to the core observability stack, often extending it with SLO management, scalable storage, or legacy monitoring models.

### Pyrra

- **What it does:** An open-source SLO tool for Kubernetes that generates Prometheus alerting and recording rules from SLO definitions, with a UI for visualizing SLOs.
- **Relevance to this repo:** A reference for SLO-as-code: SLO objectives expressed as declarative definitions that compile into alert rules. Directly informs how SLO definitions could be a first-class primitive in this repository.
- **Docs:** https://pyrra.dev/docs/

### Sloth

- **What it does:** An open-source tool that generates Prometheus SLO rules from a declarative SLO specification (OpenSLO-style).
- **Relevance to this repo:** Another reference for SLO-as-code with a focus on a simple YAML spec and rule generation. Informs how SLO definitions can be authored as files and translated into platform-specific rules.
- **Docs:** https://sloth.dev/

### Cortex

- **What it does:** An open-source, horizontally scalable, long-term storage backend for Prometheus metrics with multi-tenant support.
- **Relevance to this repo:** A reference for scalable metrics storage and multi-tenancy. Informs how an observability-as-code topology can express where metrics are stored and how tenants are separated.
- **Docs:** https://cortexmetrics.io/docs/

### Mimir

- **What it does:** The Grafana Labs successor to Cortex: an open-source, horizontally scalable, highly available Prometheus-compatible metrics backend.
- **Relevance to this repo:** A reference for the current generation of scalable metrics backends. Informs how metrics storage topology and retention are modeled in an observability-as-code repository.
- **Docs:** https://grafana.com/docs/mimir/latest/

### VictoriaMetrics

- **What it does:** An open-source, cost-effective, scalable time-series database and monitoring solution compatible with Prometheus.
- **Relevance to this repo:** A reference for an alternative metrics storage and query engine with its own clustering and downsampling model. Informs how storage-backend choice is expressed as part of an observability topology.
- **Docs:** https://docs.victoriametrics.com/

### Zabbix

- **What it does:** A mature open-source monitoring platform for networks, servers, virtual machines, and applications, with agent-based and agentless collection.
- **Relevance to this repo:** A reference for the legacy monitoring model (host-centric checks, triggers, items) that predates the cloud-native observability stack. Useful as contrast and for migration/interop vocabulary.
- **Docs:** https://www.zabbix.com/documentation/current/en/manual

### Nagios

- **What it does:** A long-standing open-source monitoring system for host and service checks, alerts, and plugin-based monitoring.
- **Relevance to this repo:** A reference for the classic check-based, alert-on-threshold monitoring model. Provides historical context for how alerting and service-state concepts evolved into modern observability primitives.
- **Docs:** https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/

---

## Vocabulary References

These terms recur across the observability domain. The definitions below are orientation only and do not override this repository's own schemas or boundary. Where applicable, a public reference is linked.

### observability-as-code

- **Meaning:** Treating dashboards, alerts, SLOs, traces, logs, metrics, runbooks, and operational visibility primitives as version-controlled, reviewable, testable, auditable, and agent-operable source material.
- **Relevance:** The core concept of this repository.
- **Reference:** See [`docs/definition.md`](definition.md).

### telemetry

- **Meaning:** The data emitted by a system about its own behavior, including metrics, logs, and traces.
- **Relevance:** The raw material that observability-as-code governs and relates to operational state.
- **Reference:** https://opentelemetry.io/docs/concepts/observability-primer/

### metrics

- **Meaning:** Numeric measurements of system behavior over time, typically aggregated as time series.
- **Relevance:** A core primitive expressed as code (recording rules, dashboards, alerts).
- **Reference:** https://prometheus.io/docs/concepts/data_model/

### traces

- **Meaning:** Records of a single request or transaction as it propagates across service boundaries, composed of spans.
- **Relevance:** A core primitive; trace contracts are a candidate schema subject in this repository.
- **Reference:** https://opentelemetry.io/docs/concepts/signals/traces/

### logs

- **Meaning:** Timestamped records of discrete events emitted by a system.
- **Relevance:** A core primitive alongside metrics and traces.
- **Reference:** https://opentelemetry.io/docs/concepts/signals/logs/

### SLO (Service Level Objective)

- **Meaning:** A target level of service quality (e.g., availability, latency) that a system is expected to meet over a period.
- **Relevance:** A first-class primitive that observability-as-code expresses as declarative definitions.
- **Reference:** https://sre.google/workbook/alerting-on-slos/

### SLI (Service Level Indicator)

- **Meaning:** A quantitative measure of a service level (e.g., error rate, request latency), used to compute SLOs.
- **Relevance:** The measurement foundation for SLO definitions expressed as code.
- **Reference:** https://sre.google/workbook/implementing-slos/

### alerting

- **Meaning:** The mechanism by which a system notifies operators when a metric, SLO, or condition crosses a defined threshold or rule.
- **Relevance:** A core primitive expressed as alert rules in code, with routing and notification topology.
- **Reference:** https://prometheus.io/docs/alerting/latest/

---

## Key Concepts

These concepts recur across prior art and adjacent projects and are likely to appear in this repository's schemas, examples, and discussions.

### Instrumentation

- **What it is:** The act of embedding telemetry generation (metrics, logs, traces) into application code, either manually or via libraries/agents.
- **Relevance:** The upstream source of telemetry that observability-as-code governs downstream. Instrumentation choices shape what primitives can be expressed as code.
- **Reference:** https://opentelemetry.io/docs/concepts/instrumentation/

### Exporters

- **What it is:** Components that convert telemetry from one format/source into a target format or backend (e.g., Prometheus exporter, OpenTelemetry exporter).
- **Relevance:** Defines the boundary between instrumented systems and storage/query backends. An observability-as-code topology may express exporter configuration as code.
- **Reference:** https://opentelemetry.io/docs/concepts/components/#exporters

### Collectors

- **What it is:** A component (e.g., the OpenTelemetry Collector) that receives, processes, and routes telemetry from instrumented sources to one or more backends.
- **Relevance:** A central routing and processing node whose pipelines can be expressed and reviewed as code.
- **Reference:** https://opentelemetry.io/docs/collector/

### Dashboards-as-code

- **What it is:** The practice of defining dashboards (panels, queries, layout) in declarative files (JSON, YAML, Terraform) rather than via UI authoring.
- **Relevance:** A direct instance of observability-as-code; dashboards are a primary primitive this repository aims to express as versioned source.
- **Reference:** https://grafana.com/docs/grafana/latest/dashboards/manage-dashboards/

### Alert rules

- **What it is:** Declarative rules that evaluate metrics or expressions and fire alerts when conditions are met, including labels, annotations, and routing.
- **Relevance:** A core primitive expressed as code (e.g., Prometheus rule files). A canonical example of reviewable, versioned operational state.
- **Reference:** https://prometheus.io/docs/alerting/latest/rules/

### SLO definitions

- **What it is:** Declarative specifications of SLIs, objectives, time windows, and burn-rate alerting that define a service level target.
- **Relevance:** A first-class primitive for observability-as-code, demonstrated by Pyrra and Sloth. A candidate schema subject for this repository.
- **Reference:** https://github.com/OpenSLO/OpenSLO

---

## Status

Reference document only. Not adopted canon. Entries are collected to orient contributors and clarify the domain. See [`docs/roadmap.md`](roadmap.md) and [`docs/v0.1-boundary.md`](v0.1-boundary.md) for the current scope and boundary of this repository.
