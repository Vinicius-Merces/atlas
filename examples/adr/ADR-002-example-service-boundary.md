# ADR-002: Keep Email Delivery Behind an Adapter

- **Status:** Accepted
- **Date:** 2026-07-30

## Context

Email delivery may change providers and has provider-specific failures.

## Decision

Application code will depend on an internal email adapter rather than the provider SDK directly.

## Consequences

- Provider changes remain isolated.
- Error translation becomes consistent.
- Adapter maintenance is required.
