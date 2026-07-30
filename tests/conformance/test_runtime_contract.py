from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
def load(path): return json.loads((ROOT/path).read_text())
def test_versions():
    version=(ROOT/'VERSION').read_text().strip()
    assert load('adapters/shared/runtime-contract.json')['version']==version
    assert load('adapters/claude/runtime-declaration.json')['version']==version
    assert load('adapters/codex/runtime-declaration.json')['version']==version
def test_capabilities():
    required=set(load('adapters/shared/runtime-contract.json')['required_capabilities'])
    for runtime in ['claude','codex']: assert required<=set(load(f'adapters/{runtime}/runtime-declaration.json')['capabilities'])
def test_runtime_roles():
    assert load('adapters/claude/runtime-declaration.json')['canonical'] is True
    assert load('adapters/codex/runtime-declaration.json')['canonical'] is False
