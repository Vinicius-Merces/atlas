# Adapter Drift Model

Adapter drift occurs when a runtime adapter no longer represents the current
canonical ATLAS capabilities or semantics.

## Drift types

### Inventory drift

Canonical assets exist but are missing from the adapter catalog.

### Semantic drift

A mapped asset changes meaning or responsibility.

### Path drift

Adapter references point to moved or missing canonical files.

### Support drift

Support claims exceed available validation evidence.

### Documentation drift

Runtime guidance describes obsolete behavior.

## Drift severity

- Informational
- Warning
- High
- Blocking

## Drift invariant

A beta-supported runtime may not ship with blocking inventory or path drift.
