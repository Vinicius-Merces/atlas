---
name: api-contract-analysis
description: "Assess API compatibility and identify migration risks."
---

# API Contract Analysis Skill

## Purpose

Assess API compatibility and identify migration risks.

## Inputs

- Existing API contract
- Proposed contract
- Known consumers
- Data validation rules

## Procedure

1. Compare paths and methods.
2. Compare request schemas.
3. Compare response schemas.
4. Check authentication and authorization.
5. Identify breaking changes.
6. Evaluate versioning or migration needs.
7. Define validation and rollback.

## Output

- Compatible changes
- Breaking changes
- Consumer impact
- Migration strategy
- Validation checklist

## Domain

The skill covers the project and engineering context described by its purpose: Assess API compatibility and identify migration risks.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Assess API compatibility and identify migration risks.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
