# Monorepo Change Workflow

## Trigger

A change affects multiple packages, shared configuration, or repository-wide
tooling.

## Sequence

1. Map affected packages.
2. Inspect dependency direction.
3. Identify shared contracts.
4. Define migration sequencing.
5. Implement smallest coherent cross-package change.
6. Run affected and global validation.
7. Review CI and build graph impact.
8. Update package and repository documentation.
9. Record breaking or versioned changes.

## Blocking conditions

- Unknown affected packages
- New dependency cycle
- Unapproved package-boundary violation
- Missing migration for shared contract change
