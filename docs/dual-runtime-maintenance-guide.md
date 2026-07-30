# Dual-Runtime Maintenance Guide

## One knowledge base

Claude Code and Codex share memory, contracts, architecture, ADRs, and project
documentation.

## One canonical registry

The registry defines the complete capability inventory.

## Runtime-specific layers

Claude Code uses `.claude/` directly. Codex uses `AGENTS.md` and
`adapters/codex/`.

## Release checks

Every dual-runtime release should validate:

- Registry
- Package
- Contracts
- Smoke tests
- Codex adapter
- Generated catalog synchronization
- Runtime drift
- Codex tests
