import { NextResponse } from "next/server";
import {
  visitRequestSchema,
  insertVisitRequest,
  notifyBroker,
  residenceExists,
  hashIp,
} from "@/lib/visit-request";
import { consume, clientIp } from "@/lib/rate-limit";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const MAX_BODY_BYTES = 16 * 1024;
const MIN_TIME_TO_SUBMIT_MS = 2000;

function wantsJson(request: Request): boolean {
  const accept = request.headers.get("accept") ?? "";
  const contentType = request.headers.get("content-type") ?? "";
  return accept.includes("application/json") || contentType.includes("application/json");
}

function redirect(url: string) {
  return NextResponse.redirect(url, { status: 303 });
}

export async function POST(request: Request) {
  const json = wantsJson(request);
  const origin = new URL(request.url).origin;
  const fail = (
    status: number,
    payload: Record<string, unknown>,
    redirectQuery: string,
    headers?: Record<string, string>,
  ) =>
    json
      ? NextResponse.json(payload, { status, headers })
      : redirect(`${origin}/enquire?${redirectQuery}`);

  // --- payload bounds -------------------------------------------------------
  const contentType = request.headers.get("content-type") ?? "";
  const declaredLength = Number(request.headers.get("content-length") ?? 0);
  if (declaredLength > MAX_BODY_BYTES) {
    return fail(413, { ok: false, error: "payload_too_large" }, "state=too-large");
  }
  if (
    !contentType.includes("application/json") &&
    !contentType.includes("application/x-www-form-urlencoded")
  ) {
    return fail(415, { ok: false, error: "unsupported_media_type" }, "state=unsupported");
  }

  const raw = await request.text();
  if (raw.length > MAX_BODY_BYTES) {
    return fail(413, { ok: false, error: "payload_too_large" }, "state=too-large");
  }

  let payload: Record<string, unknown>;
  if (contentType.includes("application/json")) {
    try {
      payload = JSON.parse(raw) as Record<string, unknown>;
    } catch {
      return fail(400, { ok: false, error: "malformed_json" }, "state=malformed");
    }
  } else {
    const form = new URLSearchParams(raw);
    payload = Object.fromEntries(form.entries());
    payload.consent = form.get("consent") === "on" || form.get("consent") === "true";
  }

  // --- abuse controls -------------------------------------------------------
  const ip = clientIp(request.headers);
  const decision = consume(`visit:${ip}`);
  if (!decision.allowed) {
    return fail(
      429,
      {
        ok: false,
        error: "rate_limited",
        retryAfterSeconds: decision.retryAfterSeconds,
        message: `Too many requests from this connection. Try again in about ${Math.ceil(decision.retryAfterSeconds / 60)} minute(s), or telephone the sales office.`,
      },
      `state=rate-limited&retry=${decision.retryAfterSeconds}`,
      { "Retry-After": String(decision.retryAfterSeconds) },
    );
  }

  // Honeypot: answer 200 so an automated client learns nothing, store nothing.
  if (typeof payload.website === "string" && payload.website.trim() !== "") {
    return json
      ? NextResponse.json({ ok: true, reference: "AST-000000", duplicate: false })
      : redirect(`${origin}/enquire/received?state=discarded`);
  }

  // Minimum time-to-submit.
  const renderedAt = Number(payload.renderedAt ?? 0);
  if (renderedAt > 0 && Date.now() - renderedAt < MIN_TIME_TO_SUBMIT_MS) {
    return fail(
      429,
      {
        ok: false,
        error: "too_fast",
        message: "That was submitted faster than a person can type. Please try again.",
      },
      "state=too-fast",
    );
  }

  // --- server-side validation ----------------------------------------------
  const parsed = visitRequestSchema.safeParse(payload);
  if (!parsed.success) {
    const fields: Record<string, string> = {};
    for (const issue of parsed.error.issues) {
      const key = String(issue.path[0] ?? "form");
      if (!fields[key]) fields[key] = issue.message;
    }
    return json
      ? NextResponse.json(
          {
            ok: false,
            error: "validation_failed",
            fields,
            message: "Some details need attention before we can record your request.",
          },
          { status: 422 },
        )
      : redirect(
          `${origin}/enquire?state=invalid&fields=${encodeURIComponent(Object.keys(fields).join(","))}`,
        );
  }

  if (!residenceExists(parsed.data.residenceId || null)) {
    return json
      ? NextResponse.json(
          {
            ok: false,
            error: "validation_failed",
            fields: { residenceId: "That residence does not exist." },
            message: "Select a residence from the list.",
          },
          { status: 422 },
        )
      : redirect(`${origin}/enquire?state=invalid&fields=residenceId`);
  }

  // --- authoritative write --------------------------------------------------
  const outcome = insertVisitRequest(parsed.data, {
    ipHash: ip === "unknown" ? null : hashIp(ip),
    userAgent: request.headers.get("user-agent"),
    sessionId: typeof payload.sessionId === "string" ? payload.sessionId : null,
  });

  if (outcome.kind === "store_failure") {
    return json
      ? NextResponse.json(
          {
            ok: false,
            error: "not_recorded",
            message:
              "Your request was NOT recorded. Nothing has been sent. Please try again, or telephone +351 210 000 120.",
          },
          { status: 503 },
        )
      : redirect(`${origin}/enquire?state=not-recorded`);
  }

  if (outcome.kind === "duplicate") {
    const body = {
      ok: true,
      duplicate: true,
      reason: outcome.reason,
      reference: outcome.record.reference,
      notification: outcome.record.notification_status,
      message:
        outcome.reason === "idempotency"
          ? "We already have this request. It has not been recorded twice."
          : "We already have a request from you for this residence today. It has not been recorded twice.",
    };
    return json
      ? NextResponse.json(body, { status: 200 })
      : redirect(`${origin}/enquire/received?ref=${outcome.record.reference}&duplicate=1`);
  }

  // The lead is durable at this point. The broker hand-off is attempted after,
  // and its failure degrades notification state without losing the lead.
  const notification = await notifyBroker(outcome.record);

  const body = {
    ok: true,
    duplicate: false,
    reference: outcome.record.reference,
    notification,
    message:
      notification === "delivered"
        ? "Your visit request is recorded and has reached the sales team."
        : "Your visit request is recorded. The hand-off to the sales team has not confirmed yet and is being retried; quote your reference if you telephone.",
  };

  return json
    ? NextResponse.json(body, { status: 201 })
    : redirect(
        `${origin}/enquire/received?ref=${outcome.record.reference}&notification=${notification}`,
      );
}

export async function GET() {
  return NextResponse.json(
    { ok: false, error: "method_not_allowed", message: "Use POST to submit a visit request." },
    { status: 405, headers: { Allow: "POST" } },
  );
}
