---
name: browser-flow-validation
description: "Validate critical user journeys in a real browser when releases or frontend changes need evidence for navigation, forms, auth states, errors, console/network failures, and cross-viewport behavior."
---

# Browser Flow Validation

## Purpose

Prove that critical user journeys work in a rendered browser, not only in unit tests, static analysis, component previews, or implementation reasoning.

## Trigger conditions

Use when a user-facing web change affects navigation, forms, authentication state, checkout/contact flows, routing, async loading, browser APIs, responsive behavior, or release-critical journeys.

## Inputs

- Acceptance criteria and critical user journeys
- Safe test environment and representative test data/accounts
- Current browser/E2E tooling and configuration
- Relevant frontend/backend routes and integration contracts
- Known browser, viewport, locale, and authentication requirements

## Procedure

1. Identify the smallest set of journeys whose failure would make the release materially broken.
2. Define observable outcomes for every step instead of relying on clicks without assertions.
3. Use project-native browser automation when available. Prefer Playwright when the repository already uses it or when a new browser runner is justified; do not add a second E2E stack casually.
4. Start each scenario from a controlled browser context, fixture, and authentication/data state so one test does not depend on another.
5. Exercise navigation, redirects, forms, validation, loading, success, empty, and recoverable error states that matter to the journey.
6. Assert user-visible outcomes with auto-waiting browser assertions rather than fixed sleeps.
7. Capture console errors, failed network requests, unexpected redirects, hydration/runtime exceptions, blocked resources, and relevant HTTP failures.
8. Test direct URL entry and refresh for routed application states that users or crawlers may reach without prior navigation.
9. Exercise representative mobile and desktop viewports when layout or interaction changes could alter the journey. Use `responsive-layout-audit` for deeper composition coverage.
10. Exercise keyboard/focus behavior for critical form and navigation interactions when applicable.
11. Capture screenshots, trace, video, request evidence, or equivalent diagnostics on failure according to the project's tooling and data-sensitivity rules.
12. Keep destructive or financial actions in safe sandbox/test environments and make cleanup explicit.
13. Record browser, viewport, environment, test identity class, data fixture, and exact failed step so evidence is reproducible.

## Outputs

- Critical-journey inventory
- Browser/environment matrix
- Pass/fail evidence by journey
- Console/network/runtime findings
- Reproduction steps and diagnostics
- Residual browser coverage gaps
- Release recommendation

## Limitations

- Browser automation does not replace unit, integration, contract, accessibility, visual-regression, security, or performance testing.
- A single happy-path recording is not evidence of robust behavior.
- Do not use production customer data or irreversible production actions merely to obtain browser evidence.

## Dependencies

- A safe rendered environment reachable by the selected browser tool
- Stable fixtures/test identities appropriate to the journey
- Project-native browser automation when available; Playwright is preferred only when it fits the existing stack and constraints
- `responsive-layout-audit`, `visual-regression-review`, accessibility, SaaS trust, or payment gates when their concerns are in scope

## Validation

- Run every release-critical journey from a clean browser/test state.
- Assert final URL/state and meaningful intermediate outcomes.
- Fail on uncaught runtime exceptions or material console/network failures unless an explicit expected exception is documented.
- Verify at least one recoverable error/failure path for high-risk forms or async journeys.
- Store enough diagnostics to reproduce failures without exposing secrets or unnecessary personal data.
