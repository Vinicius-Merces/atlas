---
name: technical-roadmap-synthesis
description: "Create a sequenced technical roadmap from architecture, risk, product, platform, and operational inputs."
---

# Technical Roadmap Synthesis Skill

## Purpose

Create a sequenced technical roadmap from architecture, risk, product, platform,
and operational inputs.

## Procedure

1. Define strategic outcomes.
2. Inventory current constraints and risks.
3. Group work into coherent capabilities.
4. Identify dependencies and prerequisites.
5. Separate mandatory, enabling, and optional work.
6. Sequence reversible milestones.
7. Define evidence and exit criteria.
8. Identify decisions and resource assumptions.

## Output

- Strategic outcomes
- Workstreams
- Milestones
- Dependencies
- Risks
- Decision points
- Exit criteria
- Deferred items

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to technical roadmap synthesis.
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
