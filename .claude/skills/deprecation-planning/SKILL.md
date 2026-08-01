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

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to deprecation planning.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
