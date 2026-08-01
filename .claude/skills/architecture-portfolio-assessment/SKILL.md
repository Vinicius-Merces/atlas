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

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to architecture portfolio assessment.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
