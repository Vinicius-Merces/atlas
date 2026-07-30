# Governance

Governance defines how work is classified, delegated, reviewed, and accepted.

## Authority order

1. User intent
2. Project-specific rules and constraints
3. Approved architecture decisions
4. Framework-wide rules
5. Agent recommendations
6. Tool defaults

## Execution chain

```text
Request
  ↓
Context resolution
  ↓
Orchestrator classification
  ↓
Plan and ownership assignment
  ↓
Specialist execution
  ↓
Independent validation
  ↓
Delivery decision
```

## Escalation conditions

An agent must escalate when:

- The request conflicts with an existing contract.
- The change affects unrelated domains.
- A destructive migration is required.
- Security or privacy risk is uncertain.
- The expected behavior cannot be determined from available context.
- A proposed solution would silently break compatibility.

## Review independence

The same agent may not be the sole authority for both implementing and
approving a high-impact change.

## Change classes

### Low impact

Localized, reversible, no contract or data impact.

### Medium impact

Touches shared components, public interfaces, workflows, or performance.

### High impact

Touches data models, authentication, billing, privacy, production
infrastructure, cross-service contracts, or irreversible migrations.

Higher impact requires stronger planning, review, and evidence.
