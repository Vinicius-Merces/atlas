import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import styles from "../residences.module.css";
import {
  getResidence,
  getResidences,
  residenceTypeLabel,
  statusLabel,
  planTotalSqm,
} from "@/lib/content";
import { formatEur, formatPriceBand, formatQuarter, formatSqm, orientationName } from "@/lib/format";
import { RidgeSection } from "@/components/drawings/RidgeSection";
import { SitePlan } from "@/components/drawings/SitePlan";
import { Elevation } from "@/components/drawings/Elevation";
import { FloorPlan } from "@/components/drawings/FloorPlan";
import { OrientationRose } from "@/components/drawings/OrientationRose";
import { MaterialSwatches } from "@/components/drawings/MaterialSwatches";
import { pageMetadata } from "@/lib/seo";
import { JsonLd, breadcrumbNode, residenceNode } from "@/lib/jsonld";
import { FunnelBeacon } from "@/components/FunnelBeacon";

export function generateStaticParams() {
  return getResidences().map((r) => ({ slug: r.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const residence = getResidence(slug);
  if (!residence) return pageMetadata({ title: "Not found", description: "", path: `/residences/${slug}`, noindex: true });
  return pageMetadata({
    title: `${residence.name} — ${formatSqm(residence.interiorAreaSqm)}, ${residence.bedrooms} bedrooms`,
    description: `${residence.summary} ${formatSqm(residence.interiorAreaSqm)} interior, ${formatSqm(residence.outdoorAreaSqm)} outdoor, ${residence.bedrooms} bedrooms, delivery ${formatQuarter(residence.deliveryQuarter)}. ${statusLabel(residence.status)}.`,
    path: `/residences/${residence.slug}`,
  });
}

export default async function ResidencePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const residence = getResidence(slug);
  if (!residence) notFound();

  const all = getResidences();
  const previous = all.find((r) => r.index === residence.index - 1);
  const next = all.find((r) => r.index === residence.index + 1);
  const scheduleTotal = planTotalSqm(residence);

  return (
    <>
      <FunnelBeacon event="residence_detail_viewed" subject={residence.id} />

      <div className={`page ${styles.detailHead}`}>
        <nav aria-label="Breadcrumb">
          <ol className={`annotation ${styles.crumbs}`}>
            <li>
              <Link href="/">Asteria</Link> /
            </li>
            <li>
              <Link href="/residences">Residences</Link> /
            </li>
            <li aria-current="page">{residence.name}</li>
          </ol>
        </nav>

        <div className={styles.detailGrid}>
          <div className={styles.detailMain}>
            <h1 className={styles.detailTitle}>
              <span className={styles.detailIndex}>{String(residence.index).padStart(2, "0")}</span>
              {residence.name}
            </h1>
            <p className="annotation" style={{ marginTop: "var(--space-2xs)" }}>
              {residenceTypeLabel(residence.type)} · {residence.levels} level
              {residence.levels > 1 ? "s" : ""} · faces {orientationName[residence.orientation]} ·
              +{residence.elevationM} m
            </p>
            <p className={styles.detailSummary}>{residence.summary}</p>

            {residence.status !== "available" && (
              <div className={styles.availabilityNotice}>
                <strong>{statusLabel(residence.status)}.</strong> This house is no longer available.
                Its page stays published so the record of the development remains complete.{" "}
                <Link href="/residences?status=available">
                  See the houses that are still available
                </Link>
                .
              </div>
            )}

            <div className={styles.drawingStack}>
              <Elevation residence={residence} />

              <div className="prose">
                {residence.narrative.map((paragraph, index) => (
                  <p key={index} style={index > 0 ? { marginTop: "1.1em" } : undefined}>
                    {paragraph}
                  </p>
                ))}
              </div>
            </div>
          </div>

          <aside className={styles.detailAside} aria-label="Specification">
            <div className={styles.specPanel}>
              <p className="annotation" style={{ marginBottom: "var(--space-2xs)" }}>
                Specification
              </p>
              <ul className={styles.specList}>
                <li className={styles.specItem}>
                  <span>Status</span>
                  <span className={`status status--${residence.status}`}>
                    {statusLabel(residence.status)}
                  </span>
                </li>
                <li className={styles.specItem}>
                  <span>Price band</span>
                  <span className={styles.specValue}>{formatPriceBand(residence.priceBandEur)}</span>
                </li>
                <li className={styles.specItem}>
                  <span>Interior area</span>
                  <span className={styles.specValue}>{formatSqm(residence.interiorAreaSqm)}</span>
                </li>
                <li className={styles.specItem}>
                  <span>Outdoor area</span>
                  <span className={styles.specValue}>{formatSqm(residence.outdoorAreaSqm)}</span>
                </li>
                <li className={styles.specItem}>
                  <span>Plot area</span>
                  <span className={styles.specValue}>{formatSqm(residence.plotAreaSqm)}</span>
                </li>
                <li className={styles.specItem}>
                  <span>Bedrooms</span>
                  <span className={styles.specValue}>{residence.bedrooms}</span>
                </li>
                <li className={styles.specItem}>
                  <span>Bathrooms</span>
                  <span className={styles.specValue}>{residence.bathrooms}</span>
                </li>
                <li className={styles.specItem}>
                  <span>Parking</span>
                  <span className={styles.specValue}>{residence.parking}</span>
                </li>
                <li className={styles.specItem}>
                  <span>Energy rating</span>
                  <span className={styles.specValue}>{residence.energyRating}</span>
                </li>
                <li className={styles.specItem}>
                  <span>Delivery</span>
                  <span className={styles.specValue}>
                    {formatQuarter(residence.deliveryQuarter)}
                  </span>
                </li>
                <li className={styles.specItem}>
                  <span>Indicative €/m²</span>
                  <span className={styles.specValue}>
                    {formatEur(Math.round(residence.priceBandEur.from / residence.interiorAreaSqm))}
                  </span>
                </li>
              </ul>

              <div className={styles.roseRow}>
                <OrientationRose orientation={residence.orientation} />
                <p className={styles.cardSummary} style={{ margin: 0 }}>
                  {residence.aspect}
                </p>
              </div>

              <div className={styles.asideCta}>
                <Link
                  href={`/enquire?residence=${residence.id}`}
                  className="button"
                  style={{ justifyContent: "center" }}
                >
                  {residence.status === "available"
                    ? `Request a visit to ${String(residence.index).padStart(2, "0")}`
                    : "Ask about similar houses"}
                </Link>
                <p className="annotation" style={{ textAlign: "center" }}>
                  Answered by a person within 24 hours
                </p>
              </div>
            </div>
          </aside>
        </div>
      </div>

      {/* Plans and schedule of areas */}
      <section className="page section" aria-labelledby="plans-title">
        <div className="section-head">
          <span className="section-index">03</span>
          <h2 id="plans-title" className="section-label">
            Plans and schedule of areas
          </h2>
        </div>

        <div className={styles.drawingStack}>
          {residence.plan.map((level) => (
            <div key={level.levelIndex}>
              <FloorPlan residence={residence} levelIndex={level.levelIndex} />
            </div>
          ))}
        </div>

        <table className="data-table" style={{ marginTop: "var(--space-l)" }}>
          <caption>Schedule of areas — {residence.name}</caption>
          <thead>
            <tr>
              <th scope="col">Level</th>
              <th scope="col">Room</th>
              <th scope="col" className="numeric">
                Area
              </th>
            </tr>
          </thead>
          <tbody>
            {residence.plan.flatMap((level) =>
              level.rooms.map((room, i) => (
                <tr key={`${level.levelIndex}-${room.name}`}>
                  <td>{i === 0 ? level.level : ""}</td>
                  <th scope="row" style={{ fontWeight: 400 }}>
                    {room.name}
                  </th>
                  <td className="numeric">{room.areaSqm}</td>
                </tr>
              )),
            )}
            <tr>
              <td />
              <th scope="row">Total scheduled</th>
              <td className="numeric">{scheduleTotal}</td>
            </tr>
          </tbody>
        </table>
        <p className="annotation" style={{ marginTop: "var(--space-2xs)", maxWidth: "62ch" }}>
          Scheduled total {scheduleTotal} m² against {residence.interiorAreaSqm} m² gross interior;
          the difference is wall thickness and structure.
        </p>
      </section>

      {/* Specification */}
      <section className="page section" aria-labelledby="spec-title">
        <div className="section-head">
          <span className="section-index">04</span>
          <h2 id="spec-title" className="section-label">
            Construction and systems
          </h2>
        </div>
        <ul className={styles.featureGroups}>
          {residence.features.map((group) => (
            <li key={group.group}>
              <h3 className={styles.featureGroupName}>{group.group}</h3>
              <ul className={styles.featureItems}>
                {group.items.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </li>
          ))}
        </ul>

        <h3 className={styles.featureGroupName} style={{ marginTop: "var(--space-xl)" }}>
          Material palette
        </h3>
        <MaterialSwatches materials={residence.materials} />
      </section>

      {/* Position on the ridge */}
      <section className="page section" aria-labelledby="position-title">
        <div className="section-head">
          <span className="section-index">05</span>
          <h2 id="position-title" className="section-label">
            Position on the ridge
          </h2>
        </div>
        <RidgeSection residences={all} activeId={residence.id} compact />
        <div style={{ marginTop: "var(--space-l)" }}>
          <SitePlan residences={all} activeId={residence.id} interactive={false} />
        </div>

        <nav className={styles.neighbours} aria-label="Adjacent residences">
          {previous ? (
            <Link href={`/residences/${previous.slug}`} prefetch={false}>
              <span className="annotation">← Previous on the ridge</span>
              <span className={styles.neighbourName}>{previous.name}</span>
            </Link>
          ) : (
            <span />
          )}
          {next ? (
            <Link href={`/residences/${next.slug}`} style={{ textAlign: "right" }} prefetch={false}>
              <span className="annotation">Next on the ridge →</span>
              <span className={styles.neighbourName}>{next.name}</span>
            </Link>
          ) : (
            <span />
          )}
        </nav>
      </section>

      <JsonLd
        nodes={[
          breadcrumbNode([
            { name: "Home", path: "/" },
            { name: "Residences", path: "/residences" },
            { name: residence.name, path: `/residences/${residence.slug}` },
          ]),
          residenceNode(residence),
        ]}
      />
    </>
  );
}
