# Context Engine

The context engine determines which information should guide execution.

## Priority order

1. Current user request
2. Explicit project requirements
3. Project memory
4. Accepted ADRs
5. Global rules
6. Agent instructions
7. Skills and external references
8. Defaults

## Context categories

### Stable context

Architecture, brand rules, data contracts, security policies, and domain
constraints.

### Task context

Files, requirements, errors, acceptance criteria, and affected components.

### Ephemeral context

Temporary experiments, debugging observations, and unconfirmed hypotheses.

Ephemeral context must not be promoted to persistent memory without validation.

## Conflict handling

When two sources conflict:

- Prefer the higher-priority source.
- Preserve user intent.
- Surface material uncertainty.
- Avoid silently choosing a destructive interpretation.
