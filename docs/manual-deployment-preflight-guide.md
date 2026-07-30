# Manual Deployment Preflight Guide

The package may be applied without scripts, but preflight can verify:

- Correct base version
- Patch file presence
- SHA-256 hashes
- Visible `CLAUDE-DIRECTORY` mapping
- Target version
- Deletion list

For manual copying, move the contents of `CLAUDE-DIRECTORY/` into `.claude/`.
