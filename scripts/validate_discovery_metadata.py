#!/usr/bin/env python3
"""Validate canonical discovery descriptions for ATLAS agents and skills."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
MAX_DESCRIPTION_LENGTH = 240


def read_frontmatter(path: Path) -> dict[str, object]:
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


def validate_description(
    *,
    kind: str,
    name: str,
    metadata: dict[str, object],
    failures: list[str],
    descriptions: dict[str, str],
) -> str | None:
    declared_name = metadata.get("name")
    if declared_name != name:
        failures.append(
            f"{kind} {name} declares name={declared_name!r} instead of {name!r}"
        )

    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        failures.append(f"{kind} {name} has no non-empty discovery description")
        return None

    normalized = " ".join(description.split())
    if len(normalized) > MAX_DESCRIPTION_LENGTH:
        failures.append(
            f"{kind} {name} description exceeds {MAX_DESCRIPTION_LENGTH} characters"
        )

    duplicate = descriptions.get(normalized.casefold())
    if duplicate is not None:
        failures.append(
            f"{kind} descriptions are not discriminative: {duplicate} and {name} are identical"
        )
    else:
        descriptions[normalized.casefold()] = name

    return normalized


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    failures: list[str] = []

    agent_names = list(registry.get("agents", []))
    orchestrator = registry.get("orchestrator")
    if isinstance(orchestrator, str) and orchestrator:
        agent_names.append(orchestrator)

    skill_names = list(registry.get("skills", []))

    agent_descriptions: dict[str, str] = {}
    skill_descriptions: dict[str, str] = {}

    for name in sorted(agent_names):
        path = ROOT / ".claude" / "agents" / f"{name}.md"
        if not path.is_file():
            failures.append(f"registered agent is missing: {path.relative_to(ROOT)}")
            continue
        try:
            metadata = read_frontmatter(path)
        except ValueError as exc:
            failures.append(str(exc))
            continue
        validate_description(
            kind="agent",
            name=name,
            metadata=metadata,
            failures=failures,
            descriptions=agent_descriptions,
        )

    for name in sorted(skill_names):
        canonical = ROOT / ".claude" / "skills" / name / "SKILL.md"
        wrapper = ROOT / ".agents" / "skills" / name / "SKILL.md"

        if not canonical.is_file():
            failures.append(
                f"registered skill is missing: {canonical.relative_to(ROOT)}"
            )
            continue

        try:
            metadata = read_frontmatter(canonical)
        except ValueError as exc:
            failures.append(str(exc))
            continue

        canonical_description = validate_description(
            kind="skill",
            name=name,
            metadata=metadata,
            failures=failures,
            descriptions=skill_descriptions,
        )

        if not wrapper.is_file():
            failures.append(
                f"Codex-native skill wrapper is missing: {wrapper.relative_to(ROOT)}"
            )
            continue

        try:
            wrapper_metadata = read_frontmatter(wrapper)
        except ValueError as exc:
            failures.append(str(exc))
            continue

        if wrapper_metadata.get("name") != name:
            failures.append(f"Codex wrapper {name} declares a different skill name")

        wrapper_description = wrapper_metadata.get("description")
        if not isinstance(wrapper_description, str) or not wrapper_description.strip():
            failures.append(f"Codex wrapper {name} has no discovery description")
        elif canonical_description is not None:
            normalized_wrapper = " ".join(wrapper_description.split())
            if normalized_wrapper != canonical_description:
                failures.append(
                    f"Codex wrapper {name} description drifts from canonical skill description"
                )

    if failures:
        print("Discovery metadata validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        "Discovery metadata valid: "
        f"{len(agent_names)} agents and {len(skill_names)} skills have canonical descriptions; "
        "Codex skill descriptions are synchronized."
    )


if __name__ == "__main__":
    main()
