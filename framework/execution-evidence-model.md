# Execution Evidence Model

Both Claude Code and Codex should report comparable evidence after performing
engineering work.

## Required evidence

- Request summary
- Scope
- Context consulted
- Agents or roles used
- Files changed
- Tests and checks run
- Review gates completed
- Findings
- Assumptions
- Remaining risks
- Documentation or memory updates

## Purpose

Shared evidence makes runtime behavior auditable even when invocation and tool
mechanics differ.
