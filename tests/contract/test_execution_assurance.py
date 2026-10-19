from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

from scripts.execution_assurance import delivery, models, security, validate

ROOT = Path(__file__).resolve().parents[2]
TODAY = date(2026, 10, 19)


def artifact(root, name, content):
    path = root / name
    path.write_text(content)
    return {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def security_record(root):
    source = artifact(root, "reviewed-bundle.txt", "complete immutable skill bundle")
    evidence = artifact(root, "receipt.txt", "sandbox and scan receipt (test fixture)")
    return {"kind": "security", "source": source['path'], "source_sha256": source['sha256'],
            "origin": "https://example.invalid/reviewed-source", "version": "test", "trust": "verified-external",
            "approved": True, "reviewer": "independent-test-reviewer", "permissions": ["read"], "approved_permissions": ["read"],
            "sandbox": {"enforced": True, "receipt": evidence},
            "checks": [{"type": t, "status": "passed", "source_sha256": source['sha256'], "evidence": evidence}
                       for t in ['secrets', 'dependencies']]}


def test_security_admits_reviewed_source_and_detects_tamper(tmp_path):
    data = security_record(tmp_path)
    assert security(data, tmp_path)['outcome'] == 'admitted'
    (tmp_path / data['source']).write_text('modified after review')
    with pytest.raises(ValueError):
        security(data, tmp_path)


@pytest.mark.parametrize('change', ['unapproved', 'unverified', 'blocked', 'permission', 'sandbox', 'scan', 'scan-source', 'missing-scan', 'duplicate-scan', 'receipt'])
def test_security_fails_closed(tmp_path, change):
    data = security_record(tmp_path)
    if change == 'unapproved': data['approved'] = False
    if change == 'unverified': data['trust'] = 'unverified-external'
    if change == 'blocked': data['trust'] = 'blocked'
    if change == 'permission': data['permissions'].append('shell')
    if change == 'sandbox': data['sandbox']['enforced'] = False
    if change == 'scan': data['checks'][0]['status'] = 'unavailable'
    if change == 'scan-source': data['checks'][0]['source_sha256'] = '0' * 64
    if change == 'missing-scan': data['checks'].pop()
    if change == 'duplicate-scan': data['checks'].append(data['checks'][0])
    if change == 'receipt': data['sandbox']['receipt']['sha256'] = '0' * 64
    with pytest.raises(ValueError): security(data, tmp_path)


@pytest.mark.parametrize('path', ['../escape.txt', '/etc/passwd', '.env'])
def test_evidence_path_restrictions(tmp_path, path):
    data = security_record(tmp_path)
    data['source'] = path
    with pytest.raises(ValueError): security(data, tmp_path)


def test_evidence_symlink_rejected(tmp_path):
    data = security_record(tmp_path)
    (tmp_path / 'link.txt').symlink_to(tmp_path / data['source'])
    data['source'] = 'link.txt'
    with pytest.raises(ValueError): security(data, tmp_path)


def inventory():
    return {"kind": "models", "models": [{"provider": "test-provider", "model": "test-model", "status": "active",
        "verified_on": "2026-10-18", "valid_until": "2026-10-25", "source": "https://example.invalid/models",
        "capabilities": ["chat", "tools"], "profiles": ["support"], "max_data_class": "internal", "financial_class": "free-tier"}]}


def route(data):
    return models(data, profile='support', requires={'chat', 'tools'}, data_class='internal', allow_paid=False, today=TODAY)


@pytest.mark.parametrize('field,value', [('status', 'retired'), ('status', 'deprecated'), ('status', 'unknown'),
    ('valid_until', '2026-10-18'), ('verified_on', '2026-10-20'), ('retirement_on', '2026-10-19'),
    ('capabilities', ['chat']), ('profiles', []), ('max_data_class', 'public'), ('financial_class', 'paid')])
def test_incompatible_fallback_is_rejected(field, value):
    data = inventory()
    fallback = copy.deepcopy(data['models'][0])
    fallback['model'] = 'fallback'
    fallback[field] = value
    data['models'].append(fallback)
    result = route(data)
    assert result['eligible'] == [{'provider': 'test-provider', 'model': 'test-model'}]
    assert result['rejected'][0]['model'] == 'fallback'


def test_inventory_empty_or_duplicate_and_invalid_date():
    assert route({'kind': 'models', 'models': []})['outcome'] == 'blocked'
    data = inventory()
    data['models'].append(copy.deepcopy(data['models'][0]))
    with pytest.raises(ValueError): route(data)
    data['models'][0]['verified_on'] = 'not-a-date'
    with pytest.raises(ValidationError): route(data)


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def delivery_fixture(tmp_path):
    root = tmp_path / 'product'
    root.mkdir()
    remote = tmp_path / 'remote.git'
    subprocess.run(['git', 'init', '--bare', str(remote)], check=True, capture_output=True)
    git(root, 'init')
    git(root, 'config', 'user.email', 'fixture@example.invalid')
    git(root, 'config', 'user.name', 'Fixture')
    (root / 'product.txt').write_text('working product')
    git(root, 'add', 'product.txt')
    git(root, 'commit', '-m', 'test checkpoint')
    git(root, 'branch', '-M', 'main')
    git(root, 'remote', 'add', 'origin', str(remote))
    git(root, 'push', 'origin', 'main')
    evidence = artifact(root, 'test-evidence.txt', 'functional acceptance result')
    data = {'kind': 'delivery', 'task_id': 'task-test', 'commit': git(root, 'rev-parse', 'HEAD'),
            'acceptance': [{'criterion': 'Works after refresh', 'status': 'passed', 'functional': True, 'evidence': evidence}],
            'pending': [], 'remote': {'name': 'origin', 'ref': 'refs/heads/main'}, 'deployment': 'not-requested'}
    return root, data


def test_delivery_checks_real_local_git_remote(tmp_path):
    root, data = delivery_fixture(tmp_path)
    assert delivery(data, root, 'task-test', True)['outcome'] == 'admitted'
    with pytest.raises(ValueError): delivery(data, root, 'task-other', True)
    with pytest.raises(ValueError): delivery(data, root, 'task-test', False)
    (root / 'product.txt').write_text('not committed')
    with pytest.raises(ValueError): delivery(data, root, 'task-test', True)


@pytest.mark.parametrize('change', ['pending', 'failed', 'structural', 'stale', 'tamper', 'deployment', 'deployment-proof', 'remote', 'untracked-source'])
def test_incomplete_delivery_cannot_pass(tmp_path, change):
    root, data = delivery_fixture(tmp_path)
    if change == 'pending': data['pending'] = ['one remaining case']
    if change == 'failed': data['acceptance'][0]['status'] = 'failed'
    if change == 'structural': data['acceptance'][0]['functional'] = False
    if change == 'stale': data['commit'] = '0' * 40
    if change == 'tamper': (root / 'test-evidence.txt').write_text('tampered')
    if change == 'deployment': data['deployment'] = 'not-verified'
    if change == 'deployment-proof': data['deployment'] = 'verified'
    if change == 'untracked-source': (root / 'new-feature.py').write_text('print("not remotely saved")')
    if change == 'remote':
        git(root, 'commit', '--allow-empty', '-m', 'not pushed')
        data['commit'] = git(root, 'rev-parse', 'HEAD')
    with pytest.raises(ValueError): delivery(data, root, 'task-test', True)


def test_recorder_defaults_partial_and_blocks_unproven_completion(tmp_path):
    task = tmp_path / 'task.json'
    task.write_text(json.dumps({'id': 'task-test'}))
    base = [sys.executable, str(ROOT / 'scripts/record_execution_result.py'), '--task-envelope', str(task), '--runtime', 'codex', '--summary', 'test']
    result = subprocess.run(base, capture_output=True, text=True)
    assert result.returncode == 0
    output = tmp_path / 'task.execution-result.json'
    assert json.loads(output.read_text())['status'] == 'partial'
    result = subprocess.run(base + ['--status', 'completed'], capture_output=True, text=True)
    assert result.returncode != 0
    assert json.loads(output.read_text())['status'] == 'partial'


def test_recorder_accepts_proven_delivery_and_binds_criteria(tmp_path):
    root, data = delivery_fixture(tmp_path)
    evidence = root / 'delivery.json'
    evidence.write_text(json.dumps(data))
    task = root / 'task.json'
    task.write_text(json.dumps({'id': 'task-test', 'acceptance_criteria': ['Works after refresh']}))
    base = [sys.executable, str(ROOT / 'scripts/record_execution_result.py'), '--task-envelope', str(task), '--runtime', 'codex', '--summary', 'test',
            '--status', 'completed', '--project-root', str(root), '--delivery-evidence', str(evidence), '--verify-remote']
    result = subprocess.run(base, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads((root / 'task.execution-result.json').read_text())['delivery_sha256'] == hashlib.sha256(evidence.read_bytes()).hexdigest()
    task.write_text(json.dumps({'id': 'task-test', 'acceptance_criteria': ['An additional requirement']}))
    assert subprocess.run(base, capture_output=True).returncode != 0


@pytest.mark.parametrize('foreign', ['task', 'output'])
@pytest.mark.parametrize('status', ['partial', 'completed'])
def test_recorder_cannot_write_product_state_outside_product(tmp_path, foreign, status):
    root, data = delivery_fixture(tmp_path)
    evidence = root / 'delivery.json'
    evidence.write_text(json.dumps(data))
    task = (tmp_path if foreign == 'task' else root) / 'task.json'
    task.write_text(json.dumps({'id': 'task-test', 'acceptance_criteria': ['Works after refresh']}))
    output = (tmp_path if foreign == 'output' else root) / 'result.json'
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/record_execution_result.py'), '--task-envelope', str(task),
        '--runtime', 'codex', '--summary', 'test', '--status', status, '--project-root', str(root),
        '--delivery-evidence', str(evidence), '--verify-remote', '--output', str(output)], capture_output=True)
    assert result.returncode != 0
    assert not output.exists()


