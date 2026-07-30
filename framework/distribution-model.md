# Distribution Model

ATLAS separates canonical framework knowledge from runtime-specific adapters.

## Canonical source

The canonical framework includes:

- Framework principles
- Agents
- Skills
- Workflows
- Contracts
- Reviews
- Templates
- Schemas
- Documentation

## Runtime adapters

Adapters translate canonical definitions into the conventions of a target
environment such as Claude Code, Codex, Gemini CLI, or Cursor.

## Distribution artifact

A release artifact should include:

- Version
- Changelog
- Manifest
- Canonical framework
- Selected adapters
- Validation evidence
- Integrity metadata

## Distribution invariant

Runtime adapters may translate structure and syntax, but must not silently alter
the semantic responsibility of agents, contracts, or governance rules.
