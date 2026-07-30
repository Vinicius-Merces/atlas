# Threat Modeling Workflow

## Trigger

A new system, integration, trust boundary, sensitive-data flow, or high-impact
feature is proposed.

## Sequence

1. Define scope and architecture.
2. Identify assets and data.
3. Map trust boundaries and actors.
4. Enumerate threats and abuse cases.
5. Review existing controls.
6. Prioritize risks.
7. Define mitigations.
8. Record residual risk.
9. Link findings to architecture and delivery work.
10. Define review triggers.

## Blocking conditions

- Unknown sensitive-data flow
- Undefined authentication or authorization boundary
- Critical threat without mitigation or explicit acceptance
