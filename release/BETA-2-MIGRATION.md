# Migration to 0.1.0-beta.2

## From beta.1

1. Back up project-specific memory, ADRs, and custom runtime files.
2. Copy the beta.2 cumulative package over the repository.
3. Allow matching canonical files to be replaced.
4. Review `adapters/codex/`.
5. Review `compatibility/claude-codex-capability-matrix.md`.
6. Run all validation scripts.
7. Use Claude Code or Codex against the same canonical project memory.
8. Record runtime-specific customizations separately.

## Codex adoption

Codex projects should use the adapter files as runtime-specific instructions
while preserving canonical ATLAS contracts and memory.