@pytest.mark.parametrize('target', ['tracked', 'task', 'manifest', 'receipt'])
def test_recorder_cannot_overwrite_tracked_or_input_files(tmp_path, target):
    root, data = delivery_fixture(tmp_path)
    evidence = root / 'delivery.json'
    evidence.write_text(json.dumps(data))
    task = root / 'task.json'
    task.write_text(json.dumps({'id': 'task-test', 'acceptance_criteria': ['Works after refresh']}))
    if target == 'tracked':
        output = root / 'tracked-result.json'
        output.write_text('{}')
        git(root, 'add', output.name)
        git(root, 'commit', '-m', 'tracked evidence')
        git(root, 'push', 'origin', 'main')
        data['commit'] = git(root, 'rev-parse', 'HEAD')
        evidence.write_text(json.dumps(data))
    else:
        output = {'task': task, 'manifest': evidence, 'receipt': root / 'test-evidence.txt'}[target]
    before = output.read_bytes()
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/record_execution_result.py'), '--task-envelope', str(task),
        '--runtime', 'codex', '--summary', 'test', '--status', 'completed', '--project-root', str(root),
        '--delivery-evidence', str(evidence), '--verify-remote', '--output', str(output)], capture_output=True)
    assert result.returncode != 0
    assert output.read_bytes() == before
