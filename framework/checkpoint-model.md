# Checkpoint Model

A checkpoint is an immutable snapshot of task execution at a meaningful
boundary.

## Checkpoint contents

- Task identity
- Runtime
- Timestamp
- Current state
- Completed work
- Pending work
- Changed files
- Validation
- Reviews
- Assumptions
- Risks

Checkpoints should be created before runtime handoff, risky migration, large
refactor, or session termination.
