# Free AI Demo Guide

## Goal

Use AI in client demos and low-volume products without coupling the product to one provider or committing to paid inference before the feature proves value.

The canonical architecture is `framework/free-ai-pool-model.md`. Copyable starter files live under `templates/ai-gateway/`.

## Recommended default for current ATLAS projects

For a public demo:

```text
AI_MODE=free_pool
AI_ALLOW_PAID_FALLBACK=false
```

Enable one or two routes first, not every provider at once. A practical starting order is:

1. a fast hosted free-tier route such as Groq when the selected model/capability is currently eligible;
2. Ollama Cloud or another validated hosted route;
3. Cloudflare Workers AI when the project already uses Cloudflare or benefits from serverless inference;
4. OpenRouter free routing for low-volume experimentation where model variability is acceptable;
5. local or remote Ollama for owned-compute demos and privacy-sensitive experiments.

This is a policy order, not a permanent provider ranking. Recheck current limits, model catalogs, data handling, and terms before enabling a route.

## Square Cloud projects

Current Square Cloud policy does not allow direct heavy local LLM/ML inference in its managed containers. Host the website/API there and keep inference external.

Recommended topology:

```text
browser
  |
  v
Square Cloud website/API
  |
  v
server-side AI gateway
  |
  +--> Groq
  +--> Ollama Cloud
  +--> Cloudflare Workers AI
  +--> OpenRouter
  +--> authenticated remote Ollama
```

This fits existing Square-hosted demos because only the AI inference endpoint changes. The application remains on Square Cloud.

## Local Ollama demo option

For development or a presentation, Ollama may run on the developer workstation and the project backend can call it directly when both are on the same machine/network.

If remote access is required, place a protected gateway/reverse proxy in front of Ollama. The local Ollama API does not require authentication on localhost, so raw port `11434` must not become a public unauthenticated endpoint.

A temporary tunnel can be useful for development, but temporary tunnel URLs and workstation uptime are not production infrastructure.

## Provider notes

### Ollama

Useful when you want the same ecosystem across local/self-hosted and cloud model access. Ollama exposes native APIs and compatibility with parts of the OpenAI API. Direct access to Ollama Cloud uses authenticated API access. Verify the exact model and endpoint required by the project.

Official references:

- `https://docs.ollama.com/api/authentication`
- `https://docs.ollama.com/api/openai-compatibility`
- `https://docs.ollama.com/cloud`

### Groq

Useful for fast demos and OpenAI-compatible integration. Free-plan rate limits and the supported model catalog are provider-owned state and may change.

Official references:

- `https://console.groq.com/docs/openai`
- `https://console.groq.com/docs/rate-limits`
- `https://console.groq.com/docs/models`

### Cloudflare Workers AI

Useful for projects already near Cloudflare and for serverless inference. Workers AI exposes OpenAI-compatible text generation and embedding endpoints for supported models. Free allocation and model billing rules should be checked at deployment time.

Official references:

- `https://developers.cloudflare.com/workers-ai/configuration/open-ai-compatibility/`
- `https://developers.cloudflare.com/workers-ai/platform/pricing/`

### OpenRouter

Useful as an experimentation/fallback route. `openrouter/free` chooses among currently available free models and may vary model identity between requests. Do not use this route where deterministic model identity is a product requirement.

Official references:

- `https://openrouter.ai/docs/guides/routing/routers/free-router`
- `https://openrouter.ai/docs/faq`

### GitHub Models

Useful for model prototyping and evaluation in the GitHub ecosystem. Free API/playground limits are intended for experimentation; upgrade or use a production provider when the workload moves beyond prototype capacity.

Official reference:

- `https://docs.github.com/en/github-models/use-github-models/prototyping-with-ai-models`

### Gemini Developer API

Useful when the selected free-tier model and modalities fit the demo. Review the current pricing/data-use table before sending real client data because free and paid data-handling terms may differ.

Official reference:

- `https://ai.google.dev/gemini-api/docs/pricing`

## First integration checklist

Before enabling a provider:

- create the provider key in the provider console;
- place the key only in server-side environment variables;
- choose one logical ATLAS profile such as `demo-chat` or `support-summary`;
- select and record a concrete model;
- verify required capability such as JSON/structured output, tools, vision, or embeddings;
- run representative success and failure cases;
- test a forced 429/provider outage path;
- verify timeout and fallback behavior;
- confirm no provider key appears in browser bundles, HTML, logs, or source control;
- record the provider/model/evaluation date in project evidence or memory when it is a stable project choice.

## Example integration

Copy either starter:

```text
templates/ai-gateway/python_gateway.py
templates/ai-gateway/typescript_gateway.ts
```

Copy `templates/ai-gateway/env.example` into the target project's own environment template, then enable only the routes you intend to test.

The client should call the project's own endpoint:

```text
POST /api/ai/chat
```

The endpoint invokes the gateway module server-side. Do not make the browser choose or authenticate directly to the provider.

## Recommended demo features

Good first uses are bounded and easy to validate:

- support/ticket categorization;
- summarizing a customer request;
- FAQ or documented RAG answers;
- lead intent classification;
- suggested response drafts;
- extracting structured fields from free text;
- tutoring/explanation features;
- non-authoritative recommendations.

Avoid making a free-tier model the sole authority for payments, permissions, legal/medical decisions, irreversible operations, or other high-consequence business state.

## When to graduate to paid capacity

Move from `free_pool` toward pinned/paid capacity when any of these become recurring:

- free quota exhaustion;
- inconsistent availability;
- unstable model identity;
- latency above the product budget;
- quality below the evaluation threshold;
- higher concurrency;
- client SLA expectations;
- privacy/compliance requirements;
- meaningful revenue or operational value that justifies predictable inference.

Because the application calls one gateway boundary, graduation should normally be a configuration/provider change rather than a rewrite.

## Current-source refresh rule

Free AI offers change quickly. Before shipping or marketing a demo, recheck the current primary provider documentation. The ATLAS monthly upstream/capability review should treat provider pricing, free limits, supported models, endpoint compatibility, and data-use terms as freshness-sensitive external facts.
