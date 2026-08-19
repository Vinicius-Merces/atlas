from __future__ import annotations

import json
import os
import socket
import time
from dataclasses import dataclass
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DATA_CLASS_RANK = {
    "public": 0,
    "internal": 1,
    "confidential": 2,
    "restricted": 3,
}

RETRYABLE_FAILURES = {
    "rate_limited",
    "capacity_exhausted",
    "timeout",
    "provider_unavailable",
}

VALID_MODES = {"free_pool", "provider", "local_only", "paid_allowed"}


class GatewayError(RuntimeError):
    def __init__(self, failure_class: str, message: str, provider: str | None = None):
        super().__init__(message)
        self.failure_class = failure_class
        self.provider = provider


@dataclass
class Provider:
    id: str
    adapter: str
    base_url: str
    model: str
    api_key: str
    capabilities: set[str]
    max_data_class: str
    financial_class: str
    priority: int
    enabled: bool
    cooldown_seconds: int = 30
    cooldown_until: float = 0.0

    def available(self, now: float) -> bool:
        return self.enabled and bool(self.base_url) and bool(self.model) and now >= self.cooldown_until


@dataclass
class GatewayResponse:
    text: str
    provider: str
    model: str
    attempts: int
    latency_ms: int


class FreeAIGateway:
    """Small reference router for non-streaming chat requests.

    The class is intentionally framework-neutral and dependency-free. A target
    application should wrap it with project-native authentication, rate limits,
    tenant controls, structured-output validation, and telemetry.
    """

    def __init__(self, providers: list[Provider] | None = None):
        self.mode = os.getenv("AI_MODE", "free_pool").strip() or "free_pool"
        if self.mode not in VALID_MODES:
            raise GatewayError("invalid_configuration", f"Unsupported AI_MODE: {self.mode}")
        self.pinned_provider = os.getenv("AI_PROVIDER", "").strip()
        self.max_attempts = _env_int("AI_MAX_ATTEMPTS", 3, minimum=1, maximum=8)
        self.total_timeout_ms = _env_int("AI_TOTAL_TIMEOUT_MS", 20_000, minimum=500, maximum=120_000)
        self.allow_paid_fallback = _env_bool("AI_ALLOW_PAID_FALLBACK", False)
        self.providers = providers or providers_from_env()

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        required_capabilities: Iterable[str] = ("chat",),
        data_class: str = "public",
        replay_safe: bool = True,
    ) -> GatewayResponse:
        if data_class not in DATA_CLASS_RANK:
            raise GatewayError("invalid_configuration", f"Unknown data class: {data_class}")
        if not messages:
            raise GatewayError("invalid_configuration", "At least one message is required")

        started = time.monotonic()
        deadline = started + (self.total_timeout_ms / 1000)
        required = set(required_capabilities)
        candidates = self._eligible(required, data_class)
        if not candidates:
            raise GatewayError(
                "unsupported_capability",
                f"No eligible provider for capabilities={sorted(required)} data_class={data_class}",
            )

        attempts = 0
        last_error: GatewayError | None = None
        for provider in candidates:
            if attempts >= self.max_attempts or time.monotonic() >= deadline:
                break

            attempts += 1
            remaining_seconds = max(0.25, deadline - time.monotonic())
            try:
                text = _invoke(provider, messages, timeout_seconds=remaining_seconds)
                latency_ms = int((time.monotonic() - started) * 1000)
                return GatewayResponse(
                    text=text,
                    provider=provider.id,
                    model=provider.model,
                    attempts=attempts,
                    latency_ms=latency_ms,
                )
            except GatewayError as exc:
                last_error = exc
                if exc.failure_class in {"rate_limited", "capacity_exhausted", "provider_unavailable"}:
                    provider.cooldown_until = time.monotonic() + provider.cooldown_seconds

                if exc.failure_class not in RETRYABLE_FAILURES:
                    raise
                if not replay_safe:
                    raise GatewayError(
                        "provider_unavailable",
                        "Fallback blocked because this request is not replay-safe",
                        provider=provider.id,
                    ) from exc

        if last_error is not None:
            raise last_error
        raise GatewayError("timeout", "AI gateway exhausted its attempt/timeout budget")

    def _eligible(self, required: set[str], data_class: str) -> list[Provider]:
        now = time.monotonic()
        requested_rank = DATA_CLASS_RANK[data_class]
        eligible: list[Provider] = []

        for provider in self.providers:
            if not provider.available(now):
                continue
            if not required.issubset(provider.capabilities):
                continue
            if requested_rank > DATA_CLASS_RANK.get(provider.max_data_class, -1):
                continue

            if self.mode == "local_only" and provider.financial_class != "owned-compute":
                continue
            if self.mode == "free_pool" and provider.financial_class not in {"free-tier", "owned-compute"}:
                continue
            if self.mode == "provider" and provider.id != self.pinned_provider:
                continue
            if self.mode not in {"paid_allowed", "provider"} and provider.financial_class == "paid" and not self.allow_paid_fallback:
                continue

            eligible.append(provider)

        eligible.sort(key=lambda item: item.priority)
        return eligible


