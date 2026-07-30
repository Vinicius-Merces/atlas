# Stable Contract Model

A stable contract is a declared interface whose semantic meaning should remain
compatible throughout a supported release line.

## Stable contract types

### Agent contract

Defines identity, scope, inputs, outputs, collaboration, escalation, and quality
gates.

### Memory contract

Defines what persistent knowledge may contain and how it is maintained.

### Workflow contract

Defines lifecycle, decision points, failure behavior, and completion criteria.

### Skill contract

Defines reusable capability boundaries and validation.

### Review contract

Defines evidence, findings, severity, and outcomes.

### Command contract

Defines invocation, inputs, delegated execution, output, and failure behavior.

## Stability rules

- Wording may improve without changing responsibility.
- New optional fields may be added.
- Existing required fields may not disappear without migration guidance.
- Canonical semantics may not silently change.
- Breaking changes require a new compatibility declaration.
