# Analytics Model

Analytics should explain user and system behavior without creating unnecessary
data collection.

## Analytics hierarchy

### Business outcomes

Revenue, retention, cost, risk, adoption, and strategic impact.

### Product outcomes

Task completion, activation, engagement, conversion, and satisfaction.

### Behavioral signals

Events, funnels, cohorts, paths, and feature usage.

### Operational signals

Latency, errors, reliability, capacity, and system health.

## Event design principles

- Track meaningful actions, not every click.
- Use stable and readable names.
- Define event ownership.
- Document properties and allowed values.
- Avoid sensitive data unless justified and reviewed.
- Version breaking event changes.
- Validate implementation against the tracking plan.

## Analytics invariant

A metric without a definition, owner, and decision use is not a reliable metric.
