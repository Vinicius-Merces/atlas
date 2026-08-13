# SaaS Production Trust

Navigation note for production trust capabilities. This note links canonical sources and does not redefine them.

## Canonical model

- `framework/saas-production-trust-model.md`
- `framework/capabilities/saas-production-trust.yaml`

## Primary agents

- `security-engineer`
- `backend-engineer`
- `integration-engineer`
- `platform-engineer`
- `reliability-engineer`
- `qa-engineer`

## Skills

- `authentication-flow-review`
- `authorization-boundary-review`
- `row-level-security-review`
- `secret-environment-audit`
- `webhook-reliability-review`
- `payment-integration-review`
- `external-api-resilience-review`

## Workflow

- `.claude/workflows/saas-production-readiness.md`

## Independent review

- `.claude/reviews/saas-production-trust-review.md`

## Mental model

Production trust is cumulative. Authentication, authorization, data isolation,
secret boundaries, provider reliability, financial consistency, observability,
and recovery must each be explicit when applicable. A managed provider may
implement part of a control, but it does not remove application responsibility
for the boundaries the application still owns.
