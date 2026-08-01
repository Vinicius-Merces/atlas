---
name: cloud-cost-analysis
description: "Analyze cloud or platform spending and identify evidence-based optimization opportunities."
---

# Cloud Cost Analysis Skill

## Purpose

Analyze cloud or platform spending and identify evidence-based optimization
opportunities.

## Inputs

- Billing data
- Resource inventory
- Usage metrics
- Service objectives
- Ownership and allocation tags

## Procedure

1. Establish period and baseline.
2. Allocate cost by owner, product, environment, and service.
3. Identify idle, oversized, duplicate, or anomalous resources.
4. Analyze storage, transfer, compute, and managed-service cost.
5. Evaluate commitments and pricing models.
6. Protect reliability and performance constraints.
7. Estimate savings, effort, confidence, and risk.
8. Define verification metrics.

## Output

- Cost baseline
- Allocation gaps
- Optimization opportunities
- Savings estimate
- Risks and trade-offs
- Owners
- Validation plan

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
