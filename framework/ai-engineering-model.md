# AI Engineering Model

AI-enabled features require additional controls beyond conventional software.

## Core concerns

- Model capability and limitations
- Provider and model routing
- Prompt and context construction
- Retrieval quality
- Tool permissions
- Data privacy
- Hallucination and uncertainty
- Evaluation design
- Cost, owned compute, and latency
- Provider/runtime availability
- Abuse resistance
- Human oversight

## AI delivery lifecycle

```text
Use case definition
    ↓
Risk and data classification
    ↓
Capability profile and provider constraints
    ↓
Architecture, provider and model selection
    ↓
Prompt, retrieval and tool design
    ↓
Evaluation
    ↓
Safety and privacy review
    ↓
Controlled release
    ↓
Monitoring, fallback validation and iteration
```

## Provider-neutral architecture

AI product logic should depend on a capability contract rather than a hard-coded vendor whenever replacement or fallback is a realistic requirement.

Use `framework/llm-provider-routing-model.md` when a system:

- can use more than one hosted model provider;
- mixes hosted and self-hosted/local inference;
- uses Ollama or another local/private runtime;
- requires cost-, privacy-, region-, capability-, or latency-aware routing;
- needs model fallback or provider failover;
- exposes tools or structured outputs whose semantics can differ by provider.

Provider compatibility claims must be verified at the exact endpoint/capability used. Similar API shapes do not imply full behavioral parity.

## Model selection rules

Select a concrete provider/model only after defining:

- required capabilities;
- minimum task-specific quality;
- data/privacy constraints;
- latency budget;
- cost or owned-compute constraints;
- concurrency/capacity expectations;
- fallback behavior;
- evaluation evidence.

A cheaper or local model is useful only when it meets the task's required quality and operational envelope.

## Tool-use boundary

The model proposes or requests tool actions; authoritative application code owns permission, validation, idempotency, and execution.

Consequential actions should support human approval or another explicit control when the product/risk model requires it.

A fallback or retry must not replay a side effect unless the operation is idempotent, deduplicated, or known not to have executed.

## Required evidence

An AI feature should define:

- Intended use
- Out-of-scope use
- Capability profile
- Provider/model configuration boundary
- Evaluation dataset or scenarios
- Quality metrics and threshold
- Failure examples
- Safety controls
- Cost/API budget or owned-compute assumptions
- Latency and timeout budgets
- Fallback/degraded-mode policy
- Data/privacy classification
- Human escalation path
- Observability signals without unsafe prompt/output logging

## Re-evaluation triggers

Re-run the relevant evaluation when materially changing:

- model or provider
- prompt/system instructions
- retrieval/indexing strategy
- tool set or tool permissions
- structured-output schema
- context-window strategy
- fallback chain
- safety policy

A model upgrade is a behavior change even when the application API does not change.

## Related ATLAS models

- `framework/llm-provider-routing-model.md` for provider abstraction, capability profiles, Ollama/self-hosted runtimes, and fallback.
- `framework/automation-model.md` for AI calls inside queues, scheduled jobs, and tool-driven workflows.
- `framework/observability-model.md` for correlated runtime evidence.
- `framework/testing-model.md` and `prompt-model-evaluation` for repeatable confidence.
