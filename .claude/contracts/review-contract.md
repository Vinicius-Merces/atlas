# Review Contract

Every review must define:

- Review type
- Scope
- Evidence inspected
- Findings
- Severity
- Required actions
- Outcome

## Severity levels

- **Critical:** release-blocking safety, security, or data risk
- **High:** likely regression or major contract violation
- **Medium:** important maintainability, UX, or resilience issue
- **Low:** localized improvement
- **Note:** informational observation

## Review rules

- Findings must be actionable.
- Reviewers must distinguish fact from hypothesis.
- Missing evidence must be reported.
- A reviewer must not approve work that failed mandatory validation.
