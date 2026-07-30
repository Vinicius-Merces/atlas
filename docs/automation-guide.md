# Automation Guide

## Automate stable decisions

Automation works best when the expected behavior is explicit and repeatable.

## Make failure useful

A failed check should explain what happened, why it matters, and how to correct
it.

## Preserve local reproducibility

Critical CI checks should be runnable locally with the same inputs.

## Avoid hidden mutation

Validation should not silently rewrite project files. Formatting or generation
steps should be explicit.

## Review automation drift

Tool versions, runtime assumptions, and policy requirements change. Automation
needs ownership and review.
