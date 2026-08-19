# Quality Gates Model

## Purpose

ATLAS defines quality gates by project risk and change impact instead of forcing the same toolchain onto every repository.

A gate is a required piece of evidence for a declared scope. Tools are implementations of gates, not the gate itself.

## Core principle

**Require proportionate evidence, reuse healthy project tooling, and add dependencies only when they close a real evidence gap.**

Passing one tool does not make a release safe. Failing to use a fashionable tool is not a defect when equivalent evidence already exists.

## Quality profiles

### Minimal

Use for prototypes, demos, low-risk internal utilities, documentation-only work, or very small changes with limited blast radius.

Expected evidence where applicable:

- build or syntax validation
- existing formatter/linter/type checks
- focused behavior validation
- smoke test for the changed path
- secret/dependency sanity check when runtime inputs change
- manual rendered check for user-facing changes

Minimal does not mean unvalidated. It means the evidence is intentionally narrow.

### Standard

Use for normal production features, public websites, SaaS functionality, integrations, persistent data changes, and maintained repositories.

Expected evidence where applicable:

- deterministic formatting/lint/type/schema checks
- unit tests for stable domain behavior
- integration tests at changed boundaries
- browser/E2E validation for critical user journeys
- dependency/supply-chain review when package or lockfile inputs change
- accessibility/performance/security checks proportional to the feature
- coverage visibility where it helps identify blind spots
- release smoke checks and failure diagnostics

### Production Critical

Use for high-impact or hard-to-recover systems such as authentication, authorization, payments, destructive data operations, migrations, tenant isolation, high-volume workflows, consequential AI tools, or changes with large customer/revenue impact.

In addition to Standard evidence, consider:

- contract tests and negative-path tests
- rollback/recovery rehearsal or evidence
- concurrency/idempotency tests
- migration validation against representative data
- security and privacy review
- mutation testing for small, high-value logic surfaces where conventional coverage is not enough evidence
- resilience/fault-injection testing when failure behavior is material
- production observability and alert verification
- canary/staged rollout or equivalent blast-radius control

Production Critical is a profile, not a command to maximize test count.

## Gate categories

### Static code quality

Possible evidence:

- formatter
- linter
- type checker
- schema validation
- dead-code/dependency analysis
- commit or repository policy checks

For JavaScript/TypeScript, Biome, ESLint, TypeScript, Knip, commitlint, or equivalent tools may be appropriate depending on the existing stack. ATLAS must not install all of them by default or duplicate healthy responsibilities.

### Unit and component behavior

Use when important logic can be validated deterministically without crossing system boundaries.

Prefer tests that describe stable behavior and edge cases rather than implementation structure.

### Integration and contract behavior

Use at database, API, queue, provider, filesystem, cache, auth, and module boundaries where independent components can drift.

### End-to-end and browser behavior

Use for critical user journeys where rendered or integrated behavior matters.

Prefer the repository's existing healthy runner. Playwright is a strong default when a new browser runner is justified, but ATLAS must not create parallel E2E stacks without evidence that the existing runner is inadequate.

### Coverage evidence

Coverage is a visibility signal, not proof of correctness.

Coverage services such as Codecov or equivalent reporting can be used when they improve review quality, trend visibility, or protected-branch policy. Do not optimize line percentage while leaving critical behaviors untested.

### Mutation testing

Mutation testing tools such as Stryker can be useful for compact, high-value logic where normal coverage is misleading.

Do not apply mutation testing indiscriminately to large UI or low-risk surfaces when runtime cost and maintenance exceed the evidence gained.

### Dependency and supply-chain evidence

Use dependency review, lockfile checks, provenance, vulnerability scanning, and package policy according to the project's exposure and release model.

### Non-functional evidence

Select from performance, accessibility, security, privacy, resilience, compatibility, localization, and recovery based on actual risk.

## Gate selection procedure

1. Classify the project/change as Minimal, Standard, or Production Critical.
2. Identify critical user/business behaviors and failure modes.
3. Inventory existing healthy tooling and CI evidence.
4. Map each risk to the cheapest reliable evidence that can detect it.
5. Add tooling only for uncovered risks or unreliable evidence.
6. Define blocking versus advisory outcomes before execution.
7. Define failure artifacts: logs, traces, screenshots, reports, diffs, or reproduction steps.
8. Record intentional skips with a reason and owner when the profile would normally expect the gate.
9. Reassess the profile when scope, data sensitivity, traffic, integrations, or consequence changes.

## Blocking policy

A gate can be blocking when:

- it protects a declared acceptance criterion
- it detects a known high-impact failure class
- it protects a stable contract
- it is required by security/privacy/compliance policy
- the release profile declares it mandatory

Advisory gates must remain visible and must not be mislabeled as passed release criteria.

## Flake policy

Do not hide unreliable tests behind unlimited retries or fixed sleeps.

Flaky evidence should be:

- identified explicitly
- given diagnostic artifacts
- isolated when necessary
- repaired or removed if it has no decision value

Retries may handle known transient infrastructure behavior only inside a bounded policy.

## CI resource policy

Quality gates must respect repository and hosting limits.

When builds or tests are memory/CPU constrained:

- split independent jobs when practical
- reuse caches safely
- avoid loading unnecessary workspaces/packages
- cap test workers/concurrency when memory pressure is the bottleneck
- separate expensive advisory analysis from the critical fast path when appropriate
- preserve a deterministic required gate set before adding expensive extras

A quality pipeline that repeatedly dies from resource exhaustion is not a healthy gate.

## Outputs

A project or change using this model should be able to report:

- selected quality profile
- gate matrix
- tool mapped to each gate
- required versus advisory status
- evidence location
- known untested risk
- intentional skips/exceptions
- CI/runtime cost concerns
- final release blockers

## ATLAS integration

- `framework/testing-model.md` defines the layered testing strategy.
- `test-strategy-design` turns risk into a test matrix.
- `test-automation-engineer` implements repeatable evidence.
- `supply-chain-risk-audit` handles package/build-input risk.
- `browser-flow-validation`, `frontend-craft-review`, `web-production-assurance-review`, security, privacy, and performance capabilities provide domain-specific gates.
