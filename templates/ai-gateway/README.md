# ATLAS AI Gateway Starter

This directory is a copyable starter for demos and low-volume products that need a provider-neutral AI boundary.

It is intentionally small. It demonstrates routing, fallback, privacy/capability filtering, normalized errors, cooldown, and environment-only credentials without making ATLAS itself depend on an AI SDK.

## Files

- `provider-pool.example.yaml`: declarative provider/profile shape.
- `env.example`: environment boundary for common free/owned-compute routes.
- `python_gateway.py`: dependency-free Python reference router for non-streaming chat.
- `typescript_gateway.ts`: TypeScript reference router using the platform `fetch` API.

## Recommended project topology

```text
browser / mobile client
       |
       v
project backend endpoint
       |
       v
ATLAS-style gateway module
       |
       +--> hosted provider API
       +--> authenticated remote Ollama gateway
       +--> local Ollama during development
```

Do not copy provider keys into public/browser environment variables.

## Demo-first configuration

Start with `AI_MODE=free_pool`, enable only providers whose current free plan and data policy you have verified, and keep `AI_ALLOW_PAID_FALLBACK=false`.

For a Square Cloud application, keep inference outside Square Cloud. Host the application/API on Square and call approved external inference APIs or an authenticated Ollama endpoint hosted elsewhere.

## Production migration

When traffic or quality requires paid capacity:

1. keep the same application endpoint and logical capability profiles;
2. add/pin a production provider;
3. set an explicit budget and provider policy;
4. evaluate the selected model for each production capability profile;
5. move circuit/quota state from process memory to shared storage when running multiple instances;
6. add project-native observability, rate limiting, abuse controls, privacy review, and schema validation.

The reference code is not a full production gateway. It deliberately leaves authentication middleware, persistence, tenant limits, streaming, tool execution, and framework-specific HTTP wiring to the target application.
