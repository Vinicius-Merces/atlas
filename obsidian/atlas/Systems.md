---
type: index
status: active
---

# Systems

ATLAS runtime architecture is maintained in the canonical
[[../../.claude/memory/architecture|architecture memory]].

## Runtime systems

- Claude Code: canonical implementation in `.claude/`
- Codex: supported compatibility adapter in `adapters/codex/`
- Gemini and Cursor: experimental adapters

See [[Agents]], [[Skills]], and [[Workflows]] for capability indexes.

## Product memory boundary

Each product owns its memory and generated vault view. See
[[../../.claude/memory/project-isolation|product memory isolation]] and
[[../../docs/project-local-memory-guide|project-local memory lifecycle]].
