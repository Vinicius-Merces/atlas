---
name: product-requirement-decomposition
description: "Convert a broad product request into explicit outcomes, constraints, scope, and acceptance criteria."
---

# Product Requirement Decomposition Skill

## Purpose

Convert a broad product request into explicit outcomes, constraints, scope, and
acceptance criteria.

## Inputs

- User request
- Product context
- Known constraints
- Relevant business memory

## Procedure

1. Identify the underlying problem.
2. Identify users and stakeholders.
3. Define desired outcomes.
4. Separate scope from non-goals.
5. List assumptions and unknowns.
6. Define success metrics.
7. Produce testable acceptance criteria.
8. Identify required specialist agents.

## Output

- Problem
- Users
- Outcomes
- Scope
- Non-goals
- Assumptions
- Metrics
- Acceptance criteria

## Domain

The skill covers the project and engineering context described by its purpose: Convert a broad product request into explicit outcomes, constraints, scope, and acceptance criteria.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Convert a broad product request into explicit outcomes, constraints, scope, and acceptance criteria.
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
