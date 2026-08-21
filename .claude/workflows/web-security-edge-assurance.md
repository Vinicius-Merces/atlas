# Web Security and Edge Assurance Workflow

## Trigger

A public web project or release changes browser security headers, CSP, third-party runtime origins, CDN/WAF/bot behavior, crawler access, machine-discovery policy, or exposes uncertainty about sensitive public files/configuration.

## Objective

Produce release evidence that browser security headers are intentional and effective, sensitive configuration is not publicly exposed, trusted integrations still work, and required search/AI crawlers are not accidentally blocked by edge security controls.

## Inputs

- Request, affected routes/domains, release risk, and critical integrations
- Production or production-equivalent HTTP endpoint
- Framework/server/CDN header configuration
- CDN/WAF/bot/AI-crawler policies and security-event evidence when available
- Current robots/sitemap/canonical/index intent
- Browser/E2E tooling and safe test data

## Sequence

1. **Map public security scope**
   - Read `framework/web-security-edge-assurance-model.md`.
   - Identify browser headers, third-party origins, sensitive-path risk, edge controls, and crawler/discovery requirements.

2. **Audit security headers and CSP**
   - Run `web-security-header-audit`.
   - Inventory actual origins before changing CSP.
   - Preserve release-critical analytics, conversion, chat, auth, payment, API, storage, font/image, and navigation behavior.

3. **Audit sensitive public paths**
   - Use passive GET/HEAD probes only for relevant high-risk paths.
   - Inspect any HTTP 200 body for secret-like content without printing values.
   - Route suspected credential exposure to `secret-environment-audit`; require rotation/revocation when applicable.

4. **Audit edge and crawler access**
   - Run `crawler-edge-access-audit` when SEO/GEO/public crawler access matters or edge/bot rules changed.
   - Map rule ordering across CDN, WAF, bot products, AI crawler controls, challenges, geo/IP/ASN rules, access gateways, and rate limits.
   - Keep `UA simulation` separate from verified proprietary crawler evidence.

5. **Run rendered browser regression**
   - Run `browser-flow-validation` for critical journeys affected by CSP or edge changes.
   - Inspect console CSP violations, `blocked:csp`, failed network requests, challenge loops, redirects, and third-party integration behavior.

6. **Compose adjacent assurance**
   - Use `seo-technical-audit` for canonical/index/robots/sitemap mechanics.
   - Use `generative-engine-optimization` for GEO strategy, answer-ready content, and crawler business intent.
   - Use SaaS production trust for auth/data/provider boundaries.
   - Use rate-limit/abuse, privacy, accessibility, performance, and supply-chain gates when material.

7. **Independent review**
   - Run `.claude/reviews/web-security-edge-assurance-review.md` after implementation and validation.

8. **Record evidence and continuity**
   - Record effective headers, CSP origin inventory/exceptions, passive path results, edge/crawler matrix, browser evidence, provider limitations, and residual risk.

## Responsible agents

- `security-engineer`: primary owner of CSP/header threat model, sensitive-path findings, WAF/bot security tradeoffs, and bypass review.
- `qa-engineer`: independent external HTTP/browser evidence and release outcome.
- `test-automation-engineer`: deterministic passive probes, body/challenge assertions, and regression diagnostics.
- `frontend-engineer`: implements framework-side headers/CSP and fixes browser integration regressions.
- `platform-engineer`: owns CDN/WAF/edge configuration when present.
- `orchestrator`: composes adjacent SEO/GEO/trust gates and preserves reviewer independence.

## Decision points

- Is CSP absent, permissive, staged Report-Only, or enforced?
- Which third-party origins are real runtime dependencies rather than speculative allowlist entries?
- Is an unsafe CSP token unavoidable, temporary, or removable?
- Are sensitive paths denied by the app, origin, CDN/WAF, or simply absent?
- Which edge product/rule terminates a blocked crawler request?
- Is the result an ordinary-client block, crawler-UA block, verified-bot decision, challenge, auth rule, rate limit, or origin failure?
- Does a 200 response contain the real page or an interstitial/degraded shell?
- Can a narrow exception solve the false positive without broadly weakening bot/WAF protection?

## Validation

- Effective production-equivalent security headers inspected on representative routes.
- CSP origin inventory reconciled with actual network/runtime behavior.
- Critical integrations exercised with no unexplained CSP/network breakage.
- Relevant sensitive paths return 403/404 or harmless content, with no secret-like values exposed.
- Required crawler/discovery routes tested through the production edge when in scope.
- Simulated user-agent evidence explicitly labeled as diagnostic only.
- Broad security bypasses rejected unless governed by an explicit exceptional risk decision.
- Independent review completed for significant releases.

## Failure handling

- Do not remove analytics, ads, chat, auth, payments, or API behavior merely to simplify CSP.
- Do not add `*`, broad `https:`, `'unsafe-eval'`, or blanket bot allowlists just to make tests green.
- Do not treat `robots.txt` as secret protection.
- Do not log secret values discovered by passive probes.
- Do not call a crawler verified because a forged/simulated User-Agent received 200.
- Do not call a 200 response successful if the body is a challenge/interstitial or lacks authoritative page content.
- Critical/High findings or missing release-critical evidence block unconditional approval.

## Completion criteria

- Browser security headers and CSP have evidence-backed policy and exceptions.
- Critical integrations remain functional under the effective policy.
- Sensitive public-path exposure has been checked proportionally to stack/risk.
- Edge/WAF/bot behavior is mapped when it can affect release or crawler access.
- Required search/AI discovery is not accidentally blocked by known edge policy.
- Residual limitations are explicit, including where proprietary crawler identity could not be independently verified.
