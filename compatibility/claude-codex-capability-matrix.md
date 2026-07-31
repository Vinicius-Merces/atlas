# Claude Code and Codex Capability Matrix

| Capability | Claude Code | Codex | Parity |
|---|---|---|---|
| Bootstrap | Root `CLAUDE.md` imports shared `AGENTS.md` | Reads shared `AGENTS.md` plus adapter instructions | Semantic |
| Canonical agents | Native `.claude/agents/*.md` definitions | Generated maps plus Codex entry points | Semantic |
| Contracts | Shared canonical files, loaded as required | Shared canonical files, loaded as required | Full |
| Memory | Shared `.claude/memory/`, loaded through bootstrap and task context | Shared `.claude/memory/`, loaded through bootstrap and task context | Full |
| Skills | Native `.claude/skills/*/SKILL.md` prompts | Generated native `.agents/skills/*/SKILL.md` wrappers | Runtime-native, semantic |
| Workflows | Canonical Markdown procedures selected by commands or prompts | Canonical procedures exposed through mapped entry points | Semantic, runtime-interpreted |
| Reviews | Canonical gates performed through the selected workflow | Canonical gates performed through the selected workflow | Semantic |
| Commands | Native `.claude/commands/*.md` prompts | Four task entry points plus generated command catalog | Semantic |
| Registry | Canonical registry | Generated catalogs and JSON maps | Compatible |
| Python automation | Shared artifact builders and validators | Same shared artifact builders and validators | Full |
| Package validation | Supported | Supported | Full |
| Contract tests | Supported | Shared | Full |
| Runtime-specific tests | Static smoke and contract tests | Static adapter and parity tests | Structural and semantic |
| Tool invocation | Claude-specific | Codex-specific | Different by design |

## Current status

Parity is considered **supported with documented runtime-specific
differences** for ATLAS `0.1.0`.

Native skills provide reusable prompts; they do not perform engineering work
autonomously. Markdown workflows and review files must be interpreted and their
application reported by the runtime. The repository test suite validates
structure, native skill synchronization, and semantic mappings; it does not
launch an end-to-end Claude Code or Codex process.
