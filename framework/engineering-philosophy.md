# Engineering Philosophy

ATLAS promotes disciplined engineering rather than prompt-driven improvisation.

## Primary objective

Build systems that remain understandable and trustworthy after the initial
implementation.

## Operating values

### Clarity over cleverness

Code and documentation should communicate intent without requiring the reader
to reverse-engineer hidden assumptions.

### Evidence over intuition

Performance changes require measurements. Architecture changes require
constraints and trade-offs. Security claims require validation.

### Systems over isolated outputs

A component is evaluated by how it interacts with the rest of the product,
not only by whether it works in isolation.

### Reversibility

Prefer decisions that can be reviewed, tested, migrated, and rolled back.

### Responsible autonomy

Agents may act independently inside their declared scope, but must escalate
uncertainty, destructive changes, contract changes, or cross-domain impact.

## Definition of done

A deliverable is complete only when:

- Its requirements are satisfied.
- Existing behavior is preserved or intentionally migrated.
- Validation has been performed.
- Relevant quality gates pass.
- Operational risks are documented.
- Documentation is updated.
