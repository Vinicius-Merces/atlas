# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.1`  
**Status:** First Public Beta / Contract Stabilization

ATLAS is an AI engineering framework for coordinating software development
through specialized agents, persistent memory, reusable skills, explicit
workflows, review gates, operational controls, architecture governance, and
multi-runtime distribution.

## Beta milestone

This release marks the first beta of ATLAS.

The framework now includes:

- Stable core contracts
- A canonical Claude Code runtime
- Experimental Codex, Gemini, and Cursor adapters
- Automated package validation
- Smoke and contract tests
- Compatibility and deprecation policies
- Adoption blueprints
- Project health and migration workflows
- Enterprise architecture and operational governance

## Stability commitment

During the `0.1.0-beta.x` line:

- Core contract semantics are treated as stable.
- Breaking changes require explicit migration guidance.
- Canonical paths should remain stable.
- Experimental adapters may continue to evolve.
- Deprecated assets must follow the deprecation lifecycle.
- Package validation and contract tests must pass before release.

## Core flow

```text
Project intent
    ↓
Blueprint or adoption path
    ↓
Context and memory resolution
    ↓
Orchestrator
    ↓
Specialist agents + skills
    ↓
Automated contract and package validation
    ↓
Independent review gates
    ↓
Release, operations and knowledge synchronization
```

## Supported runtime

| Runtime | Support |
|---|---|
| Claude Code | Beta-supported canonical runtime |
| Codex | Experimental adapter |
| Gemini | Experimental adapter |
| Cursor | Experimental adapter |

## Quick start

1. Copy the cumulative package into the repository.
2. Preserve project-specific memory and ADRs.
3. Run `python scripts/validate_registry.py`.
4. Run `python scripts/validate_package.py`.
5. Run `python scripts/run_smoke_tests.py`.
6. Review `docs/INDEX.md`.
7. Use `/atlas-bootstrap` or the relevant project blueprint.

## Guiding principle

> Stable contracts create freedom above them.
