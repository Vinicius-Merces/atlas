# Capability Quality Review Gate

## Scope

Independently review an ATLAS capability-quality measurement and the catalog decisions derived from it.

## Required evidence

- Complete skill-quality output
- Complete skill-routing output
- Agent-overlap output
- Canonical registry and taxonomy counts
- Curated routing fixtures
- Changed descriptions/scopes if remediation occurred
- Baseline comparison when one exists

## Review questions

### Measurement integrity

- Were all registered skills measured?
- Were all agents measured?
- Are formulas and thresholds deterministic and documented?
- Are static proxies clearly distinguished from live runtime behavior?

### Skill quality

- Do low scores correspond to actionable quality weaknesses?
- Did remediation improve actual clarity/evidence rather than only add words?
- Are contract-required failures treated separately from diagnostic scoring?

### Routing

- Are curated cases representative rather than engineered around the scoring algorithm?
- Are top collisions manually inspected?
- Did a description change improve discrimination without changing capability meaning?

### Agent boundaries

- Do high-overlap pairs still own distinct durable outcomes?
- Could a proposed new agent instead be a skill?
- Are same-domain adjacent roles distinguishable by authority, output, or decision boundary?

## Findings

Record severity, evidence, affected capability, interpretation risk, required action, and verification method.

## Required actions

Critical or High findings must be resolved before the measurement is used to justify catalog expansion. Missing full-inventory coverage, non-deterministic scoring, fabricated accuracy claims, or near-duplicate agent purpose must be treated as blocking evidence gaps.

## Outcome

Record exactly one:

- Approved
- Approved with conditions
- Changes required
- Blocked

The author of the evaluator may provide evidence but must not be the sole approver of its own measurement claims.
