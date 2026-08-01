---
name: core-contract-stabilization
description: "Evaluate whether a contract is stable enough for a beta support commitment."
---

# Core Contract Stabilization Skill

## Purpose

Evaluate whether a contract is stable enough for a beta support commitment.

## Procedure

1. Identify contract purpose.
2. Identify current consumers.
3. Review required fields and semantics.
4. Identify recent churn.
5. Evaluate compatibility needs.
6. Define stable and extensible parts.
7. Define breaking-change rules.
8. Add contract tests.
9. Record support commitment.

## Output

- Contract stability assessment
- Stable fields
- Extension points
- Breaking-change rules
- Test requirements

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to core contract stabilization.
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
