# ATLAS AI Engineering Framework

**Version:** `0.1.0-alpha.3`  
**Status:** Foundation / Structural Intelligence

ATLAS is an AI engineering framework for organizing software development with
specialized agents, persistent memory, reusable skills, explicit workflows,
quality gates, and architecture governance.

ATLAS is not a collection of isolated prompts. It is a structured operating
model for AI-assisted engineering.

## Core model

```text
User request
    ↓
Context resolution
    ↓
Orchestration
    ↓
Specialist execution
    ↓
Validation and review
    ↓
Documentation
    ↓
Delivery
```

## Foundation components

- **Framework:** principles, governance, architecture, lifecycle, and quality.
- **Agents:** specialists that execute bounded responsibilities.
- **Memory:** persistent project knowledge.
- **Contracts:** interfaces that prevent ambiguity between framework components.
- **Rules:** non-negotiable engineering constraints.
- **Workflows:** repeatable delivery sequences.
- **ADRs:** records of important architecture decisions.

## Current release

The `alpha.3` release introduces the first structural intelligence layer:

- Orchestrator agent
- Agent contract
- Memory contract
- Workflow contract
- Context engine
- Project lifecycle
- First Architecture Decision Record

## Installation

Copy the framework into the root of a project or maintain it as a dedicated
repository. Claude Code-specific configuration lives under `.claude/`.

## Guiding principle

> Knowledge should be reusable, execution should be bounded, and every
> important decision should be traceable.
