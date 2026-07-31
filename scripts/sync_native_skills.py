from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
CLAUDE_SKILLS = ROOT / ".claude" / "skills"
CODEX_SKILLS = ROOT / ".agents" / "skills"
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def parse_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError(f"{path.relative_to(ROOT).as_posix()}: missing YAML frontmatter")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, raw = line.partition(":")
        if not separator:
            continue
        value = raw.strip()
        if value.startswith('"') and value.endswith('"'):
            value = json.loads(value)
        values[key.strip()] = value

    name = values.get("name", "")
    description = values.get("description", "")
    if not name or not description:
        raise ValueError(
            f"{path.relative_to(ROOT).as_posix()}: name and description are required"
        )
    return name, description


def canonical_skill_paths() -> dict[str, Path]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    expected = registry.get("skills", [])
    resolved: dict[str, Path] = {}
    errors: list[str] = []
    for name in expected:
        path = CLAUDE_SKILLS / name / "SKILL.md"
        if not path.is_file():
            errors.append(
                f"{name}: missing canonical Claude skill "
                f"{path.relative_to(ROOT).as_posix()}"
            )
            continue
        try:
            declared_name, _ = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if declared_name != name:
            errors.append(
                f"{path.relative_to(ROOT).as_posix()}: declares "
                f"{declared_name!r}, expected {name!r}"
            )
            continue
        resolved[name] = path

    discovered = {
        path.parent.name
        for path in CLAUDE_SKILLS.glob("*/SKILL.md")
        if path.is_file()
    }
    extra = sorted(discovered - set(expected))
    if extra:
        errors.append(f"Unregistered native Claude skills: {', '.join(extra)}")
    if errors:
        raise ValueError("\n".join(errors))
    return resolved


def codex_wrapper(name: str, canonical: Path) -> str:
    _, description = parse_frontmatter(canonical)
    target = canonical.relative_to(ROOT).as_posix()
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n"
        "---\n\n"
        f"# ATLAS skill adapter: {name}\n\n"
        f"Read `{target}` completely, then follow its canonical instructions.\n"
        "Use the shared ATLAS memory, contracts, workflow, and review gates; "
        "do not create Codex-only project knowledge.\n"
    )


def expected_outputs() -> dict[Path, str]:
    return {
        CODEX_SKILLS / name / "SKILL.md": codex_wrapper(name, canonical)
        for name, canonical in canonical_skill_paths().items()
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate Claude-native ATLAS skills and synchronize Codex-native "
            "repository wrappers."
        )
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report drift without writing generated Codex skill wrappers.",
    )
    args = parser.parse_args()

    try:
        outputs = expected_outputs()
    except ValueError as exc:
        print("Native skill synchronization failed:")
        for error in str(exc).splitlines():
            print(f"- {error}")
        raise SystemExit(1) from None

    differences: list[str] = []
    for path, expected in sorted(outputs.items()):
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current == expected:
            continue
        differences.append(path.relative_to(ROOT).as_posix())
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")

    discovered = {
        path.parent.name
        for path in CODEX_SKILLS.glob("*/SKILL.md")
        if path.is_file()
    }
    stale = sorted(discovered - {path.parent.name for path in outputs})
    if stale:
        differences.extend(
            f".agents/skills/{name}/SKILL.md (stale)" for name in stale
        )

    if args.check and differences:
        print("Native skills are out of sync:")
        for difference in differences:
            print(f"- {difference}")
        raise SystemExit(1)

    if stale:
        print("Stale Codex wrappers require explicit removal:")
        for name in stale:
            print(f"- .agents/skills/{name}/SKILL.md")
        raise SystemExit(1)

    if differences:
        print(f"Synchronized {len(differences)} Codex-native skill wrappers.")
    else:
        print(f"Native skill synchronization passed: {len(outputs)} skills")


if __name__ == "__main__":
    main()
