# Knowledge Graph Model

ATLAS organizes project knowledge as linked, typed, traceable information.

## Core node types

- Project
- System
- Service
- Repository
- Agent
- Skill
- Workflow
- Contract
- Decision
- Integration
- Data domain
- Risk
- Owner

## Core relationship types

- owns
- depends on
- implements
- reviews
- supersedes
- integrates with
- stores
- governs
- produces
- consumes
- validates

## Knowledge rules

- Every important decision should link to affected systems.
- Every system should identify an owner.
- Every integration should identify its contract and failure behavior.
- Every memory note should identify a source of truth.
- Every superseded decision should link to its replacement.
- Unverified claims must remain visibly provisional.

## Obsidian compatibility

The graph can be represented through Markdown links and metadata, enabling the
same knowledge base to be browsed by humans and consumed by AI agents.
