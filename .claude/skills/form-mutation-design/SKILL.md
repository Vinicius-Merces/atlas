---
name: form-mutation-design
description: "Design and review user-initiated forms and mutations when data is created, edited, deleted, submitted, or transitioned, covering validation, authorization, concurrency, duplicate submission, optimistic UI, failure recovery, and accessible feedback."
---

# Form Mutation Design

## Purpose

Design forms and state mutations as reliable product transactions rather than button-click handlers, so UI feedback, server authority, authorization, validation, concurrency, and recovery remain consistent.

## Trigger conditions

Use for create/edit/delete flows, onboarding, lead capture, checkout-adjacent forms, settings, bulk actions, approvals, state transitions, optimistic UI, or any user action that changes authoritative state.

## Inputs

- User journey and acceptance criteria
- Authoritative data model and mutation contract
- Authentication/authorization rules
- Client and server validation rules
- Concurrency, idempotency, and retry expectations
- Loading, success, error, empty, and offline/degraded states

## Procedure

1. Define the authoritative mutation, actor, resource, preconditions, invariants, and resulting state.
2. Separate client convenience validation from server-enforced validation and authorization.
3. Define field normalization, error shape, localization, sensitive-data handling, and accessible label/error association.
4. Prevent accidental duplicate effects through disabled/pending state and server-side idempotency where consequences require it.
5. Model concurrent edits using version checks, conditional writes, conflict UX, or another explicit policy instead of silent last-write-wins by accident.
6. Use optimistic UI only when rollback/reconciliation is understandable and the mutation is safe to speculate.
7. Define cache/revalidation consequences and ensure stale UI cannot masquerade as authoritative success.
8. Exercise validation, authorization denial, network ambiguity, duplicate submit, conflict, server error, and recovery paths.
9. Preserve focus, announcement, keyboard operation, and meaningful pending/success/error feedback.
10. Record irreversible actions, confirmation strategy, audit needs, and recovery/undo semantics.

## Outputs

- Mutation contract and state-transition map
- Validation and error contract
- Concurrency/idempotency decision
- UI pending/success/failure behavior
- Negative-path evidence and residual risks

## Dependencies

- `authorization-boundary-review` for protected mutations
- `database-schema-review` when mutation invariants depend on schema constraints
- `cache-strategy-assessment` when changed state is cached
- `accessibility-audit` for material user-facing forms

## Limitations

This skill does not replace domain-specific payment, authentication, or migration review. Framework-specific form APIs are implementation choices, not substitutes for the mutation contract.

## Validation

- Submit valid, invalid, unauthorized, duplicate, conflicting, and server-failure cases.
- Verify final authoritative state rather than trusting a success toast.
- Confirm keyboard/focus/error announcement behavior for material forms.
- Re-test cache invalidation or revalidation after mutation success.
