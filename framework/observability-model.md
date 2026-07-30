# Observability Model

Observability provides evidence about internal system behavior from external
signals.

## Signal types

### Logs

Structured records of meaningful events and failures.

### Metrics

Aggregated measurements used to track health, capacity, latency, errors, and
business outcomes.

### Traces

End-to-end visibility across distributed requests and dependencies.

### Events

Domain and operational transitions that explain system state changes.

## Design principles

- Emit signals at important boundaries.
- Include correlation identifiers.
- Avoid sensitive data in telemetry.
- Prefer actionable signals over noisy volume.
- Define owners for alerts.
- Align telemetry with user impact.
- Validate dashboards and alerts before incidents occur.

## Minimum operational questions

A production system should make it possible to answer:

- Is the system healthy?
- Who is affected?
- What changed?
- Where is the failure?
- How severe is it?
- Can we mitigate or roll back?
