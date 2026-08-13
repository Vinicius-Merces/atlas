---
name: conversion-funnel-review
description: "Review conversion funnels when acquisition, landing pages, forms, onboarding, checkout, lead handoff, or activation paths change, connecting user friction and measurement to business outcomes without dark patterns."
---

# Conversion Funnel Review

## Purpose

Review a product or acquisition funnel as a sequence of user decisions and system states, identifying evidence-backed friction, measurement gaps, and recovery failures without optimizing conversion at the expense of user autonomy or trust.

## Trigger conditions

Use when landing pages, lead forms, signup/onboarding, activation, checkout, upgrade, contact/handoff, campaign flows, or meaningful funnel instrumentation changes.

## Inputs

- Funnel objective and target audience
- Entry sources and intended conversion/activation definition
- Current screens/forms/states and handoff behavior
- Analytics/event taxonomy and available funnel data
- Error, abandonment, support, CRM, or qualitative evidence when available
- Privacy/consent and product constraints

## Procedure

1. Define the funnel start, meaningful intermediate commitments, successful conversion, downstream quality signal, and false/low-quality conversions.
2. Map each step, field, choice, redirect, wait state, validation rule, authentication/payment dependency, and human handoff.
3. Separate observed friction from assumption. Use analytics, recordings/research, support evidence, browser validation, or experiments when available.
4. Review information scent, value proposition clarity, trust signals, expectation setting, form effort, mobile behavior, error recovery, and progressive disclosure.
5. Check whether required fields are necessary at that point and whether validation errors preserve user input and explain recovery.
6. Review authentication/payment/provider transitions for abandonment caused by technical failures rather than product intent.
7. Trace conversion into downstream CRM/entitlement/activation state so a UI success signal is not counted when the business outcome failed.
8. Validate analytics coverage with `analytics-implementation-audit`; define numerator/denominator and step boundaries before interpreting rates.
9. Segment only where sample size and business meaning support it; avoid storytelling from tiny slices or post-hoc correlations.
10. Identify opportunities for experiment design when evidence is uncertain rather than declaring speculative UI changes as proven lifts.
11. Reject dark patterns, hidden costs, obstructive cancellation, deceptive urgency, forced consent, or manipulative defaults even if they could raise short-term conversion.
12. Record expected tradeoffs among conversion, lead quality, support load, fraud/abuse, retention, trust, and accessibility.

## Outputs

- Funnel/state map
- Evidence-backed friction findings
- Measurement and handoff gaps
- Experiment opportunities
- Trust/accessibility risks
- Prioritized recommendations and residual uncertainty

## Dependencies

- `analytics-implementation-audit` when event evidence is material
- `browser-flow-validation` for critical rendered journeys
- `experiment-design` for uncertain causal changes
- privacy/accessibility reviews when consent or user-access barriers are material

## Limitations

- Correlation and funnel drop-off do not prove why users abandon.
- A higher conversion rate can reduce lead/customer quality or increase downstream cost.
- Does not justify manipulative UX or unsupported percentage-uplift claims.

## Validation

- Reproduce the critical funnel in a browser across representative device classes.
- Verify analytics events and downstream success state for at least the primary conversion path.
- Confirm errors, provider failures, validation, and abandonment-recovery paths preserve honest user state.
- Distinguish measured findings from experiment hypotheses in the final review.
