---
name: payment-integration-review
description: "Review payment and billing integrations when checkout, subscriptions, invoices, refunds, entitlements, webhooks, idempotency, or provider state synchronization change."
---

# Payment Integration Review

## Purpose

Review payment and billing flows as a distributed state machine where money movement, provider state, application entitlements, retries, webhooks, and reconciliation must remain consistent under failure.

## Trigger conditions

Use when adding or changing checkout, payment intents, subscriptions, invoices, refunds, credits, entitlements, provider webhooks, billing portals, payment retries, or financial reconciliation.

## Inputs

- Payment provider integration and API version
- Checkout/billing architecture
- Product/pricing/entitlement model
- Webhook/event contract
- Database state transitions
- Idempotency strategy
- Refund/cancel/dispute behavior
- Test/sandbox evidence

## Dependencies

- Authoritative payment-provider API, event, idempotency, and environment contracts
- Server-authoritative product, pricing, currency, discount, and entitlement rules
- `webhook-reliability-review` when provider events participate in state synchronization
- `authorization-boundary-review` for customer/admin billing actions
- `secret-environment-audit` for provider credentials, webhook secrets, and sandbox/live separation

## Procedure

1. Map the authoritative state for price, payment, subscription, invoice, refund, and entitlement decisions.
2. Ensure client-supplied amount, price, product, currency, discount, role, or entitlement values are not trusted without server-side validation against authoritative configuration.
3. Model each financial operation as an explicit state transition with success, failure, pending, retry, cancellation, and reconciliation states.
4. Use provider-supported idempotency for mutation retries and preserve a stable logical operation key across retries where the provider contract requires it.
5. Review webhook handling with `webhook-reliability-review`; provider events must be authenticated, deduplicated, retry-safe, and order-tolerant.
6. Do not grant durable entitlement solely because a browser returned from a checkout success page. Confirm authoritative provider/server state.
7. Review duplicate checkout/session creation, double-submit, network timeout, partial failure, and worker retry behavior for duplicate charges or duplicate business effects.
8. Review subscription upgrades/downgrades, proration, cancellation timing, grace periods, failed renewals, refunds, chargebacks/disputes, and reactivation against product rules.
9. Keep financial records and provider identifiers traceable enough for support and reconciliation without storing prohibited sensitive payment data.
10. Review authorization on customer portal, refund, cancellation, invoice download, admin billing, and connected-account actions.
11. Separate test/sandbox and live credentials, webhooks, products/prices, and environment state.
12. Pin or deliberately manage provider API versions when version behavior can affect state transitions.
13. Provide reconciliation for drift between provider state and application state.

## Outputs

- Payment/billing state model
- Authority and pricing findings
- Idempotency/retry findings
- Entitlement synchronization findings
- Refund/subscription/dispute findings
- Reconciliation and observability gaps
- Required mitigations and residual risk

## Limitations

- Does not provide accounting, tax, legal, or PCI compliance certification.
- Provider documentation and contractual requirements remain authoritative.
- Does not request or store raw card data when hosted/tokenized provider flows avoid it.

## Validation

- Use provider sandbox/test mode for positive and negative flows when available.
- Test double-submit, network retry, duplicate event, failed payment, cancellation, refund, and stale-return-page behavior as applicable.
- Verify entitlements reconcile from authoritative server/provider state.
- Confirm live secrets and live provider resources are not reachable from test/preview environments without explicit intent.
