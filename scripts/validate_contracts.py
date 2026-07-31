from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_RELATIVE = Path("compatibility/core-contracts.json")
BASELINE_RELATIVE = Path("compatibility/contract-conformance-baseline.json")


@dataclass(frozen=True)
class Requirement:
    key: str
    description: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class ContractRule:
    contract: str
    collection: str
    requirements: tuple[Requirement, ...]


@dataclass(frozen=True)
class MarkdownAsset:
    path: str
    sha256: str
    text: str
    h1: str
    frontmatter: dict[str, str]
    sections: dict[str, str]


@dataclass(frozen=True)
class Violation:
    id: str
    contract: str
    collection: str
    artifact: str
    artifact_sha256: str
    requirement: str
    expected: str


RULES = (
    ContractRule(
        "agent-contract",
        "agents",
        (
            Requirement("identity.name", "agent name", ("frontmatter:name", "h1")),
            Requirement("identity.mission", "mission", ("section:mission",)),
            Requirement(
                "identity.domain",
                "domain",
                ("frontmatter:domain", "section:domain"),
            ),
            Requirement(
                "identity.authority",
                "authority level",
                (
                    "frontmatter:authority",
                    "frontmatter:authority_level",
                    "section:authority",
                    "section:authority level",
                ),
            ),
            Requirement(
                "scope.ownership",
                "owned scope",
                ("section:scope", "section:owns", "section:responsibilities"),
            ),
            Requirement(
                "scope.boundaries",
                "explicit change boundaries",
                (
                    "section:does not own",
                    "section:boundaries",
                    "section:must not change",
                ),
            ),
            Requirement(
                "inputs",
                "required or optional inputs",
                ("section:inputs", "section:required inputs"),
            ),
            Requirement(
                "outputs",
                "expected outputs and evidence",
                ("section:outputs", "section:required outputs"),
            ),
            Requirement(
                "collaboration",
                "collaboration or escalation",
                ("section:collaboration", "section:escalation"),
            ),
            Requirement(
                "quality",
                "quality gates or validation",
                (
                    "section:quality gates",
                    "section:must validate",
                    "section:validation",
                ),
            ),
            Requirement(
                "behavior",
                "behavioral requirements",
                (
                    "section:behavioral requirements",
                    "section:required behavior",
                    "section:rules",
                ),
            ),
        ),
    ),
    ContractRule(
        "memory-contract",
        "memory",
        (
            Requirement("purpose", "Purpose property", ("property:purpose",)),
            Requirement("scope", "Scope property", ("property:scope",)),
            Requirement(
                "source-of-truth",
                "Source of truth property",
                ("property:source of truth",),
            ),
            Requirement("owner", "Owner property", ("property:owner",)),
            Requirement(
                "last-reviewed",
                "Last reviewed property",
                ("property:last reviewed",),
            ),
            Requirement(
                "related-contracts",
                "Related contracts or ADRs property",
                ("property:related contracts or adrs",),
            ),
        ),
    ),
    ContractRule(
        "workflow-contract",
        "workflows",
        (
            Requirement("trigger", "trigger", ("section:trigger",)),
            Requirement("objective", "objective", ("section:objective",)),
            Requirement("inputs", "inputs", ("section:inputs",)),
            Requirement("sequence", "execution sequence", ("section:sequence",)),
            Requirement(
                "responsible-agents",
                "responsible agents",
                ("section:responsible agents",),
            ),
            Requirement(
                "decision-points",
                "decision points",
                ("section:decision points",),
            ),
            Requirement("validation", "validation", ("section:validation",)),
            Requirement(
                "failure-handling",
                "failure handling or blocking conditions",
                ("section:failure handling", "section:blocking conditions"),
            ),
            Requirement(
                "completion-criteria",
                "completion criteria",
                ("section:completion criteria",),
            ),
            Requirement(
                "lifecycle",
                "Understand through Deliver lifecycle",
                ("lifecycle",),
            ),
        ),
    ),
    ContractRule(
        "skill-contract",
        "skills",
        (
            Requirement("name", "skill name", ("frontmatter:name", "h1")),
            Requirement("purpose", "purpose", ("section:purpose",)),
            Requirement(
                "domain",
                "domain",
                ("frontmatter:domain", "section:domain"),
            ),
            Requirement(
                "trigger-conditions",
                "trigger conditions",
                ("section:trigger conditions", "section:trigger"),
            ),
            Requirement("inputs", "inputs", ("section:inputs",)),
            Requirement(
                "outputs",
                "outputs",
                ("section:output", "section:outputs"),
            ),
            Requirement(
                "dependencies",
                "dependencies",
                ("section:dependencies",),
            ),
            Requirement(
                "limitations",
                "limitations",
                ("section:limitations", "section:limitation"),
            ),
            Requirement(
                "validation",
                "validation method",
                (
                    "section:validation",
                    "section:validation method",
                    "section:checks",
                ),
            ),
        ),
    ),
    ContractRule(
        "review-contract",
        "reviews",
        (
            Requirement("review-type", "review type", ("h1", "section:review type")),
            Requirement("scope", "scope", ("section:scope",)),
            Requirement(
                "evidence",
                "evidence inspected or required",
                (
                    "section:evidence inspected",
                    "section:required evidence",
                    "section:evidence",
                ),
            ),
            Requirement(
                "findings",
                "findings",
                ("section:findings",),
            ),
            Requirement(
                "severity",
                "severity",
                ("section:severity", "section:severity levels"),
            ),
            Requirement(
                "required-actions",
                "required actions",
                ("section:required actions",),
            ),
            Requirement(
                "outcome",
                "outcome",
                ("section:outcome", "section:outcomes"),
            ),
        ),
    ),
    ContractRule(
        "command-contract",
        "commands",
        (
            Requirement("name", "command name", ("h1",)),
            Requirement("purpose", "purpose", ("section:purpose",)),
            Requirement(
                "arguments",
                "accepted arguments or inputs",
                ("section:accepted arguments", "section:arguments", "section:inputs"),
            ),
            Requirement(
                "preconditions",
                "preconditions",
                ("section:preconditions",),
            ),
            Requirement(
                "execution",
                "execution workflow",
                (
                    "section:execution workflow",
                    "section:execution",
                    "section:workflow",
                ),
            ),
            Requirement(
                "output",
                "output format",
                ("section:output format", "section:output", "section:outputs"),
            ),
            Requirement(
                "failure",
                "failure behavior",
                ("section:failure behavior", "section:failure handling"),
            ),
        ),
    ),
)


