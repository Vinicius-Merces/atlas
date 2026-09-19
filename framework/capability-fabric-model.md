# ATLAS Capability Fabric Model

## Purpose

The Capability Fabric exposes the canonical ATLAS registry as a compact,
machine-readable discovery surface. Runtimes can search the fabric and load
only the capabilities required for a task instead of placing the complete
agent and skill catalog in the model context.

## Source of truth

`.claude/registry.json` and the canonical files referenced by that registry
remain authoritative. Files under `atlas-registry/` are generated discovery
artifacts and must never become a second hand-maintained catalog.

## Discovery flow

1. Read `atlas-registry/ard-index.json`.
2. Filter candidates by capability kind and trust decision when supplied.
3. Rank candidates using exact name, token, description, and keyword matches.
4. Return at most three candidates by default.
5. Load the canonical source paths only for the selected candidates.

Discovery is advisory. It does not grant execution authority, bypass a review,
or prove that a capability is safe for the current repository.

## Trust boundary

`atlas-registry/trust-policy.json` defines the default decision for internal,
verified external, unverified external, and blocked sources. A discovered
external capability must retain its origin, version, integrity information,
and review state. Unknown external sources are denied by default.

The generated ATLAS capabilities are marked `internal` because they resolve to
canonical repository files. This classification is not transferable to copied
or repackaged content.

## External interoperability

The fabric uses portable JSON Schema documents and stable relative paths.
Adapters may translate it to an external plugin or discovery protocol, but
ATLAS must not claim conformance to an external standard until its published
schema and compatibility tests are available in the repository.

## Validation

- Generated artifacts match canonical frontmatter and registry membership.
- Every discovered item resolves to an existing canonical file.
- Capability identifiers are unique and deterministic.
- Trust labels are valid under the trust policy.
- Discovery returns bounded, deterministic results.
