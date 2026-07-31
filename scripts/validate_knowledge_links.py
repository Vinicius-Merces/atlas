from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBSIDIAN = ROOT / "obsidian"
MEMORY = ROOT / ".claude" / "memory"
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
WIKI_LINK = re.compile(r"\[\[([^\]]+)\]\]")


def resolve_markdown_link(source: Path, target: str) -> bool:
    target = target.split("#", 1)[0].strip()
    if not target or "://" in target or target.startswith("mailto:"):
        return True
    return (source.parent / target).resolve().exists()


def resolve_wiki_link(source: Path, target: str) -> tuple[bool, str]:
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return True, ""

    direct = (source.parent / target).resolve()
    candidates = [direct, direct.with_suffix(".md")]
    for candidate in candidates:
        if candidate.is_file():
            return True, candidate.as_posix()

    if "/" not in target and "\\" not in target:
        matches = [
            path for path in OBSIDIAN.rglob("*.md") if path.stem == target
        ]
        if len(matches) == 1:
            return True, matches[0].as_posix()
        if len(matches) > 1:
            return False, f"ambiguous ({len(matches)} matches)"
    return False, "missing"


def main() -> None:
    failures: list[str] = []
    checked = 0

    for path in sorted(MEMORY.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            checked += 1
            if not resolve_markdown_link(path, target):
                failures.append(
                    f"{path.relative_to(ROOT)} -> {target}: missing"
                )

    for path in sorted(OBSIDIAN.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for target in WIKI_LINK.findall(text):
            checked += 1
            valid, detail = resolve_wiki_link(path, target)
            if not valid:
                failures.append(
                    f"{path.relative_to(ROOT)} -> {target}: {detail}"
                )

    if failures:
        print("Knowledge link validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(f"Knowledge link validation passed: {checked} links")


if __name__ == "__main__":
    main()
