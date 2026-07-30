# Distribution Guide

## Validate before packaging

A release archive should never be the first place structural problems are
discovered.

## Include provenance

Artifacts should identify source version, included adapters, validation status,
and checksum.

## Prefer reproducible builds

The same source and build process should produce equivalent release contents.

## Separate source and distribution

Generated release artifacts belong in `dist/` and should not alter canonical
source files.
