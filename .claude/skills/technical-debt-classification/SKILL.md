---
name: technical-debt-classification
description: "Classify and prioritize a technical debt item."
---

# Technical Debt Classification Skill

## Purpose

Classify and prioritize a technical debt item.

## Procedure

1. Record evidence and affected systems.
2. Classify debt category.
3. Estimate impact and likelihood.
4. Identify cost of delay.
5. Identify current workaround.
6. Define remediation options.
7. Define verification.
8. Assign owner and review date.

## Output

- Debt category
- Severity
- Impact
- Cost of delay
- Remediation options
- Owner
- Verification criteria

## Domain

The skill covers the project and engineering context described by its purpose: Classify and prioritize a technical debt item.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Classify and prioritize a technical debt item.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to technical debt classification.
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
