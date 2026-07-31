# Automation Review Gate

## Scope

Evaluate the in-scope change against this gate's Automation concerns and the checks below. Exclude unrelated implementation concerns unless they create a direct risk for this gate, and report only findings supported by evidence.

## Required evidence

- The request, acceptance criteria, and affected paths.
- The implementation diff or artifacts under review.
- Relevant tests, validator output, logs, decisions, and contracts.
- Any missing evidence, explicitly identified as unavailable.

## Review questions

- Is the automation deterministic?
- Are failures actionable?
- Is local behavior consistent with CI?
- Are secrets protected?
- Is the automation idempotent where needed?
- Is runtime cost acceptable?
- Are side effects explicit?
- Is ownership defined?

## Findings

Record each finding as a fact or hypothesis with its evidence, affected path or behavior, impact, and remediation. State `No findings` only after all required evidence has been inspected.

## Severity

Classify each finding as Critical, High, Medium, Low, or Note using `.claude/contracts/review-contract.md`. Missing mandatory evidence or failed mandatory validation prevents an approval outcome.

## Required actions

For every finding, identify the correction or decision required and how it will be verified. Unresolved Critical or High findings block approval; conditional outcomes must list their conditions.

## Outcome

Record exactly one outcome after the required evidence and mandatory validation are complete:

- Approved
- Approved with conditions
- Changes required
- Blocked
