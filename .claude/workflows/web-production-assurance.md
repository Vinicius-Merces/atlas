# Web Production Assurance Workflow

## Trigger

A public web feature or release changes critical browser journeys, routes/domains/redirects, crawl/index behavior, metadata/sitemaps/robots/canonicals, structured data, browser/edge security controls, or dependency/build inputs with production impact.

## Objective

Deliver evidence that critical journeys work in a rendered browser, browser/edge security controls preserve trusted behavior, intended public pages are technically discoverable/indexable by design, structured data is factual and valid, and changed third-party code/build inputs have received proportionate supply-chain review.

## Inputs

- Request, acceptance criteria, risk, and release scope
- Public route/domain/canonical intent
- Critical user journeys and safe test data
- Deployed or production-equivalent environment
- Browser/E2E tooling
- Robots, sitemap, metadata, structured-data output when applicable
- Security headers/CSP and CDN/WAF/bot policy when applicable
- Dependency manifests, lockfiles, CI/build inputs, and trusted base revision

## Sequence

1. **Map assurance scope**
   - Read `framework/web-production-assurance-model.md`.
   - Classify critical browser journeys, intended-indexable URLs, browser/edge-security changes, structured-data surfaces, and dependency/build deltas.

2. **Audit supply-chain delta when applicable**
   - Run `supply-chain-risk-audit` when dependencies, lockfiles, registries, scripts, CI actions, container bases, plugins, or build inputs changed.

3. **Validate critical browser journeys**
   - Run `browser-flow-validation` for release-critical user paths.
   - Use clean browser/test state and observable assertions; capture console/network/runtime failures and failure diagnostics.

4. **Audit browser and edge security when material**
   - Run `web-security-header-audit` when CSP/security headers, third-party browser origins, or sensitive public-path exposure are relevant.
   - Run `crawler-edge-access-audit` when CDN/WAF/bot/challenge rules or required search/AI crawler access are relevant.
   - Verify effective production responses and real browser/network behavior rather than source configuration alone.
   - Do not treat user-agent simulation as proof of proprietary crawler identity or access.

5. **Audit technical SEO when public discovery matters**
   - Run `seo-technical-audit` against deployed/production-equivalent HTTP behavior.
   - Verify status, redirects, canonical, robots/noindex, sitemap, rendering, metadata, and crawlable internal discovery.
   - When edge security can alter crawler behavior, reconcile SEO evidence with `crawler-edge-access-audit` rather than assuming `robots.txt` is the only gate.

6. **Validate structured data when present**
   - Run `structured-data-validation`.
   - Compare schema output with authoritative/visible page facts and current feature validation.

7. **Compose adjacent gates**
   - Use frontend craft gates for visual/responsive quality.
   - Use SaaS production trust for identity, authorization, RLS, secrets, webhooks, payments, and external API trust.
   - Use GEO/AI-search measurement for answer-engine strategy and observed outcomes when material.
   - Use accessibility/performance/privacy/release gates when material.

8. **Run independent assurance review**
   - A reviewer who did not solely implement the change runs `.claude/reviews/web-production-assurance-review.md`.
   - Significant browser/edge-security changes also require `.claude/reviews/web-security-edge-assurance-review.md`.

9. **Record evidence and continuity**
   - Record browser, security-edge, HTTP/search, structured-data, dependency, review, limitation, and residual-risk evidence.

## Required lifecycle

1. **Understand** - Identify public/release intent, critical journeys, search intent, security-edge impact, dependency delta, environment, and acceptance criteria.
2. **Inspect** - Read canonical memory, current routes, deployment behavior, browser tests, headers/CSP, edge policies, metadata, search controls, manifests/lockfiles, and relevant contracts.
3. **Plan** - Choose representative journeys/URLs/security probes/dependency checks and independent review ownership.
4. **Execute** - Implement without weakening established frontend, trust, security, discovery, or release boundaries.
5. **Validate** - Run applicable browser-flow, security-edge, SEO, structured-data, and supply-chain capabilities with real evidence.
6. **Review** - Complete independent web-production assurance and adjacent required gates.
7. **Document** - Record results, diagnostics, limitations, exceptions, and stable decisions.
8. **Deliver** - Report Approved, Approved with conditions, Changes required, or Blocked according to evidence.

