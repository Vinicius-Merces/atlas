# Capability Evaluation Model

ATLAS capability quality is measured before the catalog is expanded further.

The model separates four questions that must not be collapsed into one score:

1. **Skill quality**: is each skill structurally complete, bounded, evidence-oriented, and context-disciplined?
2. **Skill routing**: does discovery/trigger language distinguish the intended skill from neighboring capabilities?
3. **Agent overlap**: do durable responsibilities remain distinguishable, or has procedural growth created redundant personas?
4. **Upstream relevance**: has the external ecosystem produced a materially better capability or official guidance that ATLAS should adopt, adapt, watch, or reject?

## Measurement principle

A metric is evidence about the repository, not proof of live-model behavior.

ATLAS therefore uses deterministic static measurements as a baseline and labels them honestly:

- structural score is a contract-quality measurement;
- lexical routing is a retrieval proxy;
- pairwise agent overlap is an ambiguity proxy;
- upstream popularity is discovery evidence, not quality evidence;
- live Claude Code/Codex behavior remains a separate runtime evaluation problem.

## Skill quality dimensions

Each registered skill receives a 0–100 diagnostic score across canonical metadata/discovery, contract-required sections, trigger clarity, validation/evidence strength, dependencies/limitations, and context-size discipline.

Scores are not allowed to reward verbosity by itself. Missing required sections remain contract failures regardless of aggregate score.

## Routing measurements

For every registered skill, the evaluator uses the skill's trigger conditions as a query against canonical discovery descriptions and records whether its own description is recovered in top-1, top-3, and top-5.

A curated fixture set adds realistic requests with expected skills. This is intentionally stricter than checking that files exist but intentionally weaker than claiming live LLM accuracy.

High description similarity is reviewed as a collision signal, not automatically treated as an error.

## Agent-overlap measurements

Agent analysis combines canonical description, Mission, Owns / Responsibilities / Scope text, and taxonomy domain.

The report distinguishes same-domain adjacency from cross-domain similarity and ranks the highest-overlap pairs.

A new agent should not be added merely because a procedure is missing. If the missing behavior can be a skill attached to an existing durable responsibility, prefer the skill.

## Upstream capability review

Use `framework/upstream-capability-radar-model.md` for recurring external research across official runtime/platform documentation, maintained repositories, standards/research, and marketplaces used only as discovery sources.

External candidates must be compared against the current ATLAS catalog before admission.

The preferred order is:

1. improve an existing framework model when the value is a durable principle;
2. improve an existing skill when the durable owner/capability already exists;
3. add a new skill only for a reusable, bounded, materially new procedure;
4. add a tool/dependency only when executable behavior is required and its security/lifecycle cost is justified;
5. add a new agent only for a distinct durable responsibility that cannot be expressed as an existing role plus skill.

Each candidate receives one outcome:

- adopt concept;
- adapt capability;
- integrate tool;
- watch;
- reject/duplicate.

Record provenance, maintenance/freshness, license, overlap, security, context footprint, runtime portability, and exit cost for adopted/integrated candidates.

## Baseline policy

The first complete measurement becomes the comparison baseline.

Afterward, aggregate metrics must not regress silently; new skills must meet the current skill contract; material routing regressions require explanation or correction; near-duplicate agent purpose is blocking until clarified; and thresholds may tighten only after measuring the current catalog.

External ecosystem changes do not invalidate the baseline automatically. They create review candidates that must pass the same ATLAS admission rules.

## P1 admission gate

Before implementing a new capability layer, ATLAS must measure currently registered skills, measure routing separation, measure agent pairs relevant to the scope, inspect the weakest/colliding results, and confirm whether the missing behavior belongs in an existing model/skill before creating a new durable role.

When the change originates from external research, also apply the Upstream Capability Radar intake and record why the candidate is being adopted instead of merely copied.

This keeps ATLAS from becoming catalog inflation or a mirror of marketplace trends.

## Review cadence

Internal capability quality should be checked whenever the catalog changes materially.

External ecosystem review may run monthly or on major Claude Code, Codex, agent-skill-standard, browser/search, AI-provider, or tooling changes. The cadence is a discovery process, not permission for automatic repository mutation.
