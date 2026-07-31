# Runtime Execution Guide

## Executable golden path

Generate one complete set of lifecycle artifacts in a disposable directory:

```bash
python scripts/build_golden_path.py --output-dir .atlas/examples/golden-path --runtime codex
```

Use `--runtime claude-code` to target Claude Code. The command creates and
validates a task envelope, bounded context pack, execution plan, checkpoint,
cross-runtime handoff, continuation plan, execution result, evidence record,
and hash manifest. It refuses to overwrite those known outputs unless
`--force` is supplied; `--force` does not authorize replacement of unrelated
files in the directory.

This is artifact generation, not autonomous product implementation. The
generated plan declares `requires_external_execution: true`; an AI agent or
human must still execute the selected workflow, run its validations and
reviews, and record the real outcome. The generated `completed` result refers
only to successful golden-path artifact generation and must not be presented
as evidence that the example feature was implemented.

## Record actual execution

After the selected workflow has really been performed, create a portable
result from the routed task:

```bash
python scripts/record_execution_result.py \
  --task-envelope .atlas/tasks/task-envelope.json \
  --runtime codex \
  --status completed \
  --summary "Describe the observed result" \
  --changed-file "path/actually-changed" \
  --validation "command: observed outcome" \
  --review "review gate: observed outcome" \
  --output .atlas/tasks/execution-result.json

python scripts/validate_execution_result.py .atlas/tasks/execution-result.json
```

List options may be repeated for changed files, validation, reviews, findings,
assumptions, remaining risks, and knowledge updates. The recorder removes
duplicate entries while preserving order. Choose `completed`, `partial`,
`blocked`, or `failed` according to observed execution; it writes evidence but
does not run code, tests, or review gates itself.

## Normal lifecycle

1. Route the task with `scripts/atlas_route.py`.
2. Validate the task envelope.
3. Build and review the context pack.
4. Build an execution plan for Claude Code or Codex.
5. Execute the selected workflow.
6. Record and validate the execution result with
   `scripts/record_execution_result.py`.
7. Preserve evidence and update stable knowledge only when verified facts
   changed.
