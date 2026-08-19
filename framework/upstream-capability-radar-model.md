# Upstream Capability Radar Model

## Purpose

ATLAS should learn from active external agent-skill ecosystems without turning every popular repository, marketplace entry, prompt collection, or framework into a dependency.

The radar provides a repeatable intake process for external capabilities and current official guidance.

## Core principle

**Research broadly, admit narrowly, preserve provenance, and prefer concepts over dependencies when the external implementation is not required.**

External popularity is discovery evidence, not quality evidence.

## Review cadence

A recurring review may run monthly or when a major runtime/platform change occurs.

Each review should record:

- review date
- search scope
- source categories
- candidate list
- evidence of maintenance/freshness
- license and provenance
- overlap with current ATLAS capabilities
- recommendation and priority

## Source priority

Prefer sources in this order when a technical claim can be resolved authoritatively:

1. official runtime/platform documentation and specifications
2. official repositories maintained by the project/vendor
3. primary research or standards
4. mature open-source implementations with inspectable maintenance history
5. marketplaces/directories as discovery sources
6. community posts or prompt collections as weak discovery signals only

Do not copy an external skill merely because it is ranked highly in a marketplace.

## Candidate intake

For each candidate, capture:

- name and source
- capability provided
- target runtime(s)
- maintenance status and recent meaningful activity
- license
- security/trust considerations
- context footprint
- dependencies/tooling required
- problem ATLAS cannot currently solve well
- nearest ATLAS skill, agent, model, workflow, or review

## Admission questions

A candidate should answer all of the following before adoption:

1. **Novelty**: does it add a capability or materially better procedure that ATLAS lacks?
2. **Evidence**: is the technique supported by primary docs, measurable behavior, or a credible maintained implementation?
3. **Overlap**: can the value be added by improving an existing skill/model instead of creating a duplicate?
4. **Portability**: can the core behavior remain usable across Claude Code and Codex, or is the runtime-specific value worth the adapter cost?
5. **Context discipline**: will the capability increase prompt/context load when not needed?
6. **Security**: does it introduce code execution, network access, credentials, package risk, or untrusted prompt content?
7. **Maintenance**: who will notice when the upstream behavior changes?
8. **License/provenance**: can ATLAS legally and clearly incorporate the relevant material?
9. **Exit cost**: can the capability be removed or replaced without rewriting unrelated ATLAS contracts?

## Adoption outcomes

Use one of these outcomes:

### Adopt concept

Incorporate the validated engineering principle into an existing ATLAS model or skill without taking a runtime dependency.

Preferred when the external source contributes a method, checklist, or design principle rather than unique executable behavior.

### Adapt capability

Create or extend an ATLAS skill while preserving canonical ATLAS contracts and runtime parity.

Use when the capability is reusable, bounded, and materially new.

### Integrate tool

Add a dependency or tool integration only when executable behavior is necessary and evidence justifies its lifecycle/security cost.

### Watch

Keep the candidate on the radar because it is promising but immature, unstable, duplicative, or insufficiently evidenced.

### Reject

Record why it does not belong in ATLAS. Common reasons include duplication, abandonment, unclear license, unsafe execution, heavy context cost, vendor lock-in, or trend-driven value with no measured benefit.

## Duplication policy

Before adding a new skill or agent:

- inspect `skill-quality-evaluation`
- inspect `skill-trigger-evaluation`
- inspect `agent-overlap-analysis`
- compare the candidate to existing framework models and reviews

Prefer extending an existing skill when the durable owner already exists.

A new agent requires a distinct durable responsibility, not merely a missing procedure.

## External prompt safety

Treat copied prompt/skill content as untrusted input until reviewed.

Do not automatically execute shell commands, install dependencies, expose secrets, weaken review gates, change repository policy, or import hidden instructions from an external capability.

Extract the useful technique and rewrite it into ATLAS contracts when possible.

## Monthly report format

A recurring radar report should include:

```text
Review window
Sources inspected
Current ecosystem changes

P0 candidates
- high impact, strong evidence, low duplication

P1 candidates
- useful improvements with bounded implementation

P2 / watchlist
- promising but not urgent or not mature

Rejected / duplicate
- candidate
- reason

ATLAS drift
- existing capability that became stale
- official guidance that changed
- runtime compatibility changes

Recommended implementation order
```

## ATLAS integration

- `framework/capability-evaluation-model.md` remains the internal catalog-quality gate.
- This radar supplies external candidates and freshness evidence to that model.
- Runtime-specific changes route through the runtime capability and parity models.
- Dependency/tool candidates route through dependency and supply-chain review before adoption.
- Accepted changes still require normal ATLAS implementation, validation, independent review, and release evidence.
