# AI Engineering Guide

## Begin with the use case

Do not begin with a model. Begin with the user need, decision boundary, risk,
and success criteria.

## Evaluate representative failures

Evaluation should include ambiguous requests, missing context, adversarial
inputs, unsupported tasks, tool failures, and sensitive-data scenarios.

## Limit permissions

AI systems should receive the minimum data, tools, and write permissions needed
for the task.

## Design fallback behavior

Critical workflows should define what happens when the model is unavailable,
uncertain, too slow, too expensive, or produces invalid output.

## Monitor quality

Track quality signals, human overrides, escalation, latency, cost, tool errors,
and recurring failure patterns.
