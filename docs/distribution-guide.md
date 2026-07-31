# Distribution Guide

## Validate before packaging

A release archive should never be the first place structural problems are
discovered.

## Include provenance

Artifacts should identify source version, included adapters, validation status,
and checksum.

## Prefer reproducible builds

The same source and build process should produce equivalent release contents.

Official builders normalize ZIP metadata and create internal content manifests:

```bash
python scripts/build_release.py --kind cumulative
python scripts/build_release.py --kind recovery
python scripts/build_incremental_release.py --base <directory-or-git-ref>
```

Validate each result with `scripts/validate_release_artifacts.py`.

## Separate source and distribution

Generated release artifacts belong in `dist/` and should not alter canonical
source files.

The external `.sha256` and `.manifest.json` files are generated after the final
ZIP is closed. Do not place a self-referential final ZIP checksum inside the
archive.
