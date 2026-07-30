from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
contract=json.loads((ROOT/'adapters/shared/runtime-contract.json').read_text())
required=set(contract['required_capabilities'])
for runtime in ['claude','codex']:
    d=json.loads((ROOT/f'adapters/{runtime}/runtime-declaration.json').read_text())
    assert not (required-set(d['capabilities']))
print('Claude Code and Codex conform to the universal runtime contract.')
