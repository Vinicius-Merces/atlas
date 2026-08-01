# Agent Contract

Every ATLAS agent must define the following.

## Identity

- Name
- Mission
- Authority level

Domain is expressed through Mission; a separate Domain field that restates
Mission is redundant and must not be added.

## Scope

- What the agent owns
- What the agent may change
- What the agent must not change

## Inputs

- Required context
- Optional context
- Dependencies

## Outputs

- Expected artifacts
- Required structure
- Validation evidence

## Collaboration

- Agents consulted before execution
- Agents consulted after execution
- Escalation targets

## Quality gates

- Domain-specific acceptance criteria
- Testing obligations
- Documentation obligations

## Behavioral requirements

An agent must:

- Stay within scope.
- Preserve existing contracts.
- Use project memory and rules.
- Report uncertainty.
- Avoid duplicating other agents' responsibilities.
- Provide evidence for completion.

An agent must not:

- Invent project facts.
- Hide failed validation.
- Make destructive changes without approval.
- Promote temporary assumptions to permanent memory.
