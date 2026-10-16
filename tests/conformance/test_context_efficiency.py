from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import build_context_pack as builder
from scripts.validate_context_pack import verify

ROOT = Path(__file__).resolve().parents[2]


def setup_pack(tmp_path, monkeypatch):
    monkeypatch.setattr(builder, 'ROOT', tmp_path)
    envelope = {'id': 'one', 'task_type': 'feature', 'summary': 'First task',
                'primary_role': 'worker', 'workflow': 'feature', 'constraints': ['Keep compatibility'],
                'acceptance_criteria': ['Behavior works'], 'affected_paths': ['large.py']}
    for name in builder.canonical_sources({**envelope, 'affected_paths': []}):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'Canonical instructions for {name}\n')
    (tmp_path / 'large.py').write_text('á' * 6000)
    return envelope


def save(tmp_path, envelope, content, manifest):
    path = tmp_path / 'context.md'
    path.write_bytes(content.encode('utf-8'))
    manifest['context_pack'] = str(path)
    manifest_path = path.with_suffix('.manifest.json')
    manifest_path.write_text(json.dumps(manifest))
    return manifest_path, path


def test_budget_includes_metadata_and_defers_optional_sources(tmp_path, monkeypatch):
    envelope = setup_pack(tmp_path, monkeypatch)
    content, data = builder.compose(envelope, [], 4000, 3000)
    assert len(content) <= 3000
    assert data['rendered_chars'] == len(content)
    assert data['deferred_sources'] == ['large.py']
    assert 'large.py' not in data['source_hashes']
    assert 'Keep compatibility' in content
    assert data['measurement_unit'] == 'characters'
    manifest, path = save(tmp_path, envelope, content, data)
    assert verify(manifest, path, task_id='one', root=tmp_path)['deferred_sources']


def test_mandatory_instructions_are_never_silently_cut(tmp_path, monkeypatch):
    envelope = setup_pack(tmp_path, monkeypatch)
    path = tmp_path / 'AGENTS.md'
    path.write_text('REQUIRED RULE\n' * 100)
    content, _ = builder.compose(envelope, [], 200, 10000)
    assert path.read_text().rstrip() in content
    with pytest.raises(SystemExit, match='cannot fit mandatory'):
        builder.compose(envelope, [], 200, 200)


def test_prefix_is_stable_when_task_metadata_changes(tmp_path, monkeypatch):
    envelope = setup_pack(tmp_path, monkeypatch)
    first, left = builder.compose(envelope, [], 4000, 12000)
    second, right = builder.compose({**envelope, 'id': 'two', 'summary': 'Second task'}, [], 4000, 12000)
    size = left['stable_prefix_chars']
    assert first[:size] == second[:size]
    assert left['stable_prefix_sha256'] == right['stable_prefix_sha256']
    assert left['context_sha256'] != right['context_sha256']
    assert 'large.py' in left['truncated_sources']
    assert '[Excerpt truncated' in first


@pytest.mark.parametrize('mutation', ['change-source', 'remove-source', 'change-pack', 'wrong-task', 'outside-root'])
def test_freshness_and_integrity_reject_invalid_context(tmp_path, monkeypatch, mutation):
    envelope = setup_pack(tmp_path, monkeypatch)
    content, data = builder.compose(envelope, [], 4000, 12000)
    manifest, path = save(tmp_path, envelope, content, data)
    verify(manifest, path, task_id='one', root=tmp_path)
    if mutation == 'change-source':
        # A change beyond the excerpt must also invalidate the derived pack.
        with (tmp_path / 'large.py').open('a') as stream:
            stream.write('changed tail')
    elif mutation == 'remove-source':
        (tmp_path / 'AGENTS.md').unlink()
    elif mutation == 'change-pack':
        path.write_text(content + 'tampered')
    elif mutation == 'outside-root':
        data['sources'].append('../outside.txt')
        data['source_hashes']['../outside.txt'] = hashlib.sha256(b'outside').hexdigest()
        manifest.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        verify(manifest, path, task_id='wrong' if mutation == 'wrong-task' else 'one', root=tmp_path)


def test_context_secrets_and_missing_required_sources(tmp_path, monkeypatch):
    envelope = setup_pack(tmp_path, monkeypatch)
    (tmp_path / '.env.production').write_text('SECRET=hidden')
    content, data = builder.compose(envelope, ['.env.production'], 4000, 12000)
    assert 'SECRET=hidden' not in content
    assert '.env.production' in data['missing_sources']
    (tmp_path / 'AGENTS.md').unlink()
    with pytest.raises(SystemExit, match='Required context source'):
        builder.compose(envelope, [], 4000, 12000)


def test_planner_requires_manifest_and_refuses_stale_even_with_legacy_flag(tmp_path):
    task = tmp_path / 'task.json'
    envelope = {'id': 'planner-check', 'task_type': 'feature', 'summary': 'Test integration',
                'primary_role': 'product-architect', 'workflow': 'feature-delivery',
                'reviews': [], 'validation': [], 'context_pack': str(tmp_path / 'context.md')}
    context = tmp_path / 'context.md'
    context.write_text('legacy')
    task.write_text(json.dumps(envelope))
    command = [sys.executable, 'scripts/build_execution_plan.py', '--task-envelope', str(task), '--runtime', 'codex']
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0 and 'manifest is required' in result.stderr
    built = subprocess.run([sys.executable, 'scripts/build_context_pack.py', '--task-envelope', str(task), '--output', str(context)], cwd=ROOT, capture_output=True, text=True)
    assert built.returncode == 0, built.stderr
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['context_verified'] is True
    context.write_text(context.read_text() + 'tampered')
    result = subprocess.run([*command, '--allow-unverified-context'], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0 and 'integrity' in result.stderr
