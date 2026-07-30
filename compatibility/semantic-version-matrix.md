# Semantic Version Compatibility Matrix

| Source | Target | Expected compatibility | Migration |
|---|---|---|---|
| alpha.14 | beta.1 | Transitional-compatible | Replace cumulative files and review beta notes |
| beta.1 | later beta patch | Backward-compatible by default | Review changelog |
| beta.x | 0.1.0 stable | Migration guidance required | To be defined |
| experimental adapter | later adapter version | Not guaranteed | Review adapter notes |

## Rules

- Beta patch releases should preserve stable contract semantics.
- Experimental adapters may change structure before stable support.
- Breaking changes require explicit classification and migration guidance.
