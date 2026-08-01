---
name: architecture-assessment
description: "Evaluate whether a proposed change fits existing architecture and preserves clear boundaries."
---

# Architecture Assessment Skill

## Purpose

Evaluate whether a proposed change fits existing architecture and preserves
clear boundaries.

## Trigger conditions

Use when a task changes shared components, data ownership, service boundaries,
public interfaces, or cross-domain dependencies.

## Inputs

- Proposed change
- Architecture memory
- Relevant ADRs
- Existing component structure

## Procedure

1. Identify affected boundaries.
2. Determine current ownership.
3. Map new dependencies.
4. Check contract compatibility.
5. Evaluate reversibility.
6. Identify migration needs.
7. Recommend approval, revision, or ADR creation.

## Output

- Current architecture
- Proposed impact
- Risks
- Alternatives
- Recommendation
- ADR requirement

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
