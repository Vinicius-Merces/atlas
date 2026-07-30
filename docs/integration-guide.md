# Integration Guide

## Treat failure as part of the contract

Retries, timeouts, partial success, duplication, ordering, and provider outages
must be designed intentionally.

## Own the adapter

External contracts should be isolated behind a maintained adapter when
possible.

## Test real differences

Sandbox behavior may not match production. Document and validate environment
differences.

## Plan deprecation

Integrations should define versioning, migration, and removal before emergency
changes make them unavoidable.
