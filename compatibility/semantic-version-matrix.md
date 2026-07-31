# Semantic Version Compatibility Matrix

| Source | Target | Expected compatibility | Migration |
|---|---|---|---|
| alpha.14 | beta.1 | Transitional-compatible | Replace cumulative files and review beta notes |
| beta.1 | later beta patch | Backward-compatible by default | Review changelog |
| beta.x | rc.x | Backward-compatible by default | Apply the documented beta-to-RC patch or cumulative package |
| rc.x | 0.1.0 stable | Contract-compatible unless explicitly documented | Review stable release notes and support policy |
| 0.1.x stable | later 0.1.x stable | Backward-compatible by default | Apply the documented stable patch or cumulative package |
| experimental adapter | later adapter version | Not guaranteed | Review adapter notes |

## Rules

- Beta patch releases should preserve stable contract semantics.
- Release candidates freeze core contract semantics for stable validation.
- Experimental adapters may change structure before stable support.
- Breaking changes require explicit classification and migration guidance.
