# Manual Deployment Preflight Guide

Preflight is mandatory before manually applying an incremental package. It
validates the extracted patch against the exact installed repository without
copying, replacing, or deleting target files.

## Run before copying

```bash
python scripts/manual_deploy_preflight.py \
  --patch-root <extracted-patch-root> \
  --installed-root <installed-repository> \
  --output <preflight-report.json>
```

Use the extracted versioned patch root containing `PATCH-MANIFEST.json`.
Supplying the installed root is required for an operational preflight because
that is what allows version and target-state conflicts to be detected. The
command writes a report with outcome `passed` or `blocked` and exits nonzero
when blocked.

## Operation safety

Each manifest operation has a distinct rule:

- `add`: must not carry `base_sha256`, and its target must not already exist;
- `replace`: must carry a valid `base_sha256`, and the installed target must be
  a regular file whose canonical SHA-256 still matches that base;
- `delete`: must carry `base_sha256`, must not carry a payload hash, and the
  installed target must still match the declared base.

Any mismatch is a conflict, not permission to overwrite. Stop and explicitly
merge the project-owned change or rebuild the package from the correct base.
Symlink targets and symlink payloads are also blocked.

## Other enforced checks

Preflight also checks:

- installed `VERSION` equals `from_version`;
- every non-delete payload exists and matches its declared SHA-256;
- target and package paths are safe and remain inside their roots;
- operations, target paths, and payload paths are valid and non-duplicated;
- `.claude/...` targets use `CLAUDE-DIRECTORY/...` payload mappings;
- the visible payload contains exactly the files declared by the manifest;
- `FILES-TO-ADD.md`, `FILES-TO-REPLACE.md`, and `FILES-TO-DELETE.md` exactly
  match the manifest.

Preserve the passed report. Its hash is recorded by an `applied` or `simulated`
deployment receipt. See the
[Manual Deployment Guide](manual-deployment-guide.md) and
[Deployment Receipt Guide](manual-deployment-receipt-guide.md).
