# Free AI Pool Model

## Purpose

The ATLAS Free AI Pool is a provider-neutral routing pattern for demos, prototypes, learning projects, and low-volume AI features that should begin with little or no inference spend while retaining a clean migration path to paid capacity.

It extends `framework/llm-provider-routing-model.md`. The pool is not a promise that any third-party free tier will remain free, available, or production-grade. Free eligibility is runtime discovery metadata that must be rechecked against the provider's current terms, limits, data policy, and model catalog.

## Core principle

**Keep product code stable while inference providers remain replaceable. Route by capability and policy first, then by free capacity.**

The application calls one server-side AI gateway. The gateway owns provider selection, credentials, capability checks, fallback, rate/cost boundaries, observability, and migration to paid capacity.

```text
product / client
      |
      v
server-side AI gateway
      |
      v
capability + privacy + budget policy
      |
      +--> free/low-cost hosted provider
      +--> remote Ollama
      +--> local/self-hosted Ollama
      +--> paid provider when explicitly allowed
```

The browser must not receive provider API keys or call privileged provider endpoints directly.

## Operating modes

Projects should expose an environment-owned mode rather than hard-code a provider throughout business logic.

### `free_pool`

Use eligible zero-financial-cost or project-approved free-tier routes first. Appropriate for demos and low-volume non-sensitive features.

### `provider`

Pin a specific validated provider/model for deterministic testing, client commitments, debugging, or production control.

### `local_only`

Allow only local/self-hosted or approved private endpoints. Use when data policy prohibits third-party inference.

### `paid_allowed`

Use the normal provider router and permit paid routes inside an explicit budget. This is the normal graduation path when a demo scales.

Recommended boundary:

```text
AI_ENABLED=true
AI_MODE=free_pool
AI_DEFAULT_PROFILE=support-summary
AI_MAX_ATTEMPTS=3
AI_TOTAL_TIMEOUT_MS=20000
AI_ALLOW_PAID_FALLBACK=false
```

Secrets and concrete production endpoints remain environment-owned.

## Candidate provider classes

The pool may include any provider that passes the current capability and policy checks. Common candidates include:

### Ollama local or self-hosted

Use a local machine, workstation, private server, VPS, or GPU host running Ollama. There is no per-token API bill, but the operator owns compute, electricity, capacity, patching, network exposure, and uptime.

Do not expose the unauthenticated local Ollama API directly to the public internet. Put authentication, TLS, rate limiting, request limits, and observability in front of it.

### Ollama Cloud

Ollama cloud models can be reached through the Ollama ecosystem and direct authenticated cloud API. Treat free-plan availability, cloud model access, limits, and model identifiers as discoverable external state rather than permanent ATLAS defaults.

### Groq

Groq exposes OpenAI-compatible interfaces for supported operations and maintains free-plan rate limits for experimentation. Model availability and limits vary, so the pool must read configuration rather than embed a permanent model list.

### Cloudflare Workers AI

Workers AI can provide serverless inference and OpenAI-compatible text/embedding endpoints for supported models. The free allocation and model billing rules are external state. A Cloudflare Worker or server-side application may act as the gateway boundary.

### OpenRouter free routes

`openrouter/free` and model `:free` variants are useful for experiments and low-volume demos. Free model availability can change and routing may select different models, so do not use an uncontrolled free route when a product requires deterministic model identity or validated model-specific behavior.

### GitHub Models

Free API/playground capacity is useful for prototyping and evaluation. Treat free limits as development capacity rather than a production SLA.

### Gemini free tier

May be used when the current free tier, data policy, and required modalities fit the project. Review provider data-use terms before sending client or sensitive data.

## Provider record

Each route in the pool should declare at least:

```yaml
id: groq-demo
adapter: openai-compatible
class: hosted
financial_class: free-tier
priority: 20
enabled: true
base_url_env: GROQ_BASE_URL
api_key_env: GROQ_API_KEY
model_env: GROQ_MODEL
capabilities:
  - chat
  - structured-output
privacy:
  max_data_class: public
fallback:
  eligible: true
health:
  cooldown_seconds: 30
```

Do not store the API key itself in the provider record.

## Capability profiles

Route logical tasks rather than raw prompts. A project can start with profiles such as:

- `classification-low-cost`
- `structured-extraction`
- `support-summary`
- `demo-chat`
- `rag-answer`
- `vision-analysis`
- `tool-using-agent`
- `high-reasoning`

Each profile declares required capabilities, maximum accepted data classification, latency budget, quality threshold, replay safety, and whether paid fallback is allowed.

Example:

```yaml
profiles:
  support-summary:
    requires: [chat]
    data_class: internal
    latency_ms: 8000
    paid_fallback: false
    replay_safe: true
```

A provider that has not been evaluated for the profile is not silently considered compatible merely because it accepts the same HTTP request shape.

## Free-pool routing algorithm

For each request:

