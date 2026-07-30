# Framework Architecture

ATLAS separates concerns into layers.

## Knowledge layer

- Memory
- Architecture records
- Project documentation
- Domain references

## Capability layer

- Skills
- Tools
- Reusable patterns
- Integration adapters

## Execution layer

- Agents
- Workflows
- Commands

## Governance layer

- Rules
- Contracts
- Quality gates
- Review policies

## Runtime adapters

Runtime-specific directories such as `.claude/` translate ATLAS concepts into
the conventions of an AI coding environment.

## Data flow

```text
User request
    ↓
Context engine
    ↓
Governance and contracts
    ↓
Orchestrator
    ↓
Agent + skills
    ↓
Project changes
    ↓
Review and quality gates
```
