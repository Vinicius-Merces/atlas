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
