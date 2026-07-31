---
name: memory-update-proposal
description: "Produce a reviewable proposal instead of silently rewriting durable memory."
---

# Memory Update Proposal

## Purpose

Produce a reviewable proposal instead of silently rewriting durable memory.

## Output

- Evidence
- Drift or contradiction
- Severity
- Proposed update
- Required approval
- Validation

## Domain

The skill covers the project and engineering context described by its purpose: Produce a reviewable proposal instead of silently rewriting durable memory.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Produce a reviewable proposal instead of silently rewriting durable memory.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to memory update proposal.
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
