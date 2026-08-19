# Observability Model

Observability provides evidence about internal system behavior from external signals.

## Signal types

### Logs

Structured records of meaningful events and failures.

### Metrics

Aggregated measurements used to track health, capacity, latency, errors, and business outcomes.

### Traces

End-to-end visibility across distributed requests and dependencies.

### Events

Domain and operational transitions that explain system state changes.

## OpenTelemetry-first portability

For new systems, distributed services, or projects without a conflicting established standard, prefer OpenTelemetry-compatible instrumentation and OTLP-compatible signal transport when practical.

The objective is provider-neutral telemetry, not mandatory deployment of one specific backend or collector in every project.

OpenTelemetry is an instrumentation and telemetry framework, not the storage/visualization backend. Projects may export to open-source or commercial backends according to operational needs.

Use an OpenTelemetry Collector when it materially helps to:

- receive telemetry from multiple services or formats;
- batch, filter, sample, enrich, or redact signals;
- export the same instrumentation to one or more backends;
- reduce application coupling to vendor-specific agents;
- centralize telemetry routing and policy.

Do not add a Collector or SDK merely for architectural fashion when the project already has a healthy, sufficient observability standard.

## Telemetry contract

A production service should define, where applicable:

- service name and environment
- version/release identifier
- request/trace/correlation identifiers
- stable error classification
- latency and throughput measurements
- dependency/provider spans
- user-impact or business outcome signals
- privacy/redaction policy
- sampling policy
- retention/volume expectations
- backend/export path
- dashboard and alert ownership

Attribute cardinality must be controlled. User IDs, raw URLs with unbounded query values, prompt text, secrets, or other high-cardinality/sensitive values must not be added casually to metric dimensions.

## Design principles

- Emit signals at important boundaries.
- Include correlation identifiers.
- Prefer provider-neutral semantic conventions when they fit the stack.
- Avoid sensitive data in telemetry.
- Do not log raw AI prompts/outputs by default.
- Prefer actionable signals over noisy volume.
- Define owners for alerts.
- Align telemetry with user impact.
- Validate dashboards and alerts before incidents occur.
- Treat telemetry cost and cardinality as part of the design.
- Preserve application function if the telemetry backend is unavailable unless policy explicitly requires fail-closed behavior.

## AI/provider observability

When LLMs or other external AI providers are used, record provider-neutral operational evidence where policy permits:

- logical capability profile
- concrete provider/model identifier
- latency
- timeout/retry/fallback state
- structured-output validation failures
- tool-call failure classes
- rate/capacity errors
- API cost estimate or owned-compute class when available

Do not emit prompts, retrieved private context, personal data, secrets, or model output merely to improve debugging convenience.

## Minimum operational questions

A production system should make it possible to answer:

- Is the system healthy?
- Who or what journey is affected?
- What changed?
- Where is the failure?
- Which dependency/provider is contributing?
- How severe is it?
- Is the failure transient, capacity-related, or deterministic?
- Can we mitigate, fail over, degrade safely, or roll back?

## Related ATLAS capabilities

- `observability-design` turns these principles into signal, dashboard, and alert requirements.
- `framework/llm-provider-routing-model.md` defines provider-neutral LLM telemetry requirements.
- `external-api-resilience-review` applies when provider outages/rate limits are material.
- privacy and security review define what telemetry may contain.
