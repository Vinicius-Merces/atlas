# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.6`  
**Status:** Beta / Cross-Runtime Handoff and Resumable Execution

ATLAS coordinates software engineering through shared memory, specialized
agents, reusable skills, workflows, review gates, validation, runtime
contracts, and portable execution evidence.

## Beta.6 milestone

Claude Code and Codex can now hand off work through one shared, validated task
state.

### New capabilities

- Cross-runtime task handoff
- Execution checkpoints
- Resumable task state
- Handoff manifests
- Checkpoint validation
- Runtime continuation planning
- Portable execution evidence
- Interrupted-task recovery

## Runtime flow

```text
Task envelope
  ↓
Context pack
  ↓
Runtime A
  ↓
Checkpoint + handoff manifest
  ↓
Runtime B
  ↓
Continuation plan
  ↓
Validated execution result
```

## Commands

```bash
python scripts/create_checkpoint.py --task-envelope task.json --runtime codex
python scripts/create_handoff.py --checkpoint checkpoint.json --to-runtime claude-code
python scripts/validate_handoff.py handoff.json
python scripts/build_continuation_plan.py --handoff handoff.json
```

Claude Code remains canonical. Codex remains synchronized and beta-supported.
Both runtimes share the same contracts, memory, routing, evidence, and handoff
formats.
