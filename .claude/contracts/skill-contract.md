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
