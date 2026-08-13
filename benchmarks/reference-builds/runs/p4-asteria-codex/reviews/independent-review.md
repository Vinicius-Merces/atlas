# Independent review — P4 Asteria Codex

- Reviewer: `independent-agent:/root/asteria_independent_review`
- Review independence: separate agent; read-only review; no implementation edits
- Initial outcome: `Blocked`
- Post-remediation outcome: `Blocked`

## Findings closed after remediation

- Local persistence/idempotency: SQLite, `BEGIN IMMEDIATE`, restart-safe idempotency and concurrent duplicate control.
- Analytics truth: the authoritative event enters the outbox in the same transaction as the lead.
- Abuse boundary: persistent rate events, explicit proxy trust, hashed actor identity, same-origin/rate-limited analytics.
- Content: twelve navigable residences and three distinct article bodies.
- Source SEO/schema: noindex 404 without canonical; `numberOfBedrooms: 4` replaces the inaccurate room count.
- Accessibility source provisions: focusable status, dynamic menu name, Escape and focus restoration.
- Automated coverage: six Node tests plus real concurrent, restart and origin executions.

## Open findings

### BF-01 — High — browser/craft proof absent

No real browser screenshots, viewport matrix, keyboard/focus run, accessibility tree, console/network trace or form flow exists. `marketing-responsive`, `marketing-accessibility`, `marketing-browser-primary-flow` and related browser/craft checks cannot pass.

Cause: evidence gap plus environment/tooling blocker.

### BF-02 — High — production proof absent

No public HTTPS deployment, deployed redirect/canonical/robots/sitemap responses, structured-data validator, mobile performance run or production analytics exists. `marketing-production-domain`, `marketing-seo-indexing` and related production checks cannot pass.

Cause: evidence gap plus environment/deployment blocker.

### ARCH-01 — Medium — multi-instance architecture unproven

SQLite is authoritative for one process and a persistent volume. Horizontal or ephemeral hosting requires a shared transactional database.

### OPS-01 — Low — no outbox delivery worker

The outbox preserves conversion truth atomically, but `delivered_at` is not reconciled by a downstream worker. Durable recording passes locally; downstream delivery is not verified.

## Verification performed by reviewer

- Syntax checks passed.
- Node tests: 6 passed, 0 failed.
- `git diff --check` passed.
- SQLite inspection: one lead, two idempotency keys with the same lead ID and one authoritative outbox event.
- Concurrent `201/200 duplicate`, restart persistence and cross-origin `403` evidence accepted.

## Final review disposition

`Blocked`. Code remediation materially improved local correctness, but the canonical rubric blocks any run whose responsive, accessibility, primary browser flow, production domain or deployed SEO checks are not `pass`. No such status is promoted without direct evidence.
