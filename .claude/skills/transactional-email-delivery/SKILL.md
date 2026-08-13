---
name: transactional-email-delivery
description: "Design transactional email delivery for verification, recovery, invitations, receipts, alerts, and workflow messages, covering authoritative triggers, template data, provider handoff, idempotency, retries, suppression, security, observability, and delivery-state reconciliation."
---

# Transactional Email Delivery

## Purpose

Make transactional email a reliable consequence of authoritative product state rather than an untracked side effect.

## Trigger conditions

Use for verification, password recovery, magic links, invitations, receipts, account/security alerts, workflow notifications, or other non-marketing email tied to product events.

## Inputs

- Authoritative trigger and recipient rules
- Template/content variables and localization
- Provider contract and environment configuration
- Security sensitivity and link/token requirements
- Retry, suppression, bounce, and observability requirements

## Procedure

1. Define the authoritative event that permits sending and prevent client-only state from becoming the trigger.
2. Classify message sensitivity and ensure tokens/links are scoped, expiring, single-use where required, and do not leak secrets in templates or logs.
3. Define stable message identity so retries do not create uncontrolled duplicates.
4. Separate enqueue/acceptance from provider delivery and from actual recipient delivery/read semantics.
5. Validate template variables, escaping, localization, plain-text alternative, accessible structure, and brand consistency.
6. Handle provider timeout, 429/5xx, bounce, complaint, suppression, invalid recipient, and provider outage explicitly.
7. Record correlation identifiers, template/version, provider message id, and delivery state without logging sensitive token values.
8. Define sandbox/test-recipient controls so non-production environments cannot message real customers accidentally.
9. Reconcile security-critical or financially important messages when provider/application state can diverge.

## Outputs

- Trigger and message-state model
- Template data contract
- Retry/idempotency/suppression behavior
- Security and environment controls
- Delivery observability and reconciliation plan

## Dependencies

- `external-api-resilience-review` for provider behavior
- `secret-environment-audit` for API keys/signing material
- `background-job-reliability` when delivery is queued
- `authentication-flow-review` for identity/recovery messages

## Limitations

Email acceptance does not prove inbox placement or user reading. Marketing consent/campaign systems require additional privacy and compliance review.

## Validation

- Exercise success, duplicate trigger, provider timeout, provider rejection, bounce/suppression, and retry paths.
- Verify non-production recipient protection.
- Inspect actual rendered HTML/plain-text output and links.
- Confirm logs and analytics do not expose recovery or verification secrets.
