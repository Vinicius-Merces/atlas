---
name: crawler-edge-access-audit
description: "Audit CDN, WAF, bot, challenge, robots, and crawler-access behavior for search and AI discovery using external HTTP evidence without treating user-agent simulation as crawler proof."
---

# Crawler Edge Access Audit

## Purpose

Verify that intended search, assistant, and AI-search crawlers can reach authoritative public content through the actual production edge while unrelated bot/security protections remain proportionate.

## Trigger conditions

Use when GEO/SEO relies on crawler access, a CDN/WAF/bot product changes, a crawler receives 403/challenge/degraded content, AI Crawl Control or similar policy is configured, a production release changes edge rules, or crawler accessibility must be proven rather than assumed.

## Inputs

Required:
- target production or production-equivalent domain/routes;
- intended index/crawl policy;
- CDN/WAF/bot/challenge configuration evidence available to the project;
- relevant crawler categories and business allow/block decisions.

Optional:
- `robots.txt`, robots meta/X-Robots-Tag, sitemap, `llms.txt`, or other public discovery surfaces;
- provider security-event logs;
- known verified-bot documentation;
- external HTTP probe evidence from more than one network/origin;
- Search Console/Bing/webmaster or answer-engine observations.

## Procedure

1. Identify the actual edge chain: DNS/proxy/CDN, WAF custom and managed rules, bot products, AI crawler controls, browser-integrity/challenge features, rate limits, geo/IP/ASN policies, access gateways, and origin firewall behavior.
2. Define crawler purpose classes separately: normal search indexing, AI search/retrieval, user-invoked assistant fetches, training crawlers, monitoring/automation, and unknown automation. Do not apply one allow/block decision to all bots.
3. Build a dated crawler-access matrix with crawler/service, purpose, intended policy, route scope, robots behavior, edge controls, observed response, evidence source, and limitations.
4. Verify `robots.txt`, meta/X-Robots directives, sitemap/canonical intent, and any supplementary discovery surfaces. `robots.txt` is crawl policy, not access control or secret protection.
5. Inspect edge rule ordering. An `Allow` decision in an AI-crawler product does not prove access if an earlier WAF/user-agent/bot rule blocks the same request.
6. Perform external HTTP diagnostics from production-relevant networks when possible. Record status, redirects, content type, representative title/body markers, and challenge/interstitial signatures.
7. Use crawler-like user agents only as diagnostics for explicit UA-dependent behavior. Label these results `UA simulation`; never call them proof that the named proprietary crawler is allowed or verified.
8. When a platform supports verified-bot identity, inspect current official provider guidance and security-event evidence rather than assuming user-agent identity. Verified crawlers can depend on provider IP ownership, reverse DNS, cryptographic/Web Bot Auth, or other signals.
9. Distinguish IP/origin filtering from user-agent filtering by comparing a normal browser UA and crawler-like UA from the same external origin where safe. A shared 403 suggests a broader edge decision; a crawler-only 403 suggests UA/bot-policy interaction but still requires provider evidence.
10. Treat HTTP 200 as insufficient by itself. Confirm the response contains authoritative page content rather than a challenge, login screen, shell, alternate block page, or materially degraded representation.
11. If security protection is the terminating control, do not broadly allow all bots, all verified bots, GitHub/Azure ranges, datacenter traffic, or entire countries merely to make monitoring green. Create the narrowest exception compatible with the provider and threat model, or use a different trusted validation source.
12. Re-test after edge changes and record before/after evidence. Route content/entity/GEO questions back to `generative-engine-optimization` and technical index/canonical mechanics to `seo-technical-audit`.

## Outputs

- Edge-control map and rule-order findings.
- Dated crawler-access matrix.
- External HTTP/body evidence with clear `UA simulation` versus verified evidence labels.
- Discovery-surface consistency findings.
- Security/crawlability conflicts, remediation, and residual-risk statement.

## Dependencies

- `seo-technical-audit` for indexability/canonical/robots/sitemap mechanics.
- `generative-engine-optimization` for GEO strategy and crawler business intent.
- `web-security-header-audit` when edge changes interact with browser security or challenge behavior.
- `rate-limit-abuse-control` when crawler access conflicts with rate/concurrency protection.
- Current official CDN/WAF/search/AI provider documentation for bot identity and product behavior.

## Limitations

- User-agent simulation does not prove proprietary crawler access or identity.
- Successful fetch does not prove indexing, ranking, citation, referral, or future crawl frequency.
- A crawler may use multiple user agents/purposes whose policies differ.
- Security-event visibility and bot verification features vary by provider and plan.
- Provider behavior can change independently of repository code.

## Validation

- Confirm intended public routes return authoritative content through the production edge for ordinary external clients.
- Verify named crawler-policy changes against edge rule ordering and current provider evidence.
- Label simulated UA results separately from verified crawler/security-event evidence.
- Check status plus response-body markers; reject challenge/interstitial content as successful crawler access even when status is 200.
- Verify required search/AI discovery is not blocked by unintended WAF, bot, challenge, auth, geo, IP, or rate-limit behavior.
- Verify remediations do not create broad security bypasses solely for CI or crawler tests.
- Route significant work through `web-security-edge-assurance-review`.
