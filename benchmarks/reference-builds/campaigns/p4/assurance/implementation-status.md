# P4.1/P4.2 implementation status

## Closed from the Asteria remediation backlog

- Portable browser evidence has a campaign-owned Chromium/Playwright fallback workflow.
- Environment capability state can be frozen before implementation with runtime/model/tool provenance.
- Evidence references are repository-bounded and deterministically checked for existence.
- Essential non-text contrast below 3:1 fails assurance validation.
- 404 assurance checks reject non-404 status, missing `noindex`, conflicting `index`, and canonicalisation to another document.
- Visual evidence must declare `baseline-diff`, `capture-only`, or `unavailable`; capture-only evidence is explicitly warned and cannot masquerade as automated regression.
- Advertised retry/recovery claims require implementation and execution evidence references.
- Shared mutable caches are checked against an explicit freshness budget.
- Public deployment evidence now has an explicit class and HTTPS evidence contract.
- A campaign-owned controlled public preview path is active through GitHub Actions plus a pinned Cloudflare Quick Tunnel.
- Controlled deployment evidence records frozen source commit, URL, TLS, HTTP response, lifecycle and provider identity.
- The controlled preview can feed the portable browser runner using the public HTTPS URL.
- Controlled previews are deterministically prevented from satisfying `marketing-production-domain`.

## Externally activated for comparison-grade preview

The P4.2 controlled preview adapter requires no target-runtime credential and is available through `.github/workflows/reference-build-controlled-deployment.yml`. The PR path includes an external-ingress smoke that starts a deterministic origin, opens the public HTTPS ingress, probes it, validates the evidence sidecar and uploads the resulting artifact.

This removes the Codex-vs-Claude asymmetry for public browser/network/SEO evidence without pretending that a temporary testing tunnel is production.

## Claimable production still intentionally disabled

The persistent production provider shape is Vercel, but `claimable_production.enabled` remains `false`. Activation requires one campaign-owned project and deployment credential topology that can be used identically for every compared target, plus immutable deployment/source mapping and inspectable environment/deployment logs.

Until those campaign-owned credentials exist, a production-domain blocker remains real. Native provider access available to only one runtime must not be used to create an unfair target advantage.

## Intentionally unchanged

- No agents added.
- No skills added.
- The P3 scoring rubric and Asteria fixture are unchanged.
- Historical P4 target branches and frozen scores are unchanged.
- Portable fallback evidence is labeled separately from runtime-native evidence.
- Controlled-preview evidence is labeled separately from claimable-production evidence.

## Exit criteria

P4.2 is framework-complete when the controlled deployment contract/tests pass normal ATLAS CI and the dedicated GitHub Actions smoke successfully proves the public HTTPS ingress. Persistent production activation is a separate credentialed capability and is not faked to close this phase.
