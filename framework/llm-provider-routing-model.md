# LLM Provider Routing Model

## Purpose

ATLAS treats model providers as replaceable runtime dependencies rather than embedding one vendor directly into product logic.

The routing layer selects a model only after the task's capability, data, reliability, latency, and cost requirements are known. Provider choice is an architecture decision, not a prompt-level convenience.

## Core principle

**Route by capability and policy, fail safely, and keep provider-specific behavior behind an adapter boundary.**

A system must not assume that two providers exposing similar HTTP shapes have identical model capabilities, tool semantics, structured-output behavior, context limits, streaming behavior, or failure modes.

## Provider contract

Every configured provider should expose or document the following fields when relevant:

- provider identifier
- provider type: hosted, self-hosted, local, or managed private endpoint
- base URL or SDK boundary
- authentication method
- model identifier
- supported capabilities: chat, text generation, embeddings, vision, audio, tools, structured outputs, streaming, reasoning controls
- context and output limits
- timeout budget
- latency class
- cost class or compute ownership
- data/privacy classification and retention constraints
- region or residency constraints when material
- concurrency and rate-limit expectations
- health-check method
- retry-safe failure classes
- fallback eligibility
- evaluation status for the intended task

Unknown capability is treated as unsupported until verified.

## Routing order

Use the following order when selecting a provider/model:

1. **Required capability**: exclude models that cannot perform the required operation reliably.
2. **Data policy**: exclude providers that violate privacy, residency, retention, or contractual requirements.
3. **Quality evidence**: prefer models that pass the task-specific evaluation threshold.
4. **Reliability**: consider health, rate limits, concurrency, timeout behavior, and operational maturity.
5. **Latency**: choose within the user-journey or background-job budget.
6. **Cost/compute**: optimize only after capability, policy, and minimum quality are satisfied.
7. **Fallback compatibility**: verify that an alternate provider can preserve required semantics before declaring it a fallback.

Do not route solely by model popularity, benchmark headlines, parameter count, or nominal token price.

## Provider classes

### Hosted provider

A third party operates inference and exposes an API or SDK.

Validate authentication, data handling, quotas, provider outages, version drift, and billing controls.

### Self-hosted or local provider

The project or operator owns the inference runtime or compute environment.

Validate CPU/GPU/RAM/storage requirements, model load time, concurrency, queueing, context limits, model lifecycle, health checks, and capacity under representative traffic. A model with no per-token API charge still has infrastructure and operational cost.

### Ollama profile

Ollama is a supported example of a self-hosted/local provider profile.

When an application uses Ollama through an OpenAI-compatible endpoint, treat that compatibility as partial and capability-scoped. Verify each endpoint and behavior required by the application instead of assuming full OpenAI API parity.

Recommended configuration boundary:

```text
LLM_PROVIDER=ollama
LLM_BASE_URL=http://<ollama-host>:11434/v1
LLM_MODEL=<validated-model>
LLM_TIMEOUT_MS=<budget>
LLM_FALLBACK_PROVIDER=<optional-provider>
```

Secrets, authentication headers, private hostnames, and production endpoints remain environment-owned and must not be committed to ATLAS memory or source templates.

A product hosted on one platform may call an Ollama runtime hosted elsewhere. Co-location is not required and must not be assumed.

## Capability profiles

Define reusable capability profiles instead of scattering model names through application code. Examples:

- `classification-low-cost`
- `structured-extraction`
- `support-summary`
- `rag-answer`
- `vision-analysis`
- `tool-using-agent`
- `high-reasoning`

Each profile should declare minimum quality, required features, maximum latency, privacy class, and fallback rules. Environment configuration maps the profile to concrete provider/model identifiers.

## Fallback rules

Fallback is allowed only when it preserves the task's safety and product semantics.

A fallback policy should define:

- which failures trigger fallback
- maximum attempts and total timeout
- whether the request is safe to replay
- which provider/model is next
- whether degraded quality is acceptable
- whether the user must be informed
- whether the operation should fail closed instead

Do not replay an LLM/tool operation that may already have caused an external side effect unless the operation is explicitly idempotent or deduplicated.

Use circuit-breaking or provider quarantine when repeated failures would otherwise amplify load and latency.

## Structured outputs and tools

For structured outputs:

- validate the returned object against a schema
- distinguish malformed output from provider transport failure
- retry only inside a bounded budget
- never treat model-generated identifiers, permissions, prices, or authorization decisions as trusted without authoritative validation

For tool use:

- keep tool authorization outside the model
- validate arguments server-side
- separate proposal from execution for consequential actions when appropriate
- record correlation between model request, tool call, result, and final response

## Evaluation gate

A provider/model is not production-approved for a capability profile until it has been evaluated on representative scenarios.

Record at minimum:

- evaluation date
- model and provider version/identifier
- prompt/retrieval/tool configuration
- representative success and failure cases
- quality threshold
- latency distribution or representative measurements
- cost/compute observations
- known capability gaps

Re-evaluate after material model, prompt, retrieval, tool, or provider changes.

## Observability

Record provider-neutral telemetry where practical:

- logical capability profile
- concrete provider and model
- request correlation identifier
- latency
- retry/fallback count
- input/output size or token-equivalent metrics where available and policy-safe
- error class
- structured-output validation failures
- tool-call failures
- estimated API cost or owned-compute class when available

Do not emit raw prompts, secrets, personal data, or model outputs into telemetry by default.

## Failure policy

The router must distinguish at least:

- invalid configuration
- provider unavailable
- authentication failure
- rate limit or capacity exhaustion
- timeout
- unsupported capability
- malformed/invalid structured output
- safety/policy rejection
- context limit exceeded
- evaluation not approved

Unknown or ambiguous failures must not silently downgrade into a lower-trust provider.

## ATLAS integration

- `framework/ai-engineering-model.md` defines the broader AI lifecycle.
- `prompt-model-evaluation` supplies comparative quality evidence.
- `external-api-resilience-review` applies to hosted providers.
- `observability-design` defines runtime signals.
- `privacy-impact-assessment` and security review apply when data leaves the project boundary.
- `automation-model` applies when LLM calls participate in background jobs or tool-driven workflows.
