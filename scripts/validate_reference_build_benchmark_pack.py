#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "benchmarks" / "reference-builds"
SPECS = SUITE / "specs"
EXAMPLES = SUITE / "examples"
EXPECTED_SPECS = {
    "premium-marketing-site",
    "multitenant-subscription-saas",
    "internal-operations-system",
}
AXES = [
    "brief_fidelity",
    "architecture_quality",
    "capability_routing",
    "implementation_completeness",
    "frontend_craft",
    "security_isolation",
    "failure_resilience",
    "browser_reality",
    "production_readiness",
    "independent_review",
]
WORKFLOW = "reference-build-benchmark"
REVIEW = "reference-build-benchmark-review"
MODEL = "framework/reference-build-benchmark-model.md"
OVERLAY = "framework/capabilities/reference-build-benchmark.yaml"
MEMORY = ".claude/memory/capabilities/reference-build-benchmark.md"
AGENTS = {
    "reference-implementation-reviewer",
    "qa-engineer",
    "solution-blueprint-engineer",
    "runtime-parity-reviewer",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def headings(path: Path) -> set[str]:
    return {
        line[3:].strip().lower()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ")
    }


def main() -> int:
    failures: list[str] = []
    required_files = [
        ROOT / MODEL,
        ROOT / OVERLAY,
        ROOT / MEMORY,
        ROOT / ".claude/workflows/reference-build-benchmark.md",
        ROOT / ".claude/reviews/reference-build-benchmark-review.md",
        SUITE / "README.md",
        SUITE / "scoring-rubric.yaml",
        SUITE / "submission.schema.json",
        ROOT / "scripts/run_reference_build_benchmark.py",
    ]
    for path in required_files:
        if not path.is_file():
            failures.append(f"missing artifact: {path.relative_to(ROOT)}")

    if failures:
        print("Reference build benchmark pack validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    registry = json.loads((ROOT / ".claude/registry.json").read_text(encoding="utf-8"))
    if WORKFLOW not in registry.get("workflows", []):
        failures.append("reference-build-benchmark workflow is not registered")
    if REVIEW not in registry.get("reviews", []):
        failures.append("reference-build-benchmark-review is not registered")
    pointer = registry.get("assurance", {}).get("reference_build_benchmark_model")
    if pointer != MODEL:
        failures.append(f"assurance model pointer mismatch: {pointer!r}")
    if len(registry.get("agents", [])) + 1 != 87:
        failures.append("P3 must not inflate the 87-agent surface")
    if len(registry.get("skills", [])) != 128:
        failures.append("P3 must reuse the 128-skill catalog rather than add benchmark-only skills")

    overlay = load_yaml(ROOT / OVERLAY)
    build_ids = {row.get("id") for row in overlay.get("reference_builds", []) if isinstance(row, dict)}
    if build_ids != EXPECTED_SPECS:
        failures.append(f"overlay reference-build set mismatch: {sorted(build_ids)}")
    all_overlay_skills: set[str] = set()
    for values in overlay.get("reused_capabilities", {}).values():
        if isinstance(values, list):
            all_overlay_skills.update(values)
    unknown_overlay = sorted(all_overlay_skills - set(registry.get("skills", [])))
    if unknown_overlay:
        failures.append("overlay references unknown skills: " + ", ".join(unknown_overlay))

    rubric = load_yaml(SUITE / "scoring-rubric.yaml")
    if rubric.get("version") != 1:
        failures.append("rubric version must be 1")
    if rubric.get("axis_order") != AXES:
        failures.append("rubric axis_order does not match canonical 10-axis order")
    factors = rubric.get("status_factors")
    if factors != {"pass": 1.0, "partial": 0.5, "fail": 0.0, "unverified": 0.0}:
        failures.append("status factors changed unexpectedly")

    spec_paths = sorted(SPECS.glob("*.yaml"))
    spec_ids = set()
    registered_skills = set(registry.get("skills", []))
    for path in spec_paths:
        spec = load_yaml(path)
        spec_id = spec.get("id")
        spec_ids.add(spec_id)
        if spec.get("version") != 1:
            failures.append(f"{path.name}: version must be 1")
        if list(spec.get("axes", {}).keys()) != AXES:
            failures.append(f"{path.name}: axes must use canonical order")
            continue
        weight = sum(float(spec["axes"][name].get("weight", 0)) for name in AXES)
        if abs(weight - 100.0) > 1e-9:
            failures.append(f"{path.name}: axis weights sum to {weight}, expected 100")
        check_ids: list[str] = []
        for axis in AXES:
            checks = spec["axes"][axis].get("checks", [])
            if not checks:
                failures.append(f"{path.name}: axis {axis} has no checks")
            for check in checks:
                check_id = check.get("id") if isinstance(check, dict) else None
                if not isinstance(check_id, str) or not check_id:
                    failures.append(f"{path.name}: invalid check id in {axis}")
                else:
                    check_ids.append(check_id)
        if len(check_ids) != len(set(check_ids)):
            failures.append(f"{path.name}: duplicate check ids")
        blockers = set(spec.get("blocking_checks", []))
        if not blockers or not blockers <= set(check_ids):
            failures.append(f"{path.name}: blocking_checks must be non-empty and declared")
        unknown = sorted(set(spec.get("required_capabilities", [])) - registered_skills)
        if unknown:
            failures.append(f"{path.name}: unknown required capabilities: {', '.join(unknown)}")
        execution_workflow = spec.get("execution_workflow")
        if execution_workflow not in registry.get("workflows", []):
            failures.append(f"{path.name}: execution workflow not registered: {execution_workflow}")

    if spec_ids != EXPECTED_SPECS:
        failures.append(f"spec set mismatch: {sorted(spec_ids)}")

    schema = json.loads((SUITE / "submission.schema.json").read_text(encoding="utf-8"))
    schema_validator = Draft202012Validator(schema)
    for spec_id in sorted(EXPECTED_SPECS):
        submission_path = EXAMPLES / f"{spec_id}.harness-smoke.yaml"
        if not submission_path.is_file():
            failures.append(f"missing harness smoke submission: {submission_path.relative_to(ROOT)}")
            continue
        submission = load_yaml(submission_path)
        schema_errors = sorted(schema_validator.iter_errors(submission), key=lambda error: list(error.path))
        for error in schema_errors:
            failures.append(f"{submission_path.name}: schema: {error.message}")

    workflow_required = {
        "trigger", "objective", "inputs", "sequence", "responsible agents",
        "decision points", "validation", "failure handling", "completion criteria",
        "required lifecycle",
    }
    workflow_heads = headings(ROOT / ".claude/workflows/reference-build-benchmark.md")
    missing_heads = sorted(workflow_required - workflow_heads)
    if missing_heads:
        failures.append("benchmark workflow missing headings: " + ", ".join(missing_heads))

    review_required = {
        "review type", "scope", "evidence inspected", "findings",
        "severity", "required actions", "outcome",
    }
    review_heads = headings(ROOT / ".claude/reviews/reference-build-benchmark-review.md")
    missing_review = sorted(review_required - review_heads)
    if missing_review:
        failures.append("benchmark review missing headings: " + ", ".join(missing_review))

    for agent in sorted(AGENTS):
        path = ROOT / ".claude/agents" / f"{agent}.md"
        if "## P3 Reference Build Benchmark" not in path.read_text(encoding="utf-8"):
            failures.append(f"agent missing P3 routing: {agent}")

    smoke = subprocess.run(
        [sys.executable, str(ROOT / "scripts/run_reference_build_benchmark.py"), "--suite-smoke"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if smoke.returncode != 0:
        failures.append("benchmark harness smoke failed: " + (smoke.stdout + smoke.stderr).strip())
    else:
        try:
            data = json.loads(smoke.stdout)
        except json.JSONDecodeError as exc:
            failures.append(f"benchmark harness smoke output is not JSON: {exc}")
        else:
            if data.get("count") != 3:
                failures.append(f"benchmark harness smoke expected 3 builds, got {data.get('count')}")
            for row in data.get("results", []):
                if row.get("outcome") != "harness-only":
                    failures.append(f"harness smoke became claimable-like: {row}")

    if failures:
        print("Reference build benchmark pack validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Reference build benchmark pack valid: "
        "3 reference builds, 10 axes, 128 skills reused, 87 agents preserved."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
