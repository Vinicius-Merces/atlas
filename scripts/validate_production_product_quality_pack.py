#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
OVERLAY = ROOT / "framework" / "capabilities" / "production-product-quality.yaml"
MODEL = ROOT / "framework" / "production-product-quality-model.md"
WORKFLOW = ROOT / ".claude" / "workflows" / "production-product-quality-readiness.md"
REVIEW = ROOT / ".claude" / "reviews" / "production-product-quality-review.md"
MEMORY = ROOT / ".claude" / "memory" / "capabilities" / "production-product-quality.md"
BASELINE = ROOT / "docs" / "assurance" / "capability-quality-baseline-2026-08-13.md"
PRODUCTION_SKILLS = {"database-schema-review", "saas-multitenancy-review", "background-job-reliability", "cache-strategy-assessment"}
GROWTH_SKILLS = {"conversion-funnel-review", "analytics-implementation-audit", "content-discoverability-review"}
REQUIRED_SKILLS = PRODUCTION_SKILLS | GROWTH_SKILLS


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path.relative_to(ROOT)}")
    raw, _ = text[4:].split("\n---\n", 1)
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError(f"invalid frontmatter: {path.relative_to(ROOT)}")
    return data


def main() -> None:
    failures: list[str] = []
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    skills = set(registry.get("skills", []))
    workflows = set(registry.get("workflows", []))
    reviews = set(registry.get("reviews", []))
    if not REQUIRED_SKILLS <= skills:
        failures.append("P1 skills are not fully registered")
    if "production-product-quality-readiness" not in workflows:
        failures.append("P1 readiness workflow is not registered")
    if "production-product-quality-review" not in reviews:
        failures.append("P1 independent review is not registered")
    assurance = registry.get("assurance", {})
    if not isinstance(assurance, dict) or assurance.get("production_product_quality_model") != "framework/production-product-quality-model.md":
        failures.append("registry assurance.production_product_quality_model is missing")
    for path in [OVERLAY, MODEL, WORKFLOW, REVIEW, MEMORY, BASELINE]:
        if not path.is_file():
            failures.append(f"missing P1 artifact: {path.relative_to(ROOT)}")
    if OVERLAY.is_file():
        overlay = yaml.safe_load(OVERLAY.read_text(encoding="utf-8")) or {}
        groups = overlay.get("skills", {})
        if not isinstance(groups, dict):
            failures.append("P1 overlay skills must be grouped mapping")
        else:
            if set(groups.get("production_systems", [])) != PRODUCTION_SKILLS:
                failures.append("P1 production-system skill set drifted")
            if set(groups.get("product_growth", [])) != GROWTH_SKILLS:
                failures.append("P1 product/growth skill set drifted")
        if overlay.get("preferred_workflow") != "production-product-quality-readiness":
            failures.append("P1 preferred workflow drifted")
        if overlay.get("required_review") != "production-product-quality-review":
            failures.append("P1 required review drifted")
    for name in sorted(REQUIRED_SKILLS):
        canonical = ROOT / ".claude" / "skills" / name / "SKILL.md"
        wrapper = ROOT / ".agents" / "skills" / name / "SKILL.md"
        if not canonical.is_file():
            failures.append(f"missing canonical P1 skill: {name}")
            continue
        metadata = frontmatter(canonical)
        if metadata.get("name") != name or not str(metadata.get("description", "")).strip():
            failures.append(f"invalid discovery metadata for P1 skill: {name}")
        text = canonical.read_text(encoding="utf-8")
        for heading in ["## Purpose", "## Trigger conditions", "## Inputs", "## Procedure", "## Outputs", "## Dependencies", "## Limitations", "## Validation"]:
            if heading not in text:
                failures.append(f"P1 skill {name} missing {heading}")
        if not wrapper.is_file() or f".claude/skills/{name}/SKILL.md" not in wrapper.read_text(encoding="utf-8"):
            failures.append(f"P1 Codex wrapper missing canonical reference: {name}")
    if MODEL.is_file():
        model = MODEL.read_text(encoding="utf-8").lower()
        for marker in ["database", "multiten", "background", "cache", "conversion", "analytics", "discoverability", "capability evaluation"]:
            if marker not in model:
                failures.append(f"P1 model missing marker: {marker}")
    if WORKFLOW.is_file():
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for name in REQUIRED_SKILLS:
            if name not in workflow:
                failures.append(f"P1 workflow does not route skill: {name}")
    if failures:
        print("Production/product quality pack validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Production/product quality pack valid: 7 skills, 1 workflow, 1 independent review gate")


if __name__ == "__main__":
    main()
