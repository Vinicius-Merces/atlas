---
name: observability-design
description: "Design logs, metrics, traces, dashboards, and alerts for a feature or service."
---

# Observability Design Skill

## Purpose

Design actionable, privacy-aware logs, metrics, traces, dashboards, and alerts for a feature or service while keeping instrumentation portable where practical.

## Inputs

- System boundaries and deployment topology
- Critical user journeys and business outcomes
- Failure modes and dependencies
- Existing telemetry/instrumentation standards
- Operational ownership
- Privacy/security constraints
- Traffic, cardinality, and telemetry-cost constraints

## Procedure

1. Identify critical user and system outcomes that operations must be able to observe.
2. Map failure points, dependencies, asynchronous boundaries, external providers, and recovery paths.
3. Inventory existing instrumentation and observability backends before adding a new stack.
4. Define logs, metrics, traces, and domain/operational events for the important boundaries.
5. Prefer OpenTelemetry-compatible instrumentation and OTLP-compatible transport for new/distributed systems when it improves portability and does not conflict with a healthy project standard.
6. Decide whether an OpenTelemetry Collector is useful for batching, processing, redaction, sampling, enrichment, multi-backend export, or reducing vendor-specific application coupling. Do not deploy one by default without a reason.
7. Define service/environment/version resource attributes and correlation requirements across requests, jobs, queues, and dependencies.
8. Define stable error classes and avoid using free-form error strings as the primary metric dimension.
9. Review metric/span/log attributes for bounded cardinality. Do not place secrets, raw prompts, sensitive payloads, or unbounded user/content values in telemetry dimensions.
10. Define sampling, retention/volume expectations, and what must remain unsampled for correctness or incident evidence.
11. Define dashboards around user impact, service health, dependency health, capacity, latency, and failure/recovery behavior.
12. Define actionable alert thresholds, owners, runbook/escalation links, and anti-noise policy.
13. Validate that telemetry export/backend failure does not unintentionally break the product unless a policy explicitly requires fail-closed behavior.
14. For AI/model integrations, correlate logical capability profile, provider/model, latency, retries/fallback, validation failures, and provider errors without logging sensitive prompt/output content by default.
15. Validate privacy, diagnostic usefulness, telemetry cost, and expected behavior under incident conditions.

## OpenTelemetry guidance

OpenTelemetry is a vendor-neutral instrumentation/telemetry framework, not an observability backend.

Use it when the project benefits from one instrumentation model that can export to open-source or commercial backends. Existing healthy vendor instrumentation does not need to be replaced merely for conformity.

When an OpenTelemetry Collector is used, document:

- receivers/protocols
- processors, sampling, filtering, redaction, or enrichment
- exporters/backends
- deployment/topology
- failure/backpressure expectations
- config ownership
- resource limits

## Output

- Signal map
- Resource/correlation convention
- Telemetry schema and cardinality constraints
- Sampling/retention/volume policy
- Collector decision and topology when applicable
- Dashboard requirements
- Alerts, owners, and escalation/runbook requirements
- Privacy/redaction constraints
- AI/provider telemetry requirements when applicable
- Validation plan and residual observability gaps

## Trigger conditions

Use when a feature/service changes operational behavior, adds dependencies/providers, changes failure modes, or needs new production evidence, dashboards, traces, or alerts.

## Dependencies

- `framework/observability-model.md`
- Canonical project memory and operational ownership
- `external-api-resilience-review` when provider/API failure is material
- privacy/security review when telemetry can contain sensitive data
- `framework/llm-provider-routing-model.md` when LLM/provider routing exists

## Limitations

- Does not require OpenTelemetry, a Collector, Sentry, Datadog, New Relic, Grafana, or any other specific vendor for every project.
- Does not treat telemetry volume as observability quality.
- Does not grant authority to expose sensitive production data for debugging.
- Does not approve release readiness by itself.

## Validation

- Confirm every critical outcome/failure has an inspectable signal or a documented blind spot.
- Verify representative correlation across at least one important request/job/dependency path when traces or correlation are required.
- Validate dashboards/alerts against real or safely simulated failure evidence where practical.
- Inspect cardinality and sensitive-data behavior.
- Verify the product remains stable when telemetry export/backends are unavailable unless policy says otherwise.
- Record missing/stale evidence and residual risk rather than guessing.
