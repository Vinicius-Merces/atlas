# RelayOps Frontend Direction — Remediation

## Visual thesis

RelayOps should feel like a calm field-service control room: dense enough for dispatch work, legible under pressure, and visibly governed by a single operational line. The interface should communicate movement from intake to schedule, field execution, evidence, and audit before the user reads every label.

## Product vocabulary

- relay line, station, dispatch, field, evidence, exception, tenant context, audit trail
- work-order identifiers, schedules, priorities, technicians, entitlement versions, correlation IDs
- exception-first status rather than decorative multicolor dashboards

## Signature moment and aesthetic risk

The authenticated dashboard uses a live `Relay Line` built from authoritative work-order counts. A moving tracer communicates continuity between intake, scheduling, field execution, and attention states. The risk is a darker command surface inside an otherwise light operational UI; it is justified because it makes the product model immediately recognizable without converting the SaaS into a marketing page.

## Token grammar

- 8 px-derived spacing rhythm, 6–14 px related radii, one petrol accent plus warm orange exception emphasis
- tabular changing numbers; color reserved for state, priority, focus, and exception
- layered shadows under 10% opacity from a consistent top-left light source
- one outlined SVG icon family; no emoji or repeated icon chips
- strong table, form, detail, empty, success, error, and destructive-state hierarchy

## Motion inventory

- page-stage entrance: orientation after navigation
- active navigation indicator: current location
- Relay Line tracer and live-status breathing: operational continuity
- count interpolation: state emphasis on dashboard entry
- button, row, and panel response: direct-manipulation feedback
- dialog/backdrop transition: spatial continuity
- toast transition and `aria-live`: mutation feedback
- reduced-motion path removes continuous and large movement while preserving state

## Responsive composition

- phone: off-canvas navigation with dismissing scrim, 2×2 Relay Line labels, horizontally scrollable operational tables with an explicit affordance
- tablet: compact sidebar or off-canvas transition, single-column details, retained operational rail
- laptop: dense 214–260 px sidebar and two-column supporting panels
- wide desktop: anchored 1,800 px working canvas with controlled line lengths and denser table space

## Acceptance matrix

- routes: login, protected dashboard, work orders, order detail, customers/dialog, billing, import/export, support
- viewports: 360, 768, 1280, 1920 px
- states: navigation open/closed, dialog open, validation error, mutation success, empty search, billing enabled/revoked, import partial failure, privileged support denial/success, reduced motion
- evidence: screenshots, console errors, page errors, failed requests, HTTP errors, overflow, keyboard/focus, accessible names and contrast observations

