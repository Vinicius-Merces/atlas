---
name: adr-authoring
description: "Capture an important architecture decision with sufficient context and traceability."
---

# ADR Authoring Skill

## Purpose

Capture an important architecture decision with sufficient context and
traceability.

## Procedure

1. Define the decision problem.
2. Record constraints and forces.
3. Identify credible alternatives.
4. State the selected decision.
5. Record positive and negative consequences.
6. Define rollout and migration.
7. Link affected systems and contracts.
8. Define review or supersession triggers.

## Output

- Complete ADR
- Related systems
- Related risks
- Migration notes
- Follow-up actions

## Domain

The skill covers the project and engineering context described by its purpose: Capture an important architecture decision with sufficient context and traceability.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Capture an important architecture decision with sufficient context and traceability.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to adr authoring.
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
