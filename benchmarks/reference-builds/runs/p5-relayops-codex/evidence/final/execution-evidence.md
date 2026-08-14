# RelayOps P5 — Final Local Execution Evidence

## Identity and integrity

- Runtime: `codex`
- Model: `GPT-5`
- Branch: `bench/p5-relayops-codex`
- Campaign base: `99cdbdbf40ca2709bb4e0d99b7d3320d9f89610b`
- First frozen result commit: `6295efb`
- First frozen score: `75.38`, outcome `blocked`
- Fixture SHA-256: `3227ec96f8528476bffbfd860112534158cb5c562a1474e329760685f78d59b9`
- Rubric SHA-256: `6463ae7fde36affecc20eff21f0ec73e04e0fb44c920a3cbc9115502a1b56b31`
- Isolation attestation remains unchanged; no prohibited branch or prior RelayOps implementation was consulted.

## Product execution

- `node scripts/build.mjs`: passed; dependency-free Node SSR bundle generated.
- `NODE_ENV=test node --test tests/*.test.js`: 16/16 passed after frontend and independent-review remediation.
- `validate_benchmark_runner_contract.py`: passed against the frozen runner contract.
- `validate_relayops_assurance.py`: passed with five direct cross-tenant denial attempts and billing/recovery/admin/import/secret gates present.
- `validate_all.py --profile full`: passed after isolating the test temp root; ATLAS framework, schemas, registry, 128 skills, 87 agents, runtime adapters, campaign packs, policies, documentation, smoke/contract/Codex/conformance groups, and 311 repository tests were green.

The executed assurance suite covers session lifecycle, role denial, database/object isolation, storage read/write isolation, search isolation, cache/job isolation, duplicate delivery, bounded retry and recovery, notification/provider recovery, billing entitlement authority, duplicate/out-of-order webhooks, privileged support/audit, CSV partial failure/replay, secret scanning, and real HTTP auth/origin/logout behavior.

Independent review exposed and remediation closed six gaps missed by the original 13-test suite: work-order creation SQL and idempotency, entitlement enforcement on operational mutations, duplicate-webhook recovery after provider outage, role enforcement on synthetic billing events and explicit reconciliation, technician assignment scope on dashboard/search, and invite password policy. Three added tests plus expanded HTTP coverage execute these paths directly.

## Frontend remediation

- Frozen direction: `benchmarks/reference-builds/runs/p5-relayops-codex/frontend-direction.md`
- Product-specific signature: authoritative `Relay Line` command surface derived from work-order states.
- Motion: page orientation, operational tracer, count interpolation, status pulse, navigation/button/table/dialog/toast feedback.
- Reduced motion: continuous tracers and breathing effects removed; core state remains visible.
- Responsive composition: off-canvas navigation and scrim, compact rail, adaptive panels, explicit horizontal table affordance, retained semantic tables.
- State treatment: mutation busy state, focus, validation error, toast success/error, empty search, dialog, destructive billing/support, enabled/revoked entitlement, partial import.

## Executed HTTP and asset checks

Local production-equivalent server on the frozen runner port model returned:

| Route | HTTP | HTML bytes | Total local time |
|---|---:|---:|---:|
| `/login` | 200 | 3,271 | 0.003 s |
| `/demo/manager` → `/app` | 200 | 9,970 | 0.191 s |
| `/app/work-orders` | 200 | 10,760 | 0.059 s |
| `/app/customers` | 200 | 7,958 | 0.003 s |
| `/app/billing` | 200 | 6,850 | 0.074 s |
| `/app/import-export` | 200 | 5,839 | 0.009 s |

Public client assets total 45,466 uncompressed bytes: CSS 35,863 bytes and JavaScript 9,603 bytes. No frontend runtime dependency or third-party script was added.

## Browser and deployment truth

The runtime-native browser was unavailable in the pre-implementation environment manifest. The required campaign-portable browser and controlled HTTPS preview depend on publishing this branch and invoking the shared GitHub workflow. Publication was rejected by the session's external-write policy. No standalone or Codex-specific browser harness was substituted.

Therefore these claims remain `unverified` in the final local submission:

- rendered responsive behavior at 360/768/1280/1920;
- rendered accessibility, focus order, contrast, overflow, console and network evidence;
- browser authentication and operational journeys;
- controlled-preview deployment evidence;
- claimable production configuration (which controlled-preview could not satisfy in any case).

No source-code inference is presented as rendered-browser proof.