LIFECYCLE = (
    "understand",
    "inspect",
    "plan",
    "execute",
    "validate",
    "review",
    "document",
    "deliver",
)


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_hash(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(encoded)


def normalized_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], int]:
    if not lines or lines[0].strip() != "---":
        return {}, 0
    metadata: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return metadata, index + 1
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[normalized_heading(key)] = value.strip().strip("\"'")
    return metadata, 0


def parse_markdown(root: Path, path: Path) -> MarkdownAsset:
    data = path.read_bytes()
    text = data.decode("utf-8")
    lines = text.splitlines()
    frontmatter, body_start = parse_frontmatter(lines)
    h1 = ""
    sections: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []

    def close_section() -> None:
        nonlocal buffer
        if current is not None:
            sections[current] = "\n".join(buffer).strip()
        buffer = []

    for line in lines[body_start:]:
        if line.startswith("# ") and not h1:
            h1 = line[2:].strip()
        if line.startswith("## "):
            close_section()
            current = normalized_heading(line[3:])
            continue
        if current is not None:
            buffer.append(line)
    close_section()
    return MarkdownAsset(
        path=path.relative_to(root).as_posix(),
        sha256=sha256_bytes(data),
        text=text,
        h1=h1,
        frontmatter=frontmatter,
        sections=sections,
    )


