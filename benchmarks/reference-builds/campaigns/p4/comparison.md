# P4 Asteria target comparison

This document records the first isolated Asteria campaign after all three runs were frozen. It compares observed benchmark evidence, not hypothetical model capability.

## Fixed experiment

- Fixture: `premium-marketing-site`
- Fixture SHA-256: `e57da062e6223f6ecbea84a64813f6d8e73f9b0954cda065da5edbc680762947`
- Rubric SHA-256: `6463ae7fde36affecc20eff21f0ec73e04e0fb44c920a3cbc9115502a1b56b31`
- Campaign base: `3ccdf6e6209c3aea949e62226af1cb6b35167487`
- Target branches were isolated and did not inherit another Asteria implementation.

## Observed scores

| Axis | GPT-5.6 Sol calibration | Codex / GPT-5 | Claude Code / claude-opus-5 |
|---|---:|---:|---:|
| Brief fidelity | 10.00 | 10.00 | 10.00 |
| Architecture quality | 6.67 | 5.33 | 6.67 |
| Capability routing | 8.00 | 8.00 | 6.67 |
| Implementation completeness | 14.00 | 10.50 | 14.00 |
| Frontend Craft | 18.00 | 4.00 | 14.00 |
| Security & isolation | 5.00 | 5.00 | 5.00 |
| Failure resilience | 8.00 | 6.67 | 6.67 |
| Browser reality | 10.00 | 0.00 | 10.00 |
| Production readiness | 8.40 | 2.40 | 8.40 |
| Independent review | 0.00 | 1.25 | 5.00 |
| **Total** | **88.07** | **53.15** | **86.40** |

All three results are `blocked` and `claimable=false` because the canonical rubric does not allow a high aggregate score to override blocking evidence gaps or failures.

The calibration is diagnostic and is not part of the official target ranking. Among the official targets, the observed ranking is:

1. Claude Code / `claude-opus-5`: 86.40
2. Codex / `GPT-5`: 53.15

## What the scores actually mean

The raw target gap must not be read as a pure model-quality delta. Codex could execute local Node/API evidence but its environment could not produce the required real-browser evidence or public deployment. That forced `browser_reality=0`, removed rendered responsive/accessibility/visual-regression credit, and reduced production readiness.

Claude Code had Chromium via Playwright and produced a substantially richer browser/evidence pack: 74/74 independently reproduced Playwright checks, responsive measurements, screenshots, accessibility artifacts, failure flows, SEO, structured-data, security, performance and supply-chain evidence. Public deployment was still unavailable.

Therefore P4 exposes two separate variables:

1. implementation/reasoning quality;
2. runtime tool/evidence availability.

Future campaigns should preserve both rather than collapse them into one unexplained score.

## Strong signals shared across targets

- Brief fidelity reached 10/10 in every run.
- Security & isolation reached 5/5 in every run.
- Both official runtimes selected relevant ATLAS capabilities without agent inflation.
- Both target runs honestly remained blocked instead of fabricating browser or production proof.
- Neither target reused the calibration or the other target implementation.

## Claude Code findings worth preserving

The independent reviewers found real defects despite the high score:

- non-text contrast on form/control boundaries was 2.47:1 and failed the required experience;
- SVG annotation labels became too small at phone widths;
- the mobile site-plan interaction disappeared while copy still instructed the user to use it;
- screenshots were reproducible captures but not a true baseline/diff visual-regression system;
- 404 responses emitted conflicting robots directives and canonicalised to the homepage;
- UI/planning copy claimed automatic broker retry although no retry worker/path existed;
- the capability-routing record cited evidence paths that were never produced;
- residence cache policy used an excessively long shared-cache lifetime for mutable inventory.

These are benchmark findings, not reasons to discard the run. They are exactly the kind of measured failure P3/P4 were created to surface.

## Codex findings worth preserving

Codex demonstrated strong brief routing and local security, then materially improved persistence during remediation by moving to transactional SQLite with durable idempotency, rate events and an analytics outbox. Its independent reviewer correctly kept the run blocked because browser, viewport, accessibility and public-deployment evidence were unavailable.

The central Codex lesson is environmental: a target without a portable browser evidence path cannot meaningfully compete on Frontend Craft or Browser Reality, even when source quality may be stronger than the observed score can prove.

## Evidence-led remediation backlog for ATLAS

P4 justifies framework work in the following order:

1. **Portable browser evidence runner.** Add a runtime-neutral fallback that can run Chromium/Playwright in CI when the coding runtime cannot expose or install a browser. Record that the evidence was produced by the fallback runner rather than pretending the coding runtime produced it.
2. **Controlled public benchmark deployment.** Provide the same ephemeral HTTPS deployment path to every target so `marketing-production-domain` and deployed SEO can be tested fairly. Credentials and provider choice must be campaign-owned, not target-specific.
3. **Non-text contrast validation.** Extend accessibility evidence beyond axe text contrast to WCAG 2.2 SC 1.4.11 control boundaries, focus indicators and meaningful graphical objects.
4. **404 SEO truth checks.** Inspect all robots meta directives, canonical behavior and status-specific metadata instead of first-match extraction that can hide conflicting directives.
5. **Recovery-claim verification.** Any UI or planning claim such as automatic retry, queueing, reconciliation or notification recovery must link to an executable path/evidence. A durable failed state alone cannot justify retry copy.
6. **Evidence-reference integrity.** Benchmark validation should fail or downgrade submissions that cite missing evidence paths.
7. **Real visual regression.** Distinguish screenshot collection from baseline/diff regression. Require deterministic baselines or explicit human-review-only labeling.
8. **Mutable-content cache review.** Public inventory/status pages need cache policy tied to content freshness rather than very long shared-cache defaults.
9. **Environment capability manifest.** Freeze browser, deployment, network and subagent/reviewer availability before implementation so score interpretation can separate runtime constraints from implementation quality.

No new agent is justified by these findings. They are evaluator, workflow, assurance and portable-execution improvements around existing responsibilities.

## P4 conclusion

P4 succeeded as an experiment because it produced differentiated, non-perfect results and exposed both implementation defects and runtime constraints. It did not merely confirm that ATLAS can route instructions.

The next framework changes should be driven by the backlog above, then the campaign should be repeated or extended to RelayOps. Until the evidence environment is normalized, raw cross-runtime score differences must always be reported with their environment constraints.
