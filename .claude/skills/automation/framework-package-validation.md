# Framework Package Validation Skill

## Purpose

Verify that an ATLAS distribution is structurally complete and internally
consistent.

## Procedure

1. Read `VERSION`.
2. Compare version references in README, registry, and runtime metadata.
3. Validate required directories.
4. Validate registry JSON.
5. Validate agent metadata.
6. Confirm referenced files exist.
7. Confirm changelog contains the current version.
8. Detect empty placeholders and broken links where possible.
9. Verify archive readability.
10. Produce validation report.

## Output

- Package version
- File count
- Passed checks
- Failed checks
- Warnings
- Release recommendation
