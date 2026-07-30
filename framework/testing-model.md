# Testing Model

ATLAS uses layered testing to provide proportionate confidence.

## Test layers

### Static validation

Formatting, linting, type checking, schema validation, dependency checks, and
policy validation.

### Unit testing

Isolated behavior of functions, components, and domain logic.

### Integration testing

Contracts between modules, databases, services, and external systems.

### End-to-end testing

Critical user journeys through representative system boundaries.

### Non-functional testing

Performance, accessibility, security, resilience, compatibility, and recovery.

### Production validation

Canary checks, synthetic monitoring, telemetry verification, and post-release
observation.

## Testing principles

- Test behavior, not implementation trivia.
- Prioritize critical and high-risk paths.
- Preserve fast feedback.
- Avoid unstable tests without diagnostic value.
- Report untested areas explicitly.
- Pair migrations with data validation.
- Pair incidents with regression coverage when practical.
