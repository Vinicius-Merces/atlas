# /atlas-bootstrap

## Purpose

Initialize ATLAS in an existing or new repository.

## Accepted arguments

- Required: a concise request to initialize ATLAS in an existing or new repository.
- Optional: affected paths or artifacts, constraints, risk level, target runtime, and acceptance criteria relevant to this command.

## Preconditions

- Run from the repository root with `AGENTS.md`, relevant memory, and canonical contracts available.
- Confirm that referenced tasks, files, artifacts, or runtime state exist when the command depends on them.
- Inspect repository status and obtain explicit authorization before any destructive or externally visible action.

## Execution workflow

1. Inspect repository state, relevant memory, contracts, and prior task evidence.
2. Validate the accepted arguments and preconditions.
3. Select the responsible agents, closest canonical workflow, and required review gates.
4. Perform the requested operation: initialize ATLAS in an existing or new repository.
5. Run validation proportional to risk and inspect the resulting evidence.
6. Return the completed result, partial work, or blocker without overstating execution.

## Output format

- Repository map
- Initial memory index
- Architecture summary
- Commands and workflows
- Agent recommendations
- Risks and gaps
- Bootstrap completion report

## Failure behavior

- Stop before mutation when required context, authorization, or a mandatory precondition is missing.
- Do not hide failed gates or claim completion, approval, deployment, or release without supporting evidence.
- Report partial completion, the exact blocker, evidence already collected, pending scope, and the next safe action.