def providers_from_env() -> list[Provider]:
    return [
        _provider(
            "groq-demo",
            adapter="openai-compatible",
            enabled_env="GROQ_ENABLED",
            base_url_env="GROQ_BASE_URL",
            base_url_default="https://api.groq.com/openai/v1",
            api_key_env="GROQ_API_KEY",
            model_env="GROQ_MODEL",
            capabilities_env="GROQ_CAPABILITIES",
            max_data_class_env="GROQ_MAX_DATA_CLASS",
            financial_class="free-tier",
            priority=10,
        ),
        _provider(
            "ollama-cloud",
            adapter="ollama-native",
            enabled_env="OLLAMA_CLOUD_ENABLED",
            base_url_env="OLLAMA_CLOUD_BASE_URL",
            base_url_default="https://ollama.com/api",
            api_key_env="OLLAMA_API_KEY",
            model_env="OLLAMA_CLOUD_MODEL",
            capabilities_env="OLLAMA_CLOUD_CAPABILITIES",
            max_data_class_env="OLLAMA_CLOUD_MAX_DATA_CLASS",
            financial_class="free-tier",
            priority=20,
        ),
        _provider(
            "cloudflare-workers-ai",
            adapter="openai-compatible",
            enabled_env="CLOUDFLARE_AI_ENABLED",
            base_url_env="CLOUDFLARE_AI_BASE_URL",
            base_url_default="",
            api_key_env="CLOUDFLARE_API_KEY",
            model_env="CLOUDFLARE_AI_MODEL",
            capabilities_env="CLOUDFLARE_AI_CAPABILITIES",
            max_data_class_env="CLOUDFLARE_AI_MAX_DATA_CLASS",
            financial_class="free-tier",
            priority=30,
        ),
        _provider(
            "openrouter-free",
            adapter="openai-compatible",
            enabled_env="OPENROUTER_ENABLED",
            base_url_env="OPENROUTER_BASE_URL",
            base_url_default="https://openrouter.ai/api/v1",
            api_key_env="OPENROUTER_API_KEY",
            model_env="OPENROUTER_MODEL",
            capabilities_env="OPENROUTER_CAPABILITIES",
            max_data_class_env="OPENROUTER_MAX_DATA_CLASS",
            financial_class="free-tier",
            priority=40,
        ),
        _provider(
            "github-models",
            adapter="openai-compatible",
            enabled_env="GITHUB_MODELS_ENABLED",
            base_url_env="GITHUB_MODELS_BASE_URL",
            base_url_default="https://models.github.ai/inference",
            api_key_env="GITHUB_MODELS_TOKEN",
            model_env="GITHUB_MODELS_MODEL",
            capabilities_env="GITHUB_MODELS_CAPABILITIES",
            max_data_class_env="GITHUB_MODELS_MAX_DATA_CLASS",
            financial_class="free-tier",
            priority=45,
        ),
        _provider(
            "gemini-free",
            adapter="openai-compatible",
            enabled_env="GEMINI_ENABLED",
            base_url_env="GEMINI_BASE_URL",
            base_url_default="https://generativelanguage.googleapis.com/v1beta/openai",
            api_key_env="GEMINI_API_KEY",
            model_env="GEMINI_MODEL",
            capabilities_env="GEMINI_CAPABILITIES",
            max_data_class_env="GEMINI_MAX_DATA_CLASS",
            financial_class="free-tier",
            priority=47,
        ),
        _provider(
            "ollama-remote",
            adapter="ollama-native",
            enabled_env="OLLAMA_REMOTE_ENABLED",
            base_url_env="OLLAMA_REMOTE_BASE_URL",
            base_url_default="",
            api_key_env="OLLAMA_REMOTE_GATEWAY_KEY",
            model_env="OLLAMA_REMOTE_MODEL",
            capabilities_env="OLLAMA_REMOTE_CAPABILITIES",
            max_data_class_env="OLLAMA_REMOTE_MAX_DATA_CLASS",
            max_data_class_default="confidential",
            financial_class="owned-compute",
            priority=50,
        ),
        _provider(
            "ollama-local",
            adapter="ollama-native",
            enabled_env="OLLAMA_LOCAL_ENABLED",
            base_url_env="OLLAMA_LOCAL_BASE_URL",
            base_url_default="http://127.0.0.1:11434/api",
            api_key_env="OLLAMA_LOCAL_GATEWAY_KEY",
            model_env="OLLAMA_LOCAL_MODEL",
            capabilities_env="OLLAMA_LOCAL_CAPABILITIES",
            max_data_class_env="OLLAMA_LOCAL_MAX_DATA_CLASS",
            max_data_class_default="confidential",
            financial_class="owned-compute",
            priority=60,
        ),
    ]


