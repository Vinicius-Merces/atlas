---
name: ai-system-design
description: "Design an AI-enabled system with explicit capabilities, limitations, data flow, and evaluation."
---

# AI System Design Skill

## Purpose

Design an AI-enabled system with explicit capabilities, limitations, data flow,
and evaluation.

## Inputs

- User need
- Available data
- Model constraints
- Tool requirements
- Risk classification

## Procedure

1. Define intended and prohibited uses.
2. Choose model interaction pattern.
3. Design context, retrieval, and tools.
4. Define structured outputs and fallbacks.
5. Identify security and privacy risks.
6. Define evaluations.
7. Define cost, latency, and monitoring.

## Output

- Architecture
- Data flow
- Model responsibilities
- Tool permissions
- Evaluation plan
- Risks and controls

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
