# AI Feature Delivery Workflow

## Trigger

A feature relies on generative AI, retrieval, model inference, or tool-using
agents.

## Sequence

1. Define intended and prohibited use.
2. Classify data and risk.
3. Design model, context, retrieval, and tool boundaries.
4. Define evaluation scenarios and thresholds.
5. Implement guarded behavior and fallbacks.
6. Run security and privacy reviews.
7. Run model and prompt evaluations.
8. Validate cost, latency, and observability.
9. Release gradually.
10. Monitor quality and failures.

## Blocking conditions

- No evaluation plan
- Uncontrolled sensitive data exposure
- Unsafe tool permissions
- No fallback for critical flow
- Undefined user escalation