def registered_asset_paths(root: Path) -> dict[str, list[Path]]:
    registry_path = root / ".claude" / "registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    agent_names = list(registry.get("agents", []))
    orchestrator = registry.get("orchestrator")
    if isinstance(orchestrator, str) and orchestrator not in agent_names:
        agent_names.append(orchestrator)
    collections: dict[str, list[Path]] = {
        "agents": [
            root / ".claude" / "agents" / f"{name}.md"
            for name in agent_names
        ],
        "workflows": [
            root / ".claude" / "workflows" / f"{name}.md"
            for name in registry.get("workflows", [])
        ],
        "reviews": [
            root / ".claude" / "reviews" / f"{name}.md"
            for name in registry.get("reviews", [])
        ],
        "commands": [
            root / ".claude" / "commands" / f"{name}.md"
            for name in registry.get("commands", [])
        ],
        "memory": [
            path
            for path in sorted((root / ".claude" / "memory").glob("*.md"))
            if path.name not in {"README.md", "index.md"}
        ],
    }
    skill_paths: list[Path] = []
    for name in registry.get("skills", []):
        native = root / ".claude" / "skills" / name / "SKILL.md"
        if native.is_file():
            skill_paths.append(native)
            continue
        legacy = sorted((root / ".claude" / "skills").rglob(f"{name}.md"))
        skill_paths.append(legacy[0] if len(legacy) == 1 else native)
    collections["skills"] = skill_paths
    return collections


def structural_validation(root: Path) -> tuple[dict, dict[str, list[Path]]]:
    manifest_path = root / MANIFEST_RELATIVE
    if not manifest_path.is_file():
        fail("Missing core contract manifest")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid core contract manifest: {exc}")
    if not isinstance(data, dict):
        fail("Core contract manifest must be an object")

    version_path = root / "VERSION"
    if not version_path.is_file():
        fail("Missing VERSION")
    version = version_path.read_text(encoding="utf-8").strip()
    if data.get("version") != version:
        fail(
            f"Core contract manifest version {data.get('version')} "
            f"does not match VERSION {version}"
        )

    contracts = data.get("contracts")
    if not isinstance(contracts, list) or not contracts:
        fail("Core contract manifest contracts must be a non-empty array")
    names: set[str] = set()
    paths: set[str] = set()
    expected_names = {rule.contract for rule in RULES}
    for index, contract in enumerate(contracts):
        if not isinstance(contract, dict):
            fail(f"Contract entry {index} must be an object")
        name = contract.get("name")
        relative = contract.get("path")
        status = contract.get("status")
        if not isinstance(name, str) or not name:
            fail(f"Contract entry {index} has no valid name")
        if name in names:
            fail(f"Duplicate contract name: {name}")
        names.add(name)
        if not isinstance(relative, str) or not relative:
            fail(f"Contract {name} has no valid path")
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            fail(f"Contract {name} has unsafe path: {relative}")
        if relative in paths:
            fail(f"Duplicate contract path: {relative}")
        paths.add(relative)
        path = root / Path(*pure.parts)
        if not path.is_file():
            fail(f"Missing contract file: {relative}")
        if not path.read_text(encoding="utf-8").strip():
            fail(f"Empty contract file: {relative}")
        if status != data.get("stability"):
            fail(
                f"Contract {name} status {status} does not match "
                f"manifest stability {data.get('stability')}"
            )
    if names != expected_names:
        missing = sorted(expected_names - names)
        unknown = sorted(names - expected_names)
        detail = []
        if missing:
            detail.append(f"missing: {', '.join(missing)}")
        if unknown:
            detail.append(f"unknown: {', '.join(unknown)}")
        fail("Core contract rule coverage mismatch (" + "; ".join(detail) + ")")

    canonical_paths = data.get("canonical_paths")
    if not isinstance(canonical_paths, list) or not canonical_paths:
        fail("canonical_paths must be a non-empty array")
    if len(canonical_paths) != len(set(canonical_paths)):
        fail("canonical_paths contains duplicates")
    for relative in canonical_paths:
        if not isinstance(relative, str) or not relative:
            fail("canonical_paths entries must be non-empty strings")
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            fail(f"Unsafe canonical path: {relative}")
        if not (root / Path(*pure.parts)).exists():
            fail(f"Missing canonical path: {relative}")

    collections = registered_asset_paths(root)
    missing_assets = sorted(
        path.relative_to(root).as_posix()
        for paths_for_collection in collections.values()
        for path in paths_for_collection
        if not path.is_file()
    )
    if missing_assets:
        fail("Missing registered contract assets: " + ", ".join(missing_assets))
    return data, collections


