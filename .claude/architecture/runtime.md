# Claude Runtime Architecture

Claude Code acts as an execution runtime for ATLAS.

## Resolution order

1. Current request
2. Project memory
3. Rules
4. Contracts
5. Orchestrator
6. Specialist agents
7. Skills and tools
8. Validation workflows

## Design goal

Claude-specific files should remain adapters rather than the canonical source
of framework philosophy. Canonical framework rules live under `framework/`.
