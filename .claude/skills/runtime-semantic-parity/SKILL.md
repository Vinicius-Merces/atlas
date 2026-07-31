---
name: runtime-semantic-parity
description: "Compare two runtime implementations for semantic equivalence."
---

# Runtime Semantic Parity Skill

## Purpose

Compare two runtime implementations for semantic equivalence.

## Checks

- Agent responsibility
- Workflow sequence
- Command intent
- Review coverage
- Contract enforcement
- Memory usage
- Escalation behavior
- Evidence output

## Output

- Parity findings
- Missing mappings
- Semantic differences
- Severity
- Recommendation

## Domain

The skill covers the project and engineering context described by its purpose: Compare two runtime implementations for semantic equivalence.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Compare two runtime implementations for semantic equivalence.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to runtime semantic parity.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
