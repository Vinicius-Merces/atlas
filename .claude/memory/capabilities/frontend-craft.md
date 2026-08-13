---
atlas_type: capability-overlay
capability: frontend-craft
purpose: Produce distinctive, production-ready web interfaces through deliberate visual direction, stack selection, motion/3D discipline, responsive evidence, performance budgets, and independent anti-template review.
canonical_model: framework/frontend-craft-model.md
preferred_workflow: frontend-feature-delivery
required_review: frontend-craft-review
primary_agent: frontend-engineer
collaborating_agents:
  - ux-director
  - design-system-engineer
  - qa-engineer
  - performance-engineer
skills:
  - frontend-stack-selection
  - interface-visual-direction
  - motion-choreography
  - immersive-3d-experience
  - responsive-layout-audit
  - visual-regression-review
  - frontend-craft-review
  - web-performance-field-readiness
---

# Frontend Craft

Capability navigation note for the ATLAS frontend craft overlay.

The canonical rules live in `framework/frontend-craft-model.md` and `framework/capabilities/frontend-craft.yaml`. This note exists for Obsidian/navigation and must not become a second source of truth.

## Delivery path

`interface-visual-direction` → `frontend-stack-selection` → implementation → optional `motion-choreography` / `immersive-3d-experience` → `responsive-layout-audit` → `visual-regression-review` → `web-performance-field-readiness` → independent `frontend-craft-review`.

## Runtime principle

Claude Code consumes canonical skills from `.claude/skills/`. Codex-native wrappers in `.agents/skills/` must preserve the same meaning and point back to the canonical source.
