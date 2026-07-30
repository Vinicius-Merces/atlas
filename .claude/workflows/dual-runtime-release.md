# Dual-Runtime Release Workflow

## Trigger

A beta release supports Claude Code and Codex.

## Sequence

1. Freeze canonical source.
2. Validate Claude Code runtime.
3. Synchronize Codex runtime.
4. Validate Codex adapter.
5. Run contract and parity tests.
6. Update support policy and matrix.
7. Publish known limitations.
8. Build cumulative package.
9. Approve or block dual-runtime support.
