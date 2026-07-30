# Memory Conflict and Staleness Policy

## Conflict indicators

- Two documents define different values for the same rule.
- Memory contradicts an accepted ADR.
- Memory conflicts with current code or contract behavior.
- A source of truth has changed without a memory update.
- Ownership is unclear.

## Resolution order

1. Current explicit user requirement
2. Source-of-truth system or document
3. Accepted ADR
4. Newer validated memory
5. Older memory
6. Agent assumption

## Required behavior

Agents must not silently choose between materially conflicting memories.

They should:

- Identify the conflict
- Determine the source of truth
- Update or retire stale memory
- Document architecture-impacting resolution

## Staleness signals

- Missing review date
- Deprecated integration references
- Nonexistent paths
- Retired technology
- Version mismatch
- Conflicting implementation evidence
