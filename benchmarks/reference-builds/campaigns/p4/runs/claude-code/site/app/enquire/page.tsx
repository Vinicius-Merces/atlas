import { randomUUID } from "node:crypto";
import Link from "next/link";
import type { Metadata } from "next";
import styles from "./enquire.module.css";
import { getResidences, getSettings } from "@/lib/content";
import { TIMEFRAMES, CONTEXTS, timeframeLabels, contextLabels } from "@/lib/visit-request";
import { EnquireForm } from "@/components/EnquireForm";
import { FunnelBeacon } from "@/components/FunnelBeacon";
import { pageMetadata } from "@/lib/seo";
import { JsonLd, breadcrumbNode, faqNode } from "@/lib/jsonld";

export const metadata: Metadata = pageMetadata({
  title: "Request a visit",
  description:
    "Request a visit to the Asteria ridge. Visits leave from the sales office in Oeiras and take about ninety minutes on foot. Answered by a person within 24 hours.",
  path: "/enquire",
});

const FAQ = [
  {
    question: "What happens after I send this form?",
    answer:
      "Your request is recorded immediately with a reference code beginning AST- and passed to the sales team. A person answers within 24 hours, Monday to Saturday.",
  },
  {
    question: "How long does a visit take?",
    answer:
      "About ninety minutes. Visits leave from the sales office at Rua da Pedreira 12, Oeiras, and cross the ridge on foot, so sturdy shoes are genuinely necessary.",
  },
  {
    question: "Is there a show home?",
    answer:
      "Not yet. Two houses are under construction and can be walked through in shell form. Everything else is seen as drawings and on the ground itself.",
  },
  {
    question: "Will I be added to a mailing list?",
    answer:
      "No. Requesting a visit consents to us answering that request only. Marketing contact would need a separate opt-in, which this form does not ask for.",
  },
];

type Search = { [key: string]: string | string[] | undefined };

export default async function EnquirePage({ searchParams }: { searchParams: Promise<Search> }) {
  const params = await searchParams;
  const residences = getResidences();
  const s = getSettings();

  const requested = Array.isArray(params.residence) ? params.residence[0] : params.residence;
  const defaultResidence = residences.find((r) => r.id === requested)?.id;

  const state = Array.isArray(params.state) ? params.state[0] : params.state;

  return (
    <>
      <FunnelBeacon event="enquire_opened" />

      <div className={`page ${styles.wrap}`}>
        <div className="section-head">
          <span className="section-index">07</span>
          <span className="section-label">The visit</span>
        </div>

        <div className={styles.layout}>
          <div className={styles.formColumn}>
            <h1 className={styles.title}>Request a visit</h1>
            <p className="lede" style={{ marginTop: "var(--space-s)", marginBottom: "var(--space-l)" }}>
              Ninety minutes on the ridge with someone who can answer questions about the ground, the
              terms and the programme. Your name, email, timing, purchase type and consent are
              required; everything else just makes the conversation useful.
            </p>

            {/* Server-rendered outcome for the no-JavaScript path, where the
                endpoint redirects back here with an explicit state. */}
            {state === "invalid" && (
              <div className={styles.serverNotice} role="alert">
                <p>
                  <strong>Some details need attention.</strong> Check the highlighted fields and send
                  again.
                </p>
              </div>
            )}
            {state === "not-recorded" && (
              <div className={styles.serverNotice} role="alert">
                <p>
                  <strong>Your request was not recorded.</strong> Nothing has been sent. Please try
                  again, or telephone{" "}
                  <a href={`tel:${s.telephone.replace(/\s/g, "")}`}>{s.telephone}</a>.
                </p>
              </div>
            )}
            {state === "rate-limited" && (
              <div className={styles.serverNotice} role="alert">
                <p>
                  <strong>Too many requests from this connection.</strong> Wait a few minutes, or
                  telephone <a href={`tel:${s.telephone.replace(/\s/g, "")}`}>{s.telephone}</a>.
                </p>
              </div>
            )}

            <EnquireForm
              residences={residences.map((r) => ({
                id: r.id,
                index: r.index,
                name: r.name,
                status: r.status,
              }))}
              defaultResidence={defaultResidence}
              timeframes={TIMEFRAMES.map((value) => ({ value, label: timeframeLabels[value] }))}
              contexts={CONTEXTS.map((value) => ({ value, label: contextLabels[value] }))}
              telephone={s.telephone}
              responseHours={s.responsePromiseHours}
              initialIdempotencyKey={randomUUID()}
              renderedAt={Date.now()}
            />
          </div>

          <aside className={styles.aside} aria-labelledby="visit-aside-title">
            <h2 id="visit-aside-title" className={styles.asideTitle}>
              Before you come
            </h2>
            <dl className={styles.faq}>
              {FAQ.map((item) => (
                <div key={item.question} className={styles.faqItem}>
                  <dt className={styles.faqQuestion}>{item.question}</dt>
                  <dd className={styles.faqAnswer}>{item.answer}</dd>
                </div>
              ))}
            </dl>

            <div className={styles.direct}>
              <p className="annotation">Or contact us directly</p>
              <p className={styles.directLine}>
                <a href={`tel:${s.telephone.replace(/\s/g, "")}`}>{s.telephone}</a>
              </p>
              <p className={styles.directLine}>
                <a href={`mailto:${s.email}`}>{s.email}</a>
              </p>
              <p className="annotation">{s.openingHours}</p>
              <p style={{ marginTop: "var(--space-s)" }}>
                <Link href="/contact">Sales office and directions →</Link>
              </p>
            </div>
          </aside>
        </div>
      </div>

      <JsonLd
        nodes={[
          breadcrumbNode([
            { name: "Home", path: "/" },
            { name: "Request a visit", path: "/enquire" },
          ]),
          faqNode(FAQ),
        ]}
      />
    </>
  );
}
