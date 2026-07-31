---
name: semantic-compatibility-verification
description: "Verify that a change preserves the meaning of a stable ATLAS contract."
---

# Semantic Compatibility Verification Skill

## Purpose

Verify that a change preserves the meaning of a stable ATLAS contract.

## Procedure

1. Compare source and target definitions.
2. Identify changed responsibilities or required behavior.
3. Identify consumers and adapters.
4. Run structural and contract tests.
5. Inspect migration requirements.
6. Classify compatible, transitional, or breaking change.
7. Produce evidence and recommendation.

## Output

- Compatibility classification
- Semantic changes
- Affected assets
- Required migration
- Release recommendation

## Domain

The skill covers the project and engineering context described by its purpose: Verify that a change preserves the meaning of a stable ATLAS contract.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Verify that a change preserves the meaning of a stable ATLAS contract.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to semantic compatibility verification.
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
