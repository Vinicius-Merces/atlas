# Installation

## Project-local installation

Copy the `.claude/`, `framework/`, and relevant documentation folders into the
root of a project.

```text
project/
├── .claude/
├── framework/
└── ...
```

## Standalone framework repository

ATLAS may also be maintained as a dedicated repository and selectively copied
or synchronized into projects.

## Claude Code usage

Claude-specific configuration lives under `.claude/`.

The initial setup should include:

- `.claude/rules/global.md`
- `.claude/contracts/`
- `.claude/agents/orchestrator.md`
- project-specific memory

## Project customization

Add stable project context under `.claude/memory/`. Do not put secrets,
temporary debugging notes, or unverified assumptions in persistent memory.
