from __future__ import annotations

import importlib.util
import json
from pathlib import Path

SERVER = Path(__file__).parents[1] / "server.py"
spec = importlib.util.spec_from_file_location("asteria_server", SERVER)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_validation_rejects_invalid_fields() -> None:
    errors = mod.validate({"name": "x", "email": "bad", "phone": "1", "interest": "Other", "consent": False, "idempotency_key": "short"})
    assert {"name", "email", "phone", "interest", "consent", "idempotency_key"} <= set(errors)


def test_validation_accepts_complete_payload() -> None:
    payload = {"name": "Ada Mercer", "email": "ada@example.com", "phone": "+5511999999999", "interest": "Solis", "consent": True, "idempotency_key": "1234567890abcdef"}
    assert mod.validate(payload) == {}


def test_existing_returns_same_record(tmp_path, monkeypatch) -> None:
    leads = tmp_path / "leads.jsonl"
    leads.write_text(json.dumps({"lead_id": "lead_one", "idempotency_key": "abcdefghijklmnop"}) + "\n", encoding="utf-8")
    monkeypatch.setattr(mod, "LEADS", leads)
    assert mod.existing("abcdefghijklmnop")["lead_id"] == "lead_one"
