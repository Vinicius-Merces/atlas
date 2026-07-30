# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.3`  
**Status:** Beta / Claude Code + Codex Synchronization Runtime

ATLAS is an AI engineering framework for coordinating software development
through specialized agents, persistent memory, reusable skills, explicit
workflows, review gates, operational controls, architecture governance, and
multi-runtime distribution.

## Beta.3 milestone

This release moves the Codex adapter from manual mapping toward a synchronized
runtime generated from the canonical ATLAS registry.

## Runtime support

| Runtime | Support |
|---|---|
| Claude Code | Beta-supported canonical runtime |
| Codex | Beta-supported synchronized runtime |
| Gemini | Experimental adapter |
| Cursor | Experimental adapter |

## What beta.3 adds

- Runtime Synchronization Engineer agent
- Runtime Catalog Maintainer agent
- Adapter Drift Auditor agent
- Registry-to-runtime generation skill
- Adapter drift detection skill
- Command catalog synthesis skill
- Runtime synchronization workflow
- Adapter drift audit workflow
- Runtime catalog publication workflow
- Runtime synchronization review gate
- Adapter drift review gate
- Full Codex catalogs generated from the registry
- Root `AGENTS.md` for Codex-compatible project guidance
- Generated Codex indexes for agents, commands, skills, workflows, and reviews
- Runtime synchronization scripts
- Drift detection scripts
- Full parity tests against canonical registry collections
- Codex task protocol
- Shared execution evidence format
- Dual-runtime maintenance guide

## Validation

```bash
python scripts/sync_codex_adapter.py --check
python scripts/validate_codex_adapter.py
python scripts/detect_runtime_drift.py
python scripts/run_codex_tests.py
```

## Runtime principle

Claude Code remains the canonical implementation source. Codex receives a
generated and validated compatibility layer that preserves the same semantics,
memory, contracts, and governance.
