# Troubleshooting

## `.claude` does not appear

Enable hidden items in the file manager. In an incremental package,
`CLAUDE-DIRECTORY/` represents `.claude/`; rename or copy to the canonical
hidden target rather than leaving both directories.

## Base version is incorrect

Do not apply the incremental patch. Apply missing intermediate releases or use
the cumulative package.

## Codex catalog is out of sync

Run `python scripts/sync_codex_adapter.py`, review generated changes, then run
the same command with `--check`.

## Runtime drift is reported

Run the Codex validator and inspect runtime declarations, generated maps,
support status, and canonical paths. Do not silence drift without reconciling
the source.

## Source manifest is stale

Run `python scripts/manage_version.py` and
`python scripts/validate_source_of_truth.py`. Update only controlled current
version surfaces; never rewrite historical release notes or migrations.

## CI YAML fails

Parse `.github/workflows/validate.yml` with a real YAML parser and confirm all
steps remain inside `jobs.validate.steps`. Install `requirements-test.txt`
before reproducing locally.

## Checksum mismatch

Stop. Download or copy the artifact again. The external checksum must match the
final closed ZIP before extraction.

## Manual preflight is blocked

Do not copy any patch file. An existing `add` target, missing
`replace`/`delete` target, symlink, or mismatch with `base_sha256` means the
installed repository differs from the declared base. Preserve local work and
either merge the conflict explicitly or rebuild the patch from the correct
base. Never edit a preflight report to change its outcome.

## Applied or simulated receipt is rejected

Both statuses require `--preflight-report` pointing to a passed report with the
same `from_version` and `to_version`, plus at least one concrete
`--validation`. Use the default `pending` status while those facts are not yet
available; a pending receipt must not be presented as deployment completion.

## Package mapping fails

Every `.claude/...` target in an incremental package must use a corresponding
`CLAUDE-DIRECTORY/...` package path. Package instructions must remain outside
that visible payload directory.

## Generated artifacts appear in a release

Rebuild with the official builders. Archives must exclude caches, `dist/`,
`.atlas/`, `reports/`, `.vscode/`, `.git/`, and secrets.

In a Git worktree, tracked files and non-ignored untracked files are eligible
release inputs, so inspect `git status` before building. Ignoring a tracked file
does not remove it from the payload.

## Release build rejects a symlink

Official builders reject symlinks in the enumerated source payload. Do not
replace the error with link-following behavior; make the intended regular-file
content explicit or remove the symlink from the release source.

## Golden path refuses to overwrite

Use a fresh disposable output directory, or inspect the existing generated
artifacts before passing `--force`. Force replaces only the known golden-path
outputs and still does not execute implementation work.

## Audit bundle verification fails

Do not rely on the bundle until verification passes. Rebuild after intentional
record changes; restore missing records; investigate hash mismatches; and fix
schema-invalid recognized evidence rather than editing its indexed hash. Also
confirm record paths remain workspace-relative and are not symlinks.

## Memory is stale

Run:

```bash
python scripts/validate_memory_freshness.py --strict
python scripts/audit_memory_drift.py
python scripts/build_reconciliation_proposal.py
```

Review proposals manually before changing durable memory.
