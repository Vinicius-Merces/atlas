import Link from "next/link";
import type { Metadata } from "next";
import styles from "../enquire.module.css";
import received from "./received.module.css";
import { getSettings, getResidenceById } from "@/lib/content";
import { findByReference } from "@/lib/visit-request";
import { pageMetadata } from "@/lib/seo";

export const dynamic = "force-dynamic";

/**
 * The no-JavaScript confirmation surface. The reference shown here is read back
 * from the authoritative store, not echoed from the request — if the row is not
 * there, this page says so rather than claiming success.
 */
export const metadata: Metadata = pageMetadata({
  title: "Visit request received",
  description: "Confirmation of a visit request to Asteria Residences.",
  path: "/enquire/received",
  noindex: true,
});

type Search = { [key: string]: string | string[] | undefined };

function one(value: string | string[] | undefined): string {
  return Array.isArray(value) ? (value[0] ?? "") : (value ?? "");
}

export default async function ReceivedPage({ searchParams }: { searchParams: Promise<Search> }) {
  const params = await searchParams;
  const reference = one(params.ref);
  const duplicate = one(params.duplicate) === "1";
  const s = getSettings();

  const record = reference ? findByReference(reference) : null;
  const residence = record?.residence_id ? getResidenceById(record.residence_id) : undefined;

  return (
    <div className={`page ${styles.wrap}`}>
      <div className="section-head">
        <span className="section-index">07</span>
        <span className="section-label">Visit request</span>
      </div>

      {record ? (
        <div className={received.panel}>
          <h1 className={received.title}>
            {duplicate ? "We already have this request." : "Recorded."}
          </h1>
          <p className={received.reference}>{record.reference}</p>
          <dl className={received.detail}>
            <div>
              <dt className="annotation">Status</dt>
              <dd>Received{duplicate ? " — not recorded twice" : ""}</dd>
            </div>
            <div>
              <dt className="annotation">Sales team hand-off</dt>
              <dd>
                {record.notification_status === "delivered"
                  ? "Confirmed"
                  : record.notification_status === "failed"
                    ? "Retrying — your request is safely recorded either way"
                    : "In progress"}
              </dd>
            </div>
            {residence && (
              <div>
                <dt className="annotation">Residence of interest</dt>
                <dd>
                  <Link href={`/residences/${residence.slug}`}>{residence.name}</Link>
                </dd>
              </div>
            )}
            <div>
              <dt className="annotation">You will hear from us</dt>
              <dd>Within {s.responsePromiseHours} hours, from a person</dd>
            </div>
          </dl>
          {record.notification_status === "failed" && (
            <p className={received.degraded}>
              The hand-off to the sales team has not confirmed yet and is being retried
              automatically. If you would rather not wait, telephone{" "}
              <a href={`tel:${s.telephone.replace(/\s/g, "")}`}>{s.telephone}</a> and quote the
              reference above.
            </p>
          )}
          <p className={received.actions}>
            <Link href="/residences" className="button button--ghost">
              Back to the twelve
            </Link>
            <Link href="/" className="button button--ghost">
              Home
            </Link>
          </p>
        </div>
      ) : (
        <div className={received.panel}>
          <h1 className={received.title}>We cannot confirm that request.</h1>
          <p className="prose">
            {reference
              ? `No visit request with the reference ${reference} exists in our records. Nothing has been sent.`
              : "No reference was supplied, so there is nothing for us to look up. Nothing has been sent."}{" "}
            Please submit the form again, or telephone{" "}
            <a href={`tel:${s.telephone.replace(/\s/g, "")}`}>{s.telephone}</a>.
          </p>
          <p className={received.actions}>
            <Link href="/enquire" className="button">
              Back to the form
            </Link>
          </p>
        </div>
      )}
    </div>
  );
}
