from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError
from scripts import discover_capabilities as discovery

from scripts.discover_capabilities import discover
from scripts.generate_capability_fabric import build


ROOT = Path(__file__).resolve().parents[2]


def test_generated_catalog_matches_committed_artifacts() -> None:
    catalog, index = build()
    assert catalog == json.loads((ROOT / "atlas-registry/capabilities.json").read_text())
    assert index == json.loads((ROOT / "atlas-registry/ard-index.json").read_text())


def test_capability_ids_are_unique_and_paths_resolve() -> None:
    catalog, _ = build()
    capabilities = catalog["capabilities"]
    identifiers = [item["id"] for item in capabilities]
    assert len(identifiers) == len(set(identifiers))
    assert all((ROOT / item["path"]).is_file() for item in capabilities)
    assert all(item["trust"] == "internal" for item in capabilities)


def test_discovery_is_bounded_and_relevant() -> None:
    results = discover("browser security review", limit=3, kinds={"skill"})
    assert 0 < len(results) <= 3
    assert all(item["kind"] == "skill" for item in results)
    assert any("security" in item["id"] or "browser" in item["id"] for item in results)


def test_exact_name_has_highest_priority() -> None:
    results = discover("ai-search-measurement", limit=3, kinds={"skill"})
    assert results[0]["id"] == "skill:ai-search-measurement"


def test_all_registered_agents_including_orchestrator_are_indexed() -> None:
    registry = json.loads((ROOT / ".claude/registry.json").read_text())
    catalog, _ = build()
    assert {item['name'] for item in catalog['capabilities'] if item['kind'] == 'agent'} == set(registry['agents']) | {registry['orchestrator']}


@pytest.mark.parametrize('trust', ['verified-external', 'unverified-external', 'blocked', 'unknown', None])
def test_discovery_denies_non_allowed_sources(tmp_path, monkeypatch, trust) -> None:
    item = {'id': 'skill:test', 'kind': 'skill', 'description': 'test', 'keywords': []}
    if trust is not None:
        item['trust'] = trust
    index = tmp_path / 'index.json'
    index.write_text(json.dumps({'capabilities': [item]}))
    monkeypatch.setattr(discovery, 'INDEX', index)
    assert discover('test', limit=3, kinds=set()) == []


@pytest.mark.parametrize('level', ['blocked', 'unverified-external', 'verified-external'])
def test_schema_rejects_external_allow(level) -> None:
    policy = json.loads(discovery.POLICY.read_text())
    policy['levels'][level] = 'allow'
    validator = Draft202012Validator(json.loads(discovery.POLICY_SCHEMA.read_text()))
    assert not validator.is_valid(policy)


def test_policy_is_enforced_and_invalid_policy_fails_closed(tmp_path, monkeypatch) -> None:
    policy = json.loads(discovery.POLICY.read_text())
    policy['levels']['internal'] = 'deny'
    path = tmp_path / 'policy.json'
    path.write_text(json.dumps(policy))
    monkeypatch.setattr(discovery, 'POLICY', path)
    assert discover('ai-search-measurement', limit=3, kinds=set()) == []
    policy['levels']['blocked'] = 'allow'
    path.write_text(json.dumps(policy))
    with pytest.raises(ValidationError):
        discover('test', limit=3, kinds=set())


@pytest.mark.parametrize('limit', [-1, 0, 11])
def test_discovery_rejects_invalid_limits(limit) -> None:
    with pytest.raises(ValueError):
        discover('test', limit=limit, kinds=set())
