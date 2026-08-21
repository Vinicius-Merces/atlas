# Web Security and Edge Assurance Review Gate

## Scope

Independently evaluate a significant public-web release across browser security headers/CSP, sensitive public-path exposure, CDN/WAF/bot behavior, and intended search/AI crawler access.

This review complements Web Production Assurance, SaaS Production Trust, and GEO. It does not replace deeper penetration testing or provider-specific security review.

## Required evidence

- Affected domains/routes, release scope, and critical integrations
- Effective production or production-equivalent response headers
- CSP origin/directive inventory and exception rationale
- Browser console/network results for affected critical journeys
- Passive sensitive-path results without secret values
- CDN/WAF/bot/AI-crawler configuration/security-event evidence available to the project
- Dated crawler-access matrix when search/AI discovery is in scope
- External HTTP evidence including response-body/content markers, not status alone
- Adjacent SEO/GEO/trust evidence required by scope

Missing release-critical evidence prevents an unconditional Approved outcome.

## Review questions

### Security headers and CSP

- Are headers verified from effective responses rather than inferred only from config?
- Is CSP based on an observed origin inventory?
- Are `object-src`, `base-uri`, and framing restrictions intentionally safe?
- Are wildcard/broad schemes, `data:`, `blob:`, `'unsafe-inline'`, or `'unsafe-eval'` justified by a real consumer and residual-risk note?
- If Report-Only is used, is there a concrete path to enforcement?
- Did browser validation prove that analytics/conversion, chat, auth, payments, APIs, fonts/images, and other critical integrations still function?
- Are CSP violations or `blocked:csp` requests unexplained?

### Sensitive public paths

- Were probes passive, bounded, and relevant to the stack?
- Do `.env`, repository metadata, private-key/config, service-account, and debug-path checks avoid usable secret exposure?
- If a 200 response was observed, was its body inspected rather than automatically classified as exposure?
- Were secret values excluded from logs/evidence?
- When exposure was plausible, was credential rotation/revocation handled rather than only deleting code/files?

### Edge and bot security

- Which exact edge layers can terminate the request before the application?
- Are rule ordering and overlapping CDN/WAF/bot/AI-crawler controls understood?
- Does a permissive setting in one product get overridden by an earlier block/challenge rule?
- Was any broad bot, verified-bot, datacenter, country, Azure/GitHub, or IP-range bypass introduced merely to make automation pass?
- Are exceptions narrow, justified, and limited to the control actually causing the false positive?

### Search and AI crawler access

- Are search/retrieval, assistant/user-fetch, training, and unknown automation treated as separate policy categories?
- Are `robots.txt`, meta/X-Robots, sitemap, canonical, and edge behavior coherent with crawler intent?
- Are simulated user-agent results explicitly labeled `UA simulation`?
- Is proprietary/verified crawler identity claimed only when supported by provider/security-event evidence?
- Does HTTP 200 contain authoritative content rather than a Cloudflare/CDN challenge, login/interstitial, or degraded shell?
- Are required SEO/GEO crawlers free from known unintended WAF/bot/challenge/geo/rate-limit blocks?

## Findings

Record each finding with severity, evidence, affected route/control/integration/crawler, security or discovery impact, required remediation, and verification method. State `No findings` only after every applicable evidence source has been inspected.

## Severity

Use `.claude/contracts/review-contract.md`: Critical, High, Medium, Low, or Note.

Normally blocking examples include:

- usable credential/private-key exposure;
- CSP/security-header change that breaks a release-critical flow;
- broad security bypass added solely for CI/crawler convenience;
- known unintended site-wide blocking of required search/AI discovery;
- production behavior contradicting the claimed edge/header policy;
- fabricated claim that a proprietary crawler was verified from user-agent simulation alone.

## Required actions

For every finding, identify the correction, accepted policy exception, or missing evidence and how it will be revalidated. Critical/High findings must be resolved or explicitly governed before approval.

## Outcome

Record exactly one outcome:

- Approved
- Approved with conditions
- Changes required
- Blocked

The sole implementing agent may provide evidence and remediation but must not be the only approver of significant security-edge work.
