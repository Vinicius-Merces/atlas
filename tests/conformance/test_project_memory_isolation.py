from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/project_memory.py'


def project(tmp_path, name):
    root = tmp_path / name
    root.mkdir()
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    subprocess.run(['git', '-C', str(root), 'remote', 'add', 'origin', f'https://example.invalid/{name}.git'], check=True)
    (root / 'README.md').write_text(f'# Product {name}\n')
    (root / 'VERSION').write_text('9.8.7\n')
    return root


def run(action, root, *extra):
    return subprocess.run([sys.executable, str(SCRIPT), action, '--project-root', str(root), *extra], cwd=ROOT, capture_output=True, text=True)


def load(root, name='latest-session.json'):
    return json.loads((root / '.atlas/continuity' / name).read_text())


def test_two_projects_resume_independently_without_writing_framework(tmp_path):
    before = (ROOT / '.atlas/continuity/latest-session.json').read_bytes()
    left, right = project(tmp_path, 'alpha'), project(tmp_path, 'beta')
    memory = left / '.claude/memory/architecture.md'
    memory.parent.mkdir(parents=True)
    memory.write_text('# Alpha architecture\nOnly alpha uses engine A.\n')
    result = run('init', left)
    assert result.returncode == 0, result.stderr
    a = json.loads(result.stdout)
    result = run('init', right)
    assert result.returncode == 0, result.stderr
    b = json.loads(result.stdout)
    assert a['project_id'] != b['project_id']
    assert load(left)['framework_version'] == (ROOT / 'VERSION').read_text().strip()
    assert (left / 'VERSION').read_text() == '9.8.7\n'
    session = load(left)
    session.update(session_id='session-alpha-done', summary='Alpha checkpoint', pending_work=['Finish alpha validation'], next_action='Run alpha integration', risks=['Alpha risk'])
    staged = left / '.atlas/continuity/staged.json'
    staged.write_text(json.dumps(session))
    result = run('close', left, '--session-file', str(staged))
    assert result.returncode == 0, result.stderr
    # A separate process resumes from files only, with no conversation state.
    resumed = run('start', left)
    assert resumed.returncode == 0, resumed.stderr
    assert json.loads(resumed.stdout)['pending_work'] == ['Finish alpha validation']
    assert json.loads(run('start', right).stdout)['pending_work'] != ['Finish alpha validation']
    assert 'Only alpha uses engine A' in (left / a['obsidian_view']).read_text()
    assert 'Only alpha uses engine A' not in (right / b['obsidian_view']).read_text()
    assert (ROOT / '.atlas/continuity/latest-session.json').read_bytes() == before
    assert len(list((left / '.atlas/continuity/sessions').glob('*.json'))) == 1


def test_foreign_session_and_identity_are_rejected(tmp_path):
    left, right = project(tmp_path, 'alpha'), project(tmp_path, 'beta')
    assert run('init', left).returncode == run('init', right).returncode == 0
    before = (right / '.atlas/continuity/latest-session.json').read_bytes()
    staged = right / '.atlas/continuity/staged.json'
    staged.write_text(json.dumps(load(left)))
    result = run('close', right, '--session-file', str(staged))
    assert result.returncode != 0 and 'identity/version' in result.stderr
    assert (right / '.atlas/continuity/latest-session.json').read_bytes() == before
    subprocess.run(['git', '-C', str(right), 'remote', 'set-url', 'origin', 'https://example.invalid/another.git'], check=True)
    assert 'origin changed' in run('start', right).stderr


def test_initialization_is_idempotent_and_preserves_user_memory(tmp_path):
    root = project(tmp_path, 'alpha')
    assert run('init', root).returncode == 0
    memory = root / '.claude/memory/custom.md'
    memory.write_text('# Validated alpha decision\n')
    before = (root / '.atlas/continuity/latest-session.json').read_bytes()
    assert run('init', root).returncode == 0
    assert memory.read_text() == '# Validated alpha decision\n'
    assert (root / '.atlas/continuity/latest-session.json').read_bytes() == before
    resumed = json.loads(run('start', root).stdout)
    assert '.claude/memory/custom.md' in resumed['memory_sources']
    assert resumed['obsidian_status'] == 'stale'


@pytest.mark.parametrize('kind', ['outside-symlink', 'copied-framework', 'unbound-continuity'])
def test_init_blocks_unsafe_or_ambiguous_roots_before_writing(tmp_path, kind):
    root = project(tmp_path, 'alpha')
    if kind == 'outside-symlink':
        (root / '.atlas').symlink_to(ROOT / '.atlas', target_is_directory=True)
    elif kind == 'copied-framework':
        memory = root / '.claude/memory/architecture.md'
        memory.parent.mkdir(parents=True)
        memory.write_bytes((ROOT / '.claude/memory/architecture.md').read_bytes())
    else:
        path = root / '.atlas/continuity/latest-session.json'
        path.parent.mkdir(parents=True)
        path.write_text('{}')
    result = run('init', root)
    assert result.returncode != 0
    if kind != 'outside-symlink':
        assert not (root / '.atlas/project-memory.json').exists()


def test_edited_obsidian_view_is_not_overwritten(tmp_path):
    root = project(tmp_path, 'alpha')
    result = run('init', root)
    view = root / json.loads(result.stdout)['obsidian_view']
    view.write_text('User edited this view')
    staged = root / '.atlas/continuity/staged.json'
    staged.write_text(json.dumps(load(root)))
    result = run('close', root, '--session-file', str(staged))
    assert result.returncode != 0 and 'view was edited' in result.stderr
    assert view.read_text() == 'User edited this view'


def test_original_atlas_and_subdirectories_are_not_product_targets(tmp_path):
    assert run('init', ROOT).returncode != 0
    root = project(tmp_path, 'alpha')
    subdir = root / 'src'
    subdir.mkdir()
    assert run('init', subdir).returncode != 0


def test_nested_memory_symlink_cannot_read_the_toolkit_memory(tmp_path):
    root = project(tmp_path, 'alpha')
    memory = root / '.claude/memory'
    memory.mkdir(parents=True)
    (memory / 'index.md').symlink_to(ROOT / '.claude/memory/index.md')
    result = run('init', root)
    assert result.returncode != 0 and 'escapes' in result.stderr
    assert not (root / '.atlas/project-memory.json').exists()
