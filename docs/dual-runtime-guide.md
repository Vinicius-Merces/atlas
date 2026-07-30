# Claude Code and Codex Guide

## Shared foundation

Both runtimes should read the same project memory, ADRs, architecture, contracts,
and documentation.

## Claude Code

Uses the canonical `.claude/` implementation directly.

## Codex

Uses `adapters/codex/` for runtime-specific role, command, workflow, and review
instructions.

## Avoid duplication

Do not create separate business memory or architecture decisions for each
runtime.

## Validate parity

Run Codex adapter validation and runtime parity review after changing canonical
agents, workflows, commands, reviews, or contracts.
