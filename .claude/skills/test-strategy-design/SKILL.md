---
name: test-strategy-design
description: "Create a proportionate testing strategy based on behavior, risk, and architecture."
---

# Test Strategy Design Skill

## Purpose

Create a proportionate testing strategy based on behavior, risk, and
architecture.

## Inputs

- Acceptance criteria
- Architecture
- Risk level
- Existing coverage
- Release constraints

## Procedure

1. Identify critical behaviors.
2. Map unit, integration, and end-to-end boundaries.
3. Add non-functional testing where relevant.
4. Define test data and environment needs.
5. Define automation priorities.
6. Identify manual validation.
7. Define release and production checks.

## Output

- Test matrix
- Automation scope
- Manual scope
- Environments
- Data needs
- Exit criteria

## Domain

The skill covers the project and engineering context described by its purpose: Create a proportionate testing strategy based on behavior, risk, and architecture.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Create a proportionate testing strategy based on behavior, risk, and architecture.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
