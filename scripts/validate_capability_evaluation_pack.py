#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
OVERLAY = ROOT / "framework" / "capabilities" / "capability-evaluation.yaml"
MODEL = ROOT / "framework" / "capability-evaluation-model.md"
WORKFLOW = ROOT / ".claude" / "workflows" / "capability-quality-assessment.md"
REVIEW = ROOT / ".claude" / "reviews" / "capability-quality-review.md"
MEMORY = ROOT / ".claude" / "memory" / "capabilities" / "capability-evaluation.md"
FIXTURES = ROOT / "tests" / "fixtures" / "capability-routing-cases.yaml"
REQUIRED_SKILLS = {"skill-quality-evaluation", "skill-trigger-evaluation", "agent-overlap-analysis"}
REQUIRED_SCRIPTS = {"evaluate_skill_quality.py", "evaluate_skill_routing.py", "analyze_agent_overlap.py"}


def main() -> None:
    failures: list[str] = []
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    skills = set(registry.get("skills", []))
    workflows = set(registry.get("workflows", []))
    reviews = set(registry.get("reviews", []))
    if not REQUIRED_SKILLS <= skills:
        failures.append("capability evaluation skills are not fully registered")
    if "capability-quality-assessment" not in workflows:
        failures.append("capability-quality-assessment workflow is not registered")
    if "capability-quality-review" not in reviews:
        failures.append("capability-quality-review is not registered")
    assurance = registry.get("assurance", {})
    if not isinstance(assurance, dict) or assurance.get("capability_evaluation_model") != "framework/capability-evaluation-model.md":
        failures.append("registry assurance.capability_evaluation_model is missing")
    for path in [OVERLAY, MODEL, WORKFLOW, REVIEW, MEMORY, FIXTURES]:
        if not path.is_file():
            failures.append(f"missing capability evaluation artifact: {path.relative_to(ROOT)}")
    for script in REQUIRED_SCRIPTS:
        if not (ROOT / "scripts" / script).is_file():
            failures.append(f"missing capability evaluator: {script}")
    if OVERLAY.is_file():
        overlay = yaml.safe_load(OVERLAY.read_text(encoding="utf-8")) or {}
        if set(overlay.get("skills", [])) != REQUIRED_SKILLS:
            failures.append("capability evaluation overlay skill set drifted")
        if overlay.get("preferred_workflow") != "capability-quality-assessment":
            failures.append("capability evaluation preferred workflow drifted")
        if overlay.get("required_review") != "capability-quality-review":
            failures.append("capability evaluation required review drifted")
    fixture_data = yaml.safe_load(FIXTURES.read_text(encoding="utf-8")) if FIXTURES.is_file() else {}
    cases = (fixture_data or {}).get("cases", [])
    if len(cases) < 20:
        failures.append("capability routing fixture set must contain at least 20 cases")
    for case in cases:
        if case.get("expected") not in skills:
            failures.append(f"routing fixture references unregistered skill: {case.get('expected')}")
    for name in REQUIRED_SKILLS:
        wrapper = ROOT / ".agents" / "skills" / name / "SKILL.md"
        if not wrapper.is_file() or f".claude/skills/{name}/SKILL.md" not in wrapper.read_text(encoding="utf-8"):
            failures.append(f"Codex wrapper missing canonical reference: {name}")
    if failures:
        print("Capability evaluation pack validation failed:")
        for item in failures:
            print(f"- {item}")
        raise SystemExit(1)
    print(f"Capability evaluation pack valid: {len(REQUIRED_SKILLS)} skills, 3 evaluators, {len(cases)} routing fixtures")


if __name__ == "__main__":
    main()
