# Manual Deployment Guide

ATLAS treats manual deployment as a supported operating mode, not a fallback.

## Before copying

- Verify the external ZIP checksum.
- Read `from_version` and `to_version`.
- Preserve the installed repository or a cumulative recovery package.
- Review additions, replacements, and deletions separately.
- Stop if the installed `VERSION` does not match the required base.
- Run `scripts/manual_deploy_preflight.py` against the extracted patch and
  installed root before copying. A passed report is mandatory.
- Stop on any existing add target, missing replace/delete target, symlink, or
  `base_sha256` mismatch; merge project-owned changes explicitly or rebuild the
  patch from the correct base.

## Copy rules

- Copy additions without removing unrelated project files.
- Allow listed replacements to overwrite their exact targets.
- Map `CLAUDE-DIRECTORY/...` to `.claude/...`.
- Never copy package instructions into `.claude/`.
- Remove only paths explicitly listed in `FILES-TO-DELETE.md`.
- Treat an empty deletion list as no deletion authorization.

## After copying

- Confirm `VERSION`.
- Confirm no permanent `CLAUDE-DIRECTORY/` remains.
- Review project-specific memory and intentional customizations.
- Run validators, tests, and runtime drift detection when Python is available.
- Record a deployment receipt. The default is `pending`; claim `applied` or
  `simulated` only with the passed preflight report and concrete validation.

## Rollback

Restore the preserved repository or use the validated recovery package. Do not
attempt rollback by deleting files that merely appear absent from another ZIP.

See [Installation](installation.md),
[Deployment Preflight Guide](manual-deployment-preflight-guide.md),
[Deployment Receipt Guide](manual-deployment-receipt-guide.md),
[Framework Upgrade Guide](framework-upgrade-guide.md), and
[Troubleshooting](troubleshooting.md).
