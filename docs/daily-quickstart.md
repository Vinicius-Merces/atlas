# Daily Quickstart

This guide shows one complete ATLAS work cycle. Start at the repository root
with Python and the project's own development dependencies available.

## 1. Start the runtime

### Claude Code

The root `CLAUDE.md` imports `AGENTS.md`. Confirm the runtime has read the
resume packet and relevant memory, then invoke a command such as:

```text
/atlas-plan Add export support to the account dashboard
```

### Codex

Use a request such as:

```text
Read AGENTS.md and .atlas/continuity/resume-packet.json when present.
Validate repository state, then follow adapters/codex/commands/atlas-plan.md
for: Add export support to the account dashboard.
```

For ordinary work, this high-level path is preferred: give the runtime a clear
outcome and acceptance criteria, then let it follow the canonical ATLAS
lifecycle.

## 2. Optionally create the executable task artifacts

The scripts below make the lifecycle explicit and reviewable:

```bash
python scripts/atlas_route.py --task-type feature --runtime codex --summary "Add export support to the account dashboard" --output .atlas/tasks/export.task.json
python scripts/validate_task_envelope.py .atlas/tasks/export.task.json
python scripts/build_context_pack.py --task-envelope .atlas/tasks/export.task.json --output .atlas/tasks/export.context.md
python scripts/build_execution_plan.py --task-envelope .atlas/tasks/export.task.json --runtime codex --output .atlas/tasks/export.plan.json
```

For Claude Code, use `--runtime claude-code` in both runtime-aware commands.
Supported task types and their routes are declared in
`adapters/shared/task-routing-policy.json`; an unknown type uses the default
orchestrator route.

These commands create scaffolding. Review the route, add affected code and ADRs
to the context, and make the plan repository-specific. By default, the context
builder creates a manifest and records both context paths in the task envelope;
use `--no-update-envelope` only when a read-only envelope is required.

To explore the entire artifact lifecycle in a disposable directory instead,
run:

```bash
python scripts/build_golden_path.py --output-dir .atlas/examples/golden-path --runtime codex
```

This produces validated lifecycle artifacts and a hash manifest. It does not
implement the routed feature: an AI agent or human must still execute the plan
and replace the demonstration result with observed implementation evidence.

## 3. Execute the selected workflow

The task envelope names the primary role, workflow, reviews, and validation.
Ask the runtime to load those canonical files before editing. For a feature,
the normal path is:

```text
.claude/workflows/feature-delivery.md
relevant .claude/agents/
relevant .claude/skills/
required .claude/reviews/
applicable .claude/contracts/
```

Agents, skills, workflows, and reviews define responsibility and procedure.
They do not prove execution by existing on disk; the runtime performs the work
and must report what it actually used.

## 4. Validate and review

Run the target project's tests first. When changing ATLAS itself, install the
declared test dependencies and run the portable full profile:

```bash
python -m pip install --requirement requirements-test.txt
python scripts/validate_all.py --profile full
```

The runner prints its policy report without rewriting repository state by
default. Use `--profile quick` for a faster foundational check while iterating;
the full profile remains the completion gate.

Use the review gates named by the route and add architecture, security, privacy,
UX, data, or compatibility review when the impact requires them.

## 5. Record the result

Record the observed execution result and validate it:

```bash
python scripts/record_execution_result.py --task-envelope .atlas/tasks/export.task.json --runtime codex --status completed --summary "Describe the observed result" --changed-file "path/actually-changed" --validation "command: observed outcome" --review "review gate: observed outcome" --output .atlas/tasks/export.execution-result.json
python scripts/validate_execution_result.py .atlas/tasks/export.execution-result.json
```

Repeat `--changed-file`, `--validation`, `--review`, `--finding`,
`--assumption`, `--remaining-risk`, and `--knowledge-update` as needed. Use
`partial`, `blocked`, or `failed` instead of `completed` when that is what
occurred; the recorder stores supplied evidence but does not perform or verify
the implementation.

An evidence record can be initialized with:

```bash
python scripts/create_evidence_record.py --task-id <task-id> --runtime codex --status completed
```

The generator creates empty evidence fields. Populate sources, decisions,
changed files, validation, reviews, assumptions, and remaining risks with
observed results before treating the record as complete.

## 6. Pause, hand off, or close

For interrupted work, create a checkpoint:

```bash
python scripts/create_checkpoint.py --task-envelope .atlas/tasks/export.task.json --runtime codex --output .atlas/tasks/export.checkpoint.json
```

Complete its placeholder fields before using it for handoff. At session close:

```bash
python scripts/create_session_brief.py --summary "Implemented and validated account export" --runtime codex --next-action "Review and merge the completed change"
python scripts/build_resume_packet.py
```

Review the generated session brief and resume packet before committing. If
facts changed, update durable memory or an ADR separately; do not promote
temporary observations automatically.

## 7. Deliver

Return a concise evidence report containing:

- requested outcome and scope;
- context and roles used;
- changed files;
- tests and review gates;
- findings and assumptions;
- remaining risks;
- documentation, memory, and continuity updates.

Use [Operations Guide](operations-guide.md) for the operating model,
[Troubleshooting](troubleshooting.md) for common failures, and
[Release Guide](release-guide.md) when preparing distribution artifacts.
