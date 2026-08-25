---
name: web-security-header-audit
description: "Audit public web security headers and CSP using observed runtime origins, sensitive-path exposure checks, and browser validation without breaking trusted integrations."
---

# Web Security Header Audit

## Purpose

Audit and harden browser-facing security headers for public web applications, with special attention to CSP correctness, sensitive public-path exposure, and regression safety for trusted integrations.

## Trigger conditions

Use when a public site is being prepared for production, security headers are missing or changed, CSP is added/tightened, third-party scripts/integrations change, a passive scan reports exposed configuration, or an audit/release needs browser-layer security evidence.

## Inputs

Required:
- public routes/environment or production-equivalent responses;
- framework/server/CDN header configuration;
- current third-party runtime integrations;
- critical browser journeys and integration expectations.

Optional:
- browser console/network evidence;
- CSP violation reports;
- passive sensitive-path probe results;
- analytics/ads/chat/auth/payment/storage/provider documentation;
- secret-environment audit evidence.

## Procedure

1. Inventory effective response headers on representative public routes and redirects. Do not infer production behavior only from source configuration.
2. Evaluate HSTS, CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, framing protection, and relevant CORS behavior.
3. For CSP, inventory actual origins used by scripts, styles, images, fonts, frames, workers, forms, media, and `connect-src` traffic before editing policy.
4. Map release-critical third-party integrations such as analytics, advertising/conversion tracking, authentication, payments, chat, storage, monitoring, maps, and APIs. Record the directive each dependency requires.
5. Start from least privilege. Prefer `default-src 'self'`, `object-src 'none'`, restrictive `base-uri`, and explicit `frame-ancestors`, then add only observed/required sources.
6. Treat `*`, broad `https:`, `'unsafe-inline'`, `'unsafe-eval'`, `data:`, and `blob:` as explicit exceptions requiring a real consumer, threat/risk note, and a narrower-alternative check.
7. Use `Content-Security-Policy-Report-Only` when the dependency inventory is incomplete or production impact is uncertain. Report-Only is a staging mechanism, not a permanent substitute for enforcement without an explicit exception.
8. Run a rendered-browser regression after policy changes. Inspect console CSP violations and network requests such as `blocked:csp`; verify forms, tracking/conversion events, chat, auth/payment flows, APIs, fonts/images, and navigation that are in scope.
9. Passively probe common sensitive public paths relevant to the project. Expected results are normally 403/404 or an intentionally harmless body. Inspect any 200 response for secret-like content without printing values.
10. If usable credentials/private keys may have been exposed, invoke `secret-environment-audit` and require rotation/revocation evidence.
11. Record the final policy, origin inventory, exceptions, effective production headers, browser evidence, unresolved risks, and rollback path.

## Sensitive-path examples

Choose only safe GET/HEAD probes relevant to the stack, for example:

- `/.env`, `/production/.env`, known environment-file variants;
- `/.npmrc`;
- `/.git/config`;
- `/.ssh/authorized_keys`;
- project-relevant service-account/Firebase admin JSON names;
- private-key/config/debug/server-status paths.

Never brute-force large wordlists as part of this skill, and never log secret values.

## Outputs

- Effective security-header matrix by representative route/environment.
- CSP origin/directive inventory and final policy or staged Report-Only policy.
- Integration compatibility evidence.
- Passive sensitive-path findings.
- Required remediations, exceptions, rollback path, and residual risk.

## Dependencies

- `browser-flow-validation` for rendered regression evidence.
- `secret-environment-audit` when sensitive configuration or credentials may be exposed.
- `analytics-implementation-audit` when analytics/conversion collection is release-critical.
- `integration-contract-mapping` when third-party runtime requirements are unclear.
- Current official framework/browser/provider documentation for CSP and integration-specific requirements.

## Limitations

- Header presence does not prove exploit absence.
- A passive path check is not a penetration test and cannot prove the absence of hidden sensitive files.
- CSP can reduce browser exploitability but does not repair server-side authorization, injection, or secret-management defects.
- Report-Only observations depend on actual exercised traffic; unvisited flows can still fail after enforcement.

## Validation

- Confirm effective production or production-equivalent headers, not only configuration source.
- Verify CSP parses and is consistent with the observed origin inventory.
- Verify `object-src`, `base-uri`, and framing policy are intentionally restrictive.
- Verify every broad source or unsafe token has a documented consumer and residual-risk note.
- Exercise critical integrations in a real browser and inspect console/network for unexplained CSP blocking.
- Verify representative sensitive paths do not return usable secret/private-key material.
- Route significant work through `web-security-edge-assurance-review`.
