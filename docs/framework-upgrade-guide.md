# Framework Upgrade Guide

## Replace cumulative files safely

Copy the new cumulative package over the repository and allow matching files to
be replaced.

## Review obsolete files

Uploading a cumulative package does not delete files that were removed from the
new framework version.

## Protect project-specific knowledge

Project memory, local ADRs, secrets, and intentional customizations require
special care.

## Validate after upgrade

Run registry and package validation, then test representative commands and
workflows.
