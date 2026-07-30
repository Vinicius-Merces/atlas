# Database Migration Analysis Skill

## Purpose

Assess schema and data migrations for integrity, compatibility, and operational
risk.

## Inputs

- Current schema
- Proposed schema
- Application consumers
- Data volume
- Availability requirements

## Procedure

1. Classify additive, transitional, or destructive change.
2. Identify read and write compatibility.
3. Evaluate locks and execution time.
4. Define dual-read or dual-write needs.
5. Plan backfill and validation.
6. Define rollback or forward-fix strategy.
7. Identify monitoring and stop conditions.

## Output

- Migration class
- Compatibility risks
- Execution plan
- Data validation
- Rollback or forward-fix
- Release constraints
