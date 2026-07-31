# Manual Deployment Receipt Guide

A deployment receipt records what was applied or simulated; it does not apply
the patch. Preserve the extracted patch, passed preflight report, validation,
source commit, and release URL needed to support the claim.

## Pending receipt

The recorder defaults to `pending` and leaves `applied_at` empty. This is safe
for preparation or an interrupted deployment and does not claim that files
were changed:

```bash
python scripts/record_manual_deploy.py \
  --from-version <from-version> \
  --to-version <to-version> \
  --patch <archive-name> \
  --patch-root <extracted-patch-root> \
  --operator-note "Deployment prepared; application not yet confirmed"
```

When `--patch-root` is supplied, the recorder verifies manifest versions,
records the manifest SHA-256, and populates the exact add, replace, and delete
targets.

## Applied or simulated receipt

Use `applied` only after copying and post-deployment validation; use
`simulated` only for a completed installation simulation:

```bash
python scripts/record_manual_deploy.py \
  --from-version <from-version> \
  --to-version <to-version> \
  --patch <archive-name> \
  --patch-root <extracted-patch-root> \
  --preflight-report <passed-preflight-report.json> \
  --status applied \
  --validation "validation command: observed outcome" \
  --source-commit <release-commit> \
  --release-url <release-url>
```

Both final statuses require a preflight report whose outcome is `passed` and
whose versions match the receipt, plus at least one concrete `--validation`.
The receipt stores hashes for the patch manifest and preflight report. Repeat
`--validation` and `--operator-note` when needed.

By default receipts are written under `.atlas/deployments/`. Include them in
the next audit bundle and verify that bundle before relying on it as evidence.
See the [Deployment Preflight Guide](manual-deployment-preflight-guide.md) and
[Audit Bundle Guide](audit-bundle-guide.md).
