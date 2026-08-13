---
name: supply-chain-risk-audit
description: "Audit dependency and build supply-chain risk when packages, lockfiles, registries, install scripts, CI actions, container bases, or third-party build inputs change."
---

# Supply Chain Risk Audit

## Purpose

Treat third-party code and build inputs as part of the application's attack surface, reviewing what changed, where it came from, what executes during install/build, and whether the project can detect, contain, and recover from compromised or vulnerable dependencies.

## Trigger conditions

Use when adding/upgrading dependencies, regenerating lockfiles, changing package registries, installing plugins/extensions, changing CI actions, container/base images, Git dependencies, build tools, package scripts, or other third-party code executed in development, CI, build, or runtime.

## Inputs

- Dependency manifests and lockfiles
- Dependency diff relative to the trusted base
- Package-manager audit/advisory output when available
- Registry/source/provenance information
- Install/build/lifecycle scripts
- CI workflow and third-party action references
- Container/base-image references when applicable
- Existing dependency policy, allowlists, and exceptions

## Procedure

1. Identify every direct dependency/build input added, removed, or changed and the transitive graph changes visible in lockfiles or dependency-review tooling.
2. Confirm package names, source registries, Git URLs, namespaces/scopes, and versions are intentional. Investigate look-alike names, unexpected registry changes, new forks, unpublished/replaced packages, or source changes.
3. Review known vulnerability and malware/advisory evidence using the project's ecosystem tools and available dependency-review service. Do not limit review to direct dependencies.
4. Inspect lifecycle/install/postinstall/build scripts and newly executable tooling before trusting it. Flag network downloads, shell execution, credential access, filesystem mutation, native compilation, or opaque binary fetching that exceeds the dependency's expected purpose.
5. Review maintainer/upstream signals proportionally to risk: ownership transfer, sudden release pattern changes, dormant/unmaintained packages, suspicious new maintainers, compromised release channels, or abandoned security response.
6. Verify lockfile/integrity behavior and that CI uses reproducible dependency resolution where the ecosystem supports it. Unexpected broad lockfile churn requires explanation.
7. Review third-party CI actions/plugins/build images with the same trust model as dependencies. Follow project policy for pinning, provenance, least privilege, and update review.
8. Review dependency permissions and runtime reach. A development-only formatter and a production request-path package do not have the same blast radius.
9. Review license/policy compatibility with `dependency-manager` when policy requires it, but do not confuse license acceptance with security acceptance.
10. Prefer smaller dependency surface and built-in/platform capabilities when a new dependency provides marginal value relative to its execution or maintenance risk.
11. Verify update/rollback/removal path for high-impact dependencies and whether security advisories can be detected after merge.
12. Record accepted risks with owner, rationale, scope, and expiry/revisit condition when a vulnerable or weakly maintained dependency cannot immediately be removed.

## Outputs

- Dependency/build-input change inventory
- Vulnerability/malware/advisory findings
- Install-script/execution findings
- Source/provenance/maintenance findings
- CI/build/container supply-chain findings
- Blast-radius assessment
- Required remediation, exception, or rollback actions

## Limitations

- Absence of a known advisory is not proof that a dependency is safe.
- Popularity, download count, star count, or a passing package-manager audit are not sufficient trust evidence by themselves.
- This skill does not require arbitrary installation or execution of an untrusted package merely to inspect it.

## Dependencies

- Dependency manifests/lockfiles or equivalent resolved graph
- Trusted base revision for dependency-diff comparison
- Ecosystem-native audit/advisory tooling and repository dependency review when available
- `dependency-impact-analysis`, `security-review`, or release gates when change risk warrants them

## Validation

- Compare dependency/lockfile changes against the intended manifest change.
- Run available advisory/dependency-review checks and retain the result without suppressing blocking findings silently.
- Inspect newly introduced lifecycle scripts or executable build inputs before approval.
- Verify unexpected source/registry/provenance changes are explained.
- Unresolved malware evidence, critical vulnerable dependency with reachable impact, or unexplained executable supply-chain behavior blocks approval unless governed by an explicit security exception.
