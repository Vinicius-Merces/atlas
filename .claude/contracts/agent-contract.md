# Agent Contract

Every ATLAS agent must define the following.

## Identity

- Name
- Mission
- Authority level

Domain is expressed through Mission; a separate Domain field that restates
Mission is redundant and must not be added.

## Canonical runtime label

Every agent Markdown file must define a non-empty YAML frontmatter `description`.
This field is the canonical human-facing purpose label for the agent across ATLAS
runtime adapters, generated catalogs, selectors, and routing surfaces.

The description must:

- say what outcome or responsibility the agent owns;
- be specific enough to distinguish the agent from adjacent roles;
- be concise enough to scan in a runtime picker or hover/description surface;
- prefer action-oriented language over generic labels such as "expert" or "helper";
- remain semantically equivalent across Claude Code, Codex, and generated views.

Do not create a second free-form `label` field that can drift from `description`.
Runtime adapters may translate the canonical description into a native display
field, but they must not change its meaning.

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