def has_evidence(asset: MarkdownAsset, evidence: str) -> bool:
    kind, _, value = evidence.partition(":")
    if kind == "h1":
        return bool(asset.h1.strip())
    if kind == "frontmatter":
        return bool(asset.frontmatter.get(normalized_heading(value), "").strip())
    if kind == "section":
        return bool(asset.sections.get(normalized_heading(value), "").strip())
    if kind == "property":
        pattern = re.compile(
            rf"^\s*-\s+\*\*{re.escape(value)}:\*\*\s+\S",
            re.IGNORECASE | re.MULTILINE,
        )
        return bool(pattern.search(asset.text))
    if kind == "lifecycle":
        lowered = asset.text.lower()
        return all(re.search(rf"\b{word}\b", lowered) for word in LIFECYCLE)
    raise ValueError(f"Unknown evidence matcher: {evidence}")


def collect_violations(
    root: Path,
    collections: dict[str, list[Path]],
) -> tuple[list[Violation], int]:
    violations: list[Violation] = []
    assets_checked = 0
    for rule in RULES:
        for path in collections[rule.collection]:
            asset = parse_markdown(root, path)
            assets_checked += 1
            for requirement in rule.requirements:
                if any(has_evidence(asset, item) for item in requirement.evidence):
                    continue
                violation_id = (
                    f"{rule.contract}:{asset.path}:{requirement.key}"
                )
                violations.append(
                    Violation(
                        id=violation_id,
                        contract=rule.contract,
                        collection=rule.collection,
                        artifact=asset.path,
                        artifact_sha256=asset.sha256,
                        requirement=requirement.key,
                        expected=requirement.description,
                    )
                )
    violations.sort(key=lambda item: item.id)
    return violations, assets_checked


def ruleset_payload() -> list[dict]:
    return [
        {
            "contract": rule.contract,
            "collection": rule.collection,
            "requirements": [asdict(requirement) for requirement in rule.requirements],
        }
        for rule in RULES
    ]


def baseline_candidate(version: str, violations: list[Violation]) -> dict:
    by_contract = Counter(item.contract for item in violations)
    by_requirement = Counter(
        f"{item.contract}:{item.requirement}" for item in violations
    )
    nonconforming_assets = sorted(
        {
            (item.artifact, item.artifact_sha256)
            for item in violations
        }
    )
    return {
        "baseline_version": 1,
        "framework_version": version,
        "ruleset_sha256": canonical_json_hash(ruleset_payload()),
        "known_violation_count": len(violations),
        "known_violations_sha256": canonical_json_hash(
            [item.id for item in violations]
        ),
        "nonconforming_assets_sha256": canonical_json_hash(
            [
                {"path": path, "sha256": digest}
                for path, digest in nonconforming_assets
            ]
        ),
        "counts_by_contract": dict(sorted(by_contract.items())),
        "counts_by_requirement": dict(sorted(by_requirement.items())),
    }


