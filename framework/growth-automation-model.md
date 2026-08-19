# Growth Automation Model

## Purpose

ATLAS treats growth automation as an end-to-end product and data workflow, not a collection of disconnected marketing scripts.

The model connects acquisition, conversion, qualification, CRM state, follow-up, nurture, reactivation, attribution, experimentation, and human handoff while preserving consent, trust, deliverability, and operational reliability.

## Core principle

**Automate the next useful action from trusted state, measure downstream quality, and never optimize a local conversion metric by degrading user trust or lead/customer quality.**

## Lifecycle map

```text
Acquisition source
    ↓
Landing/content experience
    ↓
Intent/conversion event
    ↓
Identity + consent state
    ↓
Qualification/enrichment
    ↓
CRM/customer state
    ↓
Routing/ownership
    ↓
Follow-up / nurture / activation
    ↓
Outcome
    ↓
Retention / reactivation / referral
    ↓
Attribution + experiment learning
```

A project may use only a subset. The lifecycle should still make state transitions explicit so leads or customers do not disappear between tools.

## Source-of-truth contract

Define authoritative ownership for:

- person/account identity
- consent and communication preferences
- acquisition source/campaign metadata
- qualification state
- lifecycle stage
- assigned owner/team
- last meaningful interaction
- current next action
- conversion/customer outcome
- suppression/unsubscribe status

Do not allow each automation tool to become an independent CRM.

## Event contract

Lifecycle automation should be driven by stable events/state changes where possible.

Each event should define:

- event name and version
- actor/entity identifiers
- timestamp/source
- consent/privacy context when communication may follow
- deduplication/idempotency key
- required properties
- downstream consumers
- retention policy

Use `event-taxonomy-design` and analytics review for measurement events. Operational workflow events may need stronger delivery/idempotency guarantees than analytics events.

## Lead/customer routing

Routing logic should be explicit and testable.

Examples:

- region
- service/product interest
- account type
- qualification threshold
- workload/round-robin ownership
- existing relationship/owner
- language/timezone
- urgency or SLA

Random or round-robin assignment must still preserve deterministic evidence of who owns the record after the decision.

## Follow-up automation

Define:

- trigger
- delay/window
- eligible lifecycle states
- channel
- template/content ownership
- personalization source
- suppression conditions
- frequency limits
- retry/failure behavior
- human handoff rule
- success/stop condition

Never continue automated outreach after unsubscribe/opt-out or another authoritative suppression state.

## AI in growth automation

AI can assist with bounded tasks such as:

- lead/message classification
- structured extraction
- summarization
- suggested segmentation
- draft personalization
- next-action recommendation
- FAQ/RAG responses
- sales/support handoff summaries

Use `framework/llm-provider-routing-model.md` to choose hosted or self-hosted/local models by capability, privacy, latency, and cost.

AI must not become the source of truth for consent, identity, pricing, contractual claims, inventory, permissions, or CRM ownership.

For outbound messages, material offers, legal/regulated claims, or high-value accounts, define whether human approval is required before a model-generated draft is sent.

## Automation reliability

Apply `framework/automation-model.md`.

Growth automation should define:

- idempotency/deduplication
- queue/retry/backoff behavior
- failed-work visibility
- provider/channel failure behavior
- rate/frequency limits
- reconciliation when CRM and delivery provider disagree
- audit/correlation identifiers

A successful UI form submission is not a successful lead workflow until the downstream authoritative state is committed.

## Measurement model

Measure the complete funnel, not only click or form-submit rate.

Possible stages:

- qualified traffic
- meaningful CTA engagement
- valid conversion
- reachable/consented lead
- qualified lead
- accepted/routed lead
- first response
- meeting/activation
- opportunity/order/customer
- retained/reactivated outcome

Track false/low-quality conversions and downstream cost where material.

## Attribution discipline

Preserve original and recent source metadata according to the project's attribution model.

Do not silently overwrite acquisition provenance during later sessions or CRM imports.

Treat attribution as an analytical model with limitations, not ground truth about causality.

## Experimentation

Use `experiment-design` when changing messaging, offers, forms, routing, timing, or lifecycle logic and causal confidence matters.

Define guardrail metrics for:

- lead/customer quality
- unsubscribe/complaint rate
- support load
- fraud/abuse
- downstream conversion/retention
- accessibility/trust

A higher top-of-funnel conversion rate can be a regression when downstream quality collapses.

## Privacy and trust

- Collect only data needed for a defined purpose.
- Respect consent, suppression, unsubscribe, and deletion requirements.
- Do not infer sensitive traits for marketing unless clearly lawful, necessary, and approved by project governance.
- Do not fabricate urgency, scarcity, testimonials, personalization facts, or social proof.
- Keep model-generated claims grounded in authoritative business data.

## Outputs

A growth automation design should be able to report:

- lifecycle/state map
- source-of-truth ownership
- event/trigger map
- routing rules
- follow-up/nurture rules
- consent/suppression controls
- AI-assisted steps and approval boundaries
- automation reliability contract
- funnel and downstream-quality metrics
- attribution approach
- experiment opportunities
- operational owners and failure paths

## ATLAS integration

- `conversion-funnel-review` finds friction and handoff gaps.
- `event-taxonomy-design` and `analytics-implementation-audit` protect measurement quality.
- `framework/automation-model.md` protects workflow reliability.
- `framework/llm-provider-routing-model.md` governs AI provider/model routing.
- `experiment-design` governs causal tests.
- privacy/security review governs sensitive data and communication risk.
