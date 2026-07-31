---
name: compatibility-matrix-analysis
description: "Evaluate compatibility across framework versions, runtimes, adapters, and project states."
---

# Compatibility Matrix Analysis Skill

## Purpose

Evaluate compatibility across framework versions, runtimes, adapters, and project states.

## Procedure

1. Define compatibility scope.
2. Inventory versions and environments.
3. Identify contracts and paths that changed.
4. Inspect adapter support.
5. Run smoke and structural tests.
6. Record limitations.
7. Classify support status.
8. Define upgrade or mitigation path.

## Output

- Compatibility matrix
- Evidence
- Limitations
- Breaking changes
- Upgrade guidance

## Domain

The skill covers the project and engineering context described by its purpose: Evaluate compatibility across framework versions, runtimes, adapters, and project states.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Evaluate compatibility across framework versions, runtimes, adapters, and project states.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to compatibility matrix analysis.
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
