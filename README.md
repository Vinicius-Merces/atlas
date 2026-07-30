# ATLAS AI Engineering Framework

**Version:** `0.1.0-alpha.5`  
**Status:** Foundation / Memory and Skills Runtime

ATLAS is an AI engineering framework for coordinating software development
through specialized agents, persistent memory, reusable skills, explicit
workflows, review gates, and architecture governance.

## Core flow

```text
User request
    ↓
Context engine
    ↓
Memory resolution
    ↓
Orchestrator
    ↓
Specialist agents + skills
    ↓
Reviews and quality gates
    ↓
Documentation
    ↓
Delivery
```

## What alpha.5 adds

- Memory Engine specification
- Memory taxonomy and lifecycle
- Memory staleness and conflict policies
- Project memory templates
- First reusable skill library
- Refactoring workflow
- Release workflow
- Security review gate
- UX review gate
- Reusable commands
- Expanded runtime registry

## Runtime layers

- **Knowledge:** memory, ADRs, project documentation
- **Capability:** skills and tools
- **Execution:** agents, workflows, commands
- **Governance:** rules, contracts, reviews, quality gates
