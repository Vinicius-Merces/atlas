# /atlas-cost

## Purpose

Analyze technology cost, allocation, unit economics, and optimization options.

## Accepted arguments

- Required: a concise request to analyze technology cost, allocation, unit economics, and optimization options.
- Optional: affected paths or artifacts, constraints, risk level, target runtime, and acceptance criteria relevant to this command.

## Preconditions

- Run from the repository root with `AGENTS.md`, relevant memory, and canonical contracts available.
- Confirm that referenced tasks, files, artifacts, or runtime state exist when the command depends on them.
- Inspect repository status and obtain explicit authorization before any destructive or externally visible action.

## Execution workflow

1. Inspect repository state, relevant memory, contracts, and prior task evidence.
2. Validate the accepted arguments and preconditions.
3. Select the responsible agents, closest canonical workflow, and required review gates.
4. Perform the requested operation: analyze technology cost, allocation, unit economics, and optimization options.
5. Run validation proportional to risk and inspect the resulting evidence.
6. Return the completed result, partial work, or blocker without overstating execution.

## Output format

- Baseline
- Ownership and allocation gaps
- Opportunities
- Savings estimates
- Trade-offs
- Validation plan

## Failure behavior

- Stop before mutation when required context, authorization, or a mandatory precondition is missing.
- Do not hide failed gates or claim completion, approval, deployment, or release without supporting evidence.
- Report partial completion, the exact blocker, evidence already collected, pending scope, and the next safe action.
