type DataClass = "public" | "internal" | "confidential" | "restricted";
type Adapter = "openai-compatible" | "ollama-native";
type FailureClass =
  | "invalid_configuration"
  | "authentication_failure"
  | "permission_failure"
  | "rate_limited"
  | "capacity_exhausted"
  | "timeout"
  | "provider_unavailable"
  | "unsupported_capability"
  | "invalid_structured_output"
  | "context_limit"
  | "provider_error";

type Message = { role: "system" | "user" | "assistant"; content: string };

type Provider = {
  id: string;
  adapter: Adapter;
  baseUrl: string;
  model: string;
  apiKey: string;
  capabilities: Set<string>;
  maxDataClass: DataClass;
  financialClass: "free-tier" | "owned-compute" | "paid";
  priority: number;
  enabled: boolean;
  cooldownSeconds: number;
  cooldownUntil: number;
};

export type GatewayResponse = {
  text: string;
  provider: string;
  model: string;
  attempts: number;
  latencyMs: number;
};

export class GatewayError extends Error {
  constructor(
    public readonly failureClass: FailureClass,
    message: string,
    public readonly provider?: string,
  ) {
    super(message);
  }
}

const DATA_CLASS_RANK: Record<DataClass, number> = {
  public: 0,
  internal: 1,
  confidential: 2,
  restricted: 3,
};

const RETRYABLE = new Set<FailureClass>([
  "rate_limited",
  "capacity_exhausted",
  "timeout",
  "provider_unavailable",
]);

export class FreeAIGateway {
  private readonly mode = env("AI_MODE", "free_pool");
  private readonly pinnedProvider = env("AI_PROVIDER", "");
  private readonly maxAttempts = boundedInt("AI_MAX_ATTEMPTS", 3, 1, 8);
  private readonly totalTimeoutMs = boundedInt("AI_TOTAL_TIMEOUT_MS", 20_000, 500, 120_000);
  private readonly allowPaidFallback = boolEnv("AI_ALLOW_PAID_FALLBACK", false);

  constructor(private readonly providers: Provider[] = providersFromEnv()) {}

  async chat(
    messages: Message[],
    options: {
      requiredCapabilities?: string[];
      dataClass?: DataClass;
      replaySafe?: boolean;
    } = {},
  ): Promise<GatewayResponse> {
    if (messages.length === 0) {
      throw new GatewayError("invalid_configuration", "At least one message is required");
    }

    const required = new Set(options.requiredCapabilities ?? ["chat"]);
    const dataClass = options.dataClass ?? "public";
    const replaySafe = options.replaySafe ?? true;
    const started = Date.now();
    const deadline = started + this.totalTimeoutMs;
    const candidates = this.eligible(required, dataClass);

    if (candidates.length === 0) {
      throw new GatewayError(
        "unsupported_capability",
        `No eligible provider for ${[...required].join(", ")} at data class ${dataClass}`,
      );
    }

    let attempts = 0;
    let lastError: GatewayError | undefined;

    for (const provider of candidates) {
      if (attempts >= this.maxAttempts || Date.now() >= deadline) break;
      attempts += 1;

      const timeoutMs = Math.max(250, deadline - Date.now());
      try {
        const text = await invoke(provider, messages, timeoutMs);
        return {
          text,
          provider: provider.id,
          model: provider.model,
          attempts,
          latencyMs: Date.now() - started,
        };
      } catch (error) {
        const gatewayError = asGatewayError(error, provider.id);
        lastError = gatewayError;

        if (["rate_limited", "capacity_exhausted", "provider_unavailable"].includes(gatewayError.failureClass)) {
          provider.cooldownUntil = Date.now() + provider.cooldownSeconds * 1000;
        }

        if (!RETRYABLE.has(gatewayError.failureClass)) throw gatewayError;
        if (!replaySafe) {
          throw new GatewayError(
            "provider_unavailable",
            "Fallback blocked because this request is not replay-safe",
            provider.id,
          );
        }
      }
    }

    if (lastError) throw lastError;
    throw new GatewayError("timeout", "AI gateway exhausted its attempt/timeout budget");
  }

