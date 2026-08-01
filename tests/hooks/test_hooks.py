import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOKS_JSON = ROOT / ".claude" / "hooks" / "hooks.json"
SCRIPTS_DIR = ROOT / ".claude" / "hooks" / "scripts"
BLOCK_STRAY_DOCS = SCRIPTS_DIR / "block_stray_docs.py"
SESSION_END_REMINDER = SCRIPTS_DIR / "session_end_reminder.py"


def run_hook(script: Path, payload: dict | str) -> subprocess.CompletedProcess:
    stdin = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run(
        [sys.executable, str(script)],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )


def test_hooks_json_is_valid_and_scripts_exist() -> None:
    data = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    hooks = data["hooks"]
    assert "PreToolUse" in hooks
    assert "SessionEnd" in hooks
    for event, entries in hooks.items():
        for entry in entries:
            assert "matcher" in entry
            assert "description" in entry
            for inner in entry["hooks"]:
                assert inner["type"] == "command"
                assert inner["command"] == "python"
                script_arg = inner["args"][0]
                relative = script_arg.replace("${CLAUDE_PLUGIN_ROOT}/hooks/", "")
                hooks_dir = HOOKS_JSON.parent
                assert (hooks_dir / relative).exists(), f"{event}: missing {relative}"


def test_block_stray_docs_scripts_exist() -> None:
    assert BLOCK_STRAY_DOCS.exists()
    assert SESSION_END_REMINDER.exists()


def test_blocks_stray_root_markdown_file() -> None:
    cwd = str(Path("C:/fake-project") if os.name == "nt" else Path("/fake-project"))
    file_path = str(Path(cwd) / "RANDOM_NOTES.md")
    payload = {"tool_name": "Write", "tool_input": {"file_path": file_path}, "cwd": cwd}
    result = run_hook(BLOCK_STRAY_DOCS, payload)
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_allows_markdown_file_in_subdirectory() -> None:
    cwd = str(Path("C:/fake-project") if os.name == "nt" else Path("/fake-project"))
    file_path = str(Path(cwd) / "docs" / "guide.md")
    payload = {"tool_name": "Write", "tool_input": {"file_path": file_path}, "cwd": cwd}
    result = run_hook(BLOCK_STRAY_DOCS, payload)
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_allows_allowlisted_root_filenames() -> None:
    cwd = str(Path("C:/fake-project") if os.name == "nt" else Path("/fake-project"))
    for name in ("README.md", "CLAUDE.md", "AGENTS.md", "CONTRIBUTING.md", "CHANGELOG.md"):
        file_path = str(Path(cwd) / name)
        payload = {"tool_name": "Write", "tool_input": {"file_path": file_path}, "cwd": cwd}
        result = run_hook(BLOCK_STRAY_DOCS, payload)
        assert result.returncode == 0
        assert result.stdout.strip() == "", name


def test_ignores_non_write_tools() -> None:
    cwd = str(Path("C:/fake-project") if os.name == "nt" else Path("/fake-project"))
    file_path = str(Path(cwd) / "NOTES.md")
    payload = {"tool_name": "Edit", "tool_input": {"file_path": file_path}, "cwd": cwd}
    result = run_hook(BLOCK_STRAY_DOCS, payload)
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_ignores_non_doc_extensions() -> None:
    cwd = str(Path("C:/fake-project") if os.name == "nt" else Path("/fake-project"))
    file_path = str(Path(cwd) / "config.json")
    payload = {"tool_name": "Write", "tool_input": {"file_path": file_path}, "cwd": cwd}
    result = run_hook(BLOCK_STRAY_DOCS, payload)
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_fails_open_on_missing_cwd() -> None:
    payload = {"tool_name": "Write", "tool_input": {"file_path": "NOTES.md"}}
    result = run_hook(BLOCK_STRAY_DOCS, payload)
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_fails_open_on_invalid_json() -> None:
    result = run_hook(BLOCK_STRAY_DOCS, "not valid json")
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_session_end_reminder_never_blocks() -> None:
    result = run_hook(SESSION_END_REMINDER, {"session_id": "abc"})
    assert result.returncode == 0
    assert "atlas-checkpoint" in result.stderr or "atlas-close-session" in result.stderr


def test_session_end_reminder_fails_open_on_invalid_json() -> None:
    result = run_hook(SESSION_END_REMINDER, "not valid json")
    assert result.returncode == 0
