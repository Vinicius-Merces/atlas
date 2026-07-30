# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.2`  
**Status:** Beta / Claude Code + Codex Runtime Parity

ATLAS is an AI engineering framework for coordinating software development
through specialized agents, persistent memory, reusable skills, explicit
workflows, review gates, operational controls, architecture governance, and
multi-runtime distribution.

## Beta.2 milestone

This release promotes Codex from a foundation adapter to an actively validated
beta runtime alongside Claude Code.

## Runtime support

| Runtime | Support |
|---|---|
| Claude Code | Beta-supported canonical runtime |
| Codex | Beta-supported compatibility runtime |
| Gemini | Experimental adapter |
| Cursor | Experimental adapter |

## Runtime architecture

```text
Canonical ATLAS definitions
├── agents
├── contracts
├── skills
├── workflows
├── reviews
├── commands
├── memory
└── governance
        ↓
   ┌───────────────┬───────────────┐
   │               │               │
Claude Code      Codex          Experimental
runtime          runtime        adapters
```

## What beta.2 adds

- Codex Runtime Engineer agent
- Runtime Parity Reviewer agent
- Runtime Capability Mapper agent
- Codex runtime generation skill
- Runtime semantic parity skill
- Dual-runtime validation skill
- Codex synchronization workflow
- Runtime parity workflow
- Dual-runtime release workflow
- Codex runtime review gate
- Runtime parity review gate
- Codex-specific commands
- Functional Codex adapter structure
- Agent, skill, workflow, review, and command mappings
- Codex runtime manifest
- Claude-to-Codex capability matrix
- Codex validation scripts
- Codex compatibility tests
- Dual-runtime migration and usage guides

## Quick validation

```bash
python scripts/validate_registry.py
python scripts/validate_package.py
python scripts/validate_contracts.py
python scripts/validate_codex_adapter.py
python scripts/run_smoke_tests.py
python scripts/run_contract_tests.py
python scripts/run_codex_tests.py
```

## Stability commitment

During the `0.1.0-beta.x` line:

- Core contract semantics remain stable.
- Claude Code and Codex compatibility are validated independently.
- Breaking changes require migration guidance.
- Experimental adapters may evolve more rapidly.
