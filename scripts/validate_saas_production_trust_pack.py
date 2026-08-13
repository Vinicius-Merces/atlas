#!/usr/bin/env python3
"""Validate the ATLAS SaaS Production Trust capability pack."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
OVERLAY = ROOT / "framework" / "capabilities" / "saas-production-trust.yaml"
MODEL = ROOT / "framework" / "saas-production-trust-model.md"
WORKFLOW = ROOT / ".claude" / "workflows" / "saas-production-readiness.md"
REVIEW = ROOT / ".claude" / "reviews" / "saas-production-trust-review.md"
MEMORY = ROOT / ".claude" / "memory" / "capabilities" / "saas-production-trust.md"

REQUIRED_SKILLS = {
    "authentication-flow-review",
    "authorization-boundary-review",
    "row-level-security-review",
    "secret-environment-audit",
    "webhook-reliability-review",
    "payment-integration-review",
    "external-api-resilience-review",
}

REQUIRED_AGENTS = {
    "security-engineer": {
        "framework/saas-production-trust-model.md",
        "authentication-flow-review",
        "authorization-boundary-review",
        "row-level-security-review",
        "secret-environment-audit",
        "webhook-reliability-review",
        "payment-integration-review",
        "external-api-resilience-review",
    },
    "backend-engineer": {
        "framework/saas-production-trust-model.md",
        "authorization-boundary-review",
        "row-level-security-review",
        "payment-integration-review",
    },
    "integration-engineer": {
        "framework/saas-production-trust-model.md",
        "webhook-reliability-review",
        "payment-integration-review",
        "external-api-resilience-review",
    },
    "platform-engineer": {
        "framework/saas-production-trust-model.md",
        "secret-environment-audit",
    },
}


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    try:
        raw, _ = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError(
            f"unterminated YAML frontmatter: {path.relative_to(ROOT)}"
        ) from exc
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError(f"invalid YAML frontmatter: {path.relative_to(ROOT)}")
    return data


def main() -> None:
    failures: list[str] = []

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registered_skills = set(registry.get("skills", []))
    registered_workflows = set(registry.get("workflows", []))
    registered_reviews = set(registry.get("reviews", []))

    missing_registry_skills = sorted(REQUIRED_SKILLS - registered_skills)
    if missing_registry_skills:
        failures.append(
            "SaaS production trust skills missing from registry: "
            + ", ".join(missing_registry_skills)
        )

    if "saas-production-readiness" not in registered_workflows:
        failures.append("saas-production-readiness workflow is not registered")
    if "saas-production-trust-review" not in registered_reviews:
        failures.append("saas-production-trust-review gate is not registered")

    trust = registry.get("trust", {})
    if not isinstance(trust, dict) or trust.get("saas_production_trust_model") != (
        "framework/saas-production-trust-model.md"
    ):
        failures.append(
            "registry trust.saas_production_trust_model is missing or invalid"
        )

    for path in [MODEL, OVERLAY, WORKFLOW, REVIEW, MEMORY]:
        if not path.is_file():
            failures.append(
                f"missing SaaS production trust artifact: {path.relative_to(ROOT)}"
            )

    overlay: dict[str, object] = {}
    if OVERLAY.is_file():
        loaded = yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            overlay = loaded
        else:
            failures.append("SaaS production trust overlay must be a YAML mapping")

    overlay_skills = overlay.get("skills", [])
    if not isinstance(overlay_skills, list) or set(overlay_skills) != REQUIRED_SKILLS:
        failures.append(
            "SaaS production trust overlay skills do not match the required skill set"
        )
    if overlay.get("canonical_model") != "framework/saas-production-trust-model.md":
        failures.append("SaaS production trust overlay canonical_model is invalid")
    if overlay.get("preferred_workflow") != "saas-production-readiness":
        failures.append("SaaS production trust overlay preferred_workflow is invalid")
    if overlay.get("required_review") != "saas-production-trust-review":
        failures.append("SaaS production trust overlay required_review is invalid")

    for name in sorted(REQUIRED_SKILLS):
        canonical = ROOT / ".claude" / "skills" / name / "SKILL.md"
        wrapper = ROOT / ".agents" / "skills" / name / "SKILL.md"
        if not canonical.is_file():
            failures.append(f"missing canonical SaaS production trust skill: {name}")
            continue
        try:
            metadata = frontmatter(canonical)
        except ValueError as exc:
            failures.append(str(exc))
            continue
        if metadata.get("name") != name:
            failures.append(f"SaaS production trust skill {name} declares wrong name")
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            failures.append(
                f"SaaS production trust skill {name} has no discovery description"
            )
        if not wrapper.is_file():
            failures.append(f"missing Codex-native SaaS trust wrapper: {name}")
        else:
            wrapper_text = wrapper.read_text(encoding="utf-8")
            canonical_ref = f".claude/skills/{name}/SKILL.md"
            if canonical_ref not in wrapper_text:
                failures.append(
                    f"Codex wrapper {name} does not reference canonical skill {canonical_ref}"
                )
            try:
                wrapper_metadata = frontmatter(wrapper)
                if wrapper_metadata.get("description") != description:
                    failures.append(
                        f"Codex wrapper {name} discovery description drifted from canonical skill"
                    )
            except ValueError as exc:
                failures.append(str(exc))

    for agent, required_terms in REQUIRED_AGENTS.items():
        path = ROOT / ".claude" / "agents" / f"{agent}.md"
        if not path.is_file():
            failures.append(f"missing SaaS trust agent: {agent}")
            continue
        text = path.read_text(encoding="utf-8")
        missing_terms = sorted(term for term in required_terms if term not in text)
        if missing_terms:
            failures.append(
                f"agent {agent} is missing SaaS trust references: "
                + ", ".join(missing_terms)
            )

    if WORKFLOW.is_file():
        workflow_text = WORKFLOW.read_text(encoding="utf-8")
        for name in sorted(REQUIRED_SKILLS):
            if name not in workflow_text:
                failures.append(
                    f"SaaS production workflow does not reference required skill: {name}"
                )

    if MODEL.is_file():
        model_text = MODEL.read_text(encoding="utf-8").lower()
        markers = [
            "authentication",
            "authorization",
            "rls",
            "service-role",
            "idempotency",
            "webhook",
            "payment",
            "retry",
            "reconciliation",
            "independent review",
        ]
        for marker in markers:
            if marker not in model_text:
                failures.append(
                    f"SaaS production trust model is missing required marker: {marker}"
                )

    if failures:
        print("SaaS production trust pack validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        "SaaS production trust pack valid: "
        f"{len(REQUIRED_SKILLS)} skills, 1 workflow, 1 independent review gate"
    )


if __name__ == "__main__":
    main()
