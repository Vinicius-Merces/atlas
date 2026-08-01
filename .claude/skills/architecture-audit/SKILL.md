---
name: architecture-audit
description: "Audit architecture for clarity, ownership, coupling, resilience, and alignment."
---

# Architecture Audit Skill

## Purpose

Audit architecture for clarity, ownership, coupling, resilience, and alignment.

## Checks

- System boundaries
- Data ownership
- Integration contracts
- Dependency direction
- Architecture decisions
- Failure domains
- Security boundaries
- Operational ownership
- Migration state
- Strategic alignment

## Output

- Evidence
- Findings
- Severity
- Risks
- Recommendations
- Missing documentation

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to architecture audit.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
