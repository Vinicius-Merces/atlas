#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = "reference-build-benchmark"
REVIEW = "reference-build-benchmark-review"


def update_registry() -> None:
    path = ROOT / ".claude" / "registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["workflows"] = sorted(set(data.get("workflows", [])) | {WORKFLOW})
    data["reviews"] = sorted(set(data.get("reviews", [])) | {REVIEW})
    data.setdefault("assurance", {})["reference_build_benchmark_model"] = (
        "framework/reference-build-benchmark-model.md"
    )
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_validate_all() -> None:
    path = ROOT / "scripts" / "validate_all.py"
    text = path.read_text(encoding="utf-8")
    if '"reference-build-benchmark-pack"' in text:
        return
    marker = '''        _python_step(
            root,
            "full-stack-delivery-pack",
            "Validate P2 full-stack delivery capability pack",
            "validate_full_stack_delivery_pack.py",
        ),
'''
    addition = marker + '''        _python_step(
            root,
            "reference-build-benchmark-pack",
            "Validate P3 reference build benchmark pack",
            "validate_reference_build_benchmark_pack.py",
        ),
'''
    if marker not in text:
        raise SystemExit("validate_all insertion marker not found")
    path.write_text(text.replace(marker, addition, 1), encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("| Workflows | 83 |", "| Workflows | 84 |")
    text = text.replace("| Reviews | 74 |", "| Reviews | 75 |")
    if "## Reference Build Benchmark P3" not in text:
        section = '''
## Reference Build Benchmark P3

P3 makes complete-product execution measurable. ATLAS now ships three fixed reference briefs: a premium marketing site, a multi-tenant subscription SaaS, and a dense internal operations system, plus a deterministic 10-axis scoring harness.

The canonical model is `framework/reference-build-benchmark-model.md`; fixtures and rubric live under `benchmarks/reference-builds/`; execution uses `reference-build-benchmark`; independent review uses `reference-build-benchmark-review`.

A harness-smoke run only proves that fixtures and scoring work and is always non-claimable. A live result may be compared across Claude Code and Codex only when the exact fixture/rubric version, run metadata, inspectable evidence, blockers, and independent review are preserved.

P3 intentionally adds no new agents or skills: it tests whether the existing **87 agent surfaces and 128 skills** can actually compose into complete products before ATLAS expands the catalog again.

'''
        marker = "## Discovery descriptions and hover surfaces"
        if marker not in text:
            raise SystemExit("README P3 insertion marker not found")
        text = text.replace(marker, section + marker, 1)
    path.write_text(text, encoding="utf-8")


def update_agents() -> None:
    blocks = {
        "reference-implementation-reviewer": (
            "Own the independent product/evidence review for live reference builds. "
            "Map findings to benchmark axis/check ids, reject placeholder completeness, "
            "and never convert a harness-smoke result into a product claim."
        ),
        "qa-engineer": (
            "Collect reproducible browser, negative-path, responsive, accessibility, "
            "failure, and deployment evidence required by reference-build checks. "
            "Missing evidence remains unverified rather than inferred pass."
        ),
        "solution-blueprint-engineer": (
            "Map each fixed P3 brief to the closest blueprint and delivery workflow while "
            "preserving fixture constraints. Do not turn the benchmark brief into a hidden source template."
        ),
        "runtime-parity-reviewer": (
            "Compare Claude Code and Codex reference-build results only after each run is "
            "independently scored on the exact same fixture and rubric; disclose material tool/environment differences."
        ),
    }
    for agent, body in blocks.items():
        path = ROOT / ".claude" / "agents" / f"{agent}.md"
        text = path.read_text(encoding="utf-8")
        if "## P3 Reference Build Benchmark" not in text:
            text = text.rstrip() + "\n\n## P3 Reference Build Benchmark\n\n" + body + "\n"
            path.write_text(text, encoding="utf-8")


def update_research() -> None:
    path = ROOT / "docs" / "research" / "agent-skill-landscape-2026.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if "## P3 Reference Build Benchmark" in text:
        return
    text = text.rstrip() + '''

## P3 Reference Build Benchmark

Implemented after P2 to stop capability growth from becoming speculative.

P3 adds no agents and no skills. It introduces three fixed complete-product briefs, a shared 10-axis scoring rubric with build-specific weights, blocking checks, deterministic submission scoring, harness-smoke fixtures, independent benchmark review, and exact-fixture Claude Code/Codex comparison.

The next capability additions should be justified by repeated live reference-build evidence: implementation failure, routing failure, missing capability, workflow weakness, evidence gap, or fixture ambiguity. Prefer repairing existing skills/workflows before adding new durable roles.
'''
    path.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    update_registry()
    update_validate_all()
    update_readme()
    update_agents()
    update_research()
    print("P3 integration applied")


if __name__ == "__main__":
    main()