  private eligible(required: Set<string>, dataClass: DataClass): Provider[] {
    const now = Date.now();

    return this.providers
      .filter((provider) => provider.enabled && provider.baseUrl && provider.model)
      .filter((provider) => now >= provider.cooldownUntil)
      .filter((provider) => [...required].every((capability) => provider.capabilities.has(capability)))
      .filter((provider) => DATA_CLASS_RANK[dataClass] <= DATA_CLASS_RANK[provider.maxDataClass])
      .filter((provider) => {
        if (this.mode === "local_only") return provider.financialClass === "owned-compute";
        if (this.mode === "free_pool") return ["free-tier", "owned-compute"].includes(provider.financialClass);
        if (this.mode === "provider") return provider.id === this.pinnedProvider;
        if (provider.financialClass === "paid" && !this.allowPaidFallback) return false;
        return true;
      })
      .sort((a, b) => a.priority - b.priority);
  }
}

function providersFromEnv(): Provider[] {
  return [
    provider({
      id: "groq-demo",
      adapter: "openai-compatible",
      enabledEnv: "GROQ_ENABLED",
      baseUrlEnv: "GROQ_BASE_URL",
      baseUrlDefault: "https://api.groq.com/openai/v1",
      apiKeyEnv: "GROQ_API_KEY",
      modelEnv: "GROQ_MODEL",
      capabilitiesEnv: "GROQ_CAPABILITIES",
      maxDataClassEnv: "GROQ_MAX_DATA_CLASS",
      financialClass: "free-tier",
      priority: 10,
    }),
    provider({
      id: "ollama-cloud",
      adapter: "ollama-native",
      enabledEnv: "OLLAMA_CLOUD_ENABLED",
      baseUrlEnv: "OLLAMA_CLOUD_BASE_URL",
      baseUrlDefault: "https://ollama.com/api",
      apiKeyEnv: "OLLAMA_API_KEY",
      modelEnv: "OLLAMA_CLOUD_MODEL",
      capabilitiesEnv: "OLLAMA_CLOUD_CAPABILITIES",
      maxDataClassEnv: "OLLAMA_CLOUD_MAX_DATA_CLASS",
      financialClass: "free-tier",
      priority: 20,
    }),
    provider({
      id: "cloudflare-workers-ai",
      adapter: "openai-compatible",
      enabledEnv: "CLOUDFLARE_AI_ENABLED",
      baseUrlEnv: "CLOUDFLARE_AI_BASE_URL",
      baseUrlDefault: "",
      apiKeyEnv: "CLOUDFLARE_API_KEY",
      modelEnv: "CLOUDFLARE_AI_MODEL",
      capabilitiesEnv: "CLOUDFLARE_AI_CAPABILITIES",
      maxDataClassEnv: "CLOUDFLARE_AI_MAX_DATA_CLASS",
      financialClass: "free-tier",
      priority: 30,
    }),
    provider({
      id: "openrouter-free",
      adapter: "openai-compatible",
      enabledEnv: "OPENROUTER_ENABLED",
      baseUrlEnv: "OPENROUTER_BASE_URL",
      baseUrlDefault: "https://openrouter.ai/api/v1",
      apiKeyEnv: "OPENROUTER_API_KEY",
      modelEnv: "OPENROUTER_MODEL",
      capabilitiesEnv: "OPENROUTER_CAPABILITIES",
      maxDataClassEnv: "OPENROUTER_MAX_DATA_CLASS",
      financialClass: "free-tier",
      priority: 40,
    }),
    provider({
      id: "ollama-remote",
      adapter: "ollama-native",
      enabledEnv: "OLLAMA_REMOTE_ENABLED",
      baseUrlEnv: "OLLAMA_REMOTE_BASE_URL",
      baseUrlDefault: "",
      apiKeyEnv: "OLLAMA_REMOTE_GATEWAY_KEY",
      modelEnv: "OLLAMA_REMOTE_MODEL",
      capabilitiesEnv: "OLLAMA_REMOTE_CAPABILITIES",
      maxDataClassEnv: "OLLAMA_REMOTE_MAX_DATA_CLASS",
      maxDataClassDefault: "confidential",
      financialClass: "owned-compute",
      priority: 50,
    }),
    provider({
      id: "ollama-local",
      adapter: "ollama-native",
      enabledEnv: "OLLAMA_LOCAL_ENABLED",
      baseUrlEnv: "OLLAMA_LOCAL_BASE_URL",
      baseUrlDefault: "http://127.0.0.1:11434/api",
      apiKeyEnv: "OLLAMA_LOCAL_GATEWAY_KEY",
      modelEnv: "OLLAMA_LOCAL_MODEL",
      capabilitiesEnv: "OLLAMA_LOCAL_CAPABILITIES",
      maxDataClassEnv: "OLLAMA_LOCAL_MAX_DATA_CLASS",
      maxDataClassDefault: "confidential",
      financialClass: "owned-compute",
      priority: 60,
    }),
  ];
}

