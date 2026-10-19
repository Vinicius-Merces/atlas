"""Bounded lexical extraction and project-local disposable range cache.

Cache only ranges, never source text, model responses or mutable tool results.
Fresh source bytes are read and hashed by the caller on every build.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
import tempfile
from pathlib import Path

VERSION = "sections-symbols-v1"
STOP = set("the a an and or to of for in is with this that from as on be by do it at de da do das dos e o os a as um uma para por em com que ao no na nos nas".split())
TASK_FIELDS = ("id", "task_type", "summary", "risk", "constraints", "acceptance_criteria", "affected_paths",
               "primary_role", "supporting_roles", "workflow", "skills", "reviews", "runtime")


def task_digest(envelope: dict) -> str:
    return digest({key: envelope.get(key) for key in TASK_FIELDS})


def terms(text: str) -> set[str]:
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    return {word for word in re.findall(r"[^\W_]+", text.lower()) if len(word) > 2 and word not in STOP}


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def units(text: str, suffix: str) -> list[tuple[int, int, str]]:
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    if suffix == ".py":
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError, RecursionError):
            return []
        result = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start = min([node.lineno, *[d.lineno for d in node.decorator_list]])
                result.append((offsets[start - 1], offsets[node.end_lineno], node.name))
        return result
    if suffix in {".md", ".markdown"}:
        headings = []
        fence = None
        for number, line in enumerate(lines):
            marker = re.match(r"^\s*(`{3,}|~{3,})", line)
            if marker:
                symbol = marker[1][0]
                if fence is None:
                    fence = symbol
                elif fence == symbol:
                    fence = None
                continue
            match = re.match(r"^(#{1,6})\s+(.+)", line)
            if match and fence is None:
                headings.append((number, len(match[1]), match[2]))
        result = []
        for index, (number, level, title) in enumerate(headings):
            end = next((n for n, depth, _ in headings[index + 1:] if depth <= level), len(lines))
            result.append((offsets[number], offsets[end], title))
        return result
    return []


def select(text: str, suffix: str, query: set[str], limit: int, mode: str) -> dict:
    if len(text) <= limit:
        return {"strategy": "full", "ranges": [[0, len(text)]] if text else []}
    candidates = units(text, suffix) if mode == "relevant" else []
    ranked = sorted(
        ((10 * len(query & terms(title)) + len(query & terms(text[start:end])), start, end)
         for start, end, title in candidates), key=lambda item: (-item[0], item[2] - item[1], item[1]))
    chosen: list[list[int]] = []
    remaining = limit
    for score, start, end in ranked:
        if score == 0 or remaining <= 0:
            break
        # Do not include an overlapping class/section twice.
        if any(start < right and end > left for left, right in chosen):
            continue
        end = min(end, start + remaining)
        chosen.append([start, end])
        remaining -= end - start
    if not chosen:
        return {"strategy": "prefix", "ranges": [[0, min(len(text), limit)]]}
    return {"strategy": "python-symbols" if suffix == ".py" else "markdown-sections", "ranges": sorted(chosen)}


def safe_cache(root: Path) -> Path | None:
    cache = root / ".atlas/cache/context-extractions"
    if any(p.is_symlink() for p in [cache, cache.parent, cache.parent.parent]):
        return None
    if not cache.resolve().is_relative_to(root.resolve()):
        return None
    return cache


def valid_payload(data: dict, key: str, size: int, limit: int) -> bool:
    if not isinstance(data, dict) or set(data) != {"key", "selection", "checksum"} or data["key"] != key:
        return False
    selection = data["selection"]
    if not isinstance(selection, dict) or set(selection) != {"strategy", "ranges"}:
        return False
    if selection["strategy"] not in {"full", "prefix", "python-symbols", "markdown-sections"}:
        return False
    ranges = selection["ranges"]
    if not isinstance(ranges, list):
        return False
    previous, total = 0, 0
    for item in ranges:
        if not isinstance(item, list) or len(item) != 2:
            return False
        start, end = item
        if type(start) is not int or type(end) is not int or not previous <= start < end <= size:
            return False
        previous = end
        total += end - start
    return total <= limit and data["checksum"] == digest({"key": key, "selection": selection})


def extract(root: Path, relative: str, text: str, source_hash: str, query: set[str],
            limit: int, *, use_cache: bool, mode: str) -> tuple[str, dict, str]:
    namespace = str(root.resolve())
    marker = root / ".atlas/project-memory.json"
    if marker.is_file() and not marker.is_symlink():
        try:
            namespace += "|" + str(json.loads(marker.read_text())["project_id"])
        except (ValueError, KeyError, TypeError):
            use_cache = False
    key = digest({"project": namespace, "path": relative, "hash": source_hash,
                  "query": sorted(query), "limit": limit, "version": VERSION, "mode": mode})
    cache = safe_cache(root) if use_cache else None
    path = cache / f"{key}.json" if cache else None
    state = "miss" if path else "bypassed"
    selected = None
    if path and path.is_symlink():
        path, state = None, "bypassed"
    if path and path.is_file():
        try:
            raw = json.loads(path.read_text()) if path.stat().st_size < 1_000_000 else None
            if valid_payload(raw, key, len(text), limit):
                selected, state = raw["selection"], "hit"
        except (OSError, ValueError, TypeError):
            pass
    if selected is None:
        selected = select(text, Path(relative).suffix.lower(), query, limit, mode)
        if path:
            record = {"key": key, "selection": selected}
            record["checksum"] = digest(record)
            temporary = None
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
                    temporary = Path(stream.name)
                    stream.write(json.dumps(record, sort_keys=True))
                temporary.replace(path)
            except OSError:
                state = "bypassed"
            finally:
                if temporary and temporary.exists():
                    temporary.unlink()
    ranges = selected["ranges"]
    pieces, positions = [], []
    for start, end in ranges:
        first = text.count("\n", 0, start) + 1
        last = text.count("\n", 0, max(start, end - 1)) + 1
        positions.append({"start": start, "end": end, "start_line": first, "end_line": last})
        piece = text[start:end]
        if selected["strategy"] not in {"full", "prefix"}:
            piece = f"[Source lines {first}-{last}]\n" + piece
        pieces.append(piece)
    excerpt = "\n\n".join(pieces)
    if sum(end - start for start, end in ranges) < len(text):
        excerpt += "\n[Excerpt truncated; selected ranges only. Read the source before relying on omitted content.]"
    excerpt = excerpt.rstrip()
    metadata = {"strategy": selected["strategy"], "ranges": positions, "cache_key": key,
                "excerpt_sha256": hashlib.sha256(excerpt.encode()).hexdigest(), "extractor_version": VERSION}
    return excerpt, metadata, state
