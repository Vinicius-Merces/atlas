---
name: integration-contract-mapping
description: "Document the complete behavioral and operational contract of an integration."
---

# Integration Contract Mapping Skill

## Purpose

Document the complete behavioral and operational contract of an integration.

## Inputs

- Provider documentation
- Consumer implementation
- Authentication method
- Example payloads

## Procedure

1. Identify ownership and environments.
2. Map requests, responses, events, or files.
3. Define authentication and permissions.
4. Define errors, timeouts, and retries.
5. Define rate limits and idempotency.
6. Define observability and escalation.
7. Define versioning and deprecation.
8. Define test and sandbox strategy.

## Output

- Contract map
- Ownership
- Data mapping
- Failure behavior
- Security requirements
- Test strategy
- Lifecycle rules

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
