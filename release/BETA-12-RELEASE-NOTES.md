# ATLAS 0.1.0-beta.12 Release Notes

ATLAS beta.12 completes the repository hardening planned before the first
release candidate. It makes release construction reproducible, turns policy
and compatibility declarations into executable gates, closes Claude/Codex
runtime parity gaps, and adds an end-to-end lifecycle test that exercises
routing through audit evidence.

## Highlights

- Deterministic cumulative, incremental, and recovery archives with internal
  content manifests, external manifests, and SHA-256 checksum files
- Exact manual patch operations, visible `CLAUDE-DIRECTORY/` mapping, explicit
  deletions, preflight validation, and beta.11 upgrade simulation
- One controlled version source with protected historical release records
- Generated Codex parity maps whose canonical and adapter paths are validated
- Canonical agent definitions consolidated under `.claude/agents/`
- Executable policies for runtime drift, source of truth, CI, schemas,
  packages, support, exceptions, deletion safety, cleanliness, and release
  stability
- Durable memory, continuation artifacts, knowledge-link validation, and
  tamper-detecting evidence bundles
- Expanded installation, runtime, deployment, release, support, rollback, and
  troubleshooting documentation

## Runtime support

- Claude Code: beta-supported canonical runtime
- Codex: beta-supported adapter with generated parity maps
- Gemini and Cursor: experimental adapters

## Release status

All local repository gates and packaging simulations pass. Promotion to an RC
still requires a successful GitHub-hosted CI run and independent release
review. Those external approvals are deliberately not inferred from local
validation.

