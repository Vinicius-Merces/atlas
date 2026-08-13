import { createHash, randomUUID } from "node:crypto";
import { z } from "zod";
import { db, isUniqueViolation, violatedColumn } from "./db";
import { getResidenceById } from "./content";

/**
 * The lead mutation, implemented against the contract in
 * planning/05-lead-mutation-contract.md.
 */

export const TIMEFRAMES = ["immediate", "3-6-months", "6-12-months", "exploring"] as const;
export const CONTEXTS = ["primary-home", "second-home", "investment", "broker"] as const;

export const timeframeLabels: Record<(typeof TIMEFRAMES)[number], string> = {
  immediate: "Ready now",
  "3-6-months": "In three to six months",
  "6-12-months": "In six to twelve months",
  exploring: "Exploring, no fixed date",
};

export const contextLabels: Record<(typeof CONTEXTS)[number], string> = {
  "primary-home": "A primary home",
  "second-home": "A second home",
  investment: "An investment",
  broker: "I am a broker acting for a buyer",
};

export const visitRequestSchema = z.object({
  name: z.string().trim().min(2, "Enter your full name.").max(80, "Name is too long."),
  email: z
    .string()
    .trim()
    .toLowerCase()
    .max(254, "Email address is too long.")
    .regex(/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/, "Enter a valid email address."),
  phone: z
    .string()
    .trim()
    .regex(/^[0-9+\-\s()]{6,24}$/, "Enter a valid telephone number, or leave it blank.")
    .optional()
    .or(z.literal("")),
  residenceId: z
    .string()
    .trim()
    .regex(/^A(0[1-9]|1[0-2])$/, "Select a residence from the list.")
    .optional()
    .or(z.literal("")),
  timeframe: z.enum(TIMEFRAMES, { message: "Choose when you are looking to buy." }),
  context: z.enum(CONTEXTS, { message: "Tell us what kind of purchase this is." }),
  preferredDates: z.string().trim().max(120, "Keep preferred dates under 120 characters.").optional().or(z.literal("")),
  message: z.string().trim().max(2000, "Keep your message under 2000 characters.").optional().or(z.literal("")),
  consent: z.literal(true, { message: "We need your consent before we can contact you." }),
  idempotencyKey: z.string().uuid("Missing or malformed submission key."),
  website: z.string().max(0).optional().or(z.literal("")),
  renderedAt: z.coerce.number().int().nonnegative().optional(),
});

export type VisitRequestInput = z.infer<typeof visitRequestSchema>;

export type StoredVisitRequest = {
  reference: string;
  name: string;
  email: string;
  phone: string | null;
  residence_id: string | null;
  timeframe: string;
  context: string;
  preferred_dates: string | null;
  message: string | null;
  status: string;
  notification_status: string;
  notification_error: string | null;
  notification_attempts: number;
  created_at: string;
};

const REFERENCE_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"; // Crockford base32

export function generateReference(): string {
  const bytes = randomUUID().replace(/-/g, "");
  let out = "";
  for (let i = 0; i < 8; i += 1) {
    out += REFERENCE_ALPHABET[parseInt(bytes.slice(i * 2, i * 2 + 2), 16) % 32];
  }
  return `AST-${out}`;
}

export function hashIp(ip: string): string {
  const salt = process.env.ASTERIA_IP_SALT ?? "asteria-local-salt";
  return createHash("sha256").update(`${salt}:${ip}`).digest("hex").slice(0, 32);
}

function dedupeKey(email: string, residenceId: string | null, now: Date): string {
  const day = now.toISOString().slice(0, 10);
  return createHash("sha256")
    .update(`${email}|${residenceId ?? "-"}|${day}`)
    .digest("hex")
    .slice(0, 40);
}

export type InsertOutcome =
  | { kind: "created"; record: StoredVisitRequest }
  | { kind: "duplicate"; record: StoredVisitRequest; reason: "idempotency" | "same-day" }
  | { kind: "store_failure"; error: string };

/**
 * Persist the lead. The write is the authoritative moment: the funnel
 * conversion event is inserted in the SAME transaction, so a conversion event
 * can never exist without its lead, and a lead can never produce two events.
 */
