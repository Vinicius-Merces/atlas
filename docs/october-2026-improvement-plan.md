# October 2026 improvement plan

## Preserved decisions

The baseline is `9c15d3c`, including PRs 31–34. Product memory stays in each
product's Git repository; `.claude/memory/` is canonical and Obsidian is a local
derived view. Start/close remain explicit, not an automatic background recorder.
Context limits, complete mandatory instructions, hashes and freshness checks
remain mandatory. No catalog expansion, mandatory inference gateway, paid scanner,
or new executor is introduced.

## Assessment of the supplied audit

The P0 priorities address concrete gaps: discovery trust does not authorize code
execution, result schemas accept completion without functional proof, and model
identifiers alone do not establish continued compatibility. Passing framework
tests does not demonstrate product effectiveness or token savings.

External announcements and model retirement dates are not baked into policy.
Verify provider documentation and actual project access before integration.
Agent Skills format: https://agentskills.io/specification
GenAI conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
AI Search guidance: https://developers.google.com/search/docs/appearance/ai-features
No availability of a dedicated Search Console metric is assumed.

## Sequence and acceptance

| Phase | Deliverable | Acceptance evidence |
| --- | --- | --- |
| 1, P0 | Security Execution Gate | Reviewed source digest, scoped permissions, sandbox receipt, passing secret/dependency evidence; external source without explicit approval fails |
| 1, P0 | Delivery Effectiveness Gate | Functional acceptance cases, immutable hashed evidence, exact task/commit, verified remote checkpoint, explicit pending work; incomplete delivery cannot be recorded completed |
| 1, P0 | Model Lifecycle Guard | Dated model inventory; expired/deprecated/retired/unknown or unevaluated candidates excluded; each fallback independently passes capability/privacy/cost rules |
| 2, P1 | Context sections and hash cache | Optional sections only; whole mandatory instructions; source identity and selection keys; tamper/stale/cross-project invalidation tests; characters and tokens reported separately |
| 2, P1 | GenAI observability | Session-scoped cost, usage, cache, latency p95, fallback/failure metrics; versioned convention mapping; content capture off; measured unknowns never reported as zero |
| 2, P1 | AI Search measurement | Feature detection per property; dated metric definitions and exports; AI/multimodal observations separate from organic totals and conversion attribution |
| 2, P1 | Router evaluation and Ollama doctor | Compare deterministic baseline and evaluated routes offline; explicit endpoint consent before probes; inventory/context/tool support measured, no model decides permission or budgets |
| 3, P1/P2 | Product/browser effectiveness | Project-owned Playwright evidence for critical journeys, screenshots, mobile and accessibility; reviewed outcomes/remaining IDs; no screenshot count as proof of quality |
| 3, P2 | Frontend/growth/skill benchmark | Representative real product cohorts; qualified leads and business outcomes; source/license checks before external adoption; no automatic bulk installs |

## Execution boundary

Phase 1 is an offline evidence admission layer plus an optional explicit remote
Git checkpoint check. It does not create a sandbox, run untrusted scripts, scan
dependencies, infer current provider catalogs, or certify production. Runtimes
must gather evidence with their existing tools and call the gates before the
corresponding action. Independent review and CI remain required before merge.

## Measurement and rollback

Use project-owned task IDs and commit-bound acceptance cases. Record completed
and total items, reopened defects, restarts, unavailable checks and confirmed
remote persistence. Collect an observation window before calculating rates.
Do not publish product sessions into upstream ATLAS. Revert this change as one
commit if compatibility fails; preserve historical records and versioned evidence.

## Deferred work

Phases 2 and 3 are planned, not completed by this phase. Live production checks,
model discovery, paid services, real token-cache savings and adoption across
existing products require separate project evidence. This avoids conflating
framework conformance with product results.
