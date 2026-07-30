# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.7`  
**Status:** Beta / Parallel Workstreams and Conflict-Safe Execution

ATLAS coordinates software engineering through shared memory, specialized
agents, reusable skills, workflows, review gates, runtime contracts, portable
execution evidence, resumable tasks, and conflict-safe parallel execution.

## Beta.7 milestone

Claude Code and Codex can now work on parallel task branches while protecting
shared files, dependencies, and canonical knowledge.

### New capabilities

- Workstream decomposition
- File and resource leases
- Conflict prediction
- Parallel execution manifests
- Merge readiness checks
- Cross-runtime result reconciliation
- Shared-state protection
- Workstream completion reports

## Parallel execution flow

```text
Task envelope
  ↓
Workstream decomposition
  ↓
Resource claims and conflict analysis
  ↓
Claude Code and Codex execute independently
  ↓
Workstream checkpoints
  ↓
Merge readiness validation
  ↓
Result reconciliation
  ↓
Final reviews and execution result
```

## Commands

```bash
python scripts/create_workstreams.py --task-envelope task.json
python scripts/claim_resources.py --workstream workstream.json
python scripts/detect_workstream_conflicts.py --manifest parallel-manifest.json
python scripts/validate_merge_readiness.py --manifest parallel-manifest.json
```

Claude Code remains canonical. Codex remains synchronized and beta-supported.
Both runtimes use the same workstream, resource claim, checkpoint, and evidence
formats.
