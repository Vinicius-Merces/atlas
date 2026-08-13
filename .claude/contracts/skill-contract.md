# Skill Contract

A skill is reusable expertise or a repeatable technical capability.

## Required metadata

- Name
- Purpose
- Trigger conditions
- Inputs
- Outputs
- Dependencies
- Limitations
- Validation method

Domain is expressed through Purpose; a separate Domain field that restates
Purpose is redundant and must not be added. Trigger conditions must not
restate Purpose verbatim; state only the scope/evidence condition for
firing.

## Discovery metadata

Every `SKILL.md` must define YAML frontmatter `name` and `description` compatible
with the Agent Skills format used by supported runtimes.

The `description` is the canonical routing and human-facing discovery label for
the skill. It is the source ATLAS exposes to generated catalogs and to runtime
picker, recommendation, hover, tooltip, or description surfaces when the runtime
supports them. ATLAS must not maintain a second free-form hover label that could
drift from this canonical description.

The `description` is a routing contract, not marketing copy. It must state both:

- what repeatable capability the skill provides; and
- when a runtime should activate or recommend it.

Keep the most important trigger terms near the beginning. Avoid broad descriptions
that could match unrelated tasks and avoid vague descriptions that make automatic
discovery unreliable. Descriptions must remain concise and discriminative enough
to scan in runtime discovery UI.

Codex-native wrappers under `.agents/skills/` must preserve the canonical `name`
and `description` exactly. Runtime adapters may translate the description into a
native display field, but they must not change its meaning.

The main `SKILL.md` should remain focused on the procedure. Large reference
material, scripts, examples, or reusable assets should live in bounded companion
resources and be loaded only when needed. This preserves progressive disclosure
and prevents the complete skill library from competing for the runtime context
window.

## Skill responsibilities

A skill should:

- Encapsulate reusable knowledge.
- Avoid project-specific assumptions unless explicitly declared.
- Produce deterministic or reviewable outputs.
- Explain failure conditions.
- Remain smaller than an agent responsibility.
- Prefer executable validation or inspectable evidence when practical.

## Skill boundaries

A skill does not own product decisions, cross-domain coordination, or release
approval.

## Quality requirements

- Clear trigger conditions
- Explicit inputs and outputs
- No hidden dependencies
- No secrets embedded
- Validation guidance included
- Concise, discriminative discovery description
- Canonical description preserved across supported runtime discovery surfaces
- Companion resources loaded only when required
