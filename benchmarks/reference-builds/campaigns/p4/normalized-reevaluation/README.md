# P4.3 Frozen Asteria Environment-Normalized Re-evaluation

P4.3 does not ask Codex or Claude Code to build Asteria again. It takes the exact first-frozen implementations that produced the original P4 scores and evaluates both through the same campaign-owned infrastructure introduced by P4.1/P4.2.

## Question answered

The original observed target scores were:

- Claude Code / `claude-opus-5`: 86.40
- Codex / `GPT-5`: 53.15

Codex lacked real-browser and public-deployment evidence in its original runtime environment. P4.3 asks a narrower and more useful question:

> What evidence becomes observable when the exact frozen implementations receive the same public HTTPS ingress, the same Chromium version, the same viewports, and the same portable collector?

This separates evidence-environment loss from implementation defects without pretending that a post-hoc portable runner is the coding runtime itself.

## Frozen targets

- Codex: `a1751e8558beddee8e8c57d2b3f47de86e1c5860`
- Claude Code: `bff32598806c7ea9b6cd4c2218ee7d5eac2d0816`

The workflow checks these commits out into `target/` while the current campaign infrastructure is checked out separately into `campaign/`. Target source is never copied into `main` and is never modified for scoring.

## Common evidence floor

Both frozen targets receive:

- GitHub-hosted Ubuntu runner
- Node 22
- pinned `cloudflared` binary and checksum
- Cloudflare Quick Tunnel `controlled-preview`
- Playwright 1.55.0
- Chromium installed by the same campaign step
- 360×800, 768×1024, 1280×800, and 1920×1080 viewports
- seven fixture-equivalent public surfaces
- one real missing route
- the same public TLS/HTTP probe
- the same portable browser collector

The runner rebuilds/restarts each target with the assigned temporary public origin after the tunnel URL is known so canonical and crawl-facing evidence are measured against the actual preview origin rather than localhost.

## What P4.3 may conclude

P4.3 may report that evidence was recovered, that a defect becomes visible under the common runner, or that one target still fails a normalized evidence check.

It may **not**:

- rewrite the historical 53.15 or 86.40 scores;
- call the controlled preview production;
- infer a new model-quality ranking from portable evidence alone;
- claim that Codex or Claude Code itself produced the portable evidence;
- mutate either frozen implementation to make the comparison greener.

A true new benchmark score requires a new target run with truthful runtime/model identity, full product-specific evidence, independent review, and the canonical scoring lifecycle.
