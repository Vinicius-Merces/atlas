# Capability Evaluation Model

ATLAS capability quality is measured before the catalog is expanded further.

The model separates three questions that must not be collapsed into one score:

1. **Skill quality**: is each skill structurally complete, bounded, evidence-oriented, and context-disciplined?
2. **Skill routing**: does discovery/trigger language distinguish the intended skill from neighboring capabilities?
3. **Agent overlap**: do durable responsibilities remain distinguishable, or has procedural growth created redundant personas?

## Measurement principle

A metric is evidence about the repository, not proof of live-model behavior.

ATLAS therefore uses deterministic static measurements as a baseline and labels them honestly:

- structural score is a contract-quality measurement;
- lexical routing is a retrieval proxy;
- pairwise agent overlap is an ambiguity proxy;
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

## Baseline policy

The first complete measurement becomes the comparison baseline.

Afterward, aggregate metrics must not regress silently; new skills must meet the current skill contract; material routing regressions require explanation or correction; near-duplicate agent purpose is blocking until clarified; and thresholds may tighten only after measuring the current catalog.

## P1 admission gate

Before implementing the P1 capability layer, ATLAS must measure all currently registered skills, measure routing separation, measure all agent pairs, inspect the weakest/colliding results, and confirm P1 work should be skills attached to existing agents unless evidence justifies a new durable role.

This keeps P1 from becoming catalog inflation.
