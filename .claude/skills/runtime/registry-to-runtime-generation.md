# Registry-to-Runtime Generation Skill

## Purpose

Generate runtime catalogs and indexes from the canonical ATLAS registry.

## Procedure

1. Read the registry.
2. Validate collection types.
3. Generate one catalog entry per canonical asset.
4. Preserve canonical names.
5. Link to canonical files when resolvable.
6. Mark generated outputs.
7. Compare generated output with committed files.
8. Report differences.

## Output

- Runtime catalogs
- Generated indexes
- Missing canonical files
- Synchronization status
