import { NextResponse } from "next/server";
import { db } from "@/lib/db";
import { consume, clientIp } from "@/lib/rate-limit";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * First-party funnel collection. Only non-conversion funnel steps are accepted
 * here: the conversion event is written server-side inside the lead
 * transaction, so a client cannot report a conversion that did not happen.
 */
const ALLOWED = new Set(["residence_detail_viewed", "enquire_opened"]);

export async function POST(request: Request) {
  const decision = consume(`events:${clientIp(request.headers)}`);
  if (!decision.allowed) {
    return new NextResponse(null, { status: 429 });
  }

  let payload: { name?: string; sessionId?: string; subject?: string };
  try {
    payload = (await request.json()) as typeof payload;
  } catch {
    return new NextResponse(null, { status: 400 });
  }

  const name = String(payload.name ?? "");
  if (!ALLOWED.has(name)) {
    return new NextResponse(null, { status: 422 });
  }

  const sessionId = String(payload.sessionId ?? "anonymous").slice(0, 64);
  const subject = payload.subject ? String(payload.subject).slice(0, 32) : null;

  try {
    db()
      .prepare(
        `INSERT OR IGNORE INTO funnel_event (name, session_id, subject, reference, dedupe_key, created_at)
         VALUES (?, ?, ?, NULL, ?, ?)`,
      )
      .run(name, sessionId, subject, `${name}:${sessionId}:${subject ?? "-"}`, new Date().toISOString());
  } catch {
    // Measurement failure must never surface to the visitor.
    return new NextResponse(null, { status: 204 });
  }

  return new NextResponse(null, { status: 204 });
}
