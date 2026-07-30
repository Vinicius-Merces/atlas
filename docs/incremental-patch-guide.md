# Incremental Patch Guide

1. Confirm the installed version matches `from_version`.
2. Run the patch preflight validator.
3. Copy the patch contents over the repository.
4. Replace listed modified files.
5. Add listed new files.
6. Remove only paths listed in `FILES-TO-DELETE.md`.
7. Run the full ATLAS validation suite.

Incremental patches are version-specific. Use a cumulative package when the
installed base is uncertain.
