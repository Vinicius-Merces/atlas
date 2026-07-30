# Review Model

ATLAS treats review as an independent quality function.

## Review types

### Architecture review

Validates boundaries, contracts, data ownership, dependencies, and
maintainability.

### Implementation review

Validates correctness, readability, duplication, error handling, and
compatibility.

### Security review

Validates trust boundaries, input handling, secrets, permissions, dependencies,
and abuse cases.

### UX review

Validates clarity, accessibility, feedback, responsiveness, and interaction
consistency.

### QA review

Validates acceptance criteria, regressions, edge cases, and release readiness.

## Review outcomes

- **Approved**
- **Approved with conditions**
- **Changes required**
- **Blocked**

## Independence rule

High-impact changes require review by an agent that did not author the primary
implementation.
