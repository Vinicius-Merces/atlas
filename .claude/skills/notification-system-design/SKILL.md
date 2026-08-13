---
name: notification-system-design
description: "Design in-app, push, email, or provider notifications with trusted recipient rules, preferences, deduplication, urgency, read state, fan-out, retries, quieting, and accessible notification-center UX."
---

# Notification System Design

## Purpose

Design notifications as a coherent product subsystem that sends the right message, to the right audience, through appropriate channels, without duplicates or notification fatigue.

## Trigger conditions

Use for notification centers, in-app alerts, email/push fan-out, workflow reminders, mentions, status changes, real-time notifications, or user notification preferences.

## Inputs

- Domain events and recipient derivation
- Channel matrix and urgency
- User preferences/consent and quieting rules
- Read/unread/archive semantics
- Delivery provider and retry behavior

## Procedure

1. Define canonical notification events separately from channel-specific delivery.
2. Derive recipients on trusted server state and tenant/authorization boundaries.
3. Define deduplication identity, aggregation/coalescing, urgency, expiration, and ordering.
4. Model user preferences, mandatory security/system notices, opt-outs, quiet hours, and locale/time zone.
5. Separate notification creation, channel fan-out, provider acceptance, and read state.
6. Design in-app pagination, unread counters, mark-read semantics, deep links, empty states, and accessible announcements.
7. Use queues/fan-out with bounded retries and dead-letter/reconciliation for material scale or provider uncertainty.
8. Prevent sensitive data from leaking into lock-screen/push/email surfaces inappropriate for the channel.
9. Instrument delivery/failure without equating delivery with engagement.

## Outputs

- Event/channel/recipient matrix
- Preference and urgency policy
- Notification data/read-state model
- Delivery/retry/dedup design
- Notification-center UX and evidence

## Dependencies

- `transactional-email-delivery` when email is a channel
- `background-job-reliability` for asynchronous fan-out
- `authorization-boundary-review` for recipient and deep-link access
- `analytics-implementation-audit` when engagement metrics are used

## Limitations

This skill does not replace provider-specific push setup or legal consent analysis. Real-time transport choice should follow actual latency/scale needs.

## Validation

- Test duplicate events, recipient changes, opt-out/mandatory notices, quiet hours, failure/retry, unread counters, and deep-link authorization.
- Confirm sensitive notification content is channel-appropriate.
- Exercise keyboard/screen-reader behavior for the in-app surface when present.
