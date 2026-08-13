---
name: secret-environment-audit
description: "Audit secrets and environment configuration when credentials, API keys, signing secrets, database URLs, CI/CD variables, or public/private runtime configuration change."
---

# Secret and Environment Audit

## Purpose

Verify that secrets and environment configuration are correctly classified, scoped, stored, rotated, injected, logged, and separated across client/server and environment boundaries.

## Trigger conditions

Use when credentials, tokens, API keys, signing secrets, database URLs, service-role keys, OAuth secrets, webhook secrets, CI/CD variables, runtime environment variables, or configuration-loading behavior change.

## Inputs

- Environment variable inventory and examples
- Runtime/client/server build boundaries
- CI/CD and hosting configuration
- Secret-store or platform configuration
- Logs, error reporting, build output, and deployment manifests
- Rotation and incident procedures where available

## Dependencies

- Runtime/framework rules that determine server-only versus client-exposed configuration
- Hosting, CI/CD, or secret-store metadata sufficient to inspect scope without revealing secret values
- Deployment/environment ownership and rotation/revocation procedures when privileged credentials are present
- Repository/build artifact inspection or secret-scanning capability where exposure is suspected

## Procedure

1. Inventory every sensitive and non-sensitive configuration value used by the changed system.
2. Classify each value as public configuration, internal configuration, credential, signing secret, encryption material, or privileged service identity.
3. Trace each value from source to build/runtime consumer. Identify every place where it can be serialized, bundled, cached, logged, persisted, or exposed.
4. Verify client-exposed/public-prefix variables contain only values explicitly safe for untrusted users.
5. Block service-role keys, database credentials, private API keys, signing secrets, and equivalent privileged values from browser/client bundles.
6. Verify production secrets are not committed to source, copied into documentation/examples, embedded in images/artifacts, or printed by diagnostics.
7. Prefer managed secret stores or platform secret facilities over plaintext files for deployed environments.
8. Review CI/CD identities and secret access for least privilege and job/environment scope.
9. Verify development, preview/staging, and production credentials are separated where the platform supports it.
10. Review rotation capability, revocation path, owner, expiration where appropriate, and blast radius if compromised.
11. Review error/logging/telemetry paths for accidental secret leakage, including request headers and provider payloads.
12. Check repository history or secret-scanning evidence when exposure is suspected; removing the current file is not sufficient if a live credential was committed.
13. Treat `.env.example` and setup documentation as schema/placeholder surfaces, never as a home for usable secrets.

## Outputs

- Configuration and secret inventory
- Public/private boundary map
- Exposure findings
- CI/CD and runtime scope findings
- Rotation/revocation gaps
- Required mitigations and residual risk

## Limitations

- Does not reveal or request secret values unnecessarily.
- Does not consider environment-variable storage automatically secure; the host/process/access model still matters.
- Does not treat key-name prefixes alone as proof of safety.

## Validation

- Inspect built/client artifacts or framework exposure rules when relevant.
- Run available secret scanners and repository checks without printing discovered secret values.
- Verify server-only credentials cannot be obtained through public routes, source maps, client bundles, logs, or generated configuration.
- If a credential may have been exposed, require revocation/rotation evidence rather than only code removal.
