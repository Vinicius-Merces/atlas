# Delivery feedback and completion rules

Apply these rules alongside the selected workflow. They do not replace domain
contracts or imply that a past defect is still present in production.

## Before execution

Identify the repository, branch, current commit, requested outcome, relevant
memory, acceptance criteria, and the latest user decision. Treat visual approval,
implementation, automated validation, remote persistence, and deployment as
separate facts. An old instruction superseded by the user is not an active gate.

## During execution

For repetitive work, enumerate the actual IDs/files, completed items and remaining
items. Save a coherent batch with its evidence before starting the next batch.
Use a remote commit when authorized. If remote persistence fails, record the local
commit and blocker; never describe a local change as saved on GitHub.

Checkpoint after each meaningful validated batch and before an interruption or
handoff. Resume from confirmed repository state, rather than starting over from a
chat summary. Preserve unrelated work and do not mark a whole collection complete
because its structural validator passed.

## Completion evidence by project type

| Work | Required evidence |
| --- | --- |
| Question banks | Exact reviewed IDs and remaining count; semantic review of scenarios, distractors, answers and explanations; overlay consistency; dated primary references for technical claims. Length balance is a diagnostic, not proof of correctness. |
| Sprites and animation | Exact approved source file; transparency, frame count, spacing, orientation and crop inspection; rendered animation in the game; timing and state transitions. Concept approval alone does not prove integration. |
| Assessments and quizzes | Refresh/recovery behavior; submission duplication; immutable correction snapshot when content changes; local timezone display; exported accents; mobile admin actions. Run applicable checks for the changed flow. |
| Cost estimators | Per-channel and total error against identified reference samples; units, quality and media; independent holdout sample before claiming general accuracy. Two calibration samples cannot establish a universal 2–5% error bound. |
| Desktop automation | Actual input mapping, capture, pause and close behavior on the target OS. Compilation or a web panel is insufficient to establish executable behavior. |

## Closeout

Apply `docs/execution-assurance-guide.md` to new completion claims. The recorder
defaults to partial and checks functional evidence, exact task criteria and a
remote checkpoint before completed. Preserve historical evidence; structural
schema validity alone is not admission.

Report what changed, what was actually tested, the remote commit/PR, deployment
status if applicable, and remaining work. Mark unavailable checks explicitly.
Keep credentials and personal participant data out of public evidence.

Populate latest-session before rebuilding the resume packet. Run
`python scripts/validate_continuity_state.py`. Never update historical evidence
versions to make a current gate pass. Store reusable lessons in canonical memory
and link them from Obsidian; task-specific state belongs in session evidence.

## Measuring effectiveness

Record per task: accepted outcome, applicable checks executed/unavailable,
reopened defects, user-requested restarts, completed/total work, and remotely
saved checkpoint. Calculate rates only when a defined denominator and observation
window exist. Counts of agents, skills or passing framework tests measure catalog
coverage and conformance; they do not establish product success or time savings.
