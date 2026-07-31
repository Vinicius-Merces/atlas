---
name: architecture-portfolio-assessment
description: "Assess multiple systems as a portfolio rather than isolated architectures."
---

# Architecture Portfolio Assessment Skill

## Purpose

Assess multiple systems as a portfolio rather than isolated architectures.

## Procedure

1. Inventory systems, owners, criticality, and lifecycle stage.
2. Map business capabilities to systems.
3. Identify duplicated capabilities and fragmented data.
4. Map strategic dependencies and constraints.
5. Identify obsolete, transitional, and target systems.
6. Evaluate reliability, security, cost, and change friction.
7. Recommend investment, consolidation, migration, or retirement.
8. Produce transition sequencing.

## Output

- Portfolio map
- Capability duplication
- Strategic dependencies
- Risk concentrations
- Target-state recommendations
- Transition roadmap

## Domain

The skill covers the project and engineering context described by its purpose: Assess multiple systems as a portfolio rather than isolated architectures.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Assess multiple systems as a portfolio rather than isolated architectures.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to architecture portfolio assessment.
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
