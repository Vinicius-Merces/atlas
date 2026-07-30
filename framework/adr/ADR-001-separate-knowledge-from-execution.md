# ADR-001: Separate Knowledge from Execution

- **Status:** Accepted
- **Date:** 2026-07-30

## Context

Agent instructions often become bloated when they embed project facts,
technical references, workflows, and execution behavior in one file. This
creates duplication and makes knowledge difficult to update.

## Decision

ATLAS separates:

- Persistent facts into **Memory**
- Reusable expertise into **Skills**
- Execution behavior into **Agents**
- Repeatable sequences into **Workflows**
- Mandatory constraints into **Rules**
- Interfaces into **Contracts**

## Consequences

### Positive

- Knowledge can be reused by multiple agents.
- Agents remain focused and easier to review.
- Project facts can evolve without rewriting agent behavior.
- Runtime-specific implementations remain replaceable.

### Negative

- The framework has more files.
- Context resolution requires discipline.
- Poorly maintained memory can still create stale guidance.

## Enforcement

New agents must not embed extensive project-specific knowledge unless that
knowledge is inseparable from their responsibility.
