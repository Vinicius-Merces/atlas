---
name: reference-implementation-review
description: "Assess whether a reference project demonstrates ATLAS correctly."
---

# Reference Implementation Review Skill

## Purpose

Assess whether a reference project demonstrates ATLAS correctly.

## Checks

- Architecture is explicit
- Memory is present
- Agents and workflows match scope
- Reviews are proportionate
- Validation is reproducible
- Operational behavior is documented
- Limitations are explicit
- Upgrade guidance exists

## Output

- Findings
- Missing artifacts
- Risk
- Instructional gaps
- Approval outcome

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to reference implementation review.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
