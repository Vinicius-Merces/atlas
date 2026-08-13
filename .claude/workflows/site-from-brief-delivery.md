# Site From Brief Delivery Workflow

## Trigger

A user asks ATLAS to create or materially rebuild a public website, landing page, portfolio, content site, campaign experience, or other user-facing web property from a business/product brief.

## Objective

Move from brief to a distinctive, responsive, accessible, fast, measurable, search-ready production site without degrading into a generic template or leaving forms/content/integrations as ungoverned afterthoughts.

## Inputs

- Business/product brief, target audience, brand constraints, desired outcomes, acceptance criteria, domain/deployment context, and non-functional constraints.
- Existing site/content/data/integrations when this is a rebuild.
- Reference material and visual preferences, treated as direction rather than copy targets.
- Authoritative conversion state, content ownership/editorial needs, analytics requirements, and privacy/security constraints.
- Supported browsers/devices plus performance and accessibility expectations.

## Sequence

1. Synthesize the brief and conversion/information objective with `project-brief-synthesis` and product/UX ownership.
2. Establish visual thesis with `interface-visual-direction`; use `frontend-stack-selection` before introducing motion/3D libraries.
3. Select/instantiate the closest blueprint and define content architecture.
4. Run `cms-content-modeling` when content will be edited or reused outside source code.
5. Design lead/contact/booking/configuration mutations with `form-mutation-design`.
6. Add `file-upload-storage-design` or `application-search-design` only when the journey requires them.
7. Implement using design-system and Frontend Craft constraints; apply `motion-choreography` / `immersive-3d-experience` only where justified.
8. Add `rate-limit-abuse-control` to public or expensive actions.
9. Validate analytics and conversion behavior with `analytics-implementation-audit` and `conversion-funnel-review` when measurable acquisition is in scope.
10. Run accessibility, responsive, visual regression, performance and real-browser validation.
11. Run `seo-technical-audit`, `structured-data-validation`, `content-discoverability-review`, and `supply-chain-risk-audit` as applicable.
12. Complete `frontend-craft-review`, `web-production-assurance-review`, and `full-stack-delivery-review` independently before production approval.

## Required lifecycle

1. **Understand** - Resolve audience, jobs-to-be-done, brand intent, content authority, conversion objective, integrations, constraints, and production target.
2. **Inspect** - Read existing implementation/content and deployed behavior when present; identify reusable assets and regressions that must not be carried forward.
3. **Plan** - Select blueprint, information architecture, visual thesis, component/system strategy, applicable P2 primitives, quality gates, evidence, and release path.
4. **Execute** - Implement incrementally, preserving authoritative mutation/content state and deliberate visual authorship.
5. **Validate** - Exercise representative viewports, keyboard/accessibility, negative form/provider states, performance, browser behavior, analytics, crawl/index, and structured-data evidence as applicable.
6. **Review** - Complete independent Frontend Craft, Web Production Assurance, and Full-Stack Delivery review gates.
7. **Document** - Record durable content/model decisions, integrations, deployment configuration, residual risks, and evidence.
8. **Deliver** - Ship only after blocking findings are resolved and production behavior matches the brief.

## Responsible agents

- `product-manager` / `product-architect`: business outcome and scope.
- `ux-director` / `content-designer`: journey, information architecture, content intent.
- `frontend-engineer` / `design-system-engineer`: premium implementation.
- `backend-engineer` / `integration-engineer`: server mutations and external providers.
- `qa-engineer`, `security-engineer`, and independent reviewers: evidence and release gates.

## Decision points

- Which blueprint best matches the product without forcing template aesthetics?
- Is content code-owned or editor-owned, and does that justify a CMS?
- What state proves a real conversion rather than a client-side success message?
- Which interactions justify Motion, GSAP, WebGL/3D, or no extra library at all?
- Do uploads, search, email, external APIs, or rate/resource controls actually apply?
- Which public pages should be crawlable/indexable, canonical, structured, or intentionally excluded?
- What evidence is required before the design can be called premium and release-ready?

## Validation

- Browser-test the primary conversion and navigation journeys on representative phone/tablet/desktop sizes.
- Prove form success against authoritative downstream state, plus validation, denial, duplicate, and provider-failure paths.
- Preserve keyboard/focus/reduced-motion accessibility and performance budgets.
- Inspect deployed crawl/index/canonical/sitemap/structured-data behavior rather than source configuration alone.
- Reject generic-template visual output that cannot explain its brand/product rationale.

## Failure handling

- Do not claim completion when a primary journey, required viewport, accessibility path, or production integration is unverified.
- Do not replace missing brand/product direction with generic component-library defaults.
- Do not treat a UI success state as authoritative when server/provider state failed or remains ambiguous.
- Do not expose credentials, private content, uploads, or provider keys to the browser to accelerate implementation.
- Do not add motion/3D that breaks reduced-motion, mobile performance, navigation, content legibility, or conversion tasks.
- When deployed SEO/browser behavior contradicts source configuration, treat the deployed evidence as the defect to resolve.

## Completion criteria

The deployed site preserves its visual thesis across viewports, critical interactions work under negative states, applicable content/search/storage primitives are governed, Frontend Craft and Web Production Assurance are approved, and release evidence is reproducible.