1. resolve the logical capability profile;
2. reject routes missing required capabilities;
3. reject routes that violate the request's privacy/data class;
4. apply `AI_MODE` and paid-fallback policy;
5. exclude providers in cooldown/quarantine or known quota exhaustion;
6. rank remaining routes by configured priority, evaluation status, reliability, latency class, and available free capacity;
7. make one bounded attempt;
8. classify the failure;
9. fall back only for retry-safe failure classes and replay-safe requests;
10. stop when the total timeout/attempt budget is exhausted;
11. return a normalized response with provider/model metadata available to server-side telemetry.

Do not retry/fallback across an action that may already have executed a consequential external tool unless the action is idempotent or reconciled first.

## Failure classes

A minimum implementation should distinguish:

- `invalid_configuration`
- `authentication_failure`
- `permission_failure`
- `rate_limited`
- `capacity_exhausted`
- `timeout`
- `provider_unavailable`
- `unsupported_capability`
- `invalid_structured_output`
- `context_limit`
- `policy_rejection`
- `evaluation_not_approved`

Authentication, permission, privacy, schema, and policy failures should normally fail closed rather than trigger blind provider hopping.

## Free-tier exhaustion

Free-tier limits are expected behavior, not exceptional architecture failures.

The gateway should:

- honor provider `Retry-After` or equivalent headers when available;
- put repeatedly rate-limited routes into bounded cooldown;
- avoid retry storms across multiple instances;
- expose quota/capacity exhaustion as a normalized reason;
- degrade gracefully for demo users;
- never enable paid fallback unless project policy explicitly allows it.

A single-process demo may keep health/cooldown state in memory. Multi-instance or production systems need shared state or provider-aware external coordination so each instance does not independently hammer an exhausted free route.

## Square Cloud profile

Square Cloud should host the application/API gateway, not local LLM inference. Current Square Cloud policy disallows direct heavy local ML/LLM inference on the platform and recommends consuming external AI APIs.

Use this topology:

```text
browser
  |
  v
Square Cloud app/API
  |
  +--> Groq / Workers AI / OpenRouter / Ollama Cloud / other approved API
  |
  +--> authenticated remote gateway -> Ollama on external compute
```

A developer workstation or separate host can provide Ollama for demos, but the public edge must add TLS, authentication, abuse controls, and request limits. Temporary development tunnels are not production infrastructure.

## Security boundary

The AI gateway must enforce:

- server-side credentials only;
- allowed provider/model list;
- request body and output size limits;
- per-user/IP/tenant rate limits where applicable;
- timeout and concurrency limits;
- prompt/tool data classification checks;
- tool authorization outside the model;
- structured-output schema validation;
- safe logging with prompts/outputs excluded by default;
- correlation IDs;
- origin/CORS policy appropriate to the application.

Remote Ollama endpoints require explicit ingress protection. Local Ollama's lack of local API authentication must never be mistaken for a safe public API posture.

## Observability

Record provider-neutral telemetry:

- capability profile;
- selected route/provider/model;
- mode (`free_pool`, `provider`, `local_only`, `paid_allowed`);
- attempt/fallback sequence;
- latency;
- normalized failure class;
- rate-limit/capacity signal when available;
- structured-output validation outcome;
- token/usage data when safely available;
- estimated financial cost or `free-tier`/`owned-compute` class.

Do not log API keys, raw sensitive prompts, or full model outputs by default.

## Promotion from demo to production

The free pool is designed to graduate rather than be replaced.

Define promotion triggers such as:

- recurring quota exhaustion;
- unacceptable p95 latency;
- model availability churn;
- need for a stable model/SLA;
- sensitive data that requires a different provider agreement;
- concurrency beyond free capacity;
- AI quality threshold not met by free routes;
- business value that justifies a paid budget.

Promotion changes provider configuration and policy, not product business logic.

A recommended progression is:

```text
free_pool
   -> pinned free/low-cost provider
   -> paid_allowed with capped budget
   -> production provider + explicit fallback
   -> private/self-hosted inference when scale/privacy economics justify it
```

## Demo UX requirements

An AI demo must tell the truth about its operating class.

- Handle model unavailable/rate-limited states without a blank UI.
- Preserve user input when inference fails.
- Do not claim guaranteed availability from a free provider.
- Do not present model-generated classifications or recommendations as authoritative business state unless validated by the application.
- Use streaming only when the selected route supports it reliably and the UI handles interruption.
- Provide a bounded retry or alternate flow rather than an infinite spinner.

## ATLAS integration

- `framework/llm-provider-routing-model.md` owns general provider selection.
- `framework/ai-engineering-model.md` owns AI lifecycle and evaluation.
- `framework/automation-model.md` owns reliable AI-assisted workflows.
- `framework/observability-model.md` owns signals and operational evidence.
- `rate-limit-abuse-control` applies to public AI endpoints.
- `external-api-resilience-review` applies to hosted providers.
- `prompt-model-evaluation` determines whether a concrete provider/model is fit for a profile.
- `secret-environment-audit` verifies credential boundaries.
- `privacy-impact-assessment` applies before sending sensitive data to external inference.

## Admission rule

A project may describe itself as using the ATLAS Free AI Pool only when provider choice is isolated behind a server-side boundary, free/paid eligibility is explicit, fallback is bounded, credentials remain private, and at least the primary capability profile has a documented evaluation path.
