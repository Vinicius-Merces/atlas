# Reliability Model

ATLAS treats reliability as a product capability rather than an operational
afterthought.

## Reliability dimensions

### Availability

The system remains usable during expected operating conditions.

### Resilience

The system degrades safely when dependencies, networks, or internal components
fail.

### Recoverability

The system can restore service and data after failure.

### Observability

Operators can understand system behavior through logs, metrics, traces, and
events.

### Operability

The system can be deployed, configured, monitored, and maintained without
unnecessary risk.

## Reliability requirements

Every production-facing system should define:

- Service objectives
- Critical user journeys
- Known failure modes
- Alerting expectations
- Recovery procedures
- Rollback mechanisms
- Data recovery boundaries
- Dependency assumptions

## Release implication

A feature that cannot be monitored, diagnosed, or safely rolled back may not be
production-ready even when its functional tests pass.
