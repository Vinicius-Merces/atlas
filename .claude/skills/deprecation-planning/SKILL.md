---
name: deprecation-planning
description: "Plan a safe deprecation and removal lifecycle."
---

# Deprecation Planning Skill

## Purpose

Plan a safe deprecation and removal lifecycle.

## Procedure

1. Identify asset and reason.
2. Identify consumers and dependencies.
3. Validate replacement.
4. Define migration steps.
5. Define announcement and removal versions.
6. Update examples and adapters.
7. Add compatibility tests.
8. Record owner and review date.

## Output

- Deprecation record
- Replacement
- Migration
- Timeline
- Impact
- Validation

## Domain

The skill covers the project and engineering context described by its purpose: Plan a safe deprecation and removal lifecycle.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Plan a safe deprecation and removal lifecycle.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to deprecation planning.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
