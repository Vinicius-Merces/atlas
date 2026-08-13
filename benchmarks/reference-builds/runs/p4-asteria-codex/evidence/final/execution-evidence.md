# P4 Asteria Codex — final execution evidence

## Identity and frozen checkpoints

- Runtime: `codex`
- Model: `GPT-5`
- Branch: `bench/p4-asteria-codex`
- Campaign base: `3ccdf6e6209c3aea949e62226af1cb6b35167487`
- First result frozen before remediation: `a1751e8558beddee8e8c57d2b3f47de86e1c5860`
- Remediated implementation: `e818410355af1237c35da71f7d4f79a356c154a6`
- Final tested source: `b259ff86f5a2a049be7d88416f227c62c0b61071`
- Fixture SHA-256: `e57da062e6223f6ecbea84a64813f6d8e73f9b0954cda065da5edbc680762947`
- Rubric SHA-256: `6463ae7fde36affecc20eff21f0ec73e04e0fb44c920a3cbc9115502a1b56b31`

The baseline evidence remains unchanged at `evidence/baseline/execution-evidence.md`. This document records only the final, post-review state.

## Product and public surfaces

The final build is a server-rendered, progressively enhanced Node site with a product-specific editorial thesis, generated hero/interior imagery and no third-party runtime dependencies. It implements home, the twelve-residence catalog and details, location, editorial index and three distinct articles, contact, privacy, terms, a real 404, robots, sitemap, lead API, analytics API and health endpoint.

The code-owned content authority is `site/src/content.js`; rendering, canonical metadata, sitemap and JSON-LD consume the same records. The contact path is a server-authoritative mutation rather than a client-only success state.

## Static and automated tests

Executed after remediation:

```text
node --check server.js
node --check src/content.js
node --check src/render.js
node --check public/app.js
NODE_ENV=test node --test tests/*.test.js
```

Result: **6 passed, 0 failed**. Coverage includes field and bot validation, canonical/schema truth, 404 indexability, all twelve residences, distinct editorial bodies, persistent idempotency and transactional analytics outbox behavior across a store restart.

Repository validation was also executed with temporary files outside the checkout:

```text
python scripts/validate_all.py --profile full
python -m pytest tests -q
```

Result: full ATLAS validation passed and **287 repository tests passed**.

## Real local HTTP execution

A real Node server was started on `127.0.0.1:4173` with a dedicated SQLite evidence database. Observed results:

| Surface | Observed result |
|---|---|
| `/api/health` | 200; `persistence: sqlite` |
| `/`, `/residencias`, detail, location, journal, article, contact, privacy, terms | 200 |
| `/nao-existe` | 404 |
| `/robots.txt`, `/sitemap.xml` | 200 |
| Residence JSON-LD | parsed JSON; `SingleFamilyResidence`, `numberOfBedrooms: 4`, truthful floor size |
| 404 metadata | `noindex,nofollow`; no canonical |

The sitemap/content authority now covers all twelve residences rather than three representative records.

## Form, persistence, failure and abuse controls

The final data path uses native SQLite with WAL and `BEGIN IMMEDIATE`. Lead creation, idempotency result and the authoritative `lead_authoritative_success` outbox event commit in one transaction. The database file is mode `0600`; runtime data is ignored by Git.

Executed evidence:

- Two simultaneous requests using different idempotency keys for the same identity returned one `201` and one `200 duplicate`, both with the same lead ID.
- A server restart followed by the original key returned `200 duplicate` with that same lead ID.
- SQLite inspection found one lead, two idempotency records pointing to it and one authoritative analytics outbox event.
- A cross-origin lead request returned `403`.
- Invalid input returns `422` with field errors.
- The explicit provider failure path returns `503`, `Retry-After: 30` and a truthful not-saved/retry message.
- Rate events are persisted; forwarded IP is trusted only when `TRUST_PROXY=true`, then represented by a SHA-256 actor hash.
- Analytics ingestion is same-origin, allowlisted and rate-limited. The durable outbox currently has no downstream delivery worker, so downstream analytics delivery is not claimed.

The SQLite design is authoritative for one instance with a persistent volume. A horizontally scaled or ephemeral-filesystem deployment would require a shared transactional database; production multi-instance readiness is not claimed.

## Security, privacy and supply chain

Server-side normalization and validation, honeypot rejection, body-size caps, origin enforcement, idempotency and persistent rate limiting are implemented. HTML and API responses include CSP, Referrer-Policy, X-Content-Type-Options, X-Frame-Options, Permissions-Policy and Cross-Origin-Opener-Policy; API responses are `no-store`. No provider credential is present in public code. The project has no third-party production dependencies or lockfile, reducing runtime supply-chain surface.

## Responsive, accessibility and interaction provisions

Source provisions include semantic landmarks, skip link, visible focus treatment, labeled controls, field-level errors with `aria-describedby`, live status, menu accessible-name updates, Escape close/focus restoration and a reduced-motion media query. CSS contains phone/tablet/wide breakpoints and fluid layout rules. These are source-level facts only: no browser-based responsive or accessibility pass is claimed.

## SEO, structured data and performance provisions

Local HTTP verified robots, sitemap, unique titles/descriptions, canonical behavior for indexable pages, truthful JSON-LD parsing and non-indexable 404 behavior. On-disk authored assets measured 210 KiB hero WebP, 166 KiB interior WebP, 23 KiB CSS and 5 KiB JS. These measurements are not Lighthouse or field data, and local verification is not deployed indexing proof.

## Browser and deployment evidence gap

The final environment retained the baseline blockers:

- `agent-browser` binary was unavailable.
- The cloud browser could not reach the local server through `terminal.local`.
- the Sites preview checkout requires `/workspace/sites`, outside writable roots, and its created remote had no checkoutable `main` branch.
- Playwright's Chromium download was truncated under the restricted network allowlist.

Consequently there are no genuine browser screenshots, viewport runs, accessibility tree, keyboard run, console/network capture, Lighthouse report, public HTTPS URL or deployed SEO/indexing response. The submission marks these checks `unverified` rather than inferring success from source.

## Final disposition

Independent re-review closed the code findings for local integrity, security, content truth, 404 behavior, schema truth and keyboard provisions. It retained the browser/deployment findings and issued `Blocked`. Because canonical blocking checks remain unverified, the final benchmark outcome must remain **Blocked**, regardless of source-level quality or numeric score.
