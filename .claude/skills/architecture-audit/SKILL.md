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

## Domain

The skill covers the project and engineering context described by its purpose: Audit architecture for clarity, ownership, coupling, resilience, and alignment.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Audit architecture for clarity, ownership, coupling, resilience, and alignment.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to architecture audit.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
