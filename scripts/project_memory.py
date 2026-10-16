"""Initialize, resume and close memory in an explicitly selected project only."""
from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import uuid

from jsonschema import Draft202012Validator

if __package__:
    from . import build_project_brief, build_resume_packet, validate_continuity_state
    from .project_memory_utils import CONFIG, identity
else:
    import build_project_brief, build_resume_packet, validate_continuity_state
    from project_memory_utils import CONFIG, identity

FRAMEWORK = Path(__file__).resolve().parents[1]
CONTINUITY = Path('.atlas/continuity')
VIEW = Path('obsidian/atlas-project/Project Memory.md')


def local(root: Path, relative: str | Path) -> Path:
    path = root / relative
    if not path.resolve().is_relative_to(root):
        raise ValueError(f'Project path escapes its repository: {relative}')
    return path


def origin(root: Path) -> str | None:
    result = subprocess.run(['git', '-C', str(root), 'config', '--get', 'remote.origin.url'], capture_output=True, text=True)
    if result.returncode:
        return None
    value = result.stdout.strip().rstrip('/').removesuffix('.git')
    # Credentials must not become identity metadata or console output.
    from urllib.parse import urlsplit
    if '://' in value:
        parsed = urlsplit(value)
        value = (parsed.hostname or '') + parsed.path
    elif '@' in value and ':' in value:
        value = value.split('@', 1)[1].replace(':', '/', 1)
    return value.lower()


def select_root(raw: Path) -> Path:
    root = raw.resolve(strict=True)
    result = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
    if result.returncode or Path(result.stdout.strip()).resolve() != root:
        raise ValueError('--project-root must be the exact root of a Git project')
    if origin(root) == 'github.com/vinicius-merces/atlas':
        raise ValueError('Product memory cannot target the upstream ATLAS repository')
    for name in [CONFIG, CONTINUITY, '.claude/memory', VIEW]:
        local(root, name)
    memory = local(root, '.claude/memory')
    for path in memory.rglob('*.md') if memory.exists() else []:
        local(root, path.relative_to(root))
    return root


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as stream:
        stream.write(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
        temporary = Path(stream.name)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def bound_identity(root: Path) -> dict:
    config = identity(root)
    if not config or not isinstance(config.get('project_id'), str):
        raise ValueError('Project memory is not initialized; run init first')
    if config.get('origin_fingerprint'):
        fingerprint = hashlib.sha256((origin(root) or '').encode()).hexdigest()
        if fingerprint != config['origin_fingerprint']:
            raise ValueError('Project origin changed; reconcile identity before continuing')
    return config


def check_view(root: Path, config: dict) -> None:
    path = local(root, VIEW)
    if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != config.get('view_sha256'):
        raise ValueError('Obsidian view was edited or is unmanaged; preserve edits in canonical memory before rebuilding')


def memory_hashes(root: Path) -> dict[str, str]:
    memory = local(root, '.claude/memory')
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(
            local(root, path.relative_to(root)).read_bytes()
        ).hexdigest()
        for path in sorted(memory.rglob('*.md'))
        if 'templates' not in path.relative_to(memory).parts
    }


def validate(root: Path, config: dict) -> dict:
    for name, schema in [('project-brief.json', 'project-brief'), ('latest-session.json', 'session-brief'), ('resume-packet.json', 'resume-packet')]:
        data = json.loads(local(root, CONTINUITY / name).read_text(encoding='utf-8'))
        definition = json.loads((FRAMEWORK / 'schemas' / (schema + '.schema.json')).read_text())
        Draft202012Validator(definition).validate(data)
        if data.get('project_id') != config['project_id']:
            raise ValueError(f'{name} belongs to another project')
    failures = validate_continuity_state.validate(root)
    if failures:
        raise ValueError('; '.join(failures))
    return json.loads(local(root, CONTINUITY / 'latest-session.json').read_text())


def rebuild(root: Path, config: dict) -> None:
    # Reuse canonical builders with explicit project roots. No subprocess writes to FRAMEWORK.
    with redirect_stdout(io.StringIO()):
        old_project, old_resume = build_project_brief.ROOT, build_resume_packet.ROOT
        try:
            build_project_brief.ROOT = build_resume_packet.ROOT = root
            build_project_brief.main([])
            build_resume_packet.main([])
        finally:
            build_project_brief.ROOT, build_resume_packet.ROOT = old_project, old_resume
    session = validate(root, config)
    lines = [f'# {config["project_name"]}: project memory', '',
             'Generated read-only view. Edit canonical files in .claude/memory/, then close the session again.',
             f'Project identity: {config["project_id"]}', '', '## Current session', '', session['summary'],
             '', '## Next action', '', session['next_action'], '', '## Pending work', '',
             *[f'- {item}' for item in session['pending_work']], '', '## Risks', '',
             *[f'- {item}' for item in session['risks']], '', '## Canonical memory', '']
    for path in sorted(local(root, '.claude/memory').rglob('*.md')):
        if 'templates' in path.relative_to(root / '.claude/memory').parts:
            continue
        local(root, path.relative_to(root))
        lines.extend([f'### Source: {path.relative_to(root).as_posix()}', '', path.read_text(encoding='utf-8'), ''])
    view = local(root, VIEW)
    view.parent.mkdir(parents=True, exist_ok=True)
    view.write_bytes(('\n'.join(lines) + '\n').encode('utf-8'))
    config['view_sha256'] = hashlib.sha256(view.read_bytes()).hexdigest()
    config['memory_source_hashes'] = memory_hashes(root)
    write_json(local(root, CONFIG), config)


