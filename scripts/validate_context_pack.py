"""Verify a derived context pack against its manifest and current source bytes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def verify(manifest_path: Path, context_path: Path, *, task_id: str, root: Path = ROOT) -> dict:
    data = json.loads(manifest_path.read_text(encoding='utf-8'))
    schema = json.loads((ROOT / 'schemas/context-pack-manifest.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator(schema).validate(data)
    if data['task_id'] != task_id:
        raise ValueError('Context manifest belongs to another task')
    declared = Path(data['context_pack'])
    if not declared.is_absolute():
        declared = root / declared
    if declared.resolve() != context_path.resolve():
        raise ValueError('Context manifest points to another pack')
    content = context_path.read_bytes()
    if data.get('context_sha256') != hashlib.sha256(content).hexdigest():
        raise ValueError('Context pack integrity is missing or changed; rebuild the pack')
    text = content.decode('utf-8')
    if len(text) != data.get('rendered_chars') or len(text) > data.get('max_total_chars', -1):
        raise ValueError('Context pack exceeds its declared budget or character count')
    prefix_chars = data.get('stable_prefix_chars')
    if not isinstance(prefix_chars, int) or not 0 <= prefix_chars <= len(text):
        raise ValueError('Invalid stable prefix size')
    if hashlib.sha256(text[:prefix_chars].encode('utf-8')).hexdigest() != data.get('stable_prefix_sha256'):
        raise ValueError('Stable prefix integrity changed')
    hashes = data.get('source_hashes', {})
    if set(hashes) != set(data['sources']):
        raise ValueError('Context manifest does not hash every included source')
    for relative in data['sources']:
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError(f'Context source is unavailable or outside repository: {relative}')
        if hashlib.sha256(path.read_bytes()).hexdigest() != hashes[relative]:
            raise ValueError(f'Stale context source: {relative}; rebuild the pack')
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--context-pack', type=Path, required=True)
    parser.add_argument('--task-id', required=True)
    args = parser.parse_args()
    try:
        verify(args.manifest, args.context_pack, task_id=args.task_id)
    except Exception as exc:
        raise SystemExit(f'Context validation failed: {exc}') from None
    print('Context integrity, source freshness and declared budget passed')


if __name__ == '__main__':
    main()
