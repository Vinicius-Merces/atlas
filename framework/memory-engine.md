# Memory Engine

The Memory Engine stores stable project knowledge and makes it available to
agents without embedding that knowledge inside execution prompts.

## Objectives

- Preserve validated project knowledge.
- Reduce repeated discovery.
- Prevent contradictory guidance.
- Keep agents focused on execution.
- Make context updates traceable.

## Memory resolution flow

```text
Task
  ↓
Identify affected domains
  ↓
Load relevant memory
  ↓
Check freshness and conflicts
  ↓
Merge with ADRs and rules
  ↓
Provide bounded context to agents
```

## Memory characteristics

A valid memory item should be:

- Stable enough to reuse
- Specific enough to guide decisions
- Traceable to a source of truth
- Owned by a person, role, or system
- Reviewable
- Free from secrets

## Canonicality

One canonical memory document should exist per topic. Related documents may
reference it, but must not redefine the same rules independently.
