# Claude Code and Codex Capability Matrix

| Capability | Claude Code | Codex | Parity |
|---|---|---|---|
| Canonical agents | Native `.claude/agents/` | Generated maps plus Codex entry points | Semantic |
| Contracts | Native | Shared canonical files | Full |
| Memory | Native project memory | Shared canonical files | Full |
| Skills | Native skill files | Mapped skill files | Semantic |
| Workflows | Native workflow files | Mapped procedures | Semantic |
| Reviews | Native review gates | Mapped review passes | Semantic |
| Commands | Native command files | Codex task entry points | Semantic |
| Registry | Canonical registry | Generated catalogs and JSON maps | Compatible |
| Package validation | Supported | Supported | Full |
| Contract tests | Supported | Shared | Full |
| Runtime-specific tests | Claude smoke tests | Codex compatibility tests | Full |
| Tool invocation | Claude-specific | Codex-specific | Different by design |

## Current status

Parity is considered **beta-supported with documented runtime-specific
differences**.
