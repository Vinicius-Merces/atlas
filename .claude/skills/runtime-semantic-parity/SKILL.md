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

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to runtime semantic parity.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
