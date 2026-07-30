from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_version_is_beta() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert "-beta." in version


def test_beta_release_documents_exist() -> None:
    required = [
        "release/BETA-1-MIGRATION.md",
        "release/BETA-1-RELEASE-NOTES.md",
        "release/KNOWN-LIMITATIONS.md",
        "compatibility/core-contracts.json",
        "compatibility/support-policy.md",
    ]
    for relative in required:
        assert (ROOT / relative).is_file(), relative
