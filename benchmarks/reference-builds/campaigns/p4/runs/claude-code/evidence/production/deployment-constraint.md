# Deployment constraint — recorded before implementation, not after scoring

Capability: `manual-deployment-preflight` / Web Production Assurance
Check affected: `marketing-production-domain` (a declared blocking check)

## What was attempted

Network egress in this run environment is allowlisted. The following were probed
directly, before any code was written (see `run-manifest.json` `notes`):

| Target | Result |
| --- | --- |
| `https://api.vercel.com/v2/user` | no route — connection refused by the egress policy (curl exit 000) |
| `https://api.netlify.com/api/v1/user` | no route (000) |
| `https://api.cloudflare.com/client/v4/user` | no route (000) |
| `https://api.trycloudflare.com` (cloudflared quick tunnel) | `403 Host not in allowlist: api.trycloudflare.com` |
| `https://loca.lt`, `https://srv.us` (tunnel providers) | no route (000) |
| `https://registry.npmjs.org/` | 200 |
| `https://api.github.com` | 200 |

Only the npm registry and GitHub are reachable. In addition, the campaign
instruction for this target permits commits and pushes **only** on
`bench/p4-asteria-claude-code`, which rules out publishing a GitHub Pages branch —
and GitHub Pages is static, so it could not host the authoritative lead mutation
that this fixture's blocking check `marketing-lead-authoritative` depends on.

## What was done instead

The site is built and validated as a **real Next.js production build** (`next build`
+ `next start`), served over HTTP on this host, with production environment
configuration supplied through real environment variables:

- `ASTERIA_ORIGIN` — drives canonical URLs, `robots.txt`, `sitemap.xml` and every
  OpenGraph URL, all verified in `evidence/seo/seo-audit.json` as
  `https://asteria-residences.example/...`
- `ASTERIA_ADMIN_KEY`, `ASTERIA_IP_SALT`, `ASTERIA_DB_PATH` — server-only, and
  proven absent from every client asset in
  `evidence/security/secret-and-header-audit.json`
- Production response headers (CSP, `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`, `Permissions-Policy`, no `X-Powered-By`) verified on live
  responses, not read from source

Four instances of the production build were run to exercise configuration
variance: normal, production-default rate limit, forced store failure, forced
provider failure. See `site/scripts/servers.sh`.

## What is therefore NOT verified

- No public domain, no public DNS record, no public TLS certificate, no HTTPS
  handshake against a real certificate authority.
- No CDN, edge cache or hosting-platform behaviour.
- No real-network latency: the performance figures use CDP network emulation
  over the loopback interface, which is stated in
  `evidence/performance/performance.json`.

## How this is scored

`marketing-production-domain` is reported as **partial**, not pass. It is a
declared blocking check, so this run is **blocked and non-claimable** under the
rubric's `require_no_blockers` rule regardless of the aggregate score.

The ATLAS reference-build workflow requires exactly this handling:

> If deployment/provider access is unavailable, mark affected checks
> `unverified`; do not assume equivalence from local code.

`partial` rather than `unverified` is used because production build, production
environment configuration, production headers and production crawl/index
behaviour *were* verified on a live server — only the public domain and its TLS
were not. Nothing else in the submission is upgraded to compensate for this, and
no other check cites a deployment that did not happen.
