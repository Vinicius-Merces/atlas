"use client";

import { useEffect } from "react";

/**
 * First-party funnel instrumentation (analytics-implementation-audit).
 *
 * There is no third-party analytics script on this site. Funnel steps are sent
 * once per session/subject to a first-party endpoint that deduplicates
 * server-side; the conversion event itself is NOT sent from here — it is written
 * by the server inside the lead transaction, so a client cannot fabricate a
 * conversion.
 */
export function FunnelBeacon({ event, subject }: { event: string; subject?: string }) {
  useEffect(() => {
    let sessionId = "";
    try {
      sessionId = window.sessionStorage.getItem("asteria.sid") ?? "";
      if (!sessionId) {
        sessionId = crypto.randomUUID();
        window.sessionStorage.setItem("asteria.sid", sessionId);
      }
    } catch {
      // Storage unavailable (private mode / blocked): send without a session id
      // rather than throwing. Measurement degrades; the page does not.
      sessionId = "no-storage";
    }

    const body = JSON.stringify({ name: event, sessionId, subject });
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon("/api/events", new Blob([body], { type: "application/json" }));
      } else {
        void fetch("/api/events", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body,
          keepalive: true,
        });
      }
    } catch {
      // Instrumentation must never break the page.
    }
  }, [event, subject]);

  return null;
}
