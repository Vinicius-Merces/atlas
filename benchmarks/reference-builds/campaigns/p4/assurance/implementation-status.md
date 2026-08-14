# P4.1 implementation status

## Closed from the Asteria remediation backlog

- Portable browser evidence now has a campaign-owned Chromium/Playwright fallback workflow.
- Environment capability state can be frozen before implementation with runtime/model/tool provenance.
- Evidence references are repository-bounded and deterministically checked for existence.
- Essential non-text contrast below 3:1 fails assurance validation.
- 404 assurance checks reject non-404 status, missing `noindex`, conflicting `index`, and canonicalisation to another document.
- Visual evidence must declare `baseline-diff`, `capture-only`, or `unavailable`; capture-only evidence is explicitly warned and cannot masquerade as automated regression.
- Advertised retry/recovery claims require implementation and execution evidence references.
- Shared mutable caches are checked against an explicit freshness budget.
- Public deployment claims require HTTPS plus evidence.

## Normalized but not externally activated

Public deployment now has a campaign-owned adapter contract. The provider remains `unconfigured` because P4 demonstrated that choosing a target-specific provider or credential path would reintroduce environment bias. Until one provider/topology can be offered equally to every target, production-domain blockers remain real and must not be promoted.

## Intentionally unchanged

- No agents added.
- No skills added.
- The P3 scoring rubric and Asteria fixture are unchanged.
- Historical P4 target branches and frozen scores are unchanged.
- Portable fallback evidence is labeled separately from runtime-native evidence.

## Exit criteria

P4.1 can be considered framework-complete when the new validator and contract tests pass the normal ATLAS CI/release profile. A future campaign may activate the deployment adapter once equal provider credentials/topology are available.
