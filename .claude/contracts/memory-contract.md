# Memory Contract

Memory stores stable project knowledge shared across agents.

## Required properties

Every memory document should identify:

- Purpose
- Scope
- Source of truth
- Owner
- Last reviewed date
- Related contracts or ADRs

## Suitable content

- Business rules
- Architecture
- Data ownership
- Brand guidance
- Integration contracts
- Security policies
- Stable product constraints

## Unsuitable content

- Secrets
- Temporary debugging findings
- Unverified assumptions
- One-off task instructions
- Sensitive production data
- Generated content without review

## Update rules

- Update memory when the source of truth changes.
- Record material architecture changes in an ADR.
- Remove stale guidance rather than accumulating contradictions.
- Prefer one canonical document per topic.
