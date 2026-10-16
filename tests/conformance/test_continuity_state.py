from __future__ import annotations

import json
from pathlib import Path

from scripts import build_resume_packet, validate_continuity_state, validate_all


def seed(root: Path) -> Path:
    (root / 'VERSION').write_text('0.1.1\n')
    continuity = root / '.atlas/continuity'
    continuity.mkdir(parents=True)
    for name, extra in {
        'project-brief.json': {},
        'latest-session.json': {'risks': ['Browser unavailable'], 'next_action': 'Validate deployed flow', 'pending_work': ['Review remaining IDs']},
    }.items():
        (continuity / name).write_text(json.dumps({'framework_version': '0.1.1', **extra}))
    return continuity


def test_builder_preserves_pending_work_and_risks(tmp_path, monkeypatch):
    continuity = seed(tmp_path)
    monkeypatch.setattr(build_resume_packet, 'ROOT', tmp_path)
    build_resume_packet.main([])
    packet = json.loads((continuity / 'resume-packet.json').read_text())
    assert packet['risks'] == ['Browser unavailable']
    assert 'Validate deployed flow' in packet['next_actions']
    assert 'Review remaining IDs' in packet['next_actions']
    assert validate_continuity_state.validate(tmp_path) == []


def test_gate_rejects_stale_state_and_template_handoffs(tmp_path, monkeypatch):
    continuity = seed(tmp_path)
    monkeypatch.setattr(build_resume_packet, 'ROOT', tmp_path)
    build_resume_packet.main([])
    path = continuity / 'resume-packet.json'
    packet = json.loads(path.read_text())
    packet.update(framework_version='0.1.0', handoffs=['templates/handoff.json'], risks=[], next_actions=[])
    (tmp_path / 'templates').mkdir()
    (tmp_path / 'templates/handoff.json').write_text('{}')
    path.write_text(json.dumps(packet))
    failures = validate_continuity_state.validate(tmp_path)
    assert any('framework_version' in f for f in failures)
    assert any('invalid handoffs' in f for f in failures)
    assert any('risk was lost' in f for f in failures)
    assert any('pending work was lost' in f for f in failures)


def test_active_briefs_are_checked_but_historical_evidence_is_untouched(tmp_path, monkeypatch):
    continuity = seed(tmp_path)
    monkeypatch.setattr(build_resume_packet, 'ROOT', tmp_path)
    build_resume_packet.main([])
    history = continuity / 'session-2026-07.json'
    history.write_text('{"framework_version":"0.1.0"}')
    before = history.read_bytes()
    assert validate_continuity_state.validate(tmp_path) == []
    active = continuity / 'latest-session.json'
    data = json.loads(active.read_text())
    data['framework_version'] = '0.1.0'
    active.write_text(json.dumps(data))
    assert any('latest-session.json: expected' in f for f in validate_continuity_state.validate(tmp_path))
    assert history.read_bytes() == before


def test_gate_is_part_of_full_validation():
    assert 'continuity-state' in {step.key for step in validate_all.full_steps(Path('.'))}
