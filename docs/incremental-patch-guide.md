# Incremental Patch Guide

1. Confirm the installed version matches `from_version`.
2. Run the patch preflight against both the extracted patch and installed
   repository; continue only when its report is `passed`.
3. Add only files listed in `FILES-TO-ADD.md`.
4. Replace only files listed in `FILES-TO-REPLACE.md`.
5. Remove only paths listed in `FILES-TO-DELETE.md`.
6. Run the full ATLAS validation suite.
7. Record an `applied` or `simulated` receipt with the passed preflight report
   and concrete validation.

Incremental patches are version-specific. Use a cumulative package when the
installed base is uncertain. An existing add target or a replace/delete target
whose content differs from `base_sha256` is a blocking conflict, not
authorization to overwrite local changes.

See the [Deployment Preflight Guide](manual-deployment-preflight-guide.md) and
[Deployment Receipt Guide](manual-deployment-receipt-guide.md).
