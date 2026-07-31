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

## Source payload

When the source root is a Git worktree root, official builders enumerate:

- every tracked file, including its current worktree content;
- every untracked file that is not ignored by Git.

Release exclusions still remove local evidence, reports, caches, editor state,
secrets, `dist/`, and `.git/`. Ignored untracked files are not silently added.
Because modified tracked files and non-ignored untracked files are eligible,
inspect `git status` and make the intended source state explicit before
building.

The builder rejects an enumerated symlink instead of following or serializing
it. Replace the symlink with an approved regular-file payload or remove it from
the release source before retrying. Outside a Git worktree root, the builder
falls back to recursive enumeration with the same release exclusions and
symlink rejection.

Incremental packages compare the current payload with the selected directory
or Git reference. Every `replace` and `delete` operation records the prior
content as `base_sha256`; an `add` operation must not carry a base hash. Those
values are enforced by manual deployment preflight.

## Integrity model

Every archive contains `CONTENT-MANIFEST.json` with one SHA-256 hash per
internal payload file. The final archive hash lives outside the ZIP in `.sha256`
and the external `.manifest.json`. The ZIP is never rebuilt after its external
hash is calculated.

## Reproducibility

Builders sort paths, normalize archive metadata, use a fixed ZIP timestamp, and
exclude caches, local runtime evidence, reports, editor state, `.git/`, secrets,
and `dist/`. Rebuilding identical source must produce the same archive hash.

## Audit evidence

After validation and installation simulation, assemble and verify the audit
bundle:

```bash
python scripts/build_audit_bundle.py
python scripts/verify_evidence_integrity.py
```

The bundle records repository provenance and hashes its record index. The
verifier checks the bundle schema, record paths and hashes, JSON syntax, and
recognized evidence schemas. See the [Audit Bundle Guide](audit-bundle-guide.md).

## Approval boundary

Failed mandatory tests, runtime drift, source drift, unsafe package mapping,
missing rollback, or an unapproved breaking change blocks release. A local
green run does not prove GitHub-hosted CI executed.
