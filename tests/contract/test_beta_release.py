import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def current_prerelease() -> tuple[str, str]:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    match = re.fullmatch(r"0\.1\.0-(beta|rc)\.(\d+)", version)
    assert match, version
    return match.group(1), match.group(2)


def test_version_is_supported_prerelease() -> None:
    channel, _ = current_prerelease()
    assert channel in {"beta", "rc"}


def test_current_prerelease_documents_exist() -> None:
    channel, number = current_prerelease()
    prefix = channel.upper()
    required = [
        f"release/{prefix}-{number}-MIGRATION.md",
        f"release/{prefix}-{number}-RELEASE-NOTES.md",
        f"release/{channel}.{number}.manifest.json",
        "release/KNOWN-LIMITATIONS.md",
        "compatibility/core-contracts.json",
        "compatibility/support-policy.md",
    ]
    for relative in required:
        assert (ROOT / relative).is_file(), relative
