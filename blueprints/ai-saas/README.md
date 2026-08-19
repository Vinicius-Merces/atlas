# AI SaaS Blueprint

## Best for

AI-assisted SaaS products with generation, chat, retrieval, workflow automation or model-backed features.

## Default capability path

`saas-from-brief-delivery` plus `ai-system-design`, provider resilience, rate/resource controls, background jobs, observability, cost controls, audit/admin operations and AI-specific evaluation as applicable.

Use `framework/llm-provider-routing-model.md` whenever provider/model choice is material. For demos, prototypes, or low-volume features where minimizing initial inference spend is a goal, compose with `framework/free-ai-pool-model.md` and the starter under `templates/ai-gateway/`.

## Demo-first provider posture

A demo may begin in `AI_MODE=free_pool` when:

- credentials remain server-side;
- each enabled provider has a verified current free/owned-compute eligibility status;
- the selected model is evaluated for the logical capability profile;
- fallback is bounded and replay-safe;
- paid fallback is disabled unless explicitly authorized;
- the UI handles rate-limit/provider-unavailable states honestly.

For Square Cloud deployments, keep the website/API on Square and call external inference APIs or an authenticated remote Ollama service. Do not attempt to run heavy local LLM inference inside Square Cloud managed containers.

## Non-negotiable gates

Explicit model/data boundaries, spend and abuse limits, deterministic business-state authority outside model output, premium streaming/error UX, security/privacy and failure degradation.

Free inference does not weaken those gates. A free route is an economic/deployment choice, not a lower assurance class for authorization, privacy, validation, or user-facing failure behavior.
