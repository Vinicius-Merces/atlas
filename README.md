# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.4`  
**Status:** Beta / Universal Runtime Contract and Conformance

ATLAS coordinates software engineering through shared memory, specialized agents,
reusable skills, workflows, review gates, validation, and runtime adapters.

## Beta.4 milestone

Claude Code and Codex now implement one provider-neutral runtime contract.

| Runtime | Support |
|---|---|
| Claude Code | Beta-supported canonical runtime |
| Codex | Beta-supported synchronized runtime |
| Gemini | Experimental |
| Cursor | Experimental |

## Added in beta.4

- Universal Runtime Contract
- Runtime declarations for Claude Code and Codex
- Machine-readable task routing
- Context packs
- Shared task and execution-result envelopes
- Runtime conformance validation
- Cross-runtime conformance tests
- Runtime-neutral evidence protocol

## Validation

```bash
python scripts/validate_runtime_contract.py
python scripts/validate_conformance.py
python scripts/run_conformance_tests.py
```

Runtimes may differ in syntax and tools, but not silently in responsibility,
memory, governance, validation, or evidence.
