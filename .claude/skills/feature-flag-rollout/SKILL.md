---
name: feature-flag-rollout
description: "Design feature flags and staged rollouts by environment, user, tenant, cohort, percentage, or kill switch with trusted evaluation context, safe defaults, metrics, rollback, lifecycle ownership, and flag removal."
---

# Feature Flag Rollout

## Purpose

Use flags as temporary controlled decision points for rollout, compatibility, experimentation, and emergency disablement without turning product logic into permanent hidden configuration.

## Trigger conditions

Use for staged launches, canaries, tenant/user allowlists, percentage rollouts, migrations, kill switches, experiments, or coordinated frontend/backend compatibility transitions.

## Inputs

- Feature risk and rollout objective
- Evaluation context fields and privacy constraints
- Environments/cohorts/tenants
- Default and provider-failure behavior
- Success/error/business metrics and rollback trigger

## Procedure

1. Define one flag purpose: release, ops kill switch, experiment, entitlement, or migration. Do not conflate authorization/entitlement with convenience flags accidentally.
2. Define trusted evaluation context and avoid user-controlled claims for privileged targeting.
3. Choose safe defaults for missing configuration/provider outage and document client/server evaluation boundaries.
4. Ensure frontend hiding does not replace backend compatibility or authorization.
5. Define rollout stages, cohort stability, percentage hashing/assignment behavior, and rollback criteria.
6. Instrument exposure/evaluation and relevant product/reliability metrics without logging excessive personal context.
7. Coordinate schema/API/data migrations so old and new code paths can coexist during rollout.
8. Add owner, creation date, cleanup condition, and expected removal date to prevent permanent flag debt.
9. Test both flag states and provider/config failure before rollout.

## Outputs

- Flag purpose and evaluation-context contract
- Rollout/rollback stages
- Failure/default behavior
- Measurement and ownership plan
- Removal condition and validation evidence

## Dependencies

- `experiment-design` when the flag powers an experiment
- `analytics-implementation-audit` for exposure/outcome measurement
- `authorization-boundary-review` when targeting intersects privileged behavior
- `version-transition-validation` for compatibility rollouts

## Limitations

Feature flags are not authorization controls by themselves and do not remove the need for migration compatibility. Provider semantics must be verified when using an external flag service.

## Validation

- Exercise all material flag states, targeted/non-targeted actors, provider/config failure, stale client state, and rollback.
- Verify assignment stability and exposure instrumentation where percentage/experiment rollout is used.
- Confirm cleanup ownership is recorded.