def _provider(
    provider_id: str,
    *,
    adapter: str,
    enabled_env: str,
    base_url_env: str,
    base_url_default: str,
    api_key_env: str,
    model_env: str,
    capabilities_env: str,
    max_data_class_env: str,
    financial_class: str,
    priority: int,
    max_data_class_default: str = "public",
) -> Provider:
    return Provider(
        id=provider_id,
        adapter=adapter,
        base_url=os.getenv(base_url_env, base_url_default).rstrip("/"),
        model=os.getenv(model_env, "").strip(),
        api_key=os.getenv(api_key_env, "").strip(),
        capabilities=_csv_set(os.getenv(capabilities_env, "chat")),
        max_data_class=os.getenv(max_data_class_env, max_data_class_default).strip(),
        financial_class=financial_class,
        priority=priority,
        enabled=_env_bool(enabled_env, False),
    )


def _invoke(provider: Provider, messages: list[dict[str, str]], *, timeout_seconds: float) -> str:
    if provider.adapter == "openai-compatible":
        url = f"{provider.base_url}/chat/completions"
        payload = {"model": provider.model, "messages": messages, "stream": False}
        body = _post_json(url, payload, provider, timeout_seconds)
        try:
            return str(body["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise GatewayError(
                "invalid_structured_output",
                "OpenAI-compatible provider returned an unexpected response shape",
                provider=provider.id,
            ) from exc

    if provider.adapter == "ollama-native":
        url = f"{provider.base_url}/chat"
        payload = {"model": provider.model, "messages": messages, "stream": False}
        body = _post_json(url, payload, provider, timeout_seconds)
        try:
            return str(body["message"]["content"])
        except (KeyError, TypeError) as exc:
            raise GatewayError(
                "invalid_structured_output",
                "Ollama provider returned an unexpected response shape",
                provider=provider.id,
            ) from exc

    raise GatewayError("invalid_configuration", f"Unsupported adapter: {provider.adapter}", provider=provider.id)


def _post_json(url: str, payload: dict[str, Any], provider: Provider, timeout_seconds: float) -> dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if provider.api_key:
        headers["Authorization"] = f"Bearer {provider.api_key}"
    if provider.id == "github-models":
        headers["Accept"] = "application/vnd.github+json"
        headers["X-GitHub-Api-Version"] = os.getenv("GITHUB_MODELS_API_VERSION", "2026-03-10")

    request = Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except HTTPError as exc:
        failure_class = _classify_http(exc.code)
        raise GatewayError(failure_class, f"Provider {provider.id} returned HTTP {exc.code}", provider=provider.id) from exc
    except (TimeoutError, socket.timeout) as exc:
        raise GatewayError("timeout", f"Provider {provider.id} timed out", provider=provider.id) from exc
    except URLError as exc:
        reason = getattr(exc, "reason", None)
        failure_class = "timeout" if isinstance(reason, (TimeoutError, socket.timeout)) else "provider_unavailable"
        raise GatewayError(failure_class, f"Provider {provider.id} request failed", provider=provider.id) from exc
    except json.JSONDecodeError as exc:
        raise GatewayError("invalid_structured_output", f"Provider {provider.id} returned invalid JSON", provider=provider.id) from exc


def _classify_http(status: int) -> str:
    if status == 401:
        return "authentication_failure"
    if status == 403:
        return "permission_failure"
    if status == 408:
        return "timeout"
    if status == 413:
        return "context_limit"
    if status == 429:
        return "rate_limited"
    if status in {409, 425, 498, 503}:
        return "capacity_exhausted"
    if 500 <= status <= 599:
        return "provider_unavailable"
    return "provider_error"


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int, *, minimum: int, maximum: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise GatewayError("invalid_configuration", f"{name} must be an integer") from exc
    return max(minimum, min(maximum, value))


def _csv_set(value: str) -> set[str]:
    return {item.strip() for item in value.split(",") if item.strip()}


if __name__ == "__main__":
    gateway = FreeAIGateway()
    response = gateway.chat(
        [{"role": "user", "content": "Reply with one short sentence confirming the gateway works."}],
        required_capabilities={"chat"},
        data_class="public",
    )
    print(
        json.dumps(
            {
                "text": response.text,
                "provider": response.provider,
                "model": response.model,
                "attempts": response.attempts,
                "latency_ms": response.latency_ms,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