def initialize(root: Path, project_name: str | None) -> dict:
    if local(root, CONFIG).exists():
        config = bound_identity(root)
        validate(root, config)
        return config
    if local(root, CONTINUITY).exists() and any(local(root, CONTINUITY).iterdir()):
        raise ValueError('Existing unbound continuity requires manual reconciliation; no files changed')
    if local(root, VIEW).exists():
        raise ValueError('Existing Obsidian view is unmanaged; no files changed')
    memory = local(root, '.claude/memory')
    for path in memory.rglob('*.md') if memory.exists() else []:
        relative = path.relative_to(root)
        local(root, relative)
        if 'templates' in path.relative_to(memory).parts:
            continue
        source = FRAMEWORK / relative
        framework_heading = path.read_text(encoding='utf-8').startswith((
            '# ATLAS Architecture Memory', '# ATLAS Business Memory',
            '# ATLAS Operations Memory', '# ATLAS Contradiction Register',
        ))
        copied_source = root != FRAMEWORK and source.is_file() and source.read_bytes() == path.read_bytes()
        if framework_heading or copied_source:
            raise ValueError(f'Upstream framework memory found at {relative}; reconcile it before initialization')
    registry = FRAMEWORK / '.claude/registry.json'
    version = json.loads(registry.read_text())['version'] if registry.exists() else (FRAMEWORK / 'VERSION').read_text().strip()
    config = {'project_id': 'project-' + uuid.uuid4().hex, 'project_name': project_name or root.name,
              'framework_version': version,
              'origin_fingerprint': hashlib.sha256(origin(root).encode()).hexdigest() if origin(root) else None}
    # Preserve all existing canonical project memory. Do not import upstream memory.
    memory.mkdir(parents=True, exist_ok=True)
    index = memory / 'index.md'
    if not index.exists():
        index.write_text('# Project memory\n\n- [Project identity](project.md)\n\nStore validated project facts here. This memory belongs only to this repository.\n')
    write_json(local(root, CONFIG), config)
    project_note = local(root, '.claude/memory/project.md')
    if not project_note.exists():
        project_note.write_text(
            '# Project-local identity\n\n'
            '- **Purpose:** Keep validated knowledge scoped to this project.\n'
            '- **Scope:** This Git repository only.\n'
            '- **Owner:** Project maintainer\n'
            '- **Source of truth:** `.atlas/project-memory.json`\n'
            f'- **Last reviewed:** {datetime.now(timezone.utc).date().isoformat()}\n'
            '- **Related contracts or ADRs:** Project-local memory protocol\n\n'
            f'Project identity: {config["project_id"]}\n\n'
            'Implementation details must be verified before adding them here.\n',
            encoding='utf-8',
        )
    session = {'session_id': 'session-' + uuid.uuid4().hex[:12], 'project_id': config['project_id'],
               'framework_version': config['framework_version'], 'runtime': 'unknown',
               'created_at': datetime.now(timezone.utc).isoformat(),
               'summary': 'Project-local memory initialized; product implementation has not been assessed.',
               'completed_work': ['Initialized isolated project memory'], 'changed_files': [], 'validation': [],
               'decisions': ['Keep project knowledge in this repository'], 'pending_work': ['Review project architecture and active work'],
               'risks': ['Initial memory contains no validated product architecture'],
               'next_action': 'Inspect project evidence and record validated facts in .claude/memory/.'}
    write_json(local(root, CONTINUITY / 'latest-session.json'), session)
    rebuild(root, config)
    return config


def close(root: Path, config: dict, session_file: Path) -> None:
    path = session_file.resolve()
    if not path.is_relative_to(local(root, CONTINUITY).resolve()):
        raise ValueError('Session input must be staged inside this project continuity directory')
    if path == local(root, CONTINUITY / 'latest-session.json').resolve():
        raise ValueError('Use a separate staged session file to preserve the previous session')
    data = json.loads(path.read_text(encoding='utf-8'))
    schema = json.loads((FRAMEWORK / 'schemas/session-brief.schema.json').read_text())
    Draft202012Validator(schema).validate(data)
    if data.get('project_id') != config['project_id'] or data['framework_version'] != config['framework_version']:
        raise ValueError('Session identity/version does not match this project')
    check_view(root, config)
    previous = validate(root, config)
    archive = local(root, CONTINUITY / 'sessions' / (previous['session_id'] + '-' + uuid.uuid4().hex[:12] + '.json'))
    if previous != data:
        write_json(archive, previous)
    write_json(local(root, CONTINUITY / 'latest-session.json'), data)
    rebuild(root, config)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init', 'start', 'close'])
    parser.add_argument('--project-root', required=True, type=Path)
    parser.add_argument('--project-name')
    parser.add_argument('--session-file', type=Path)
    args = parser.parse_args()
    try:
        root = select_root(args.project_root)
        config = initialize(root, args.project_name) if args.action == 'init' else bound_identity(root)
        if args.action == 'close':
            if not args.session_file:
                raise ValueError('close requires --session-file')
            close(root, config, args.session_file)
        session = validate(root, config)
        sources = memory_hashes(root)
        view = local(root, VIEW)
        view_status = 'current'
        if not view.exists():
            view_status = 'missing'
        elif hashlib.sha256(view.read_bytes()).hexdigest() != config.get('view_sha256'):
            view_status = 'edited'
        elif sources != config.get('memory_source_hashes'):
            view_status = 'stale'
        print(json.dumps({'project_id': config['project_id'], 'project_name': config['project_name'],
                          'summary': session['summary'], 'pending_work': session['pending_work'],
                          'risks': session['risks'], 'next_action': session['next_action'],
                          'memory_sources': sorted(sources),
                          'obsidian_view': VIEW.as_posix(), 'obsidian_status': view_status}, ensure_ascii=False, indent=2))
    except Exception as exc:
        raise SystemExit(f'Project memory failed: {exc}') from None


if __name__ == '__main__':
    main()
