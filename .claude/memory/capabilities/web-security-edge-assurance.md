# Web Security and Edge Assurance

## Status

Canonical capability memory for public-web browser security and edge/crawler assurance.

## Canonical sources

- Model: `framework/web-security-edge-assurance-model.md`
- Overlay: `framework/capabilities/web-security-edge-assurance.yaml`
- Workflow: `.claude/workflows/web-security-edge-assurance.md`
- Review: `.claude/reviews/web-security-edge-assurance-review.md`
- Skills:
  - `.claude/skills/web-security-header-audit/SKILL.md`
  - `.claude/skills/crawler-edge-access-audit/SKILL.md`

## Stable rules

1. **Configuration intent is not production evidence.** Inspect effective HTTP/browser behavior after CDN, proxy, WAF, bot, challenge, authentication, geo/IP, and rate-limit layers.
2. **CSP is an integration contract, not a checklist header.** Inventory real runtime origins first, apply least privilege, validate in a rendered browser, and do not break trusted analytics, conversion, chat, auth, payment, API, storage, font/image, or monitoring flows merely to simplify policy.
3. **Report-Only is a staging tool.** Use it when production dependencies are uncertain, then promote deliberately to enforcement or record an explicit exception.
4. **Broad CSP sources are exceptions.** Wildcards, broad schemes, `data:`, `blob:`, `'unsafe-inline'`, and `'unsafe-eval'` require a real consumer and residual-risk rationale.
5. **Sensitive-path checks are passive and bounded.** Probe only stack-relevant paths such as `.env`, `.npmrc`, repository metadata, service-account files, private-key/config, and debug endpoints. A 200 requires body inspection; never log discovered secret values.
6. **Possible live credential exposure requires rotation/revocation.** Deleting a file or changing code does not invalidate a credential that may already have escaped.
7. **Edge rule ordering matters.** An Allow in an AI-crawler control can still lose to an earlier WAF, bot fight, user-agent, challenge, geo/IP, or rate-limit rule.
8. **Crawler purposes are separate.** Search/retrieval, user-invoked assistant fetch, model training, monitoring, and unknown automation do not inherit one universal allow/block decision.
9. **UA simulation is diagnostic only.** A forged/simulated crawler User-Agent can reveal user-agent-dependent policy but cannot prove proprietary crawler verification, IP ownership, reverse-DNS verification, cryptographic bot authentication, indexing, or citation.
10. **HTTP 200 is not enough.** Confirm authoritative page title/body/content rather than a challenge, interstitial, login page, shell, or degraded alternate response.
11. **Do not weaken the perimeter just to make CI green.** Avoid broad GitHub/Azure/datacenter/country/all-bot or all-verified-bot bypasses. Prefer the narrowest provider-supported exception or another trusted validation source.
12. **Security and discoverability are composed gates.** Web Production Assurance, SEO Technical Audit, GEO, Secret Environment Audit, browser validation, and this capability must agree on the deployed behavior.

## Why this capability exists

Public-web failures can cross ownership boundaries: an application can have correct robots/canonical content while an edge rule blocks search or AI retrieval, or a CSP can be syntactically present while silently breaking conversion tracking. ATLAS therefore treats browser security and edge crawler access as observable production behavior rather than configuration trivia.

## Evidence boundary

This capability can support claims about the routes, headers, bodies, integrations, paths, and edge behavior actually tested. It does **not** prove complete vulnerability absence, proprietary crawler visits, indexing, ranking, AI citations, future crawl frequency, or the absence of undiscovered secret paths.
