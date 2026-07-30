# Skill Contract

A skill is reusable expertise or a repeatable technical capability.

## Required metadata

- Name
- Purpose
- Domain
- Trigger conditions
- Inputs
- Outputs
- Dependencies
- Limitations
- Validation method

## Skill responsibilities

A skill should:

- Encapsulate reusable knowledge.
- Avoid project-specific assumptions unless explicitly declared.
- Produce deterministic or reviewable outputs.
- Explain failure conditions.
- Remain smaller than an agent responsibility.

## Skill boundaries

A skill does not own product decisions, cross-domain coordination, or release
approval.

## Quality requirements

- Clear trigger conditions
- Explicit inputs and outputs
- No hidden dependencies
- No secrets embedded
- Validation guidance included
