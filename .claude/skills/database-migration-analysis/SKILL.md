---
name: database-migration-analysis
description: "Assess schema and data migrations for integrity, compatibility, and operational risk."
---

# Database Migration Analysis Skill

## Purpose

Assess schema and data migrations for integrity, compatibility, and operational
risk.

## Inputs

- Current schema
- Proposed schema
- Application consumers
- Data volume
- Availability requirements

## Procedure

1. Classify additive, transitional, or destructive change.
2. Identify read and write compatibility.
3. Evaluate locks and execution time.
4. Define dual-read or dual-write needs.
5. Plan backfill and validation.
6. Define rollback or forward-fix strategy.
7. Identify monitoring and stop conditions.

## Output

- Migration class
- Compatibility risks
- Execution plan
- Data validation
- Rollback or forward-fix
- Release constraints

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
