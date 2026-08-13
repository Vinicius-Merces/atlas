import { NextResponse } from "next/server";
import { timingSafeEqual } from "node:crypto";
import { findByReference, countVisitRequests, countConversionEvents } from "@/lib/visit-request";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Authoritative read-back. This is the endpoint the benchmark evidence uses to
 * prove a lead exists server-side, independently of any UI success state.
 * It is protected by a shared secret that never reaches the browser.
 */
function authorised(request: Request): boolean {
  const expected = process.env.ASTERIA_ADMIN_KEY;
  if (!expected) return false;
  const provided = request.headers.get("x-asteria-admin-key") ?? "";
  const a = Buffer.from(provided);
  const b = Buffer.from(expected);
  if (a.length !== b.length) return false;
  return timingSafeEqual(a, b);
}

export async function GET(
  request: Request,
  { params }: { params: Promise<{ reference: string }> },
) {
  if (!authorised(request)) {
    return NextResponse.json(
      { ok: false, error: "unauthorised" },
      { status: 401, headers: { "WWW-Authenticate": "ApiKey" } },
    );
  }

  const { reference } = await params;

  if (reference === "_stats") {
    return NextResponse.json({
      ok: true,
      visitRequests: countVisitRequests(),
      conversionEvents: countConversionEvents(),
    });
  }

  const record = findByReference(reference);
  if (!record) {
    return NextResponse.json({ ok: false, error: "not_found" }, { status: 404 });
  }
  return NextResponse.json({ ok: true, record });
}
