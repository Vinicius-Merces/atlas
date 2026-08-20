# Generative Engine Optimization Review Gate

## Review type
Independent release-quality review for material GEO and AI-search visibility work.

## Scope
Review factual authority, usefulness, crawlability, crawler-access evidence, canonical consistency, claim provenance, external-authority integrity, machine-discovery surface safety, measurement quality, platform-specific overclaiming, and compliance with adjacent SEO/content/schema/accessibility/privacy contracts.

## Evidence inspected
Required evidence:
- Entity/source-of-truth ledger with accountable owners and freshness expectations.
- Rendered page, route, internal-link, and accessibility evidence for changed public content.
- Technical SEO, canonicalization, indexation, and structured-data evidence where affected.
- Current official guidance used for provider-specific AI-search or named-crawler claims.
- Dated crawler-access matrix when named AI crawlers are in scope, including purpose, robots decision, path scope, observed HTTP behavior, and relevant CDN/WAF/bot-mitigation evidence.
- Public machine-discovery surfaces when changed, with documented purpose, consumer/use case, freshness, and public-data boundary evidence.
- Baseline, representative query set, answer-engine observation protocol, comparison dates, release annotations, and confounders.
- Public claim sources, third-party authority references where used, and unresolved evidence gaps.

## Findings
Each finding must state:
- affected page, entity, claim, crawler, discovery surface, measurement, or workflow artifact;
- observed fact and supporting evidence;
- why it matters to users, crawlability, authority, public-data safety, measurement integrity, or release truth;
- responsible owner or domain specialist;
- concrete remediation or decision required.

Facts, hypotheses, provider-specific observations, and missing evidence must be labeled separately.

## Severity
- **Critical:** fabricated authority/evidence, materially false public facts, secret/PII/private-endpoint leakage, privacy/security breach, or another condition requiring an immediate release block.
- **High:** unsupported material claim, contradictory canonical/entity data, invalid schema assertion, inaccessible/crawl-blocked core answer, named-crawler access claimed without production evidence, or misleading causal/performance claim.
- **Medium:** meaningful discoverability, IA, internal-link, crawler-policy, freshness, measurement, localization, or evidence weakness that reduces confidence but is bounded.
- **Low:** localized clarity, documentation, or optimization improvement with limited user/release impact.
- **Note:** non-blocking observation or future opportunity supported by evidence.

## Review questions
- Does every material answer or entity claim have a visible, accountable factual source?
- Are changes useful to the intended human audience without relying on AI-only tactics?
- Are canonical routes, locale variants, rendered content, internal links, metadata, schema, feeds, public profiles, and machine-discovery surfaces consistent?
- When named AI crawlers matter, is search/retrieval access distinguished from training access and backed by dated official guidance plus observed production or production-equivalent behavior?
- Can CDN/WAF, bot mitigation, authentication, JavaScript challenges, geo rules, or rate limits contradict the intended crawler policy?
- Does every `llms.txt`, public API description, API catalog, or similar discovery surface have a real public purpose, current content, and a clean secret/PII/private-endpoint boundary?
- Are optional machine-readable conventions described as supplementary/support-dependent rather than guaranteed ranking or citation mechanisms?
- Are external-authority gaps recorded rather than simulated or fabricated?
- Does measurement distinguish observed behavior from causality, personalization, locale, query-set bias, algorithm changes, and model volatility?
- Are `llms.txt`, special markup, generated pages, model testing, or platform-specific tactics presented only with documented value rather than ranking/citation guarantees?
- Were all adjacent SEO, schema, accessibility, privacy, localization, analytics, security, and release gates triggered by the implementation satisfied?

## Required actions
- Critical and High findings must be fixed, removed, or explicitly accepted by the authorized owner under the relevant contract before approval.
- Unsupported or fabricated claims must not be waived as a normal GEO optimization tradeoff.
- Missing canonical evidence must be supplied or the affected claim/entity change must be removed or blocked.
- Named-crawler access claims without observed production or production-equivalent evidence must be treated as unverified.
- Machine-discovery surfaces that expose private data, secrets, privileged configuration, internal-only endpoints, or personal data must be removed or routed through the owning security/privacy review before approval.
- Measurement claims without a baseline or reproducible protocol must be downgraded to observations and cannot be presented as verified improvement.
- Domain-specific failures must be routed to the owning specialist/review rather than being overridden by GEO review.

## Outcome
Record exactly one outcome:
- `Approved` when mandatory evidence is present and no unresolved blocking finding remains.
- `Approved with conditions` only for bounded non-blocking Medium/Low follow-up with explicit owner and due condition.
- `Changes required` when remediation is necessary before approval.
- `Blocked` when evidence is materially missing, claims are fabricated/unsupported, mandatory validation failed, a public discovery surface creates an unsafe data boundary, or an accountable owner has not resolved a release-critical conflict.