function provider(input: {
  id: string;
  adapter: Adapter;
  enabledEnv: string;
  baseUrlEnv: string;
  baseUrlDefault: string;
  apiKeyEnv: string;
  modelEnv: string;
  capabilitiesEnv: string;
  maxDataClassEnv: string;
  maxDataClassDefault?: DataClass;
  financialClass: Provider["financialClass"];
  priority: number;
}): Provider {
  return {
    id: input.id,
    adapter: input.adapter,
    baseUrl: env(input.baseUrlEnv, input.baseUrlDefault).replace(/\/$/, ""),
    model: env(input.modelEnv, ""),
    apiKey: env(input.apiKeyEnv, ""),
    capabilities: csvSet(env(input.capabilitiesEnv, "chat")),
    maxDataClass: env(input.maxDataClassEnv, input.maxDataClassDefault ?? "public") as DataClass,
    financialClass: input.financialClass,
    priority: input.priority,
    enabled: boolEnv(input.enabledEnv, false),
    cooldownSeconds: 30,
    cooldownUntil: 0,
  };
}

async function invoke(provider: Provider, messages: Message[], timeoutMs: number): Promise<string> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const isOpenAI = provider.adapter === "openai-compatible";
    const url = isOpenAI
      ? `${provider.baseUrl}/chat/completions`
      : `${provider.baseUrl}/chat`;
    const body = isOpenAI
      ? { model: provider.model, messages, stream: false }
      : { model: provider.model, messages, stream: false };

    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (provider.apiKey) headers.Authorization = `Bearer ${provider.apiKey}`;

    const response = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new GatewayError(classifyStatus(response.status), `Provider returned HTTP ${response.status}`, provider.id);
    }

    const json = (await response.json()) as Record<string, unknown>;
    if (isOpenAI) {
      const choices = json.choices as Array<{ message?: { content?: unknown } }> | undefined;
      const content = choices?.[0]?.message?.content;
      if (typeof content !== "string") {
        throw new GatewayError("invalid_structured_output", "Unexpected OpenAI-compatible response", provider.id);
      }
      return content;
    }

    const message = json.message as { content?: unknown } | undefined;
    if (typeof message?.content !== "string") {
      throw new GatewayError("invalid_structured_output", "Unexpected Ollama response", provider.id);
    }
    return message.content;
  } catch (error) {
    if (error instanceof GatewayError) throw error;
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new GatewayError("timeout", "Provider request timed out", provider.id);
    }
    throw new GatewayError("provider_unavailable", "Provider request failed", provider.id);
  } finally {
    clearTimeout(timeout);
  }
}

function classifyStatus(status: number): FailureClass {
  if (status === 401) return "authentication_failure";
  if (status === 403) return "permission_failure";
  if (status === 408) return "timeout";
  if (status === 413) return "context_limit";
  if (status === 429) return "rate_limited";
  if ([409, 425, 498, 503].includes(status)) return "capacity_exhausted";
  if (status >= 500) return "provider_unavailable";
  return "provider_error";
}

function asGatewayError(error: unknown, provider: string): GatewayError {
  if (error instanceof GatewayError) return error;
  return new GatewayError("provider_unavailable", "Provider request failed", provider);
}

function env(name: string, fallback: string): string {
  return (process.env[name] ?? fallback).trim();
}

function boolEnv(name: string, fallback: boolean): boolean {
  const raw = process.env[name];
  if (raw == null) return fallback;
  return ["1", "true", "yes", "on"].includes(raw.trim().toLowerCase());
}

function boundedInt(name: string, fallback: number, min: number, max: number): number {
  const raw = process.env[name];
  if (!raw) return fallback;
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed)) throw new GatewayError("invalid_configuration", `${name} must be an integer`);
  return Math.max(min, Math.min(max, parsed));
}

function csvSet(value: string): Set<string> {
  return new Set(value.split(",").map((item) => item.trim()).filter(Boolean));
}
