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

## Package mapping fails

Every `.claude/...` target in an incremental package must use a corresponding
`CLAUDE-DIRECTORY/...` package path. Package instructions must remain outside
that visible payload directory.

## Generated artifacts appear in a release

Rebuild with the official builders. Archives must exclude caches, `dist/`,
`.atlas/`, `reports/`, `.vscode/`, `.git/`, and secrets.

## Memory is stale

Run:

```bash
python scripts/validate_memory_freshness.py --strict
python scripts/audit_memory_drift.py
python scripts/build_reconciliation_proposal.py
```

Review proposals manually before changing durable memory.
