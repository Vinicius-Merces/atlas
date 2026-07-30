# System Modernization Workflow

## Trigger

A legacy system requires architectural, platform, dependency, or operational
modernization.

## Sequence

1. Establish current-state architecture.
2. Identify business-critical behavior.
3. Map dependencies and integrations.
4. Identify operational and security risks.
5. Define target architecture.
6. Compare incremental migration options.
7. Protect behavior with tests and observability.
8. Migrate in reversible stages.
9. Validate production outcomes.
10. Retire obsolete paths and update knowledge.

## Rules

- Do not rewrite without a migration strategy.
- Preserve business behavior intentionally.
- Prefer strangler and expand-contract patterns where suitable.
- Define measurable modernization outcomes.
