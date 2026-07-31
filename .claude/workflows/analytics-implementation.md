# Analytics Implementation Workflow

## Trigger

A product or system change requires new or updated measurement.

## Objective

Produce a governed and reviewable analytics implementation outcome while preserving applicable contracts, evidence, and recovery boundaries.

## Inputs

- The task request, acceptance criteria, constraints, authority, and risk classification for analytics implementation.
- Current repository state and the relevant canonical memory, contracts, decisions, and runtime declarations.
- Workflow-specific artifacts and evidence referenced by the sequence below.

## Sequence

1. Define measurement decisions.
2. Create or update tracking plan.
3. Review privacy and identity behavior.
4. Implement events and properties.
5. Validate payloads.
6. Validate transformations and metrics.
7. Update dashboards and documentation.
8. Monitor data quality after release.

## Required lifecycle

1. **Understand** - Confirm the requested outcome, scope, constraints, authority, and acceptance criteria.
2. **Inspect** - Read relevant memory, contracts, decisions, repository evidence, runtime declarations, and current state.
3. **Plan** - Define ownership, dependencies, resource claims, risks, validation, review gates, and recovery strategy.
4. **Execute** - Follow the workflow sequence incrementally within the approved scope and authority.
5. **Validate** - Run required checks and compare evidence with contracts and acceptance criteria without concealing failures.
6. **Review** - Complete independent quality gates appropriate to the risk and resolve or explicitly block on findings.
7. **Document** - Record execution evidence and update governed documentation, decisions, and memory when stable facts changed.
8. **Deliver** - Report the outcome, evidence, limitations, and remaining risks; deliver a blocked or failed status when gates do not pass.

## Responsible agents

- Orchestrator: classifies scope and risk, assigns ownership, enforces gates, and consolidates delivery evidence.
- Primary domain agent selected by task routing: owns workflow-specific inspection, execution, and evidence.
- Independent reviewers and validators required by the affected quality dimensions: approve, condition, or block the outcome.

## Decision points

- Whether the request, context, source evidence, authority, and acceptance criteria are sufficient to proceed.
- Whether risk or contract impact requires additional planning, specialist ownership, independent review, approval, rollback, or escalation.
- Whether validation evidence supports continuation and successful delivery or requires a blocked or failed outcome.

## Validation

- Run every mandatory check named in the task envelope, applicable contracts, and workflow sequence.
- Compare the result with the acceptance criteria and current canonical sources; verify changed behavior and relevant regressions.
- Record commands, outputs, reviews, limitations, and unresolved risks as execution evidence.

## Failure handling

- Stop and report blocked when required context, authority, ownership, or source evidence is unavailable or contradictory.
- Stop and report failed or blocked when a mandatory test, review, approval, or contract gate fails; do not describe the workflow as successful.
- Do not perform destructive or irreversible action without explicit authority and a proportionate recovery or rollback plan.

## Completion criteria

- Successful completion requires the workflow objective and task acceptance criteria to be satisfied.
- Required validation and independent reviews must pass, with reproducible evidence recorded.
- Decisions, documentation changes, limitations, remaining risks, and next actions must be recorded for delivery.
- If any blocking condition remains, the workflow ends with an explicit blocked or failed outcome rather than successful completion.

## Rules

- Do not collect data without a defined purpose.
- Do not silently change event meaning.
- Do not include sensitive data without approval.
