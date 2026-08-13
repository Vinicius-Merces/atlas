---
name: database-schema-review
description: "Review relational database schema changes when tables, columns, constraints, indexes, relationships, partitioning, retention, or migration-sensitive data models change, verifying integrity and query-fit before release."
---

# Database Schema Review

## Purpose

Review database schema design as an executable integrity contract, checking whether the model prevents invalid state, supports expected query patterns, survives change, and makes ownership/lifecycle rules explicit.

## Trigger conditions

Use when adding or changing tables, columns, data types, defaults, generated values, primary/foreign keys, unique/check constraints, indexes, partitioning, soft-delete/retention fields, ownership relationships, or migration-sensitive data structures.

## Inputs

- Current schema and migration history
- Proposed DDL or ORM model changes
- Important read/write query patterns
- Data volume/cardinality estimates where available
- Ownership, tenancy, retention, and deletion rules
- Existing production constraints and compatibility requirements

## Procedure

1. Map each entity, authoritative identifier, ownership boundary, lifecycle state, and relationship.
2. Verify invariant rules are enforced at the strongest practical layer using data types, `NOT NULL`, unique, check, primary-key, foreign-key, or exclusion constraints rather than comments alone.
3. Review defaults and generated values for ambiguity, environment dependence, and historical backfill behavior.
4. Inspect relationship cardinality, cascade behavior, orphan risk, cyclic dependencies, and deletion semantics.
5. Match indexes to observed or expected predicates, joins, ordering, uniqueness, and selectivity; account for write/storage overhead rather than indexing every field.
6. Review composite-index column order, partial/expression indexes, and covering strategies only when query evidence justifies them.
7. Check tenant/owner identifiers and authorization-relevant relations for compatibility with `authorization-boundary-review` and `row-level-security-review` where applicable.
8. Review timestamps, audit fields, status/state columns, retention, soft deletion, archival, and hard-deletion obligations.
9. Assess high-volume growth, hot rows, partitioning/admission thresholds, and whether the schema creates avoidable lock or scan pressure.
10. Trace every schema change through migration, backfill, compatibility window, rollback/forward-fix, and old/new application version coexistence.
11. Validate assumptions against representative query plans or database-native inspection when safe.
12. Record constraints that intentionally remain in application logic and why database enforcement is unsuitable.

## Outputs

- Entity/invariant map
- Constraint findings
- Relationship and lifecycle findings
- Index/query-fit findings
- Migration/compatibility risks
- Required changes, evidence, and residual risk

## Dependencies

- Database schema/DDL or ORM model access
- Representative query patterns or query-plan evidence when performance is material
- `database-migration-analysis` for material migration execution risk
- `row-level-security-review` when row policy participates in authorization

## Limitations

- Does not prescribe one schema style for every database engine.
- Index usefulness depends on workload/cardinality and cannot be proven from names alone.
- Does not replace migration rehearsal on large or high-risk production datasets.

## Validation

- Apply or parse the proposed schema in the closest safe database environment available.
- Execute representative inserts/updates that should both pass and violate key invariants.
- Inspect representative query plans for changed high-value paths when index behavior matters.
- Verify migration/backfill behavior against non-empty data and record unavailable production-scale evidence explicitly.
