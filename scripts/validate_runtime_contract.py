from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
contract=json.loads((ROOT/'adapters/shared/runtime-contract.json').read_text())
version=(ROOT/'VERSION').read_text().strip()
assert contract['version']==version
required=set(contract['required_capabilities'])
for runtime in ['claude','codex']:
    d=json.loads((ROOT/f'adapters/{runtime}/runtime-declaration.json').read_text())
    assert d['version']==version
    assert required<=set(d['capabilities'])
    assert (ROOT/d['implementation']).exists()
for path in contract['shared_sources'].values(): assert (ROOT/path).exists(),path
print('Universal runtime contract validation passed.')
