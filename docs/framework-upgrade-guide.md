# Framework Upgrade Guide

## Choose the correct upgrade

Use an incremental package only when the installed `VERSION` equals its
`from_version`. Otherwise use a cumulative package.

## Replace cumulative files safely

Copy the new cumulative package over the repository and allow matching files to
be replaced.

## Review obsolete files

Uploading a cumulative package does not delete files that were removed from the
new framework version.

Incremental packages are different: remove only paths explicitly listed in
`FILES-TO-DELETE.md`. Absence from either package type does not authorize
deletion.

## Protect project-specific knowledge

Project memory, local ADRs, secrets, and intentional customizations require
special care.

## Validate after upgrade

Run registry and package validation, then test representative commands and
workflows.

For incremental updates, also run runtime drift, source-of-truth, policy, and
manual preflight validation. Preserve the external checksum, release notes,
migration guide, and rollback package as upgrade evidence.

See [Manual Deployment Guide](manual-deployment-guide.md) and
[Troubleshooting](troubleshooting.md).
