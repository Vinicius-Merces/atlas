# Framework Upgrade Workflow

## Trigger

A project adopts a newer ATLAS version or runtime adapter version.

## Sequence

1. Back up current project state.
2. Record current ATLAS version and customizations.
3. Compare source and target versions.
4. Identify breaking and transitional changes.
5. Replace cumulative framework files.
6. Reapply intentional project customizations.
7. Validate registry, package, workflows, and adapters.
8. Run representative tasks.
9. Update migration record.
10. Remove obsolete files only when confirmed.

## Rules

- Cumulative replacement does not automatically delete obsolete files.
- Review deprecated files explicitly.
- Preserve project memory and project-specific decisions.
