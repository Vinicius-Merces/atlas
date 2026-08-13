# P4 Asteria Codex — first frozen result evidence

## Run identity

- Runtime: `codex`
- Model: `GPT-5`
- Branch: `bench/p4-asteria-codex`
- Campaign base commit: `3ccdf6e6209c3aea949e62226af1cb6b35167487`
- Fixture SHA-256: `e57da062e6223f6ecbea84a64813f6d8e73f9b0954cda065da5edbc680762947`
- Rubric SHA-256: `6463ae7fde36affecc20eff21f0ec73e04e0fb44c920a3cbc9115502a1b56b31`
- Environment: local Node 24 production-equivalent server; restricted network; no production deployment

## Implementation evidence

- Public routes implemented: `/`, `/residencias`, three residence detail routes, `/localizacao`, `/caderno`, three article routes, `/contato`, `/privacidade`, `/termos`.
- Operational routes implemented: `/api/health`, `/api/leads`, `/api/analytics`, `/robots.txt`, `/sitemap.xml`, real HTTP 404.
- Generated imagery: `assets/hero.webp` (1584×990, 205 KiB) and `assets/interior.webp` (1448×1086, 162 KiB).
- Client payload: authored CSS 24 KiB on disk; progressive-enhancement JavaScript 8 KiB; no runtime dependency manifest or lockfile.
- Content, sitemap and structured data use a shared code-owned authority in `site/src/content.js`.

## Executed checks

### Static and unit

Command:

```text
node --check server.js
node --check src/content.js
node --check src/render.js
node --check public/app.js
NODE_ENV=test node --test tests/*.test.js
```

Result: 4 tests passed, 0 failed. Coverage includes normalized valid lead, invalid/bot lead, canonical residence/schema rendering and HTTP 404 document generation.

### HTTP public-route matrix

Executed against the running Node server with `PUBLIC_ORIGIN=http://localhost:4173`.

| Path | Status | Canonical | Structured types |
|---|---:|---|---|
| `/` | 200 | `/` | Organization, WebSite, WebPage |
| `/residencias` | 200 | `/residencias` | Organization, WebSite, WebPage, ItemList |
| `/residencias/casa-patio` | 200 | same path | Organization, WebSite, WebPage, SingleFamilyResidence |
| `/localizacao` | 200 | same path | Organization, WebSite, WebPage |
| `/caderno` | 200 | same path | Organization, WebSite, WebPage, CollectionPage |
| `/caderno/viver-entre-cidade-e-paisagem` | 200 | same path | Organization, WebSite, WebPage, Article |
| `/contato` | 200 | same path | Organization, WebSite, WebPage |
| `/privacidade` | 200 | same path | Organization, WebSite, WebPage |
| `/termos` | 200 | same path | Organization, WebSite, WebPage |
| `/nao-existe` | 404 | `/404` | Organization, WebSite, WebPage |

Every JSON-LD block parsed successfully with `JSON.parse`. `robots.txt` and `sitemap.xml` returned 200; the sitemap contained 13 URLs.

Finding retained in the frozen baseline: the 404 response emits the default `index,follow` robots value and a `/404` canonical even though `/404` itself also returns 404.

### Form authority and failures

Executed against the running server using synthetic records only.

| Scenario | Result |
|---|---|
| Invalid fields | 422 with field-specific server errors |
| Simulated downstream failure | 503 `PROVIDER_UNAVAILABLE`, `Retry-After: 30`, explicit not-saved recovery message |
| Valid new lead | 201 with stable `ast_*` lead ID and `received` status |
| Same person/new idempotency key | 200 with same lead ID and `duplicate: true` |
| Same idempotency key retry | 200 with cached authoritative result and `duplicate: true` |

The first valid state was persisted atomically before success. A `lead_authoritative_success` analytics record was appended after persistence. Runtime lead/analytics data is excluded from Git.

### Headers

Observed on HTML/API responses: Content-Security-Policy, Referrer-Policy, X-Content-Type-Options, X-Frame-Options, Permissions-Policy and Cross-Origin-Opener-Policy. API responses are `no-store`.

## Browser and deployment evidence — unavailable in the first result

The following were attempted and retained as negative evidence:

1. `agent-browser` command: unavailable (`command not found`).
2. Cloud browser navigation to `http://terminal.local:4173`: `ERR_CONNECTION_REFUSED`; the local server was not exposed through the cloud preview bridge.
3. `sites-preview`: preview daemon mailbox/runtime could not resolve the sandbox checkout.
4. Existing Playwright package with browser installation: Chromium download returned an empty/truncated archive under the network allowlist.
5. Sites checkpoint lifecycle: remote site creation began, but the required `/workspace/sites` checkout could not persist across sandbox calls and the remote source repository has no `main` branch.

Therefore the baseline has **no real-browser screenshots, viewport interaction runs, accessibility-tree evidence, console/network capture, Lighthouse run, HTTPS domain or deployed HTTP evidence**. Source-level responsive, accessibility, reduced-motion, SEO, structured-data and performance provisions exist, but they are not promoted to browser/deployment proof.

## Baseline gate status

- Unit/API/HTTP execution: passed for the stated local scope.
- Authoritative form state: passed locally.
- Browser primary/negative flows: unverified.
- Rendered responsive/accessibility/visual regression: unverified.
- Production domain/HTTPS/deployed SEO: unverified.
- First-result benchmark disposition: necessarily blocked by canonical blocking checks, regardless of source quality.
