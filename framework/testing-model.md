# Testing Model

ATLAS uses layered testing to provide proportionate confidence.

Testing layers describe the kind of evidence needed. `framework/quality-gates-model.md` determines how much of that evidence a project or change must require based on risk and impact.

## Test layers

### Static validation

Formatting, linting, type checking, schema validation, dependency checks, dead-code analysis, and policy validation.

Reuse healthy project tooling before introducing replacements. For JavaScript/TypeScript, tools such as Biome, ESLint, TypeScript, Knip, commitlint, or equivalents may satisfy different parts of this layer, but installing all of them by default is not a quality requirement.

### Unit testing

Isolated behavior of functions, components, and domain logic.

### Integration testing

Contracts between modules, databases, services, queues, caches, and external systems.

### End-to-end testing

Critical user journeys through representative system boundaries.

Prefer an existing healthy runner. Use Playwright when it is already established or when a new real-browser runner is justified by the project. Avoid parallel E2E stacks without a specific evidence gap.

### Non-functional testing

Performance, accessibility, security, privacy, resilience, compatibility, recovery, localization, and other quality attributes selected by actual risk.

### Production validation

Canary checks, synthetic monitoring, telemetry verification, staged rollout evidence, and post-release observation.

## Quality profiles

ATLAS uses three default evidence profiles from `framework/quality-gates-model.md`:

- **Minimal** for prototypes, demos, and narrow low-risk changes;
- **Standard** for maintained production websites, SaaS features, integrations, and normal product delivery;
- **Production Critical** for high-impact authentication, authorization, payments, migrations, destructive operations, tenant isolation, consequential AI tooling, and similarly hard-to-recover changes.

The profile selects expected evidence. It does not prescribe one universal package list.

## Coverage

Coverage is useful for locating untested surfaces but is not proof of correctness.

Coverage reporting services such as Codecov or equivalent tools may be adopted when trend visibility or protected-branch review benefits from them. Coverage percentage must not replace behavior and risk analysis.

## Mutation testing

Mutation testing such as Stryker can add evidence for compact, critical logic when line/branch coverage gives false confidence.

Use it selectively because its runtime and maintenance cost can be disproportionate for broad UI, generated code, or low-risk surfaces.

## Testing principles

- Test behavior, not implementation trivia.
- Prioritize critical and high-risk paths.
- Preserve fast feedback.
- Avoid unstable tests without diagnostic value.
- Do not hide flakiness behind unlimited retries or fixed sleeps.
- Report untested areas explicitly.
- Pair migrations with data validation.
- Pair incidents with regression coverage when practical.
- Make test failures actionable with the right logs, traces, screenshots, network/console evidence, or reproduction data.
- Match concurrency and worker counts to CI memory/CPU constraints instead of letting the quality pipeline become a source of resource failures.

## Gate selection

For every material change:

1. identify critical behaviors and failure modes;
2. select the appropriate quality profile;
3. inventory existing healthy tools;
4. map risks to evidence;
5. add a tool only where evidence is missing or unreliable;
6. classify gates as required or advisory;
7. record intentional skips and residual risk.

The test strategy should be reviewable even when the implementation stack changes.
