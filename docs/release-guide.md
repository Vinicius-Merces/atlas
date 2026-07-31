# Release Guide

## Required sequence

1. Freeze intended scope.
2. Validate version consistency and generated artifacts.
3. Run registry, package, contract, schema, runtime, memory, policy, and test
   gates.
4. Review compatibility, migration, support, known limitations, and rollback.
5. Build cumulative, incremental, and recovery artifacts.
6. Validate internal content manifests and external checksums.
7. Simulate clean install and incremental upgrade.
8. Assemble validation evidence and audit bundle.
9. Make an explicit go, conditional-go, or no-go decision.

## Build commands

```bash
python scripts/build_release.py --kind cumulative
python scripts/build_release.py --kind recovery
python scripts/build_incremental_release.py --base <directory-or-git-ref>
```

## Integrity model

Every archive contains `CONTENT-MANIFEST.json` with one SHA-256 hash per
internal payload file. The final archive hash lives outside the ZIP in `.sha256`
and the external `.manifest.json`. The ZIP is never rebuilt after its external
hash is calculated.

## Reproducibility

Builders sort paths, normalize archive metadata, use a fixed ZIP timestamp, and
exclude caches, local runtime evidence, reports, editor state, `.git/`, secrets,
and `dist/`. Rebuilding identical source must produce the same archive hash.

## Approval boundary

Failed mandatory tests, runtime drift, source drift, unsafe package mapping,
missing rollback, or an unapproved breaking change blocks release. A local
green run does not prove GitHub-hosted CI executed.