export function insertVisitRequest(
  input: VisitRequestInput,
  meta: { ipHash: string | null; userAgent: string | null; sessionId: string | null },
): InsertOutcome {
  if (process.env.ASTERIA_STORE_MODE === "fail") {
    return { kind: "store_failure", error: "simulated_store_failure" };
  }

  const now = new Date();
  const database = db();
  const residenceId = input.residenceId ? input.residenceId : null;
  const key = dedupeKey(input.email, residenceId, now);
  const reference = generateReference();

  try {
    database.exec("BEGIN IMMEDIATE");
    database
      .prepare(
        `INSERT INTO visit_request
          (reference, idempotency_key, dedupe_key, name, email, phone, residence_id, timeframe,
           context, preferred_dates, message, consent, consent_at, status, notification_status,
           ip_hash, user_agent, created_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, 'received', 'pending', ?, ?, ?)`,
      )
      .run(
        reference,
        input.idempotencyKey,
        key,
        input.name,
        input.email,
        input.phone || null,
        residenceId,
        input.timeframe,
        input.context,
        input.preferredDates || null,
        input.message || null,
        now.toISOString(),
        meta.ipHash,
        meta.userAgent,
        now.toISOString(),
      );
    database
      .prepare(
        `INSERT INTO funnel_event (name, session_id, subject, reference, dedupe_key, created_at)
         VALUES ('conversion.visit_request.submitted', ?, ?, ?, ?, ?)`,
      )
      .run(
        meta.sessionId ?? "server",
        residenceId,
        reference,
        `conversion.visit_request.submitted:${reference}`,
        now.toISOString(),
      );
    database.exec("COMMIT");
  } catch (error) {
    try {
      database.exec("ROLLBACK");
    } catch {
      /* transaction already closed */
    }
    if (isUniqueViolation(error)) {
      const column = violatedColumn(error);
      const existing =
        column === "idempotency_key"
          ? findByIdempotencyKey(input.idempotencyKey)
          : findByDedupeKey(key);
      if (existing) {
        return {
          kind: "duplicate",
          record: existing,
          reason: column === "idempotency_key" ? "idempotency" : "same-day",
        };
      }
    }
    return { kind: "store_failure", error: error instanceof Error ? error.message : String(error) };
  }

  return { kind: "created", record: findByReference(reference)! };
}

const SELECT_COLUMNS = `reference, name, email, phone, residence_id, timeframe, context,
  preferred_dates, message, status, notification_status, notification_error,
  notification_attempts, created_at`;

export function findByReference(reference: string): StoredVisitRequest | null {
  return (db()
    .prepare(`SELECT ${SELECT_COLUMNS} FROM visit_request WHERE reference = ?`)
    .get(reference) ?? null) as StoredVisitRequest | null;
}

function findByIdempotencyKey(key: string): StoredVisitRequest | null {
  return (db()
    .prepare(`SELECT ${SELECT_COLUMNS} FROM visit_request WHERE idempotency_key = ?`)
    .get(key) ?? null) as StoredVisitRequest | null;
}

function findByDedupeKey(key: string): StoredVisitRequest | null {
  return (db()
    .prepare(`SELECT ${SELECT_COLUMNS} FROM visit_request WHERE dedupe_key = ?`)
    .get(key) ?? null) as StoredVisitRequest | null;
}

export function countVisitRequests(): number {
  const row = db().prepare("SELECT COUNT(*) AS n FROM visit_request").get() as { n: number };
  return row.n;
}

export function countConversionEvents(): number {
  const row = db()
    .prepare(
      "SELECT COUNT(*) AS n FROM funnel_event WHERE name = 'conversion.visit_request.submitted'",
    )
    .get() as { n: number };
  return row.n;
}

/**
 * Broker hand-off. The lead is already durable at this point; a failure here
 * degrades the notification status and is retried, and is never allowed to
 * present itself to the visitor as a lost request.
 */
export async function notifyBroker(record: StoredVisitRequest): Promise<"delivered" | "failed"> {
  const mode = process.env.ASTERIA_BROKER_MODE ?? "log";
  const database = db();
  const markAttempt = (status: "delivered" | "failed", error: string | null) => {
    database
      .prepare(
        `UPDATE visit_request
           SET notification_status = ?, notification_error = ?,
               notification_attempts = notification_attempts + 1
         WHERE reference = ?`,
      )
      .run(status, error, record.reference);
  };

  if (mode === "fail") {
    markAttempt("failed", "simulated_broker_failure");
    return "failed";
  }

  const webhook = process.env.ASTERIA_BROKER_WEBHOOK;
  if (!webhook) {
    // No provider configured in this environment: the hand-off is recorded as
    // delivered to the local sales log, which is the authoritative route here.
    markAttempt("delivered", null);
    return "delivered";
  }

  try {
    const response = await fetch(webhook, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ reference: record.reference, email: record.email }),
      signal: AbortSignal.timeout(5000),
    });
    if (!response.ok) throw new Error(`broker_http_${response.status}`);
    markAttempt("delivered", null);
    return "delivered";
  } catch (error) {
    markAttempt("failed", error instanceof Error ? error.message : String(error));
    return "failed";
  }
}

export function residenceExists(id: string | null | undefined): boolean {
  if (!id) return true;
  return Boolean(getResidenceById(id));
}
