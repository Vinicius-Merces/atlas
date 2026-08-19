from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
GATEWAY_PATH = ROOT / "templates" / "ai-gateway" / "python_gateway.py"


def load_gateway_module():
    spec = importlib.util.spec_from_file_location("atlas_free_ai_gateway", GATEWAY_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def provider(module, provider_id: str, *, priority: int, financial_class: str, max_data_class: str = "public"):
    return module.Provider(
        id=provider_id,
        adapter="openai-compatible",
        base_url="https://example.invalid/v1",
        model="demo-model",
        api_key="test-only",
        capabilities={"chat"},
        max_data_class=max_data_class,
        financial_class=financial_class,
        priority=priority,
        enabled=True,
    )


def test_free_pool_prefers_priority_and_falls_back(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_gateway_module()
    first = provider(module, "first", priority=10, financial_class="free-tier")
    second = provider(module, "second", priority=20, financial_class="free-tier")
    paid = provider(module, "paid", priority=1, financial_class="paid")

    monkeypatch.setenv("AI_MODE", "free_pool")
    monkeypatch.setenv("AI_MAX_ATTEMPTS", "3")
    monkeypatch.setenv("AI_ALLOW_PAID_FALLBACK", "false")

    calls: list[str] = []

    def fake_invoke(selected, messages, *, timeout_seconds):
        calls.append(selected.id)
        if selected.id == "first":
            raise module.GatewayError("rate_limited", "quota", provider=selected.id)
        return "ok"

    monkeypatch.setattr(module, "_invoke", fake_invoke)
    gateway = module.FreeAIGateway([paid, second, first])
    result = gateway.chat([{"role": "user", "content": "hello"}])

    assert calls == ["first", "second"]
    assert result.provider == "second"
    assert result.attempts == 2


def test_local_only_excludes_hosted_free_routes(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_gateway_module()
    hosted = provider(module, "hosted", priority=1, financial_class="free-tier")
    local = provider(module, "local", priority=50, financial_class="owned-compute", max_data_class="confidential")

    monkeypatch.setenv("AI_MODE", "local_only")
    monkeypatch.setattr(module, "_invoke", lambda selected, messages, *, timeout_seconds: selected.id)

    gateway = module.FreeAIGateway([hosted, local])
    result = gateway.chat([{"role": "user", "content": "hello"}], data_class="internal")

    assert result.provider == "local"
    assert result.text == "local"


def test_privacy_filter_rejects_route_below_requested_data_class(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_gateway_module()
    public_route = provider(module, "public", priority=1, financial_class="free-tier", max_data_class="public")

    monkeypatch.setenv("AI_MODE", "free_pool")
    gateway = module.FreeAIGateway([public_route])

    with pytest.raises(module.GatewayError) as exc:
        gateway.chat([{"role": "user", "content": "secret"}], data_class="confidential")

    assert exc.value.failure_class == "unsupported_capability"


def test_non_replay_safe_request_does_not_hop_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_gateway_module()
    first = provider(module, "first", priority=1, financial_class="free-tier")
    second = provider(module, "second", priority=2, financial_class="free-tier")

    monkeypatch.setenv("AI_MODE", "free_pool")
    calls: list[str] = []

    def fake_invoke(selected, messages, *, timeout_seconds):
        calls.append(selected.id)
        raise module.GatewayError("timeout", "timeout", provider=selected.id)

    monkeypatch.setattr(module, "_invoke", fake_invoke)
    gateway = module.FreeAIGateway([first, second])

    with pytest.raises(module.GatewayError) as exc:
        gateway.chat([{"role": "user", "content": "do something"}], replay_safe=False)

    assert calls == ["first"]
    assert exc.value.failure_class == "provider_unavailable"


def test_paid_allowed_mode_can_select_paid_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_gateway_module()
    paid = provider(module, "paid", priority=1, financial_class="paid")
    monkeypatch.setenv("AI_MODE", "paid_allowed")
    monkeypatch.setenv("AI_ALLOW_PAID_FALLBACK", "false")
    monkeypatch.setattr(module, "_invoke", lambda selected, messages, *, timeout_seconds: "paid-ok")

    result = module.FreeAIGateway([paid]).chat([{"role": "user", "content": "hello"}])
    assert result.provider == "paid"


def test_unknown_mode_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_gateway_module()
    monkeypatch.setenv("AI_MODE", "surprise-mode")
    with pytest.raises(module.GatewayError) as exc:
        module.FreeAIGateway([])
    assert exc.value.failure_class == "invalid_configuration"


def test_default_provider_catalog_includes_verified_optional_routes(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_gateway_module()
    monkeypatch.setenv("GITHUB_MODELS_ENABLED", "true")
    monkeypatch.setenv("GITHUB_MODELS_MODEL", "openai/gpt-4.1")
    monkeypatch.setenv("GEMINI_ENABLED", "true")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-demo")

    providers = {item.id: item for item in module.providers_from_env()}
    assert providers["github-models"].base_url == "https://models.github.ai/inference"
    assert providers["gemini-free"].base_url == "https://generativelanguage.googleapis.com/v1beta/openai"
    assert providers["github-models"].adapter == "openai-compatible"
    assert providers["gemini-free"].adapter == "openai-compatible"


def test_free_ai_pool_assets_are_packaged() -> None:
    required = [
        ROOT / "framework" / "free-ai-pool-model.md",
        ROOT / "docs" / "free-ai-demo-guide.md",
        ROOT / "templates" / "ai-gateway" / "provider-pool.example.yaml",
        ROOT / "templates" / "ai-gateway" / "env.example",
        ROOT / "templates" / "ai-gateway" / "python_gateway.py",
        ROOT / "templates" / "ai-gateway" / "typescript_gateway.ts",
    ]
    assert all(path.is_file() for path in required)
