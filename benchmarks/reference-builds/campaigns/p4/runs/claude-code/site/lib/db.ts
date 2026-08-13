import { DatabaseSync } from "node:sqlite";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";

/**
 * Authoritative lead store.
 *
 * Uses the Node built-in SQLite binding so the authoritative state has real
 * transactions and real UNIQUE constraints without adding a native dependency
 * (see planning/04-stack-selection.md).
 */

const DB_PATH = resolve(/* turbopackIgnore: true */ process.env.ASTERIA_DB_PATH ?? "./data/asteria.db");

let handle: DatabaseSync | null = null;

export function db(): DatabaseSync {
  if (handle) return handle;
  mkdirSync(dirname(DB_PATH), { recursive: true });
  const database = new DatabaseSync(DB_PATH);
  database.exec("PRAGMA journal_mode = WAL;");
  database.exec("PRAGMA foreign_keys = ON;");
  database.exec(`
    CREATE TABLE IF NOT EXISTS visit_request (
      id                  INTEGER PRIMARY KEY AUTOINCREMENT,
      reference           TEXT    NOT NULL UNIQUE,
      idempotency_key     TEXT    NOT NULL UNIQUE,
      dedupe_key          TEXT    NOT NULL UNIQUE,
      name                TEXT    NOT NULL,
      email               TEXT    NOT NULL,
      phone               TEXT,
      residence_id        TEXT,
      timeframe           TEXT    NOT NULL,
      context             TEXT    NOT NULL,
      preferred_dates     TEXT,
      message             TEXT,
      consent             INTEGER NOT NULL,
      consent_at          TEXT    NOT NULL,
      status              TEXT    NOT NULL DEFAULT 'received',
      notification_status TEXT    NOT NULL DEFAULT 'pending',
      notification_error  TEXT,
      notification_attempts INTEGER NOT NULL DEFAULT 0,
      ip_hash             TEXT,
      user_agent          TEXT,
      created_at          TEXT    NOT NULL
    );
  `);
  database.exec(`
    CREATE TABLE IF NOT EXISTS funnel_event (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      name         TEXT NOT NULL,
      session_id   TEXT NOT NULL,
      subject      TEXT,
      reference    TEXT,
      dedupe_key   TEXT NOT NULL UNIQUE,
      created_at   TEXT NOT NULL
    );
  `);
  database.exec(
    "CREATE INDEX IF NOT EXISTS idx_visit_request_created ON visit_request (created_at);",
  );
  database.exec("CREATE INDEX IF NOT EXISTS idx_funnel_event_name ON funnel_event (name);");
  handle = database;
  return handle;
}

export function isUniqueViolation(error: unknown): boolean {
  const message = error instanceof Error ? error.message : String(error);
  return message.includes("UNIQUE constraint failed");
}

export function violatedColumn(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  const match = message.match(/UNIQUE constraint failed: visit_request\.(\w+)/);
  return match?.[1] ?? "";
}
