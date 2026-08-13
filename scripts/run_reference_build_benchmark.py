#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUBRIC = ROOT / "benchmarks" / "reference-builds" / "scoring-rubric.yaml"


class BenchmarkError(ValueError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise BenchmarkError(f"{path} must contain a YAML mapping")
    return data


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_checks(spec: dict[str, Any], axis_order: list[str]) -> tuple[list[str], dict[str, str]]:
    axes = spec.get("axes")
    if not isinstance(axes, dict):
        raise BenchmarkError("spec.axes must be a mapping")
    ids: list[str] = []
    owners: dict[str, str] = {}
    total_weight = 0.0
    for axis_name in axis_order:
        axis = axes.get(axis_name)
        if not isinstance(axis, dict):
            raise BenchmarkError(f"missing axis: {axis_name}")
        weight = axis.get("weight")
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise BenchmarkError(f"invalid weight for axis {axis_name}")
        total_weight += float(weight)
        checks = axis.get("checks")
        if not isinstance(checks, list) or not checks:
            raise BenchmarkError(f"axis {axis_name} must define checks")
        for check in checks:
            if not isinstance(check, dict) or not isinstance(check.get("id"), str):
                raise BenchmarkError(f"invalid check in axis {axis_name}")
            check_id = check["id"]
            if check_id in owners:
                raise BenchmarkError(f"duplicate check id: {check_id}")
            ids.append(check_id)
            owners[check_id] = axis_name
    if abs(total_weight - 100.0) > 1e-9:
        raise BenchmarkError(f"axis weights must sum to 100, got {total_weight}")
    blockers = spec.get("blocking_checks", [])
    if not isinstance(blockers, list) or any(item not in owners for item in blockers):
        raise BenchmarkError("blocking_checks must reference declared check ids")
    return ids, owners


def validate_run_metadata(submission: dict[str, Any], live: bool) -> list[str]:
    run = submission.get("run")
    if not isinstance(run, dict):
        raise BenchmarkError("submission.run must be a mapping")
    required = ("runtime", "model", "repository", "commit", "evidence_root")
    missing = [key for key in required if not isinstance(run.get(key), str) or not run[key].strip()]
    if missing:
        raise BenchmarkError("missing run metadata: " + ", ".join(missing))
    warnings: list[str] = []
    if live:
        for key in ("repository", "commit", "evidence_root"):
            if run[key].startswith("synthetic://"):
                raise BenchmarkError(f"live run cannot use synthetic evidence metadata: {key}")
    elif submission.get("execution_mode") == "harness-smoke":
        warnings.append("Harness-smoke validates the scoring engine only; this result is never claimable.")
    return warnings


def threshold_label(score: float, thresholds: list[dict[str, Any]]) -> str:
    ordered = sorted(thresholds, key=lambda row: float(row["minimum"]), reverse=True)
    for row in ordered:
        if score >= float(row["minimum"]):
            return str(row["label"])
    return "insufficient"


def score_submission(spec_path: Path, submission_path: Path, rubric_path: Path = DEFAULT_RUBRIC) -> dict[str, Any]:
    spec = load_yaml(spec_path)
    submission = load_yaml(submission_path)
    rubric = load_yaml(rubric_path)

    axis_order = rubric.get("axis_order")
    if not isinstance(axis_order, list) or not all(isinstance(x, str) for x in axis_order):
        raise BenchmarkError("rubric.axis_order must be a list of strings")
    factors = rubric.get("status_factors")
    if not isinstance(factors, dict):
        raise BenchmarkError("rubric.status_factors must be a mapping")

    if submission.get("benchmark_version") != rubric.get("version"):
        raise BenchmarkError("submission benchmark_version does not match rubric version")
    if submission.get("spec_id") != spec.get("id"):
        raise BenchmarkError("submission spec_id does not match spec id")

    expected, owners = expected_checks(spec, axis_order)
    rows = submission.get("checks")
    if not isinstance(rows, list):
        raise BenchmarkError("submission.checks must be a list")
    checks: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise BenchmarkError("every submission check needs an id")
        check_id = row["id"]
        if check_id in checks:
            raise BenchmarkError(f"duplicate submission check: {check_id}")
        checks[check_id] = row
    missing = sorted(set(expected) - set(checks))
    unknown = sorted(set(checks) - set(expected))
    if missing or unknown:
        parts = []
        if missing:
            parts.append("missing checks: " + ", ".join(missing))
        if unknown:
            parts.append("unknown checks: " + ", ".join(unknown))
        raise BenchmarkError("; ".join(parts))

    execution_mode = submission.get("execution_mode")
    if execution_mode not in {"live", "harness-smoke"}:
        raise BenchmarkError("execution_mode must be live or harness-smoke")
    live = execution_mode == "live"
    warnings = validate_run_metadata(submission, live)

    axis_values: dict[str, list[float]] = {name: [] for name in axis_order}
    normalized_checks: list[dict[str, Any]] = []
    for check_id in expected:
        row = checks[check_id]
        status = row.get("status")
        if status not in factors:
            raise BenchmarkError(f"invalid status for {check_id}: {status!r}")
        evidence = row.get("evidence", [])
        if not isinstance(evidence, list) or not all(isinstance(x, str) and x.strip() for x in evidence):
            raise BenchmarkError(f"evidence for {check_id} must be a list of non-empty strings")
        if status in {"pass", "partial"} and not evidence:
            raise BenchmarkError(f"{status} check {check_id} requires evidence")
        if live and any(item.startswith("synthetic://") for item in evidence):
            raise BenchmarkError(f"live run check {check_id} cannot cite synthetic evidence")
        factor = float(factors[status])
        axis_values[owners[check_id]].append(factor)
        normalized_checks.append(
            {
                "id": check_id,
                "axis": owners[check_id],
                "status": status,
                "factor": factor,
                "evidence": evidence,
                "notes": row.get("notes", ""),
            }
        )

    axis_scores: dict[str, dict[str, float]] = {}
    overall = 0.0
    for axis_name in axis_order:
        weight = float(spec["axes"][axis_name]["weight"])
        values = axis_values[axis_name]
        factor = sum(values) / len(values)
        score = weight * factor
        overall += score
        axis_scores[axis_name] = {
            "weight": weight,
            "completion_factor": round(factor, 4),
            "score": round(score, 2),
        }
    overall = round(overall, 2)

    blockers = []
    for check_id in spec.get("blocking_checks", []):
        if checks[check_id].get("status") != "pass":
            blockers.append(check_id)

    review = submission.get("review")
    if not isinstance(review, dict):
        raise BenchmarkError("submission.review must be a mapping")
    review_outcome = review.get("outcome")
    review_rules = rubric.get("review_outcomes", {})
    if review_outcome not in review_rules:
        raise BenchmarkError(f"invalid review outcome: {review_outcome!r}")
    reviewer = review.get("reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise BenchmarkError("independent reviewer identity is required")

    base_outcome = threshold_label(overall, rubric.get("score_thresholds", []))
    review_rule = review_rules[review_outcome]
    blocked = bool(blockers) or review_rule == "block"
    if blocked:
        public_outcome = "blocked"
    elif execution_mode == "harness-smoke":
        public_outcome = "harness-only"
    elif review_rule == "cap-conditional":
        public_outcome = "conditional"
    else:
        public_outcome = base_outcome

    claimable = (
        live
        and not blocked
        and review_rule in {"allow", "cap-conditional"}
        and bool(submission["run"].get("repository"))
        and bool(submission["run"].get("commit"))
        and bool(submission["run"].get("evidence_root"))
    )

    return {
        "benchmark_version": rubric["version"],
        "spec_id": spec["id"],
        "spec_version": spec.get("version"),
        "spec_sha256": sha256(spec_path),
        "rubric_sha256": sha256(rubric_path),
        "execution_mode": execution_mode,
        "run": submission["run"],
        "score": overall,
        "base_outcome": base_outcome,
        "outcome": public_outcome,
        "claimable": claimable,
        "blocking_failures": blockers,
        "review": review,
        "axis_scores": axis_scores,
        "checks": normalized_checks,
        "warnings": warnings,
    }


def compare_results(left_path: Path, right_path: Path) -> dict[str, Any]:
    left = json.loads(left_path.read_text(encoding="utf-8"))
    right = json.loads(right_path.read_text(encoding="utf-8"))
    if left.get("spec_id") != right.get("spec_id"):
        raise BenchmarkError("comparison requires the same spec_id")
    if left.get("benchmark_version") != right.get("benchmark_version"):
        raise BenchmarkError("comparison requires the same benchmark_version")
    if left.get("spec_sha256") != right.get("spec_sha256"):
        raise BenchmarkError("comparison requires the exact same fixture content")
    if left.get("rubric_sha256") != right.get("rubric_sha256"):
        raise BenchmarkError("comparison requires the exact same rubric content")
    axes = sorted(set(left.get("axis_scores", {})) | set(right.get("axis_scores", {})))
    deltas = {}
    for axis in axes:
        l_score = float(left.get("axis_scores", {}).get(axis, {}).get("score", 0))
        r_score = float(right.get("axis_scores", {}).get(axis, {}).get("score", 0))
        deltas[axis] = round(r_score - l_score, 2)
    return {
        "spec_id": left["spec_id"],
        "benchmark_version": left["benchmark_version"],
        "left": {
            "runtime": left.get("run", {}).get("runtime"),
            "model": left.get("run", {}).get("model"),
            "score": left.get("score"),
            "claimable": left.get("claimable"),
            "outcome": left.get("outcome"),
        },
        "right": {
            "runtime": right.get("run", {}).get("runtime"),
            "model": right.get("run", {}).get("model"),
            "score": right.get("score"),
            "claimable": right.get("claimable"),
            "outcome": right.get("outcome"),
        },
        "score_delta_right_minus_left": round(float(right.get("score", 0)) - float(left.get("score", 0)), 2),
        "axis_deltas_right_minus_left": deltas,
        "warnings": [] if left.get("claimable") and right.get("claimable") else [
            "At least one result is non-claimable; treat this comparison as diagnostic only."
        ],
    }


def run_smoke_suite(root: Path) -> dict[str, Any]:
    specs = root / "specs"
    submissions = root / "examples"
    results = []
    for spec_path in sorted(specs.glob("*.yaml")):
        submission_path = submissions / f"{spec_path.stem}.harness-smoke.yaml"
        if not submission_path.is_file():
            raise BenchmarkError(f"missing harness-smoke submission for {spec_path.stem}")
        result = score_submission(spec_path, submission_path, root / "scoring-rubric.yaml")
        if result["claimable"] or result["outcome"] != "harness-only":
            raise BenchmarkError(f"harness-smoke semantics violated for {spec_path.stem}")
        results.append({"spec_id": result["spec_id"], "score": result["score"], "outcome": result["outcome"]})
    if not results:
        raise BenchmarkError("no reference-build specs found")
    return {"suite": str(root.relative_to(ROOT)), "count": len(results), "results": results}


def write_json(data: dict[str, Any], output: Path | None) -> None:
    rendered = json.dumps(data, indent=2, sort_keys=False) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Score or compare ATLAS reference-build benchmark runs.")
    p.add_argument("--rubric", default=str(DEFAULT_RUBRIC))
    p.add_argument("--spec")
    p.add_argument("--submission")
    p.add_argument("--output")
    p.add_argument("--suite-smoke", action="store_true")
    p.add_argument("--suite-root", default=str(ROOT / "benchmarks" / "reference-builds"))
    p.add_argument("--compare", nargs=2, metavar=("LEFT_RESULT", "RIGHT_RESULT"))
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        output = Path(args.output).resolve() if args.output else None
        if args.compare:
            data = compare_results(Path(args.compare[0]), Path(args.compare[1]))
            write_json(data, output)
            return 0
        if args.suite_smoke:
            data = run_smoke_suite(Path(args.suite_root).resolve())
            write_json(data, output)
            return 0
        if not args.spec or not args.submission:
            raise BenchmarkError("--spec and --submission are required unless using --suite-smoke or --compare")
        data = score_submission(Path(args.spec).resolve(), Path(args.submission).resolve(), Path(args.rubric).resolve())
        write_json(data, output)
        return 0
    except (BenchmarkError, OSError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"Reference build benchmark failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
