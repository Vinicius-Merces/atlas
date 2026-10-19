from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import build_context_pack as builder
from scripts import context_extraction as extraction
from scripts.validate_context_pack import verify

ROOT = Path(__file__).resolve().parents[2]


def project(root):
    root.mkdir(parents=True, exist_ok=True)
    task = {'id': 'task-selection', 'task_type': 'feature', 'summary': 'Recover checkpoint after refresh',
            'primary_role': 'worker', 'workflow': 'feature', 'constraints': ['Keep full safety instructions'],
            'acceptance_criteria': ['Recover checkpoint works'], 'affected_paths': ['notes.md']}
    for name in builder.canonical_sources({**task, 'affected_paths': []}):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'Complete instructions for {name}\n')
    (root / 'notes.md').write_text('# Introduction\n' + 'unrelated background\n' * 400 +
                                 '\n# Recover checkpoint\nSaved state is restored after refresh.\n')
    return task


def compose(root, task, **kwargs):
    return builder.compose(task, [], 400, 10000, root=root, **kwargs)


def save(root, task, text, data):
    pack = root / 'pack.md'
    pack.write_bytes(text.encode())
    manifest = root / 'pack.manifest.json'
    data['context_pack'] = str(pack)
    manifest.write_text(json.dumps(data))
    verify(manifest, pack, task_id=task['id'], root=root)
    return manifest, pack


def test_selects_relevant_markdown_beyond_prefix_and_records_source_map(tmp_path):
    task = project(tmp_path)
    text, data = compose(tmp_path, task)
    assert 'Saved state is restored' in text
    assert '[Source lines' in text
    item = data['source_excerpts']['notes.md']
    assert item['strategy'] == 'markdown-sections'
    assert item['ranges'][0]['start_line'] > 400
    assert data['truncated_sources'] == ['notes.md']
    prefix, baseline = compose(tmp_path, task, selection_mode='prefix')
    assert 'Saved state is restored' not in prefix
    assert baseline['extraction_max_chars'] == data['extraction_max_chars']
    assert baseline['max_total_chars'] == data['max_total_chars']
    save(tmp_path, task, text, data)


def test_python_symbol_decorators_are_selected_beyond_prefix(tmp_path):
    task = project(tmp_path)
    task['affected_paths'] = ['service.py']
    (tmp_path / 'service.py').write_text('# module background\n' * 400 +
        '@retry\nasync def recover_checkpoint():\n    """Restore saved state."""\n    return "saved"\n')
    text, data = compose(tmp_path, task)
    assert '@retry\nasync def recover_checkpoint' in text
    assert data['source_excerpts']['service.py']['strategy'] == 'python-symbols'
    save(tmp_path, task, text, data)


def test_headings_in_fenced_code_are_not_sections():
    source = '# Real\n```md\n# Fake checkpoint\n```\n# End\n'
    assert [title for _, _, title in extraction.units(source, '.md')] == ['Real', 'End']


def test_nested_method_body_is_not_hidden_by_large_parent_class(tmp_path):
    task = project(tmp_path)
    task['affected_paths'] = ['state.py']
    (tmp_path / 'state.py').write_text('class Store:\n' + '    # background detail\n' * 400 +
        '    def load(self):\n        return "checkpoint after refresh"\n')
    text, data = compose(tmp_path, task)
    assert 'return "checkpoint after refresh"' in text
    assert data['source_excerpts']['state.py']['ranges'][0]['start_line'] > 400


def test_extra_instruction_files_are_never_excerpted(tmp_path):
    task = project(tmp_path)
    path = tmp_path / 'nested/AGENTS.md'
    path.parent.mkdir()
    path.write_text('MANDATORY RULE\n' * 80)
    text, data = builder.compose(task, ['nested/AGENTS.md'], 400, 10000, root=tmp_path)
    assert path.read_text().rstrip() in text
    assert 'nested/AGENTS.md' not in data['source_excerpts']
    with pytest.raises(SystemExit, match='cannot fit mandatory'):
        builder.compose(task, ['nested/AGENTS.md'], 400, 500, root=tmp_path)


def test_warm_cache_reuses_selection_without_reparsing_and_keeps_bytes(tmp_path, monkeypatch):
    task = project(tmp_path)
    cold, first = compose(tmp_path, task)
    def should_not_parse(*args):
        raise AssertionError('warm selection must not parse source again')
    monkeypatch.setattr(extraction, 'units', should_not_parse)
    warm, second = compose(tmp_path, task)
    assert warm == cold
    assert first['source_excerpts'] == second['source_excerpts']
    assert first['extraction_cache'] == {'hit': 0, 'miss': 1, 'bypassed': 0}
    assert second['extraction_cache'] == {'hit': 1, 'miss': 0, 'bypassed': 0}


