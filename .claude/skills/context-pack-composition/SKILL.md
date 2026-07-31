---
name: context-pack-composition
description: "Assemble relevant project context while preserving sources and excluding secrets."
---

# Context Pack Composition

## Purpose

Assemble relevant project context while preserving sources and excluding secrets.

## Output

- Findings
- Evidence
- Limitations
- Required actions
- Outcome

## Domain

The skill covers the project and engineering context described by its purpose: Assemble relevant project context while preserving sources and excluding secrets.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Assemble relevant project context while preserving sources and excluding secrets.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to context pack composition.
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
