# Workflow Contract

Every workflow must define:

- Trigger
- Objective
- Inputs
- Sequence
- Responsible agents
- Decision points
- Validation
- Failure handling
- Completion criteria

## Required lifecycle

```text
Understand
→ Inspect
→ Plan
→ Execute
→ Validate
→ Review
→ Document
→ Deliver
```

## Exceptions

A step may be skipped only when:

- It is demonstrably unnecessary.
- The reason is documented.
- No quality or safety gate is bypassed.

## Failure handling

A workflow must not silently succeed when:

- Tests fail.
- Required context is unavailable.
- A contract is broken.
- A destructive action lacks approval.
