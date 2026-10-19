"""Verify a derived context pack against its manifest and current source bytes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

if __package__:
    from .context_extraction import task_digest
else:
    from context_extraction import task_digest

ROOT = Path(__file__).resolve().parents[1]


def verify(manifest_path: Path, context_path: Path, *, task_id: str, root: Path = ROOT,
           envelope: dict | None = None) -> dict:
    data = json.loads(manifest_path.read_text(encoding='utf-8'))
    schema = json.loads((ROOT / 'schemas/context-pack-manifest.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator(schema).validate(data)
    if 'project_root_sha256' in data and data['project_root_sha256'] != hashlib.sha256(str(root.resolve()).encode()).hexdigest():
        raise ValueError('Context pack belongs to another project root; rebuild locally')
    if data['task_id'] != task_id:
        raise ValueError('Context manifest belongs to another task')
    if envelope is not None and 'task_inputs_sha256' in data and data['task_inputs_sha256'] != task_digest(envelope):
        raise ValueError('Task inputs changed; rebuild the context pack')
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
    if not set(data.get('source_excerpts', {})) <= set(data['sources']):
        raise ValueError('Excerpt map references an unincluded source')
    for relative in data['sources']:
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError(f'Context source is unavailable or outside repository: {relative}')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != hashes[relative]:
            raise ValueError(f'Stale context source: {relative}; rebuild the pack')
        metadata = data.get('source_excerpts', {}).get(relative)
        if metadata is not None:
            source = raw.decode('utf-8')
            pieces, previous, size = [], 0, 0
            for item in metadata['ranges']:
                start, end = item['start'], item['end']
                if not previous <= start < end <= len(source):
                    raise ValueError('Invalid or overlapping excerpt ranges')
                previous = end
                size += end - start
                first = source.count('\n', 0, start) + 1
                last = source.count('\n', 0, max(start, end - 1)) + 1
                if (first, last) != (item['start_line'], item['end_line']):
                    raise ValueError('Excerpt line map does not match source')
                piece = source[start:end]
                if metadata['strategy'] not in {'full', 'prefix'}:
                    piece = f'[Source lines {first}-{last}]\n' + piece
                pieces.append(piece)
            excerpt = '\n\n'.join(pieces)
            if size < len(source):
                excerpt += '\n[Excerpt truncated; selected ranges only. Read the source before relying on omitted content.]'
            excerpt = excerpt.rstrip()
            if size > data['extraction_max_chars'] or hashlib.sha256(excerpt.encode()).hexdigest() != metadata['excerpt_sha256']:
                raise ValueError('Excerpt hash or declared size does not match source')
            if f'### `{relative}`\n\n{excerpt}\n' not in text:
                raise ValueError('Verified excerpt is absent from context pack')
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--context-pack', type=Path, required=True)
    parser.add_argument('--task-id', required=True)
    parser.add_argument('--project-root', type=Path)
    parser.add_argument('--task-envelope', type=Path, help='Also verify current task inputs against the snapshot')
    args = parser.parse_args()
    try:
        verify(args.manifest, args.context_pack, task_id=args.task_id,
               root=args.project_root.resolve(strict=True) if args.project_root else ROOT,
               envelope=json.loads(args.task_envelope.read_text()) if args.task_envelope else None)
    except Exception as exc:
        raise SystemExit(f'Context validation failed: {exc}') from None
    print('Context integrity, source freshness and declared budget passed')


if __name__ == '__main__':
    main()
