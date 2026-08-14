# P4.1/P4.2 Benchmark Environment, Assurance & Controlled Deployment

P4.1 normalizes the evidence environment exposed by the first Asteria campaign. P4.2 extends that work with a campaign-owned public HTTPS deployment path. Neither phase adds benchmark-only agents or skills.

## Principle

**Separate implementation quality from runtime tool availability, and make every assurance claim traceable to executable evidence.**

A coding runtime may use its native browser/deployment tools. When those tools are unavailable, campaign-owned fallbacks may collect evidence, but the evidence source must remain explicit (`runtime-native`, `campaign-portable`, or `unavailable`). Public deployment evidence must additionally declare whether it is `controlled-preview`, `claimable-production`, or `unavailable`.

## Required pre-build environment freeze

Before implementation, run `scripts/capture_benchmark_environment.py` and commit the resulting environment capability manifest. It records runtime/model identity, browser availability, portable-browser eligibility, deployment availability, network posture, independent-review availability, and common executable versions.

This manifest is interpretive evidence. It must exist before comparing raw scores across runtimes.

## Portable browser fallback

`.github/workflows/reference-build-browser-evidence.yml` can check out a frozen target ref, build and start the application, install a campaign-owned Playwright/Chromium runner, and collect a common viewport/console/network/404 metadata pack.

The fallback does not replace product-specific browser flows. It provides a minimum neutral evidence floor for public routes when the coding runtime cannot expose a browser itself.

## Controlled public deployment

`.github/workflows/reference-build-controlled-deployment.yml` checks out an immutable target ref, builds and starts it, opens a campaign-owned public HTTPS ingress, verifies that ingress externally, records TLS/HTTP/source/lifecycle evidence, and can run the portable Chromium collector against the public URL.

The active preview adapter uses a pinned Cloudflare Quick Tunnel from GitHub Actions and requires no runtime-owned credential. This is intentionally classified `controlled-preview`: it equalizes public-network evidence but is temporary testing infrastructure and cannot satisfy a production-domain blocker.

The `claimable-production` provider shape is currently Vercel and remains disabled until one campaign-owned project/credential topology can be applied identically to every compared target. Target-specific hosting convenience is not comparison-grade.

## Evidence assurance sidecar

A live run should produce an evidence-assurance JSON document matching `evidence-assurance.schema.json` and validate it with:

```bash
python scripts/validate_benchmark_evidence_assurance.py \
  --manifest path/to/evidence-assurance.json
```

Deployment evidence should match `../controlled-deployment/deployment-evidence.schema.json` and validate with:

```bash
python scripts/validate_controlled_deployment_evidence.py \
  --manifest path/to/deployment.json
```

The validators enforce the measured P4 findings:

- every cited evidence path exists inside the repository;
- essential non-text UI contrast is at least 3:1;
- 404 documents return 404, include `noindex`, do not contain a conflicting `index`, and do not canonicalise to another document;
- screenshot capture is not mislabeled as baseline/diff visual regression;
- advertised retry/recovery claims have both implementation and execution evidence;
- shared-cache lifetimes for mutable content do not exceed the declared freshness budget;
- public deployment claims use HTTPS and have evidence;
- controlled previews cannot be promoted into claimable production;
- browser and deployment absence is reported rather than silently upgraded.

## Claim discipline

P4.1/P4.2 do not make blocked runs claimable by relaxing the rubric. They reduce environment asymmetry and catch evidence-theater defects earlier. A controlled public preview can support browser, remote-network and deployed-crawl evidence, but production-domain blockers still require a persistent `claimable-production` deployment with environment configuration evidence.
