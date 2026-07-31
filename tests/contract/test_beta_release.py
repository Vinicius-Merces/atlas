import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def current_release() -> tuple[str, str | None]:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    match = re.fullmatch(r"0\.1\.0(?:-(beta|rc)\.(\d+))?", version)
    assert match, version
    return match.group(1) or "stable", match.group(2)


def test_version_is_supported_release() -> None:
    channel, _ = current_release()
    assert channel in {"beta", "rc", "stable"}


def test_current_release_documents_exist() -> None:
    channel, number = current_release()
    if channel == "stable":
        release_documents = [
            "release/0.1.0-MIGRATION.md",
            "release/0.1.0-RELEASE-NOTES.md",
            "release/0.1.0.manifest.json",
        ]
    else:
        prefix = channel.upper()
        release_documents = [
            f"release/{prefix}-{number}-MIGRATION.md",
            f"release/{prefix}-{number}-RELEASE-NOTES.md",
            f"release/{channel}.{number}.manifest.json",
        ]
    required = [
        *release_documents,
        "release/KNOWN-LIMITATIONS.md",
        "compatibility/core-contracts.json",
        "compatibility/support-policy.md",
    ]
    for relative in required:
        assert (ROOT / relative).is_file(), relative
