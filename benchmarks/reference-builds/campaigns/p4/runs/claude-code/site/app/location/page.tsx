import Link from "next/link";
import type { Metadata } from "next";
import styles from "./location.module.css";
import { getDistricts, getResidences, getSettings } from "@/lib/content";
import { SitePlan } from "@/components/drawings/SitePlan";
import { pageMetadata } from "@/lib/seo";
import { JsonLd, breadcrumbNode, districtNode, developmentNode } from "@/lib/jsonld";

export const metadata: Metadata = pageMetadata({
  title: "Location — the ridge, the village, the coast, the city",
  description:
    "Where Asteria is: a limestone ridge at Alto da Pedra, eleven minutes on foot from Pedra Alta village, sixteen from the coast at Oeiras and twenty-eight from central Lisbon.",
  path: "/location",
});

export default function LocationPage() {
  const districts = getDistricts();
  const residences = getResidences();
  const s = getSettings();

  return (
    <>
      <section className={`page ${styles.intro}`}>
        <div className="section-head">
          <span className="section-index">05</span>
          <span className="section-label">Location record</span>
        </div>
        <h1 className={styles.title}>Four distances that decide the place</h1>
        <p className="lede" style={{ marginTop: "var(--space-m)" }}>
          The ridge itself, the village you can walk to, the town that carries the services, and the
          city that makes it commutable. Times are measured door to door, not estimated.
        </p>
      </section>

      <div className={`page ${styles.layout}`}>
        {/* In-page navigation across the location content */}
        <nav className={styles.contents} aria-labelledby="contents-title">
          <h2 id="contents-title" className={styles.contentsTitle}>
            On this page
          </h2>
          <ol className={styles.contentsList}>
            {districts.map((d, i) => (
              <li key={d.id}>
                <a href={`#${d.slug}`}>
                  <span className="num">{String(i + 1).padStart(2, "0")}</span> {d.name}
                </a>
              </li>
            ))}
            <li>
              <a href="#site-plan">
                <span className="num">05</span> The site plan
              </a>
            </li>
            <li>
              <a href="#getting-here">
                <span className="num">06</span> Getting here
              </a>
            </li>
          </ol>
        </nav>

        <div className={styles.content}>
          {districts.map((d, i) => (
            <section key={d.id} id={d.slug} className={styles.district} aria-labelledby={`${d.slug}-title`}>
              <div className={styles.districtHead}>
                <span className="section-index">{String(i + 1).padStart(2, "0")}</span>
                <span className="section-label">{d.kind}</span>
              </div>
              <h2 id={`${d.slug}-title`} className={styles.districtTitle}>
                {d.name}
              </h2>
              <p className="annotation" style={{ marginTop: "var(--space-2xs)" }}>
                {d.distanceKm === 0 ? "On site" : `${d.distanceKm} km`} · {d.travelMinutes} minutes{" "}
                {d.mode}
              </p>
              <div className="prose" style={{ marginTop: "var(--space-s)" }}>
                {d.narrative.map((paragraph, index) => (
                  <p key={index} style={index > 0 ? { marginTop: "1.1em" } : undefined}>
                    {paragraph}
                  </p>
                ))}
              </div>
              <ul className={styles.highlights}>
                {d.highlights.map((h) => (
                  <li key={h}>{h}</li>
                ))}
              </ul>
            </section>
          ))}

          <section id="site-plan" className={styles.district} aria-labelledby="site-plan-title">
            <div className={styles.districtHead}>
              <span className="section-index">05</span>
              <span className="section-label">Drawing</span>
            </div>
            <h2 id="site-plan-title" className={styles.districtTitle}>
              The site plan
            </h2>
            <p className="prose" style={{ marginTop: "var(--space-s)", marginBottom: "var(--space-m)" }}>
              Twelve plots run west to east along the escarpment. The dashed green line is the
              plateau path, which is public and stays public. Select any plot to open its residence.
            </p>
            <SitePlan residences={residences} />
          </section>

          <section id="getting-here" className={styles.district} aria-labelledby="getting-here-title">
            <div className={styles.districtHead}>
              <span className="section-index">06</span>
              <span className="section-label">Practical</span>
            </div>
            <h2 id="getting-here-title" className={styles.districtTitle}>
              Getting here
            </h2>
            <table className="data-table" style={{ marginTop: "var(--space-s)" }}>
              <caption>Journey times to the sales office at {s.salesOffice.locality}</caption>
              <thead>
                <tr>
                  <th scope="col">From</th>
                  <th scope="col">Mode</th>
                  <th scope="col" className="numeric">
                    Distance
                  </th>
                  <th scope="col" className="numeric">
                    Time
                  </th>
                </tr>
              </thead>
              <tbody>
                {districts.map((d) => (
                  <tr key={d.id}>
                    <th scope="row" style={{ fontWeight: 400 }}>
                      {d.name}
                    </th>
                    <td>{d.mode}</td>
                    <td className="numeric">{d.distanceKm === 0 ? "—" : `${d.distanceKm} km`}</td>
                    <td className="numeric">{d.travelMinutes} min</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="prose" style={{ marginTop: "var(--space-m)" }}>
              Visits leave from {s.salesOffice.street}, {s.salesOffice.locality}, and take roughly
              ninety minutes on foot across the ridge.{" "}
              <Link href="/enquire">Request a visit</Link> or telephone{" "}
              <a href={`tel:${s.telephone.replace(/\s/g, "")}`}>{s.telephone}</a>.
            </p>
          </section>
        </div>
      </div>

      <JsonLd
        nodes={[
          breadcrumbNode([
            { name: "Home", path: "/" },
            { name: "Location", path: "/location" },
          ]),
          developmentNode(),
          ...districts.map(districtNode),
        ]}
      />
    </>
  );
}
