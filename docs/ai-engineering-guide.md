# AI Engineering Guide

## Begin with the use case

Do not begin with a model. Begin with the user need, decision boundary, risk, required capability, and success criteria.

Use `framework/ai-engineering-model.md` for the lifecycle and `framework/llm-provider-routing-model.md` when provider/model portability, Ollama/self-hosted inference, or fallback matters.

## Define a capability profile before a provider

Describe what the workflow needs before choosing a vendor/model.

Useful constraints include:

- operation: chat, extraction, classification, embeddings, vision, tool use, structured output, reasoning;
- minimum quality threshold;
- maximum latency/timeout;
- privacy/data-boundary requirements;
- context/output size;
- concurrency/capacity;
- cost or owned-compute budget;
- fallback/degraded-mode behavior.

Map that logical capability to a concrete provider/model through configuration when portability is valuable.

## Hosted and self-hosted models

ATLAS supports both provider classes as architecture choices.

Hosted APIs trade infrastructure ownership for provider dependency, quotas, data-boundary review, and usage cost.

Self-hosted/local inference trades per-request provider billing for owned compute, memory/storage, capacity planning, model lifecycle, and operational responsibility.

A project hosted on one platform can call an inference runtime hosted on another platform or private machine/VPS. Co-location is not assumed.

## Ollama

Ollama is a supported example profile for local/self-hosted inference.

Where a project uses its OpenAI-compatible interface, keep the base URL/model configurable and verify the exact API features the application needs. Compatibility is capability-scoped and should not be treated as universal API parity.

Example configuration boundary:

```text
LLM_PROVIDER=ollama
LLM_BASE_URL=http://<ollama-host>:11434/v1
LLM_MODEL=<validated-model>
LLM_TIMEOUT_MS=<budget>
LLM_FALLBACK_PROVIDER=<optional>
```

Do not commit real production endpoints, credentials, private network details, or secrets to shared templates or memory.

## Evaluate representative failures

Evaluation should include ambiguous requests, missing context, adversarial inputs, unsupported tasks, context-limit behavior, malformed structured outputs, provider/model differences, tool failures, and sensitive-data scenarios.

Re-run evaluation after material provider/model, prompt, retrieval, tool, or structured-output changes.

## Limit permissions

AI systems should receive the minimum data, tools, and write permissions needed for the task.

The model never becomes the authorization layer. Validate tool arguments, identities, tenant/resource ownership, prices, permissions, and business invariants using authoritative application state.

## Design fallback behavior

Critical workflows should define what happens when the model/provider is unavailable, rate-limited, uncertain, too slow, too expensive, capacity-constrained, or produces invalid output.

Fallback must preserve required capabilities and policy. Do not blindly replay a tool-driven side effect during model/provider failover when execution status is unknown.

## AI automation

When inference participates in scheduled jobs, queues, lifecycle workflows, lead qualification, content processing, or tool-driven operations, apply `framework/automation-model.md`.

Define:

- idempotency/deduplication;
- bounded timeout/retry/backoff;
- concurrency;
- failed-work/dead-letter behavior;
- validated structured output;
- fallback;
- human approval boundary when consequences are material;
- correlation and recovery evidence.

## Monitor quality and operations

Track appropriate provider-neutral signals such as:

- logical capability profile;
- provider/model;
- latency;
- retry/fallback count;
- structured-output failure rate;
- tool errors;
- human overrides/escalation;
- quality regressions;
- API cost or owned-compute class.

Do not log raw prompts, private retrieved context, secrets, personal data, or model outputs by default.

## Related models

- `framework/llm-provider-routing-model.md`
- `framework/automation-model.md`
- `framework/observability-model.md`
- `framework/testing-model.md`
- `framework/quality-gates-model.md`
