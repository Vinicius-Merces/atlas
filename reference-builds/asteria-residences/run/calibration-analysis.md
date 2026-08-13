# P4 Asteria calibration findings

The first scored live calibration produced **88.07/100**.

- Base outcome: `production-ready`
- Final outcome: `blocked`
- Claimable: `false`
- Runtime/model: `chatgpt` / `GPT-5.6 Sol`
- Frozen implementation/evidence commit: `6ad7a1ac5d6146f28ff04a4094f7b19a0557f377`

## Blocking evidence gaps

1. `marketing-accessibility` — partial. Keyboard/focus, labels, semantics, reduced motion and viewport overflow were exercised, but a complete contrast/assistive-technology audit was not performed.
2. `marketing-production-domain` — unverified. Calibration remained localhost-only by design.
3. `marketing-seo-indexing` — partial. Robots, sitemap, canonical metadata and structured data were tested locally, not against a public production domain.

Independent review also scored 0/5 because the implementing session did not self-approve its own work.

## Strong signals

Implementation completeness, capability routing, security/isolation, failure resilience and browser reality reached full weighted completion. Frontend Craft reached 18/20. Browser evidence covered four viewport classes with no horizontal overflow, no console errors and no failed requests on critical flows.

## Campaign consequence

Do not add new ATLAS agents or skills from this calibration. The remaining gaps are primarily environment/evidence/review gaps rather than missing construction capability. Codex and Claude Code target runs should start from the same P4 campaign base and remain isolated from this calibration branch.
