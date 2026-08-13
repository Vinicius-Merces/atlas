# Capability Quality After Accessibility Remediation — 2026-08-13

This record captures the deterministic capability-quality measurement after the P1 Production/Product Quality Pack and the remediation of the legacy `accessibility-audit` skill.

Static capability metrics are diagnostic proxies. They do not claim live Claude Code or Codex routing accuracy.

## Inventory

- Skills: **117**
- Agent surfaces: **87**
- Unique agent pairs: **3741**
- Curated routing fixtures: **31**

## Skill quality

- Mean: **88.46**
- Median: **88**
- Minimum: **71**
- P25: **86.0**
- P75: **90.0**
- Grades: **A 35 / B 73 / C 9 / D 0**

The previous measurement contained one D-grade capability with a minimum score of 60. The remediation of `accessibility-audit` removed the D grade and raised the catalog minimum to 71 without weakening evaluator thresholds.

The remediated audit now includes explicit scope, trigger conditions, inputs, procedure, outputs, dependencies, limitations, and validation. It covers semantic structure, keyboard and focus behavior, form validation, zoom/reflow, motion preferences, dynamic announcements, custom ARIA widgets, canvas/WebGL alternatives, negative states, and manual plus automated evidence.

## Routing proxy

- Curated top-1: **74.2%**
- Curated top-3: **87.1%**
- Curated top-5: **93.5%**
- Description pairs >= 0.55 similarity: **1**
- Description pairs >= 0.70 similarity: **0**

## Agent overlap

- Agent pairs >= 0.55 similarity: **0**
- Agent pairs >= 0.70 similarity: **0**
- Cross-domain pairs >= 0.55 similarity: **0**

## Validation evidence

The final remediation commit passed capability taxonomy validation, discovery metadata validation, capability measurement, 176 contract tests, the portable release profile, runtime/Codex synchronization, 277 full-suite tests, and cumulative/recovery/incremental release-artifact validation.

## Decision

**Approved.** The accessibility remediation improved actual procedure quality rather than gaming the scoring model. No new agent was introduced and no routing or overlap regression was observed.
