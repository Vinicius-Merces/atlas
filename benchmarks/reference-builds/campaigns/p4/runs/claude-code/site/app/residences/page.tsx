import Link from "next/link";
import type { Metadata } from "next";
import styles from "./residences.module.css";
import {
  getResidences,
  residenceTypeLabel,
  statusLabel,
  getDevelopmentFacts,
} from "@/lib/content";
import { formatPriceBand, formatQuarter, formatSqm } from "@/lib/format";
import { SitePlan } from "@/components/drawings/SitePlan";
import { pageMetadata } from "@/lib/seo";
import { JsonLd, breadcrumbNode, residenceNode } from "@/lib/jsonld";

export const metadata: Metadata = pageMetadata({
  title: "The twelve residences",
  description:
    "All twelve Asteria residences with interior and plot areas, bedrooms, orientation, elevation, price band, delivery quarter and current availability.",
  path: "/residences",
});

type Search = { [key: string]: string | string[] | undefined };

const TYPES = ["ridge", "terrace", "courtyard"] as const;
const STATUSES = ["available", "reserved", "sold"] as const;

function single(value: string | string[] | undefined): string {
  return Array.isArray(value) ? (value[0] ?? "") : (value ?? "");
}

export default async function ResidencesPage({
  searchParams,
}: {
  searchParams: Promise<Search>;
}) {
  const params = await searchParams;
  const typeFilter = single(params.type);
  const statusFilter = single(params.status);
  const bedroomFilter = single(params.bedrooms);

  const all = getResidences();
  const facts = getDevelopmentFacts();

  const filtered = all.filter((r) => {
    if (typeFilter && r.type !== typeFilter) return false;
    if (statusFilter && r.status !== statusFilter) return false;
    if (bedroomFilter && r.bedrooms < Number(bedroomFilter)) return false;
    return true;
  });

  const filtersActive = Boolean(typeFilter || statusFilter || bedroomFilter);

  return (
    <>
      <section className={`page ${styles.intro}`}>
        <div className="section-head">
          <span className="section-index">02</span>
          <span className="section-label">The index · {facts.total} houses</span>
        </div>

        <div className={styles.introGrid}>
          <div className={styles.introLead}>
            <h1 className={styles.title}>The twelve residences</h1>
            <p className="lede" style={{ marginTop: "var(--space-m)" }}>
              Four ridge houses cut into the south-west face, five terrace houses stepping in
              half-levels, three courtyard houses turned inward on the plateau. Areas are gross and
              carry a ±2% contractual tolerance.
            </p>
          </div>

          {/* Filtering is a plain GET form: it works with JavaScript disabled,
              is linkable, and is announced by the live result count. */}
          <form className={styles.filterForm} method="get" action="/residences">
            <div className={styles.filterRow}>
              <div className={styles.field}>
                <label className={styles.fieldLabel} htmlFor="filter-type">
                  Plan family
                </label>
                <select
                  className={styles.select}
                  id="filter-type"
                  name="type"
                  defaultValue={typeFilter}
                >
                  <option value="">All</option>
                  {TYPES.map((t) => (
                    <option key={t} value={t}>
                      {residenceTypeLabel(t)}
                    </option>
                  ))}
                </select>
              </div>

              <div className={styles.field}>
                <label className={styles.fieldLabel} htmlFor="filter-status">
                  Availability
                </label>
                <select
                  className={styles.select}
                  id="filter-status"
                  name="status"
                  defaultValue={statusFilter}
                >
                  <option value="">All</option>
                  {STATUSES.map((s) => (
                    <option key={s} value={s}>
                      {statusLabel(s)}
                    </option>
                  ))}
                </select>
              </div>

              <div className={styles.field}>
                <label className={styles.fieldLabel} htmlFor="filter-bedrooms">
                  Bedrooms
                </label>
                <select
                  className={styles.select}
                  id="filter-bedrooms"
                  name="bedrooms"
                  defaultValue={bedroomFilter}
                >
                  <option value="">Any</option>
                  <option value="3">3 or more</option>
                  <option value="4">4 or more</option>
                  <option value="5">5</option>
                </select>
              </div>

              <button type="submit" className="button button--ghost">
                Apply
              </button>
            </div>

            <p className={styles.resultCount} role="status" aria-live="polite">
              Showing {filtered.length} of {all.length} residences
              {filtersActive ? " (filtered)" : ""}
            </p>
          </form>
        </div>
      </section>

      <section className="page" aria-label="Site plan">
        <SitePlan residences={filtered.length ? filtered : all} />
      </section>

      <section className="page section" aria-label="Residence list">
        {filtered.length === 0 ? (
          <div className={styles.empty}>
            <h2 style={{ fontSize: "var(--step-2)" }}>No residence matches those filters</h2>
            <p className="prose" style={{ marginTop: "var(--space-2xs)" }}>
              Of the twelve houses, {facts.available} are available, {facts.reserved} reserved and{" "}
              {facts.sold} sold. Try a wider combination, or ask us directly — the sales office holds
              the authoritative position.
            </p>
            <p style={{ marginTop: "var(--space-s)", display: "flex", gap: "var(--space-2xs)", flexWrap: "wrap" }}>
              <Link href="/residences" className="button button--ghost">
                Clear filters
              </Link>
              <Link href="/enquire" className="button">
                Ask the sales office
              </Link>
            </p>
          </div>
        ) : (
          <ul className={styles.grid}>
            {filtered.map((r) => (
              <li key={r.id} className={styles.card}>
                <div className={styles.cardHead}>
                  <span className={styles.cardIndex}>{String(r.index).padStart(2, "0")}</span>
                  <span className={`status status--${r.status}`}>{statusLabel(r.status)}</span>
                </div>
                <h2 className={styles.cardTitle}>
                  <Link href={`/residences/${r.slug}`} prefetch={false}>
                    {r.name}
                  </Link>
                </h2>
                <p className="annotation">
                  {residenceTypeLabel(r.type)} · faces {r.orientation} · +{r.elevationM} m
                </p>
                <p className={styles.cardSummary} style={{ marginTop: "var(--space-2xs)" }}>
                  {r.summary}
                </p>
                <ul className={styles.cardSpecs}>
                  <li className={styles.cardSpec}>
                    <span>Interior</span>
                    <span className={styles.cardSpecValue}>{formatSqm(r.interiorAreaSqm)}</span>
                  </li>
                  <li className={styles.cardSpec}>
                    <span>Outdoor</span>
                    <span className={styles.cardSpecValue}>{formatSqm(r.outdoorAreaSqm)}</span>
                  </li>
                  <li className={styles.cardSpec}>
                    <span>Bedrooms</span>
                    <span className={styles.cardSpecValue}>
                      {r.bedrooms} · {r.bathrooms} bath
                    </span>
                  </li>
                  <li className={styles.cardSpec}>
                    <span>Price band</span>
                    <span className={styles.cardSpecValue}>{formatPriceBand(r.priceBandEur)}</span>
                  </li>
                  <li className={styles.cardSpec}>
                    <span>Delivery</span>
                    <span className={styles.cardSpecValue}>{formatQuarter(r.deliveryQuarter)}</span>
                  </li>
                </ul>
              </li>
            ))}
          </ul>
        )}
      </section>

      <JsonLd
        nodes={[
          breadcrumbNode([
            { name: "Home", path: "/" },
            { name: "Residences", path: "/residences" },
          ]),
          {
            "@type": "ItemList",
            name: "The twelve Asteria residences",
            numberOfItems: all.length,
            itemListElement: all.map((r) => ({
              "@type": "ListItem",
              position: r.index,
              item: residenceNode(r),
            })),
          },
        ]}
      />
    </>
  );
}
