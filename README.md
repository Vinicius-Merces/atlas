# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.5`  
**Status:** Beta / Executable Routing and Context Runtime

ATLAS coordinates software engineering through shared memory, specialized
agents, reusable skills, workflows, review gates, validation, and portable
runtime contracts.

## Beta.5 milestone

The provider-neutral runtime introduced in beta.4 is now executable.

### New runtime utilities

- Deterministic task routing
- Machine-readable task envelopes
- Context pack generation
- Envelope and result validation
- Runtime execution planning
- Incremental package manifests
- Patch preflight verification

## Supported runtimes

| Runtime | Support |
|---|---|
| Claude Code | Beta-supported canonical runtime |
| Codex | Beta-supported synchronized runtime |
| Gemini | Experimental |
| Cursor | Experimental |

## Core commands

```bash
python scripts/atlas_route.py --task-type feature --summary "Add account export"
python scripts/build_context_pack.py --task-envelope .atlas/tasks/task.json
python scripts/validate_task_envelope.py .atlas/tasks/task.json
python scripts/validate_execution_result.py .atlas/results/task.json
```

## Runtime flow

```text
Request
  ↓
Task router
  ↓
Task envelope
  ↓
Context pack
  ↓
Claude Code or Codex
  ↓
Execution result
  ↓
Validation and review evidence
```

Claude Code remains the canonical implementation. Codex consumes the same
contracts, memory, routing policy, context format, and evidence model.
