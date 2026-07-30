# Runtime Handoff Model

A runtime handoff transfers execution responsibility without transferring
ownership of canonical project knowledge.

## Required handoff data

- Task ID
- Source runtime
- Target runtime
- Current state
- Completed steps
- Pending steps
- Changed files
- Validation already run
- Review evidence
- Assumptions
- Remaining risks
- Context pack reference
- Checkpoint reference

## Handoff rule

The receiving runtime resumes from evidence. It does not silently repeat,
discard, or reinterpret completed work.
