# Release Confidence Model

Release confidence combines evidence rather than relying on a single test result.

## Confidence dimensions

- Package integrity
- Contract compatibility
- Test evidence
- Documentation accuracy
- Migration readiness
- Runtime compatibility
- Known limitation quality
- Rollback or recovery readiness

## Confidence states

- **High:** mandatory evidence is complete and no blocking findings remain.
- **Moderate:** release is usable with explicit non-critical limitations.
- **Low:** important evidence is missing or unresolved risk remains.
- **Blocked:** mandatory validation failed.

## Beta release rule

Beta releases may contain experimental areas, but stable and experimental
boundaries must be explicit.
