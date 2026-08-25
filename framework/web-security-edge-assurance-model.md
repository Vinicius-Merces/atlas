# Web Security and Edge Assurance Model

## Purpose

ATLAS uses this model to protect public web applications at the browser and edge layers without accidentally breaking legitimate users, conversion/analytics integrations, search crawlers, or AI-search discovery.

This model complements rather than replaces:

- `framework/web-production-assurance-model.md` for rendered behavior, SEO, schema, and supply-chain evidence;
- `framework/saas-production-trust-model.md` for identity, authorization, tenant/data isolation, secrets, providers, and payments;
- `generative-engine-optimization` for entity authority, answer-ready content, and GEO measurement.

## Core principle

**Security controls must be enforced from evidence, and discovery controls must be verified at the same edge that serves production.**

A site can have correct `robots.txt` and still be blocked by WAF, CDN bot controls, challenges, geo/IP rules, rate limits, or user-agent rules. A CSP can improve browser security while silently breaking analytics, ads, chat, APIs, fonts, or payment flows. Configuration intent is not production evidence.

## Assurance path

```text
public route + integrations + crawler intent
        ↓
third-party origin and browser execution inventory
        ↓
security headers + CSP policy
        ↓
sensitive-public-path exposure checks
        ↓
CDN / WAF / bot / challenge policy mapping
        ↓
external HTTP and crawler-path evidence
        ↓
critical browser/integration regression
        ↓
independent security-edge review
```

## 1. Security headers

For public HTTPS applications, evaluate at least:

- `Strict-Transport-Security` when HTTPS is authoritative and operationally safe;
- `Content-Security-Policy` or a documented staged `Content-Security-Policy-Report-Only` rollout;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy` appropriate to product/privacy needs;
- `Permissions-Policy` for browser capabilities that should not be generally available;
- framing protection through CSP `frame-ancestors` and, where compatibility value remains, `X-Frame-Options`;
- CSP `base-uri` and `object-src` restrictions;
- CORS only when cross-origin API access is intentionally part of the application contract.

Header presence alone is insufficient. Inspect effective production responses, redirects, CDN/proxy overrides, duplicate/conflicting values, and route-specific differences.

## 2. Content Security Policy

CSP must be designed from the actual runtime, not copied from a generic allowlist.

Required procedure:

1. Inventory first-party and third-party origins used by scripts, styles, images, fonts, frames, workers, media, forms, and network connections.
2. Trace critical integrations such as analytics, advertising/conversion tracking, authentication providers, payments, chat, storage, maps, monitoring, and APIs.
3. Start from least privilege: `default-src 'self'`, `object-src 'none'`, restrictive `base-uri`, and explicit `frame-ancestors` unless architecture proves another requirement.
4. Prefer nonce/hash-based script trust when the framework and operational complexity justify it. Do not add nonce machinery solely for appearance.
5. Treat `'unsafe-inline'`, `'unsafe-eval'`, broad `https:`, `data:`, `blob:`, and `*` as exceptions requiring an observed consumer and documented risk.
6. Use Report-Only first when production dependencies are uncertain, then promote to enforcement after violations and critical integrations are validated.
7. Validate with a real browser. A header that parses successfully is not sufficient if required requests become `blocked:csp` or console violations appear.
8. Preserve existing conversion, analytics, lead, auth, payment, chat, and API semantics. Security hardening must adapt to trusted product requirements instead of disabling them to make CSP simple.

## 3. Sensitive public-path exposure

`robots.txt` is not a confidentiality control. Public deployments should passively verify that common high-risk paths do not return usable secrets or privileged configuration.

Representative probes can include, when safe and relevant:

- `/.env`, `/.env.*`, `/production/.env`;
- `/.npmrc`;
- `/.git/config` and other repository metadata paths;
- `/.ssh/authorized_keys`;
- service-account or Firebase admin JSON names used by the project;
- `*.pem`, `*.key`, private runtime configuration, server-status/debug endpoints, and generated config files.

Expected outcome is normally `403`, `404`, or an intentionally harmless public response. A `200` is not automatically a breach, but any returned body must be inspected for secret-like content before approval. Never print discovered secret values into logs or evidence.

If live credentials may have been exposed, code removal alone is not remediation: use `secret-environment-audit` and require rotation/revocation evidence.

## 4. Edge and bot-control mapping

Inventory every layer that can terminate or transform a request before application code:

- CDN proxy and cache rules;
- WAF custom/managed rules;
- bot fight/bot-management products;
- AI crawler controls;
- browser integrity/challenge features;
- user-agent blocks;
- IP/ASN/country/geo policies;
- rate/concurrency limits;
- authentication/access gateways;
- origin firewall rules.

A policy shown as `Allow` in one product does not prove the request is allowed if an earlier rule can block or challenge it.

Do not broadly allow all bots, all datacenter traffic, GitHub/Azure IP ranges, or all verified-bot categories merely to make CI green. Prefer the narrowest exception supported by the actual terminating control.

## 5. Search and AI crawler assurance

When public discovery matters, maintain a dated crawler-access matrix containing:

- crawler/service and purpose category;
- business allow/block decision;
- official identification guidance when available;
- `robots.txt` and meta/X-Robots behavior;
- CDN/WAF/bot-control path;
- observed HTTP status/body class;
- tested route scope and timestamp;
- limitations and unresolved ambiguity.

Search/retrieval/assistant crawlers and model-training crawlers are separate policy decisions.

A simulated `User-Agent` is diagnostic only. It can reveal an explicit UA-block rule, but it cannot prove how a proprietary crawler is classified because verified bots may use IP ownership, reverse DNS, cryptographic bot authentication, provider-specific verification, or other signals. Record `UA simulation` separately from `verified crawler evidence`.

A response must be evaluated beyond the status code. `HTTP 200` can still contain a challenge/interstitial, login page, degraded shell, or alternate content. Confirm representative content markers, canonical title/body, and absence of terminating challenge behavior.

## 6. Browser and integration regression

After header or edge-security changes, validate representative critical flows in a rendered browser:

- route load and navigation;
- forms and lead submission;
- analytics and conversion events when in scope;
- chat/support widgets;
- auth/payment flows when present;
- first-party and third-party API calls;
- fonts/images/media;
- console errors and network failures.

Treat unexplained CSP violations, blocked required requests, challenge loops, or edge-only 403s as findings even when the build and unit tests are green.

## 7. Evidence model

Record:

- exact environment/domain and timestamp;
- relevant response headers;
- CSP policy and origin inventory;
- passive sensitive-path results without secret values;
- edge/WAF/bot configuration evidence available to the reviewer;
- external HTTP/crawler diagnostics and body/content evidence;
- browser/integration validation;
- unavailable evidence and residual risk.

Do not claim `secure`, `crawler-safe`, `AI-search accessible`, or `no vulnerabilities` from one passive scan. State what was tested and what remains unverified.

## 8. Release severity

Normally blocking until resolved or explicitly governed:

- exposed usable credentials/private keys;
- missing or materially unsafe CSP when browser injection risk is in scope and no accepted rollout plan exists;
- security policy that breaks a release-critical integration or conversion path;
- unintended site-wide blocking/challenge of required search/assistant crawlers;
- broad bypass introduced only to satisfy automation;
- production evidence contradicting repository configuration.

Medium/Low findings can include missing non-critical headers, justified temporary Report-Only CSP, or incomplete crawler verification when discovery is not release-critical, provided residual risk is explicit.

## External assurance basis

This model is provider-neutral. Named CDN, WAF, browser, search, advertising, and AI platforms must be implemented from their current official documentation because bot verification, CSP requirements, endpoints, and security-product behavior change over time.