def compare_baseline(expected: dict, actual: dict) -> list[str]:
    findings = []
    for field in actual:
        if expected.get(field) != actual[field]:
            findings.append(
                f"{field}: baseline={expected.get(field)!r}, "
                f"current={actual[field]!r}"
            )
    unknown = sorted(set(expected) - set(actual))
    if unknown:
        findings.append(
            "Unknown baseline fields: " + ", ".join(unknown)
        )
    return findings


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def build_report(
    *,
    mode: str,
    version: str,
    manifest: dict,
    assets_checked: int,
    violations: list[Violation],
    baseline: dict,
    baseline_findings: Iterable[str],
) -> dict:
    findings = list(baseline_findings)
    return {
        "framework_version": version,
        "mode": mode,
        "manifest": {
            "contracts": len(manifest["contracts"]),
            "canonical_paths": len(manifest["canonical_paths"]),
        },
        "summary": {
            "assets_checked": assets_checked,
            "violations": len(violations),
            "fully_conformant": not violations,
            "baseline_matches": not findings,
        },
        "baseline": baseline,
        "baseline_findings": findings,
        "violations": [asdict(item) for item in violations],
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description=(
            "Validate core contract structure and effective Markdown asset "
            "conformance."
        )
    )
    result.add_argument(
        "--root",
        default=str(ROOT),
        help="Repository root to validate",
    )
    result.add_argument(
        "--mode",
        choices=("check", "report", "strict"),
        default="check",
        help=(
            "check blocks new or changed debt against the explicit baseline; "
            "report emits all findings without blocking known debt; strict "
            "blocks every conformance violation"
        ),
    )
    result.add_argument(
        "--baseline",
        help="Override the contract conformance baseline path",
    )
    result.add_argument(
        "--output",
        help="Write the detailed conformance report to this JSON path",
    )
    result.add_argument(
        "--write-baseline",
        help=(
            "Write a compact baseline candidate to this path. This is allowed "
            "only in report mode and must be reviewed before adoption."
        ),
    )
    return result


def main() -> None:
    args = parser().parse_args()
    root = Path(args.root).resolve()
    manifest, collections = structural_validation(root)
    violations, assets_checked = collect_violations(root, collections)
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    candidate = baseline_candidate(version, violations)

    baseline_path = (
        Path(args.baseline).resolve()
        if args.baseline
        else root / BASELINE_RELATIVE
    )
    baseline: dict = {}
    baseline_findings: list[str] = []
    if baseline_path.is_file():
        try:
            baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            baseline_findings.append(f"Invalid baseline JSON: {exc}")
        else:
            if not isinstance(baseline, dict):
                baseline_findings.append("Baseline must be a JSON object")
            else:
                baseline_findings.extend(compare_baseline(baseline, candidate))
    else:
        baseline_findings.append(
            f"Missing baseline: {display_path(baseline_path, root)}"
        )

    report = build_report(
        mode=args.mode,
        version=version,
        manifest=manifest,
        assets_checked=assets_checked,
        violations=violations,
        baseline=candidate,
        baseline_findings=baseline_findings,
    )
    if args.output:
        write_json(Path(args.output).resolve(), report)
    if args.write_baseline:
        if args.mode != "report":
            fail("--write-baseline requires --mode report")
        write_json(Path(args.write_baseline).resolve(), candidate)

    print(
        f"Core contract structure valid: {len(manifest['contracts'])} contracts, "
        f"{len(manifest['canonical_paths'])} canonical paths"
    )
    print(
        "Effective contract conformance: "
        f"{assets_checked} assets checked, {len(violations)} known violations, "
        f"fully_conformant={str(not violations).lower()}"
    )

    if args.mode == "report":
        if not args.output:
            print(json.dumps(report, indent=2))
        return
    if args.mode == "strict" and violations:
        print("Strict contract validation failed:")
        for contract, count in sorted(
            Counter(item.contract for item in violations).items()
        ):
            print(f"- {contract}: {count}")
        raise SystemExit(1)
    if args.mode == "check" and baseline_findings:
        print("Contract conformance baseline mismatch:")
        for finding in baseline_findings:
            print(f"- {finding}")
        print(
            "Run --mode report to inspect every violation and review a new "
            "baseline candidate."
        )
        raise SystemExit(1)
    print(
        "Contract compatibility check passed: no new, resolved, or changed "
        f"baseline debt; {len(violations)} known violations remain explicit."
    )


if __name__ == "__main__":
    main()
