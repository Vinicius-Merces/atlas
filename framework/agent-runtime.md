# Agent Runtime

The ATLAS agent runtime coordinates bounded specialists through explicit
contracts.

## Runtime responsibilities

- Discover available agents.
- Match tasks to agent capabilities.
- Preserve ownership boundaries.
- Pass only relevant context.
- Require declared outputs.
- Enforce quality gates.
- Escalate unresolved conflicts.

## Agent selection

Selection should consider:

1. Domain ownership
2. Scope of change
3. Risk level
4. Required tools
5. Review independence
6. Project-specific constraints

## Collaboration model

Agents collaborate through artifacts, not vague conversational handoffs.

Expected artifacts include:

- Architecture proposal
- Implementation plan
- Code changes
- Test evidence
- Security findings
- UX review
- Documentation updates

## Runtime invariant

No specialist may silently redefine another specialist's contract.
