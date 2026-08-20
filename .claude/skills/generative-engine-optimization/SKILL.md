---
name: generative-engine-optimization
description: "Plan or review Generative Engine Optimization for AI-search visibility using factual entity evidence, answer-ready content, crawlability, external authority, and measured outcomes without speculative AI-only hacks."
---

# Generative Engine Optimization

## Purpose
Provide a repeatable, evidence-led GEO procedure for improving how authoritative public information can be discovered, understood, verified, cited, and navigated by people, search engines, and AI answer systems without replacing normal SEO, accessibility, or factual product quality.

## Trigger conditions
Activate when a public site needs material work on AI-search visibility, answer-engine discoverability, entity authority, answer-ready information architecture, citation readiness, crawler accessibility, public machine-discovery surfaces, or GEO measurement. Do not trigger for a metadata-only edit that has no entity, content, crawlability, authority, discovery-surface, or measurement implications.

## Inputs
Required:
- business outcome, target audience, market/locale, decision journey, and priority questions;
- rendered site/routes and current SEO/internal-link state;
- canonical entity, product/service, policy, people, location, and proof sources with accountable owners;
- available Search Console, analytics, conversion, indexation, or answer-engine observation evidence.

Optional:
- current official platform guidance for named crawlers or answer systems;
- `robots.txt`, robots meta/X-Robots-Tag behavior, CDN/WAF/bot-mitigation evidence, and production HTTP responses;
- intentionally public machine-discovery surfaces such as `llms.txt`, public API descriptions, OpenAPI documents, or standards-based API catalogs when a real consumer/use case exists;
- third-party citations, directories, research, press, partnerships, community references, and prior GEO experiments;
- structured-data inventory and content freshness records.

## Procedure
1. Define business outcome, audiences, target questions, markets/locales, and decision journeys. Do not start from a speculative list of “AI keywords”.
2. Build a factual entity map covering organization, offers, people, locations, products, policies, first-party evidence, and accountable owner for each material claim. Use `entity-authority-mapping`.
3. Inspect rendered pages, internal links, canonical routes, accessibility, freshness, and normal SEO. Route mechanics to `seo-technical-audit`; route schema truth to `structured-data-validation`.
4. When named AI crawlers or answer-system bots matter, build a dated crawler-access matrix: user agent/purpose, allow-or-block business decision, relevant path scope, `robots.txt` behavior, WAF/CDN/bot-mitigation behavior, observed HTTP status, and official guidance source. Distinguish search/retrieval crawlers from model-training crawlers instead of treating all AI bots as one class.
5. Verify crawler accessibility against production or production-equivalent responses. Configuration alone is insufficient when a CDN, firewall, JavaScript challenge, authentication rule, geo rule, or rate limit can still return blocked or degraded responses.
6. Audit machine-readable discovery surfaces only when they have a documented public consumer or operational purpose. Treat `llms.txt` and similar conventions as supplementary and support-dependent, not as universal ranking requirements. Treat API discovery standards such as an API catalog as API discovery, not as generic GEO authority. Verify these surfaces are current, intentionally public, and do not expose secrets, private endpoints, personal data, or internal identifiers.
7. Identify answer gaps: questions users need answered, concise answer blocks, qualification/context, primary evidence, date/freshness, and the next useful action.
8. Improve information architecture before creating more pages. Prefer authoritative service, product, documentation, case-study, policy, and knowledge pages with clear headings, semantic HTML, reciprocal internal links, and evidence-backed summaries.
9. Assess external authority honestly: credible references, directories, partnerships, citations, press, original research, and community presence. Record gaps and ownership; never manufacture signals.
10. Evaluate current platform guidance at recommendation time. Do not make `llms.txt`, special “GEO schema”, invisible text, prompt injection, or bulk AI pages a required tactic without documented human or crawler value.
11. Cross-check material entity facts across rendered content, metadata, structured data, feeds, locale variants, public profiles, and any machine-discovery surface. Record the exact conflicting values and canonical owner instead of normalizing by assumption.
12. Define measurement via `ai-search-measurement`: baseline, sources, representative query set, dates, geography/language, impressions/clicks/conversions where available, answer-engine observations, referral evidence where available, and confounders.
13. Prioritize work by expected user/business value, evidence strength, dependency, implementation effort, reversibility, and validation cost.
14. Produce release-ready evidence that distinguishes verified facts, observed behavior, hypotheses, limitations, and explicit non-guarantees.

## Outputs
- Entity/source-of-truth map.
- Question-to-answer/evidence map.
- Technical, crawlability, and information-architecture findings.
- Dated crawler-access matrix when named AI crawlers are in scope.
- Machine-discovery surface findings covering reachability, purpose, freshness, and leakage risk when applicable.
- External-authority gap assessment.
- Prioritized GEO backlog with owner, evidence, effort, dependency, and validation method.
- Measurement plan, observation protocol, attribution limits, and non-guarantee statement.

## Dependencies
- `entity-authority-mapping` for canonical entity and claim ownership.
- `ai-search-measurement` for baseline and outcome interpretation.
- `seo-technical-audit` for crawlability, indexation, canonicalization, rendering, and technical SEO.
- `structured-data-validation` for schema truth and eligibility checks.
- `content-discoverability-review` for independent human/content discoverability assessment.
- `secret-environment-audit` when public discovery surfaces could expose credentials, private endpoints, personal data, or privileged configuration.
- Current official platform documentation when externally visible claims depend on platform-specific behavior.

## Limitations
- GEO cannot guarantee AI citations, rankings, traffic, leads, or conversion.
- A single model response, signed-in session, locale, query wording, or point-in-time observation is not durable market evidence.
- Schema, `llms.txt`, generated pages, special markup, or model-specific tactics do not create authority when underlying claims are weak or unsupported.
- Support for machine-readable discovery conventions varies by consumer and can change; existence of a file or endpoint is not evidence that a named answer system uses it.
- Different crawlers can serve different purposes, including search/retrieval and model training; one allow/block decision must not be generalized to every AI crawler.
- External authority depends partly on third parties and cannot be manufactured or fully controlled.
- Platform behavior is time-sensitive and may change independently of site changes.

## Validation
- Confirm every material entity/claim has a canonical owner and inspectable evidence source.
- Verify answer-ready content is rendered, accessible, internally discoverable, and useful without AI-only behavior.
- Run technical SEO and structured-data validation where affected.
- For named crawler changes, verify actual production or production-equivalent HTTP access and inspect robots, CDN/WAF, bot mitigation, authentication, challenge, geo, and rate-limit boundaries that can alter reachability.
- For public machine-discovery surfaces, verify purpose, current content, public-data boundaries, and absence of secret/PII/internal leakage.
- Check page content, metadata, schema, feeds, locale variants, public profiles, and discovery surfaces for contradictory facts.
- Record a dated measurement baseline and reproducible query/observation protocol before claiming improvement.
- Route material work through `generative-engine-optimization-review`; block approval on fabricated authority, unsupported claims, missing evidence, crawler-access assumptions, public-data leakage, or causal overclaiming.
