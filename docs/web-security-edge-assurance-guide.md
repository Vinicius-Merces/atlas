# Web Security and Edge Assurance Guide

Use this guide when a public site must be hardened without breaking trusted browser integrations or intended search/AI discovery.

Canonical sources:

- `framework/web-security-edge-assurance-model.md`
- `.claude/skills/web-security-header-audit/SKILL.md`
- `.claude/skills/crawler-edge-access-audit/SKILL.md`
- `.claude/workflows/web-security-edge-assurance.md`
- `.claude/reviews/web-security-edge-assurance-review.md`

## When to run it

Run the workflow before a significant public-web release when any of these are true:

- CSP or other browser security headers are absent, changed, or tightened;
- analytics, conversion tracking, chat, authentication, payments, maps, storage, monitoring, fonts, images, or external APIs create browser origin dependencies;
- a CDN, WAF, bot product, challenge, AI crawler policy, geo/IP rule, access gateway, or rate limit changes;
- Google/Bing/AI-search discovery is expected but crawler accessibility is uncertain;
- a scan or security event suggests `.env`, repository metadata, service-account files, private keys, generated runtime configuration, or debug endpoints may be publicly reachable;
- production behavior differs from repository configuration.

## Fast operating sequence

1. Map public routes, critical integrations, index/discovery intent, and edge products.
2. Fetch representative production responses and record effective headers.
3. Inventory actual browser origins before writing or changing CSP.
4. Run bounded sensitive-path probes without brute-force enumeration and without logging secret values.
5. Map CDN/WAF/bot/challenge rule ordering before changing allow/block policy.
6. Run external ordinary-client and crawler diagnostics where justified.
7. Inspect both status and authoritative body/title/content markers.
8. Label crawler-like User-Agent results as `UA simulation` unless provider/security-event evidence verifies the crawler.
9. Run real-browser regression for critical flows and inspect CSP/network failures.
10. Complete independent `web-security-edge-assurance-review` and record residual risk.

## CSP checklist

A CSP is a browser execution policy, not a decorative header.

Review at least:

- `default-src`
- `script-src` / `script-src-elem` where applicable
- `style-src`
- `img-src`
- `font-src`
- `connect-src`
- `frame-src`
- `frame-ancestors`
- `form-action`
- `base-uri`
- `object-src`
- `worker-src` when applicable
- `media-src` / `manifest-src` when applicable
- `upgrade-insecure-requests` when appropriate

Preferred baseline principles:

- start from first-party/least privilege;
- use `object-src 'none'` unless architecture proves a need;
- restrict `base-uri` and `frame-ancestors` intentionally;
- add third-party origins only after identifying a real runtime consumer;
- treat `*`, broad `https:`, `data:`, `blob:`, `'unsafe-inline'`, and `'unsafe-eval'` as documented exceptions;
- use Report-Only when the dependency inventory is uncertain, then promote deliberately to enforcement;
- never remove release-critical tracking, auth, payment, chat, API, or other trusted behavior merely to make a policy smaller.

Browser validation should explicitly inspect console violations and requests blocked by CSP. A syntactically valid policy can still be operationally wrong.

## Sensitive-path checklist

Use only bounded, safe GET/HEAD probes relevant to the stack. Examples can include:

- `/.env` and known environment variants;
- `/.npmrc`;
- `/.git/config`;
- `/.ssh/authorized_keys`;
- project-relevant service-account/Firebase admin JSON names;
- private-key/config files;
- debug or server-status endpoints.

Interpretation:

- `403` or `404` is normally acceptable evidence for that exact path;
- `200` is a review trigger, not automatic proof of credential exposure;
- inspect the body for secret/private-key markers without recording the values;
- if a live credential may have been exposed, require rotation/revocation and appropriate incident review. File removal alone is not remediation.

## Edge and crawler checklist

Map every layer that can terminate a request before application code:

- CDN/proxy;
- WAF custom rules;
- WAF managed rules;
- bot fight / bot management;
- AI crawler controls;
- browser-integrity or challenge products;
- User-Agent rules;
- IP/ASN/country/geo rules;
- rate/concurrency limits;
- authentication/access gateways;
- origin firewall.

### Rule-order principle

An `Allow` decision in one product does not guarantee accessibility if an earlier rule blocks or challenges the same request.

When a crawler receives a 403 or challenge, identify the terminating product/rule before creating exceptions.

### Do not solve CI with a broad bypass

Avoid permanent rules that broadly allow:

- all bots;
- all verified bots;
- all datacenter traffic;
- entire GitHub/Azure/cloud IP ranges;
- entire countries;
- unrestricted monitoring headers visible to untrusted clients.

Use the narrowest provider-supported exception for the proven false-positive control, or use another trusted validation source.

## Crawler evidence levels

Keep evidence classes explicit.

### 1. UA simulation

A request manually sets a crawler-like User-Agent.

Useful for:

- detecting obvious User-Agent blocking;
- comparing normal and crawler-like treatment from the same origin;
- reproducing a custom WAF rule that keys directly on a User-Agent.

Not proof of:

- proprietary crawler identity;
- provider IP ownership;
- reverse-DNS verification;
- cryptographic/Web Bot Auth verification;
- indexing;
- AI citation.

### 2. Provider/security-event verification

Security events or official provider verification identify the bot/crawler using the provider's current mechanism.

This is stronger evidence for crawler identity, but still does not prove indexing or citation.

### 3. Search/answer-engine observation

Search Console, webmaster tooling, logs, referral evidence, or reproducible answer-engine observations provide downstream evidence. Route outcome measurement to `ai-search-measurement` and GEO interpretation to `generative-engine-optimization`.

## HTTP 200 body rule

Never classify crawler access from status alone.

Confirm representative evidence such as:

- canonical page title;
- expected body text/entity marker;
- canonical link/metadata where relevant;
- response size/content class when useful;
- absence of a terminating challenge/interstitial/login shell.

Challenge-related JavaScript strings can legitimately appear inside a normal CDN-served page, so simple keyword matching can create false positives. Prefer a combination of status, title/body markers, content structure, and challenge-specific evidence.

## Relationship to GEO

`generative-engine-optimization` owns business intent, entity authority, answer-ready content, machine-discovery surfaces, authority, and measurement design.

`crawler-edge-access-audit` owns the transport/security question: can intended public content actually be fetched through the effective edge policy?

A healthy GEO path is therefore:

```text
entity + content authority
        ↓
SEO/index intent
        ↓
edge crawler accessibility
        ↓
answer-engine observation
        ↓
measured iteration
```

Technical accessibility does not guarantee indexing, ranking, citation, referral, or conversion.

## Release evidence template

Record at minimum:

- environment/domain and timestamp;
- representative routes;
- effective security headers;
- CSP policy/origin inventory/exceptions;
- browser regression results;
- passive sensitive-path results without values;
- edge products and terminating rules investigated;
- crawler-access matrix with evidence class;
- response-body/title/content evidence;
- remediations and rollback path;
- unavailable evidence;
- residual risk;
- independent review outcome.

## Completion rule

Do not claim the release is `secure`, `crawler-safe`, `AI-search ready`, or free of vulnerabilities from one scan or one simulated crawler request. State exactly what was observed and which risks remain unverified.
