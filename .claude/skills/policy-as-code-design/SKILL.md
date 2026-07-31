---
name: policy-as-code-design
description: "Translate a stable governance rule into an executable and reviewable policy."
---

# Policy-as-Code Design Skill

## Purpose

Translate a stable governance rule into an executable and reviewable policy.

## Procedure

1. Define policy objective.
2. Identify scope and triggering conditions.
3. Define machine-readable inputs.
4. Define pass, warning, and failure states.
5. Create actionable messages.
6. Define exception process.
7. Add positive and negative test cases.
8. Assign owner and review date.

## Output

- Policy specification
- Enforcement point
- Severity
- Test cases
- Exception path
- Ownership

## Domain

The skill covers the project and engineering context described by its purpose: Translate a stable governance rule into an executable and reviewable policy.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Translate a stable governance rule into an executable and reviewable policy.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to policy as code design.
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