@pytest.mark.parametrize('change', ['source-tail', 'query', 'budget', 'version', 'mode', 'project-id'])
def test_cache_invalidates_all_selection_inputs(tmp_path, monkeypatch, change):
    task = project(tmp_path)
    _, first = compose(tmp_path, task)
    options = {}
    if change == 'source-tail':
        with (tmp_path / 'notes.md').open('a') as stream: stream.write('\nchanged tail\n')
    if change == 'query': task['summary'] = 'Inspect introduction'
    if change == 'budget': options['max_chars'] = 500
    if change == 'version': monkeypatch.setattr(extraction, 'VERSION', 'new-version-test')
    if change == 'mode': options['selection_mode'] = 'prefix'
    if change == 'project-id':
        (tmp_path / '.atlas/project-memory.json').write_text(json.dumps({'project_id': 'new-project'}))
    _, second = builder.compose(task, [], options.pop('max_chars', 400), 10000, root=tmp_path, **options)
    assert second['extraction_cache']['miss'] == 1
    assert first['source_excerpts']['notes.md']['cache_key'] != second['source_excerpts']['notes.md']['cache_key']


def test_copied_cache_is_not_shared_across_projects(tmp_path):
    left, right = tmp_path / 'left', tmp_path / 'right'
    one, two = project(left), project(right)
    _, first = compose(left, one)
    shutil.copytree(left / '.atlas/cache', right / '.atlas/cache', dirs_exist_ok=True)
    _, second = compose(right, two)
    assert second['extraction_cache']['hit'] == 0
    assert first['source_excerpts']['notes.md']['cache_key'] != second['source_excerpts']['notes.md']['cache_key']


@pytest.mark.parametrize('corruption', ['json', 'checksum', 'range', 'injected-text'])
def test_corrupt_cache_is_rebuilt_from_source(tmp_path, corruption):
    task = project(tmp_path)
    expected, data = compose(tmp_path, task)
    key = data['source_excerpts']['notes.md']['cache_key']
    cache = tmp_path / f'.atlas/cache/context-extractions/{key}.json'
    record = json.loads(cache.read_text())
    if corruption == 'checksum': record['checksum'] = '0' * 64
    if corruption == 'range': record['selection']['ranges'] = [[-1, 9999999]]
    if corruption == 'injected-text': record['selection']['text'] = 'INJECTED FROM CACHE'
    cache.write_text('not-json' if corruption == 'json' else json.dumps(record))
    text, rebuilt = compose(tmp_path, task)
    assert text == expected and 'INJECTED FROM CACHE' not in text
    assert rebuilt['extraction_cache']['miss'] == 1


def test_no_cache_does_not_read_or_write_cache(tmp_path):
    task = project(tmp_path)
    first, data = compose(tmp_path, task, use_cache=False)
    assert not (tmp_path / '.atlas/cache').exists()
    assert data['extraction_cache']['bypassed'] == 1
    assert first == compose(tmp_path, task, use_cache=False)[0]


@pytest.mark.parametrize('location', ['directory', 'entry'])
def test_cache_symlinks_cannot_write_outside_project(tmp_path, location):
    root = tmp_path / 'project'
    task = project(root)
    foreign = tmp_path / 'foreign'
    foreign.mkdir()
    marker = foreign / 'marker'
    marker.write_text('preserve')
    if location == 'directory':
        (root / '.atlas').mkdir()
        (root / '.atlas/cache').symlink_to(foreign, target_is_directory=True)
    else:
        _, data = compose(root, task)
        key = data['source_excerpts']['notes.md']['cache_key']
        path = root / f'.atlas/cache/context-extractions/{key}.json'
        path.unlink()
        path.symlink_to(marker)
    _, data = compose(root, task)
    assert data['extraction_cache']['bypassed'] == 1
    assert marker.read_text() == 'preserve'
    assert list(foreign.iterdir()) == [marker]


