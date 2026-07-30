# Framework Evolution Model

ATLAS evolves through explicit compatibility, migration, and deprecation rules.

## Change classes

### Patch-compatible

Clarifications, fixes, and backward-compatible improvements.

### Additive

New agents, skills, workflows, reviews, templates, or adapters.

### Transitional

New structure that requires a documented migration period.

### Breaking

Changes to contracts, canonical paths, semantics, or runtime behavior.

## Evolution rules

- Every release has one canonical version.
- Breaking changes require migration guidance.
- Deprecated assets remain documented during the transition period.
- Runtime adapters declare compatibility.
- Registry and package validation protect release consistency.
- Superseded architecture decisions remain traceable.
- Examples and blueprints are reviewed after contract changes.
