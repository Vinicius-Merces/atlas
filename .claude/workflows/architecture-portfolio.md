# Architecture Portfolio Workflow

## Trigger

An organization needs to assess, rationalize, or evolve a portfolio of systems.

## Objective

Produce a governed and reviewable architecture portfolio outcome while preserving applicable contracts, evidence, and recovery boundaries.

## Inputs

- The task request, acceptance criteria, constraints, authority, and risk classification for architecture portfolio.
- Current repository state and the relevant canonical memory, contracts, decisions, and runtime declarations.
- Workflow-specific artifacts and evidence referenced by the sequence below.

## Sequence

1. Inventory systems and owners.
2. Map business capabilities.
3. Classify lifecycle and criticality.
4. Identify duplication, fragmentation, and risk concentration.
5. Define target-state principles.
6. Propose invest, migrate, consolidate, contain, or retire actions.
7. Sequence transition roadmaps.
8. Define portfolio metrics.
9. Review periodically.

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

- Portfolio ownership visible
- Target state defined
- Transition actions prioritized
- Strategic dependencies explicit
- Successful completion requires the workflow objective and task acceptance criteria to be satisfied.
- Required validation and independent reviews must pass, with reproducible evidence recorded.
- Decisions, documentation changes, limitations, remaining risks, and next actions must be recorded for delivery.
- If any blocking condition remains, the workflow ends with an explicit blocked or failed outcome rather than successful completion.