@pytest.mark.parametrize('mutation', ['line-map', 'range', 'hash', 'cross-project', 'source-tail'])
def test_manifest_checks_range_map_and_project_identity(tmp_path, mutation):
    task = project(tmp_path)
    text, data = compose(tmp_path, task)
    manifest, pack = save(tmp_path, task, text, data)
    item = data['source_excerpts']['notes.md']
    if mutation == 'line-map': item['ranges'][0]['start_line'] = 1
    if mutation == 'range': item['ranges'][0]['end'] = 999999
    if mutation == 'hash': item['excerpt_sha256'] = '0' * 64
    if mutation == 'source-tail':
        with (tmp_path / 'notes.md').open('a') as stream: stream.write('out-of-excerpt change')
    manifest.write_text(json.dumps(data))
    other_root = tmp_path / 'other' if mutation == 'cross-project' else tmp_path
    with pytest.raises(ValueError): verify(manifest, pack, task_id=task['id'], root=other_root)


def test_full_pack_budget_and_deferred_range_map(tmp_path):
    task = project(tmp_path)
    text, data = builder.compose(task, [], 400, 2400, root=tmp_path)
    assert len(text) <= 2400
    assert not set(data['source_excerpts']) & set(data['deferred_sources'])
    save(tmp_path, task, text, data)


def test_explicit_product_root_does_not_fall_back_to_toolkit(tmp_path):
    task = project(tmp_path)
    path = tmp_path / 'task.json'
    path.write_text(json.dumps(task))
    command = [sys.executable, str(ROOT / 'scripts/build_context_pack.py'), '--task-envelope', str(path),
               '--project-root', str(tmp_path), '--no-cache']
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert 'Complete instructions for AGENTS.md' in (tmp_path / 'task.context.md').read_text()
    (tmp_path / 'AGENTS.md').unlink()
    assert subprocess.run(command, cwd=ROOT, capture_output=True).returncode != 0
    foreign = tmp_path.parent / 'outside.context.md'
    assert subprocess.run([*command, '--output', str(foreign)], cwd=ROOT, capture_output=True).returncode != 0
    assert not foreign.exists()


def test_context_output_cannot_overwrite_mandatory_sources(tmp_path):
    task = project(tmp_path)
    path = tmp_path / 'task.json'
    path.write_text(json.dumps(task))
    original = (tmp_path / 'AGENTS.md').read_bytes()
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_context_pack.py'), '--task-envelope', str(path),
        '--project-root', str(tmp_path), '--output', str(tmp_path / 'AGENTS.md')], cwd=ROOT, capture_output=True)
    assert result.returncode != 0
    assert (tmp_path / 'AGENTS.md').read_bytes() == original


def cli_product(root):
    task = project(root)
    task.update({'reviews': [], 'validation': [], 'runtime': 'codex'})
    (root / '.claude/registry.json').write_text(json.dumps({'agents': ['worker'], 'orchestrator': 'worker', 'workflows': ['feature']}))
    declaration = root / 'adapters/codex/runtime-declaration.json'
    declaration.parent.mkdir(parents=True)
    declaration.write_text(json.dumps({'runtime': 'codex'}))
    envelope = root / 'task.json'
    envelope.write_text(json.dumps(task))
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_context_pack.py'), '--project-root', str(root),
        '--task-envelope', str(envelope)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return envelope


@pytest.mark.parametrize('target', ['AGENTS.md', '.claude/registry.json', 'adapters/codex/runtime-declaration.json',
                                  'task.context.md', 'task.context.manifest.json', 'notes.md'])
def test_planner_cannot_overwrite_verified_inputs(tmp_path, target):
    envelope = cli_product(tmp_path)
    output = tmp_path / target
    before = output.read_bytes()
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_execution_plan.py'), '--project-root', str(tmp_path),
        '--task-envelope', str(envelope), '--runtime', 'codex', '--output', str(output)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    assert 'overwrite' in result.stderr
    assert output.read_bytes() == before


@pytest.mark.parametrize('field', ['summary', 'constraints', 'acceptance_criteria', 'affected_paths', 'reviews'])
def test_planner_rejects_changed_task_same_id(tmp_path, field):
    envelope = cli_product(tmp_path)
    command = [sys.executable, str(ROOT / 'scripts/build_execution_plan.py'), '--project-root', str(tmp_path),
               '--task-envelope', str(envelope), '--runtime', 'codex']
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    task = json.loads(envelope.read_text())
    task[field] = 'changed task' if field == 'summary' else ['changed item']
    envelope.write_text(json.dumps(task))
    result = subprocess.run([*command, '--allow-unverified-context'], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    assert 'Task inputs changed' in result.stderr
