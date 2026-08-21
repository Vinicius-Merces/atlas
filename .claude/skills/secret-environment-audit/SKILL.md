---
name: secret-environment-audit
description: "Audit secrets and environment configuration when credentials, API keys, signing secrets, database URLs, CI/CD variables, or public/private runtime configuration change."
---

# Secret and Environment Audit

## Purpose

Verify that secrets and environment configuration are correctly classified, scoped, stored, rotated, injected, logged, and separated across client/server, public-route, build-artifact, and environment boundaries.

## Trigger conditions

Use when credentials, tokens, API keys, signing secrets, database URLs, service-role keys, OAuth secrets, webhook secrets, CI/CD variables, runtime environment variables, configuration-loading behavior, or possible public configuration exposure changes.

## Inputs

- Environment variable inventory and examples
- Runtime/client/server build boundaries
- CI/CD and hosting configuration
- Secret-store or platform configuration
- Logs, error reporting, build output, and deployment manifests
- Public deployment routes/artifacts when exposure is plausible
- Rotation and incident procedures where available

## Dependencies

- Runtime/framework rules that determine server-only versus client-exposed configuration
- Hosting, CI/CD, or secret-store metadata sufficient to inspect scope without revealing secret values
- Deployment/environment ownership and rotation/revocation procedures when privileged credentials are present
- Repository/build artifact inspection or secret-scanning capability where exposure is suspected
- `web-security-header-audit` when the question includes public sensitive-path exposure or browser-facing configuration delivery

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
14. When a public deployment exists and exposure is plausible, perform bounded passive GET/HEAD probes for stack-relevant sensitive paths such as `/.env`, environment variants, `/.npmrc`, `/.git/config`, `/.ssh/authorized_keys`, service-account JSON names, private-key/config files, or debug/server-status endpoints. Do not brute-force large wordlists.
15. Treat HTTP 200 as a review trigger, not automatic proof of a breach. Inspect the response for secret/private-key markers without printing values. A 403/404 is normally acceptable evidence for that path but does not prove no other exposure exists.
16. If any live credential may have been publicly returned, stop treating code deletion as sufficient remediation and require credential rotation/revocation, downstream impact review, and incident evidence appropriate to severity.

## Outputs

- Configuration and secret inventory
- Public/private boundary map
- Exposure findings including bounded public-path evidence when applicable
- CI/CD and runtime scope findings
- Rotation/revocation gaps
- Required mitigations and residual risk

## Limitations

- Does not reveal or request secret values unnecessarily.
- Does not consider environment-variable storage automatically secure; the host/process/access model still matters.
- Does not treat key-name prefixes alone as proof of safety.
- Passive public-path checks are not penetration tests and cannot prove the absence of hidden files or alternate exposure paths.

## Validation

- Inspect built/client artifacts or framework exposure rules when relevant.
- Run available secret scanners and repository checks without printing discovered secret values.
- Verify server-only credentials cannot be obtained through public routes, source maps, client bundles, logs, generated configuration, or representative stack-relevant sensitive paths.
- For public-path probes, record path, status/body class, timestamp, and environment without storing secret values; inspect any successful response for secret-like markers.
- If a credential may have been exposed, require revocation/rotation evidence rather than only code removal.
