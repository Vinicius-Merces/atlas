---
name: ai-search-measurement
description: "Establish and interpret AI-search/GEO measurement using reproducible query sets, Search Console/analytics evidence, attribution limits, and explicit confounders."
---

# AI Search Measurement

## Purpose
Provide a reproducible measurement protocol for GEO and AI-search work so teams can distinguish observed discovery changes from unsupported causal claims, while combining answer-engine observations with normal organic, conversion, indexation, and analytics evidence.

## Trigger conditions
Activate before establishing a GEO baseline, comparing pre/post AI-search visibility, reporting answer-engine citations or links, evaluating an AI-search experiment, or making a claim that GEO work improved discovery, traffic, leads, or conversion.

## Inputs
Required:
- business/discovery outcomes and target conversion events;
- target audience, language, geography, and decision stages;
- available Search Console, analytics, indexation, and conversion evidence;
- release dates and material site/content/schema changes that may affect the comparison.

Optional:
- historical query sets, answer-engine observations, platform-provided AI reporting, campaign calendars, seasonality notes, instrumentation change logs, and competitor/reference observations.

## Procedure
1. Define conversion and discovery outcomes before choosing metrics.
2. Capture a dated baseline for organic traffic, qualified conversions, indexed URLs, branded/non-branded queries, and relevant engagement.
3. Build a representative query set by audience, intent, language, geography, and decision stage; document how each query was selected or observed.
4. Record answer-engine observations separately from analytics: engine/version where observable, signed-in state, locale, timestamp, prompt/query, citations/links, and known volatility.
5. Use Search Console or platform-provided AI reporting when available; do not assume a platform exposes complete AI-search attribution.
6. Compare cohorts over a meaningful period and annotate releases, campaigns, seasonality, index changes, content freshness, query-set changes, and instrumentation changes.
7. Separate leading indicators from business outcomes. Citation frequency or model mentions are not substitutes for qualified traffic, useful engagement, or conversion.
8. Report observed changes, confidence, data gaps, and plausible alternatives rather than stating “GEO caused X” without defensible evidence.
9. Preserve the baseline, query set, observation conditions, and analysis date so another reviewer can reproduce the comparison.

## Output
- Dated baseline and comparison window.
- Reproducible query set and answer-engine observation log.
- Analytics/Search Console metric specification and dashboard/event requirements.
- Release/confounder annotation log.
- Reporting cadence, confidence statement, attribution limits, and unresolved data gaps.

## Dependencies
- Correct analytics and conversion instrumentation for any business-outcome claim.
- Search Console or equivalent organic-search evidence when available.
- `generative-engine-optimization` for the broader GEO strategy and interpretation context.
- `entity-authority-mapping` when measured queries depend on canonical entities or factual claims.
- Current platform documentation when a metric or reporting surface is provider-specific.

## Limitations
- AI answer systems are volatile, personalized, localized, and may not expose stable rankings or complete referral attribution.
- A one-time answer, citation, signed-in session, or small prompt sample cannot establish durable visibility.
- Search Console, analytics, referral data, and provider reports may undercount or classify AI-search traffic inconsistently.
- Correlation after a GEO release does not establish causation when algorithm changes, campaigns, seasonality, indexing, brand demand, or instrumentation also changed.
- This skill does not authorize prohibited scraping, bypass platform controls, or collect personal data to improve measurement coverage.

## Validation
- Baseline and comparison windows are dated and use the same metric definitions where possible.
- Query sets document audience, intent, language, geography, and selection method.
- Answer-engine observations record enough conditions to be reproducible and are kept separate from analytics facts.
- Release, campaign, seasonality, indexation, and instrumentation confounders are annotated.
- Reports distinguish observation, inference, confidence, and unresolved alternatives.
- No causal performance claim is approved without evidence strong enough to support it.
