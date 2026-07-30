# Testing Guide

## Choose tests by risk

High-risk behavior requires stronger and more independent evidence.

## Prefer stable boundaries

Unit tests should validate domain behavior. Integration tests should validate
contracts. End-to-end tests should protect critical journeys.

## Treat flaky tests as defects

Tests that fail unpredictably reduce trust and slow delivery. Isolate causes,
improve diagnostics, or replace low-value instability.

## Test failure paths

Validate timeouts, invalid inputs, dependency failure, empty states, partial
success, and recovery.

## Preserve evidence

Release decisions should reference the tests and checks that actually ran.
