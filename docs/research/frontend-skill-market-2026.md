# Frontend Agent Skills — Market Review 2026

## Decision

ATLAS should strengthen its existing Frontend Craft sequence instead of vendoring a large external skill wholesale. The current architecture already separates visual direction, motion, responsive review, visual regression, performance, accessibility, and independent craft review. The gap exposed by RelayOps was enforcement: “premium” could still reach implementation without a frozen product-specific direction, signature interaction, state matrix, or rendered proof.

## Sources evaluated

| Source | Useful pattern | ATLAS decision |
|---|---|---|
| [Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | Start from the subject's real world, take one justified aesthetic risk, make the first viewport a thesis, and reject template defaults. | Integrated into `interface-visual-direction` as product vocabulary, signature moment, aesthetic risk, and relabeling test. |
| [Vercel Web Interface Guidelines](https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md) | Fetch current interface rules and review terse, actionable findings. | ATLAS keeps its broader independent gates; current-rule retrieval is useful for future automated review, but was not vendored. |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Searchable design intelligence, prioritized accessibility/touch/performance/layout/typography/motion rules, and persistent design-system decisions. | ATLAS adopted the priority mindset and persistent direction contract; it did not copy the external dataset or scripts. |
| [Vercel shadcn skill](https://github.com/vercel-labs/agent-skills/tree/main/skills) | Product-specific composition, state completeness, consistent density/tokens, and avoidance of untouched component defaults. | Added explicit SaaS shell and state-completeness checks while remaining framework-agnostic. |
| [StyleSeed](https://github.com/bitjaru/styleseed) | Enforcement layer, single-accent discipline, tabular numbers, exception-first status color, coherent radii/shadows, and anti-drift design locks. | Incorporated as concise token and review heuristics, without importing its multi-skill package. |
| [Claude Code Frontend Design Toolkit](https://github.com/wilwaldon/Claude-Code-Frontend-Design-Toolkit) | A strong stack combines direction, theming, motion, browser eyes, testing, and documentation while controlling context cost. | Confirms ATLAS's capability sequence; strengthened browser-proof requirements rather than adding redundant MCPs or agents. |

## Changes made

- `framework/frontend-craft-model.md`: mandatory premium delivery contract and operational SaaS authorship rules.
- `interface-visual-direction`: product vocabulary, justified risk, signature moment, state/motion inventory, viewport evidence, and unrelated-product relabeling test.
- `frontend-craft-review`: High finding for generic sidebar/cards/table shells under premium briefs; explicit state, motion, and rendered-proof gates.
- `saas-from-brief-delivery`: freezes frontend direction before UI implementation and rejects source/build-only visual approval.

## Why not install everything

Large skill packs can duplicate responsibilities, consume context, drift across runtimes, and turn stylistic databases into unexamined prescriptions. ATLAS benefits more from a small canonical contract that routes to its existing specialized capabilities and requires real browser evidence. External skills remain research inputs, not hidden authorities.
