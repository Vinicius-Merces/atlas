# Command Contract

Commands expose repeatable user-invoked operations.

## Required definition

- Name
- Purpose
- Accepted arguments
- Preconditions
- Execution workflow
- Output format
- Failure behavior

## Rules

Commands must:

- Delegate domain work to appropriate agents.
- Avoid bypassing governance.
- Validate required context.
- Report partial completion honestly.
- Never hide destructive behavior.
