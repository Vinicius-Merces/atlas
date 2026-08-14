# P4.1 Benchmark Environment & Assurance Hardening

P4.1 normalizes the evidence environment exposed by the first Asteria campaign without adding benchmark-only agents or skills.

## Principle

**Separate implementation quality from runtime tool availability, and make every assurance claim traceable to executable evidence.**

A coding runtime may use its native browser/deployment tools. When those tools are unavailable, campaign-owned fallbacks may collect evidence, but the evidence source must remain explicit (`runtime-native`, `campaign-portable`, or `unavailable`).

## Required pre-build environment freeze

Before implementation, run `scripts/capture_benchmark_environment.py` and commit the resulting environment capability manifest. It records runtime/model identity, browser availability, portable-browser eligibility, deployment availability, network posture, independent-review availability, and common executable versions.

This manifest is interpretive evidence. It must exist before comparing raw scores across runtimes.

## Portable browser fallback

`.github/workflows/reference-build-browser-evidence.yml` can check out a frozen target ref, build and start the application, install a campaign-owned Playwright/Chromium runner, and collect a common viewport/console/network/404 metadata pack.

The fallback does not replace product-specific browser flows. It provides a minimum neutral evidence floor for public routes when the coding runtime cannot expose a browser itself.

## Evidence assurance sidecar

A live run should produce an evidence-assurance JSON document matching `evidence-assurance.schema.json` and validate it with:

```bash
python scripts/validate_benchmark_evidence_assurance.py \
  --manifest path/to/evidence-assurance.json
```

The validator enforces the measured P4 findings:

- every cited evidence path exists inside the repository;
- essential non-text UI contrast is at least 3:1;
- 404 documents return 404, include `noindex`, do not contain a conflicting `index`, and do not canonicalise to another document;
- screenshot capture is not mislabeled as baseline/diff visual regression;
- advertised retry/recovery claims have both implementation and execution evidence;
- shared-cache lifetimes for mutable content do not exceed the declared freshness budget;
- public deployment claims use HTTPS and have evidence;
- browser and deployment absence is reported as a warning rather than silently upgraded.

## Claim discipline

P4.1 does not make blocked runs claimable by relaxing the rubric. It reduces environment asymmetry and catches evidence-theater defects earlier. Production-domain and deployed-indexing blockers still require a real public HTTPS environment.

## Deployment normalization

The deployment side remains campaign-owned but provider-neutral in this phase. The assurance contract records whether a campaign deployment adapter exists and refuses to infer a public deployment from localhost, preview screenshots, or source configuration. A concrete provider adapter should only be enabled when the campaign can offer the same credentials/topology to every target.
