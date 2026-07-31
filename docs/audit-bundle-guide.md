# Audit Bundle Guide

An audit bundle is a hashed index of repository-native evidence, not a copy of
Git history or proof that an unrecorded action occurred. Build it only after
execution results, deployment receipts, and continuity records reflect
observed outcomes.

## Build

```bash
python scripts/build_audit_bundle.py
```

By default the builder indexes JSON records under `.atlas/evidence/`,
`.atlas/deployments/`, and `.atlas/continuity/`, then writes
`.atlas/audit/audit-bundle.json`. Add another workspace-relative JSON directory
with repeated `--include`; use `--no-default-includes` only when intentionally
building a narrower bundle.

The manifest contains:

- the framework version and generation time;
- the source Git commit when available;
- repository state as `clean`, `dirty`, `not-git`, or `unknown`;
- one workspace-relative path and canonical SHA-256 per record;
- the record count and SHA-256 of the complete record index.

Absolute paths, paths escaping the workspace, and symlink evidence are
rejected.

## Verify

```bash
python scripts/verify_evidence_integrity.py
```

The verifier validates `schemas/audit-bundle-manifest.schema.json`, rejects
duplicate or escaping record paths, checks every indexed file and hash, parses
each record as JSON, and validates recognized receipts, evidence records,
checkpoints, and handoffs against their schemas. A hash-valid but
schema-invalid recognized record still fails.

Run verification against an explicit workspace or bundle when needed:

```bash
python scripts/verify_evidence_integrity.py \
  --root <repository-root> \
  --bundle <audit-bundle.json>
```

Rebuild the bundle whenever indexed evidence changes. A dirty repository state
is provenance, not automatic approval; release review must decide whether that
source state is intended and reproducible.
