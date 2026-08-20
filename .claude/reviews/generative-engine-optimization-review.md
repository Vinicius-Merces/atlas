# Generative Engine Optimization Review Gate

## Review type
Independent release-quality review for material GEO and AI-search visibility work.

## Scope
Review factual authority, usefulness, crawlability, canonical consistency, claim provenance, external-authority integrity, measurement quality, platform-specific overclaiming, and compliance with adjacent SEO/content/schema/accessibility/privacy contracts.

## Evidence inspected
Required evidence:
- Entity/source-of-truth ledger with accountable owners and freshness expectations.
- Rendered page, route, internal-link, and accessibility evidence for changed public content.
- Technical SEO, canonicalization, indexation, and structured-data evidence where affected.
- Current official guidance used for provider-specific AI-search claims.
- Baseline, representative query set, answer-engine observation protocol, comparison dates, release annotations, and confounders.
- Public claim sources, third-party authority references where used, and unresolved evidence gaps.

## Findings
Each finding must state:
- affected page, entity, claim, measurement, or workflow artifact;
- observed fact and supporting evidence;
- why it matters to users, crawlability, authority, measurement integrity, or release truth;
- responsible owner or domain specialist;
- concrete remediation or decision required.

Facts, hypotheses, provider-specific observations, and missing evidence must be labeled separately.

## Severity
- **Critical:** fabricated authority/evidence, materially false public facts, privacy/security breach, or another condition requiring an immediate release block.
- **High:** unsupported material claim, contradictory canonical/entity data, invalid schema assertion, inaccessible/crawl-blocked core answer, or misleading causal/performance claim.
- **Medium:** meaningful discoverability, IA, internal-link, freshness, measurement, localization, or evidence weakness that reduces confidence but is bounded.
- **Low:** localized clarity, documentation, or optimization improvement with limited user/release impact.
- **Note:** non-blocking observation or future opportunity supported by evidence.

## Review questions
- Does every material answer or entity claim have a visible, accountable factual source?
- Are changes useful to the intended human audience without relying on AI-only tactics?
- Are canonical routes, locale variants, rendered content, internal links, metadata, schema, feeds, and public profiles consistent?
- Are external-authority gaps recorded rather than simulated or fabricated?
- Does measurement distinguish observed behavior from causality, personalization, locale, query-set bias, algorithm changes, and model volatility?
- Are `llms.txt`, special markup, generated pages, model testing, or platform-specific tactics presented only with documented value rather than ranking/citation guarantees?
- Were all adjacent SEO, schema, accessibility, privacy, localization, analytics, security, and release gates triggered by the implementation satisfied?

## Required actions
- Critical and High findings must be fixed, removed, or explicitly accepted by the authorized owner under the relevant contract before approval.
- Unsupported or fabricated claims must not be waived as a normal GEO optimization tradeoff.
- Missing canonical evidence must be supplied or the affected claim/entity change must be removed or blocked.
- Measurement claims without a baseline or reproducible protocol must be downgraded to observations and cannot be presented as verified improvement.
- Domain-specific failures must be routed to the owning specialist/review rather than being overridden by GEO review.

## Outcome
Record exactly one outcome:
- `Approved` when mandatory evidence is present and no unresolved blocking finding remains.
- `Approved with conditions` only for bounded non-blocking Medium/Low follow-up with explicit owner and due condition.
- `Changes required` when remediation is necessary before approval.
- `Blocked` when evidence is materially missing, claims are fabricated/unsupported, mandatory validation failed, or an accountable owner has not resolved a release-critical conflict.
