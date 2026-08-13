/**
 * Actor-aware rate limiting for the public lead endpoint
 * (capability: rate-limit-abuse-control).
 *
 * In-process token bucket. Appropriate for a single-node deployment of this
 * size; the scaling boundary is recorded in the lead mutation contract.
 */

type Bucket = { tokens: number; updatedAt: number };

const buckets = new Map<string, Bucket>();

const CAPACITY = Number(process.env.ASTERIA_RATE_CAPACITY ?? 5);
const WINDOW_MS = Number(process.env.ASTERIA_RATE_WINDOW_MS ?? 10 * 60 * 1000);

export type RateDecision =
  | { allowed: true; remaining: number }
  | { allowed: false; retryAfterSeconds: number };

export function consume(key: string, now = Date.now()): RateDecision {
  const refillRate = CAPACITY / WINDOW_MS;
  const bucket = buckets.get(key) ?? { tokens: CAPACITY, updatedAt: now };
  const refilled = Math.min(CAPACITY, bucket.tokens + (now - bucket.updatedAt) * refillRate);

  if (refilled < 1) {
    const waitMs = (1 - refilled) / refillRate;
    buckets.set(key, { tokens: refilled, updatedAt: now });
    return { allowed: false, retryAfterSeconds: Math.max(1, Math.ceil(waitMs / 1000)) };
  }

  buckets.set(key, { tokens: refilled - 1, updatedAt: now });
  return { allowed: true, remaining: Math.floor(refilled - 1) };
}

export function resetRateLimits(): void {
  buckets.clear();
}

export function clientIp(headers: Headers): string {
  const forwarded = headers.get("x-forwarded-for");
  if (forwarded) return forwarded.split(",")[0]!.trim();
  return headers.get("x-real-ip") ?? "unknown";
}
