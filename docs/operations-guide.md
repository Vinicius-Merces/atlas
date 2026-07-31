# Operations Guide

This is the canonical operating guide for day-to-day ATLAS work. Use the
[Daily Quickstart](daily-quickstart.md) for a copyable first run and the
[Release Guide](release-guide.md) for framework publication.

## Operating model

ATLAS combines repository guidance with small automation tools:

```text
request
  -> bootstrap and repository evidence
  -> task routing and bounded context
  -> plan and selected workflow
  -> implementation
  -> validation and independent review
  -> execution evidence
  -> memory and continuity closeout
```

The repository is the source of truth. Chat history may help a current session,
but it must not become the only place that stores a durable decision,
constraint, result, or next action.

## Automation boundary

| Concern | ATLAS automates | Runtime or human judgment still required |
|---|---|---|
| Discovery | Registry, generated catalogs, canonical paths | Select only the context relevant to the request |
| Routing | Initial task envelope for known task types | Correct fallback routing, risk, scope, and ownership |
| Context | A bounded heuristic context pack and manifest | Add affected code, ADRs, constraints, and missing facts |
| Planning | A runtime-specific execution-plan skeleton | Turn steps into a repository-specific implementation plan |
| Execution | Native skill prompts plus workflow, role, and review definitions | Perform changes and coordinate the selected specialists |
| Assurance | Validators, tests, policies, schemas, and package checks | Interpret failures and perform semantic review |
| Evidence | Evidence, checkpoint, handoff, and session templates | Populate them with results that actually occurred |
| Continuity | Project brief, session brief, and resume-packet builders | Confirm current state and the next safe action |

Generating an artifact does not prove that its work occurred. Empty arrays in a
generated checkpoint, evidence record, or session brief are placeholders that
must be completed or explicitly reported as unknown.

## Daily lifecycle

### 1. Bootstrap

1. Read `VERSION` and the runtime bootstrap instructions.
2. Read `.atlas/continuity/resume-packet.json` when present.
3. Read the referenced project/session briefs, relevant memory, and accepted
   ADRs.
4. Inspect Git status and active task artifacts.
5. Reconcile repository evidence before trusting a previous-session summary.

Claude Code loads the root `CLAUDE.md`, which imports `AGENTS.md`. Codex follows
`AGENTS.md` and the mapped entry points under `adapters/codex/`.

### 2. Bound and route the task

Capture the requested outcome, acceptance criteria, constraints, affected
areas, risk, and rollback expectations. Use the smallest sufficient set of
roles and review gates. `scripts/atlas_route.py` can create an initial task
envelope, but its routing policy is a starting point and must be reviewed.

### 3. Assemble context and plan

Load relevant memory, contracts, ADRs, code, tests, and prior evidence. A
generated context pack is heuristic; add task-specific sources before
execution. Select the closest canonical workflow and produce a plan with
validation and completion criteria.

### 4. Execute

Implement the smallest coherent change. Agent files define bounded
responsibilities and native skills provide reusable prompts. Markdown workflows
and review gates remain procedures that the AI runtime must interpret. None of
these files prove that work occurred merely by existing on disk.

### 5. Validate and review

Run project-specific checks proportional to risk. For ATLAS framework changes,
run `python scripts/validate_all.py --profile full`; use `--profile quick` only
as a faster foundational check while iterating. The full profile includes
runtime parity, native skill synchronization, policies, documentation, and the
complete automated test suite. Apply independent review gates when
architecture, security, privacy, UX, data, compatibility, or release behavior
is affected.

Never convert a failed mandatory check into success by omitting it. Record
unavailable checks and their impact.

### 6. Record evidence and durable knowledge

Report request, scope, context, roles, changed files, checks, reviews, findings,
assumptions, remaining risks, and documentation or memory updates. Use
`adapters/codex/instructions/execution-evidence.md` as the shared evidence
shape.

Update `.claude/memory/` only for validated, reusable knowledge. Keep temporary
debugging observations and one-off task state out of durable memory. Use an ADR
for material architecture decisions.

### 7. Close or hand off

At a meaningful stopping point:

1. Record completed and pending work.
2. Record changed files, validation, decisions, assumptions, and risks.
3. Create a checkpoint or runtime handoff when work remains.
4. Update the latest session brief.
5. Rebuild the resume packet.
6. Confirm the next action is safe and specific.

Continuity builders write repository artifacts. Run them intentionally and
review their diffs before committing.

## Safe adoption into an existing project

Direct cumulative copying is only for an empty or dedicated repository. Before
integrating ATLAS into an existing product repository, run:

```bash
python scripts/plan_project_adoption.py --target-root <existing-project> --output adoption-plan.json --markdown-output adoption-plan.md
```

The planner is read-only for the target and returns exit code `2` when
collisions need attention. Never bulk-overwrite an existing repository. Merge
project-owned `README.md`, `LICENSE`, `AGENTS.md`, `CLAUDE.md`, `VERSION`,
`.gitignore`, `.github/`, and `.claude/memory/`; review every other occupied
path before copying. See [Installation](installation.md) for the full process.

## Runtime-specific entry points

### Claude Code

- Bootstrap: `CLAUDE.md` and `.claude/rules/`
- User commands: `.claude/commands/`
- Native specialist definitions: `.claude/agents/`
- Native reusable skills: `.claude/skills/*/SKILL.md`
- Canonical procedural references: `.claude/workflows/`, `.claude/reviews/`,
  and `.claude/contracts/`

### Codex

- Bootstrap: `AGENTS.md` and `adapters/codex/instructions/session-bootstrap.md`
- Plan, implement, review, release: `adapters/codex/commands/`
- Native skill wrappers: `.agents/skills/*/SKILL.md`
- Full inventory: generated catalogs and maps under `adapters/codex/`
- Canonical knowledge and contracts remain under `.claude/` and shared roots

Gemini and Cursor adapters are experimental and may require manual translation.

## Stop conditions

Stop, preserve evidence, and report the blocker when:

- the requested outcome conflicts with a canonical contract or source;
- repository state cannot be reconciled;
- a destructive action lacks clear authorization;
- required context is unavailable;
- mandatory validation fails;
- a high-risk change lacks rollback;
- runtime limitations prevent equivalent execution.

## Release and incidents

For releases, follow the [Release Guide](release-guide.md), package validation,
installation simulation, compatibility review, rollback, and audit evidence.

During incidents, prioritize people, data, and stabilization; preserve
timestamps and evidence; avoid speculative destructive changes. After recovery,
validate the system, produce a blameless report, track corrective actions, and
update tests, runbooks, memory, and architecture records when facts changed.
