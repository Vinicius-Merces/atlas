# Free AI Provider Verification

This note records the provider endpoint shapes used by the reusable ATLAS AI gateway. It is evidence for the starter implementation, not a promise that free tiers, model catalogs, pricing, quotas, or data-use terms remain unchanged.

## Verified endpoint shapes

- Ollama native local API: `http://localhost:11434/api`; Ollama cloud native API: `https://ollama.com/api`.
- Groq OpenAI-compatible base: `https://api.groq.com/openai/v1`.
- OpenRouter OpenAI-compatible base: `https://openrouter.ai/api/v1`.
- GitHub Models inference base: `https://models.github.ai/inference`; chat completions are sent to `/chat/completions`. Tokens need the current GitHub Models permission/scope required by the project.
- Gemini OpenAI-compatible base: `https://generativelanguage.googleapis.com/v1beta/openai`; chat completions are sent to `/chat/completions`.
- Cloudflare Workers AI base remains account/project-specific and must be supplied through `CLOUDFLARE_AI_BASE_URL`.

## Deployment rule

Before a public or client-facing demo, re-check current official provider documentation for:

1. endpoint/API compatibility;
2. model availability;
3. free-tier eligibility and quotas;
4. data-use/privacy terms;
5. tool/structured-output/vision capability support for the exact model;
6. rate-limit and retry behavior.

Do not infer a model capability merely because the provider uses an OpenAI-compatible HTTP shape.
