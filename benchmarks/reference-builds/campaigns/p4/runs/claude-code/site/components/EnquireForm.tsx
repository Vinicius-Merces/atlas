"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import styles from "./enquire-form.module.css";

type Residence = { id: string; index: number; name: string; status: string };

type Outcome =
  | { kind: "idle" }
  | { kind: "pending" }
  | { kind: "success"; reference: string; notification: string; message: string }
  | { kind: "duplicate"; reference: string; message: string }
  | { kind: "invalid"; fields: Record<string, string>; message: string }
  | { kind: "rate_limited"; message: string }
  | { kind: "not_recorded"; message: string }
  | { kind: "ambiguous"; message: string };

const FIELD_ORDER = [
  "name",
  "email",
  "phone",
  "residenceId",
  "timeframe",
  "context",
  "preferredDates",
  "message",
  "consent",
];

export function EnquireForm({
  residences,
  defaultResidence,
  timeframes,
  contexts,
  telephone,
  responseHours,
  initialIdempotencyKey,
  renderedAt,
}: {
  residences: Residence[];
  defaultResidence?: string;
  timeframes: { value: string; label: string }[];
  contexts: { value: string; label: string }[];
  telephone: string;
  responseHours: number;
  /**
   * Generated on the server so the no-JavaScript native POST carries a valid
   * idempotency key too: the duplicate-protection guarantee does not depend on
   * the client being able to run script.
   */
  initialIdempotencyKey: string;
  renderedAt: number;
}) {
  const [outcome, setOutcome] = useState<Outcome>({ kind: "idle" });
  const [idempotencyKey, setIdempotencyKey] = useState<string>(initialIdempotencyKey);
  const formRef = useRef<HTMLFormElement>(null);
  const statusRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Announce the outcome and move focus where the visitor needs to act.
    if (outcome.kind === "idle" || outcome.kind === "pending") return;
    if (outcome.kind === "invalid") {
      const first = FIELD_ORDER.find((field) => outcome.fields[field]);
      const element = first ? formRef.current?.querySelector<HTMLElement>(`[name="${first}"]`) : null;
      (element ?? statusRef.current)?.focus();
    } else {
      statusRef.current?.focus();
    }
  }, [outcome]);

  const errors = outcome.kind === "invalid" ? outcome.fields : {};
  const pending = outcome.kind === "pending";
  const settled =
    outcome.kind === "success" || outcome.kind === "duplicate";

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    const payload: Record<string, unknown> = Object.fromEntries(data.entries());
    payload.consent = data.get("consent") === "on";
    payload.idempotencyKey = idempotencyKey;
    payload.renderedAt = renderedAt;
    try {
      payload.sessionId = window.sessionStorage.getItem("asteria.sid") ?? undefined;
    } catch {
      /* storage unavailable */
    }

    setOutcome({ kind: "pending" });

    let response: Response;
    try {
      response = await fetch("/api/visit-requests", {
        method: "POST",
        headers: { "content-type": "application/json", accept: "application/json" },
        body: JSON.stringify(payload),
      });
    } catch {
      // Network rejection is AMBIGUOUS, not failure: the request may have
      // reached the server. The same idempotency key is kept, so retrying
      // cannot create a second lead.
      setOutcome({
        kind: "ambiguous",
        message:
          "We lost the connection before the server answered, so we cannot tell whether your request was recorded. Press send again — the submission key is unchanged, so this cannot create a duplicate.",
      });
      return;
    }

    let body: Record<string, unknown> = {};
    try {
      body = (await response.json()) as Record<string, unknown>;
    } catch {
      setOutcome({
        kind: "ambiguous",
        message:
          "The server answered in a way we could not read. Press send again, or telephone the sales office.",
      });
      return;
    }

    if (response.ok && body.ok) {
      const reference = String(body.reference ?? "");
      if (body.duplicate) {
        setOutcome({ kind: "duplicate", reference, message: String(body.message ?? "") });
      } else {
        setOutcome({
          kind: "success",
          reference,
          notification: String(body.notification ?? "delivered"),
          message: String(body.message ?? ""),
        });
        // A fresh key for any subsequent, genuinely new request.
        setIdempotencyKey(crypto.randomUUID());
      }
      return;
    }

    if (response.status === 422) {
      setOutcome({
        kind: "invalid",
        fields: (body.fields ?? {}) as Record<string, string>,
        message: String(body.message ?? "Some details need attention."),
      });
      return;
    }
    if (response.status === 429) {
      setOutcome({ kind: "rate_limited", message: String(body.message ?? "Too many requests.") });
      return;
    }
    setOutcome({
      kind: "not_recorded",
      message: String(
        body.message ??
          "Your request was NOT recorded. Nothing has been sent. Please try again or telephone us.",
      ),
    });
  }

  return (
    <div className={styles.wrap}>
      {/* Status region: the single place the outcome is announced. */}
      <div
        ref={statusRef}
        tabIndex={-1}
        role={outcome.kind === "invalid" || outcome.kind === "not_recorded" ? "alert" : "status"}
        aria-live="polite"
        className={
          outcome.kind === "idle"
            ? "visually-hidden"
            : `${styles.status} ${styles[`status--${outcome.kind}`] ?? ""}`
        }
      >
        {outcome.kind === "pending" && <p>Sending your request…</p>}

        {outcome.kind === "success" && (
          <>
            <p className={styles.statusHeading}>Recorded. Your reference is below.</p>
            <p className={styles.reference}>{outcome.reference}</p>
            <p>{outcome.message}</p>
            {outcome.notification !== "delivered" && (
              <p className={styles.degraded}>
                The hand-off to the sales team has not confirmed yet and is being retried
                automatically. Your request is safely recorded either way. If you would rather not
                wait, telephone <a href={`tel:${telephone.replace(/\s/g, "")}`}>{telephone}</a> and
                quote the reference.
              </p>
            )}
            <p>
              A member of the sales team answers within {responseHours} hours.{" "}
              <Link href="/residences">Keep looking at the twelve</Link>.
            </p>
          </>
        )}

        {outcome.kind === "duplicate" && (
          <>
            <p className={styles.statusHeading}>We already have this request.</p>
            <p className={styles.reference}>{outcome.reference}</p>
            <p>{outcome.message} Nothing has been recorded twice.</p>
          </>
        )}

        {outcome.kind === "invalid" && (
          <>
            <p className={styles.statusHeading}>{outcome.message}</p>
            <ul className={styles.errorList}>
              {FIELD_ORDER.filter((field) => outcome.fields[field]).map((field) => (
                <li key={field}>
                  <a href={`#field-${field}`}>{outcome.fields[field]}</a>
                </li>
              ))}
            </ul>
          </>
        )}

        {outcome.kind === "rate_limited" && (
          <>
            <p className={styles.statusHeading}>Too many requests from this connection.</p>
            <p>{outcome.message}</p>
          </>
        )}

        {outcome.kind === "not_recorded" && (
          <>
            <p className={styles.statusHeading}>Your request was not recorded.</p>
            <p>{outcome.message}</p>
            <p>Your answers are still in the form below — nothing has been cleared.</p>
          </>
        )}

        {outcome.kind === "ambiguous" && (
          <>
            <p className={styles.statusHeading}>We are not sure whether that reached us.</p>
            <p>{outcome.message}</p>
          </>
        )}
      </div>

      {/*
        A real form POST to a real endpoint. Without JavaScript this submits
        natively and the server renders the confirmation page; with JavaScript
        the handler below upgrades it to an inline, announced exchange.
      */}
      <form
        ref={formRef}
        className={styles.form}
        method="post"
        action="/api/visit-requests"
        onSubmit={handleSubmit}
        noValidate
        hidden={settled}
      >
        <input type="hidden" name="idempotencyKey" value={idempotencyKey} readOnly />
        <input type="hidden" name="renderedAt" value={renderedAt} readOnly />

        <div className={styles.honeypot} aria-hidden="true">
          <label htmlFor="field-website">Do not fill this in</label>
          <input id="field-website" name="website" type="text" tabIndex={-1} autoComplete="off" />
        </div>

        <fieldset className={styles.fieldset} disabled={pending}>
          <legend className={styles.legend}>Who you are</legend>

          <Field
            id="name"
            label="Full name"
            error={errors.name}
            required
            input={
              <input
                id="field-name"
                name="name"
                type="text"
                autoComplete="name"
                required
                aria-invalid={errors.name ? true : undefined}
                aria-describedby={errors.name ? "error-name" : undefined}
                className={styles.input}
              />
            }
          />

          <Field
            id="email"
            label="Email"
            error={errors.email}
            required
            hint="We reply here. We do not add you to a mailing list."
            input={
              <input
                id="field-email"
                name="email"
                type="email"
                autoComplete="email"
                required
                aria-invalid={errors.email ? true : undefined}
                aria-describedby={
                  [errors.email ? "error-email" : "", "hint-email"].filter(Boolean).join(" ") ||
                  undefined
                }
                className={styles.input}
              />
            }
          />

          <Field
            id="phone"
            label="Telephone"
            error={errors.phone}
            hint="Optional. Useful if you want to arrange a visit quickly."
            input={
              <input
                id="field-phone"
                name="phone"
                type="tel"
                autoComplete="tel"
                aria-invalid={errors.phone ? true : undefined}
                aria-describedby={
                  [errors.phone ? "error-phone" : "", "hint-phone"].filter(Boolean).join(" ") ||
                  undefined
                }
                className={styles.input}
              />
            }
          />
        </fieldset>

        <fieldset className={styles.fieldset} disabled={pending}>
          <legend className={styles.legend}>What you are looking for</legend>

          <Field
            id="residenceId"
            label="Residence of interest"
            error={errors.residenceId}
            hint="Optional. Leave as “No particular house yet” if you would rather see all twelve."
            input={
              <select
                id="field-residenceId"
                name="residenceId"
                defaultValue={defaultResidence ?? ""}
                aria-invalid={errors.residenceId ? true : undefined}
                aria-describedby={
                  [errors.residenceId ? "error-residenceId" : "", "hint-residenceId"]
                    .filter(Boolean)
                    .join(" ") || undefined
                }
                className={styles.input}
              >
                <option value="">No particular house yet</option>
                {residences.map((r) => (
                  <option key={r.id} value={r.id}>
                    {String(r.index).padStart(2, "0")} — {r.name}
                    {r.status !== "available" ? ` (${r.status})` : ""}
                  </option>
                ))}
              </select>
            }
          />

          <Field
            id="timeframe"
            label="When you are looking to buy"
            error={errors.timeframe}
            required
            input={
              <select
                id="field-timeframe"
                name="timeframe"
                defaultValue=""
                required
                aria-invalid={errors.timeframe ? true : undefined}
                aria-describedby={errors.timeframe ? "error-timeframe" : undefined}
                className={styles.input}
              >
                <option value="" disabled>
                  Choose one
                </option>
                {timeframes.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            }
          />

          <Field
            id="context"
            label="What kind of purchase"
            error={errors.context}
            required
            input={
              <select
                id="field-context"
                name="context"
                defaultValue=""
                required
                aria-invalid={errors.context ? true : undefined}
                aria-describedby={errors.context ? "error-context" : undefined}
                className={styles.input}
              >
                <option value="" disabled>
                  Choose one
                </option>
                {contexts.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            }
          />

          <Field
            id="preferredDates"
            label="Preferred dates for a visit"
            error={errors.preferredDates}
            hint="Optional. Visits run Monday to Saturday, 10:00–18:00."
            input={
              <input
                id="field-preferredDates"
                name="preferredDates"
                type="text"
                placeholder="e.g. weekday mornings, or the 14th–16th"
                aria-invalid={errors.preferredDates ? true : undefined}
                aria-describedby={
                  [errors.preferredDates ? "error-preferredDates" : "", "hint-preferredDates"]
                    .filter(Boolean)
                    .join(" ") || undefined
                }
                className={styles.input}
              />
            }
          />

          <Field
            id="message"
            label="Anything you want us to prepare"
            error={errors.message}
            hint="Optional, up to 2000 characters."
            input={
              <textarea
                id="field-message"
                name="message"
                rows={4}
                maxLength={2000}
                aria-invalid={errors.message ? true : undefined}
                aria-describedby={
                  [errors.message ? "error-message" : "", "hint-message"].filter(Boolean).join(" ") ||
                  undefined
                }
                className={`${styles.input} ${styles.textarea}`}
              />
            }
          />
        </fieldset>

        <div className={styles.consentRow}>
          <input
            id="field-consent"
            name="consent"
            type="checkbox"
            required
            aria-invalid={errors.consent ? true : undefined}
            aria-describedby={errors.consent ? "error-consent" : "hint-consent"}
            className={styles.checkbox}
          />
          <div>
            <label htmlFor="field-consent" className={styles.consentLabel}>
              You may contact me about this request. <span aria-hidden="true">*</span>
            </label>
            <p id="hint-consent" className={styles.hint}>
              We keep your details for 24 months and delete them on request. We do not use
              third-party tracking. <Link href="/privacy">Privacy notice</Link>.
            </p>
            {errors.consent && (
              <p id="error-consent" className={styles.error}>
                {errors.consent}
              </p>
            )}
          </div>
        </div>

        <div className={styles.actions}>
          <button type="submit" className="button" disabled={pending} aria-busy={pending}>
            {pending ? "Sending…" : "Send visit request"}
          </button>
          <p className="annotation">
            Answered by a person within {responseHours} hours · or telephone{" "}
            <a href={`tel:${telephone.replace(/\s/g, "")}`}>{telephone}</a>
          </p>
        </div>
      </form>

      {settled && (
        <p className={styles.restart}>
          <button
            type="button"
            className="button button--ghost"
            onClick={() => setOutcome({ kind: "idle" })}
          >
            Send another request
          </button>
        </p>
      )}
    </div>
  );
}

function Field({
  id,
  label,
  input,
  error,
  hint,
  required,
}: {
  id: string;
  label: string;
  input: React.ReactNode;
  error?: string;
  hint?: string;
  required?: boolean;
}) {
  return (
    <div className={styles.field}>
      <label htmlFor={`field-${id}`} className={styles.label}>
        {label}
        {required && (
          <span className={styles.required} aria-hidden="true">
            *
          </span>
        )}
        {!required && <span className={styles.optional}>optional</span>}
      </label>
      {input}
      {hint && (
        <p id={`hint-${id}`} className={styles.hint}>
          {hint}
        </p>
      )}
      {error && (
        <p id={`error-${id}`} className={styles.error}>
          {error}
        </p>
      )}
    </div>
  );
}
