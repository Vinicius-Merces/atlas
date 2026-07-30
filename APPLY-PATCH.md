# Apply ATLAS Patch Manually

## Required base

`0.1.0-beta.10`

## Target

`0.1.0-beta.11`

## Important: `.claude` updates

This package does not hide `.claude` files.

Anything inside:

```text
CLAUDE-DIRECTORY/
```

must be copied into:

```text
.claude/
```

in the repository.

## Manual deployment

1. Extract this ZIP.
2. Copy all normal folders and files into the repository root.
3. Open `CLAUDE-DIRECTORY`.
4. Copy its contents into the repository `.claude` directory.
5. Replace existing files when prompted.
6. Delete only paths listed in `FILES-TO-DELETE.md`.
7. Confirm `VERSION` now shows `0.1.0-beta.11`.

Scripts are optional and are not required for the manual update.

## Summary

- Added: 40
- Replaced: 13
- Deleted: 0