## Responsible agents

- `qa-engineer`: primary independent release/behavior evidence owner.
- `test-automation-engineer`: browser automation, passive HTTP/security probes, fixtures, determinism, diagnostics, and CI integration.
- `frontend-engineer`: implements public-route, rendering, security-header/CSP, metadata, structured-data, and browser fixes while preserving craft/accessibility/performance.
- `content-designer`: validates page/entity meaning, public content hierarchy, titles/descriptions, and factual structured-data claims where assigned.
- `security-engineer`: reviews CSP/security headers, sensitive-path findings, edge/WAF/bot tradeoffs, high-risk dependency/build-input findings, and unsafe bypasses.
- `dependency-manager`: owns dependency delta, source, advisories, maintenance, scripts, and rollback assessment.
- `orchestrator`: routes adjacent gates and preserves reviewer independence.

## Decision points

- Which journeys are truly release-critical rather than every possible click path?
- Is browser automation already available and healthy, or is a new tool justified?
- Do effective production headers match repository intent, and can CSP break a trusted integration?
- Can CDN/WAF/bot/challenge controls alter ordinary or crawler access before the application?
- Which URLs are intentionally indexable, duplicate, redirected, noindex, error, or private?
- Do canonical, sitemap, redirect, and robots/noindex signals agree?
- Does JavaScript rendering hide essential public content or links from the intended fetch path?
- Which structured-data types are actually justified by page meaning and current search support?
- Which dependency/build changes execute code or have production reach?
- Is missing evidence safe to defer, or does it block the release claim?

## Validation

- Run `browser-flow-validation` for release-critical journeys and retain reproducible failure diagnostics.
- Run `web-security-header-audit` when public browser-security headers/CSP or sensitive-path exposure are material.
- Run `crawler-edge-access-audit` when edge security can alter intended search/AI crawler access.
- Run `seo-technical-audit` for public discoverability changes using deployed/production-equivalent HTTP responses.
- Run `structured-data-validation` for every changed schema surface and compare markup with authoritative page facts.
- Run `supply-chain-risk-audit` for changed dependencies/build inputs and retain advisory/dependency-diff/script/provenance evidence.
- Verify applicable adjacent frontend craft, accessibility, performance, SaaS trust, privacy, GEO, and release gates.
- Complete independent reviews required by the affected capability packs.
- Record browser/tool versions, environment, representative URLs, test-state class, security/edge evidence, dependency base, commands, validator output, limitations, and exceptions without secrets.

## Failure handling

- Do not mark a journey passed when assertions were skipped, flaky failures were merely retried away, or console/network errors remain unexplained.
- Do not simplify CSP by disabling a release-critical trusted integration or by adding broad unexplained wildcards/unsafe tokens.
- Do not broadly allow bots, datacenter traffic, or CI-origin IP ranges solely to make crawler validation green.
- Do not claim proprietary crawler verification from a simulated User-Agent.
- Do not change robots/canonical/noindex expectations solely to make a crawler test green without confirming product search intent.
- Do not add fabricated structured data to silence validator warnings.
- Do not accept broad unexplained lockfile churn, malware evidence, critical reachable vulnerability, or opaque install/build execution merely because the application build succeeds.
- Do not use `robots.txt` as private-data protection.
- Do not claim ranking, indexing, AI citation, rich-result display, or complete vulnerability absence from this workflow.
- Unresolved Critical or High findings block approval.

## Completion criteria

- Critical journeys have rendered browser evidence or an explicit blocking gap.
- Applicable security headers/CSP and edge controls have effective production evidence and do not break critical integrations.
- Relevant sensitive public paths have no observed usable secret exposure.
- Intended-indexable public URLs have coherent status/redirect/canonical/robots/sitemap/rendering behavior, including edge behavior where material.
- Changed structured data is valid, non-conflicting, and factually grounded where applicable.
- Changed dependency/build inputs have a reviewed source, delta, execution surface, and advisory risk where applicable.
- Independent review is Approved or Approved with resolved/accepted conditions.
- Residual risks and unavailable evidence are explicit.
