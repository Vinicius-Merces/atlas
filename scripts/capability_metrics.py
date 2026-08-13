from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

import yaml

ROOT = Path(__file__).resolve().parents[1]

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "before", "by", "can", "for", "from", "has", "have", "if", "in", "into", "is", "it", "of", "on", "or", "that", "the", "their", "this", "to", "use", "using", "when", "where", "with", "without", "within", "while", "should", "must", "may", "will", "across", "after", "all", "any", "each", "every", "not", "only", "than", "then", "through", "under", "over", "its", "them", "they", "we", "you", "your"
}


def normalize_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def parse_markdown(path: Path) -> tuple[dict[str, object], str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    metadata: dict[str, object] = {}
    body = text
    if text.startswith("---\n"):
        try:
            raw, body = text[4:].split("\n---\n", 1)
        except ValueError as exc:
            raise ValueError(f"unterminated frontmatter: {path}") from exc
        loaded = yaml.safe_load(raw)
        if isinstance(loaded, dict):
            metadata = loaded
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[normalize_heading(match.group(1))] = body[start:end].strip()
    return metadata, body, sections


def section(sections: dict[str, str], *names: str) -> str:
    for name in names:
        value = sections.get(normalize_heading(name))
        if value is not None:
            return value
    return ""


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9][a-z0-9+./_-]*", text.lower())
    return [word for word in words if len(word) > 1 and word not in STOPWORDS]


def jaccard(left: str, right: str) -> float:
    a = set(tokenize(left))
    b = set(tokenize(right))
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def build_idf(documents: Iterable[str]) -> dict[str, float]:
    docs = [set(tokenize(item)) for item in documents]
    total = len(docs)
    counts: Counter[str] = Counter()
    for tokens in docs:
        counts.update(tokens)
    return {term: math.log((1 + total) / (1 + count)) + 1.0 for term, count in counts.items()}


def vectorize(text: str, idf: dict[str, float]) -> dict[str, float]:
    counts = Counter(tokenize(text))
    if not counts:
        return {}
    maximum = max(counts.values())
    return {term: (count / maximum) * idf.get(term, 1.0) for term, count in counts.items()}


def cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    common = set(left) & set(right)
    numerator = sum(left[key] * right[key] for key in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def markdown_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def has_any(text: str, words: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(word.lower() in lowered for word in words)
