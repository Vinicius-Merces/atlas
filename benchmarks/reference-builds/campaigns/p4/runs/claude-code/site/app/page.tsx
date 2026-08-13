import Link from "next/link";
import type { Metadata } from "next";
import styles from "./page.module.css";
import {
  getResidences,
  getDistricts,
  getJournalEntries,
  getDevelopmentFacts,
  getSettings,
  residenceTypeLabel,
  statusLabel,
} from "@/lib/content";
import { compactEur, formatPriceBand, formatQuarter, formatSqm } from "@/lib/format";
import { RidgeSection } from "@/components/drawings/RidgeSection";
import { SitePlan } from "@/components/drawings/SitePlan";
import { pageMetadata } from "@/lib/seo";
import { JsonLd, breadcrumbNode, residenceNode } from "@/lib/jsonld";

export const metadata: Metadata = pageMetadata({
  title: "Asteria Residences — twelve houses on the Alto da Pedra ridge",
  description:
    "Twelve architect-designed houses at 148–178 m on a limestone ridge 22 km from central Lisbon. Full areas, plans, price bands and delivery quarters published. Visits by appointment.",
  path: "/",
});

export default function HomePage() {
  const residences = getResidences();
  const districts = getDistricts();
  const journal = getJournalEntries().slice(0, 3);
  const facts = getDevelopmentFacts();
  const s = getSettings();

  const typologies = (["ridge", "terrace", "courtyard"] as const).map((type) => ({
    type,
    label: residenceTypeLabel(type),
    items: residences.filter((r) => r.type === type),
  }));

  return (
    <>
      {/* 01 — Statement and the ridge datum */}
      <section className={`page ${styles.hero}`} aria-labelledby="hero-title">
        <div className={styles.heroKicker}>
          <span className="section-index">01</span>
          <span className="section-label">
            {s.developmentLocality}, {s.developmentRegion} · {s.developmentCountry}
          </span>
          <span className="section-label">
            {facts.minElevationM}–{facts.maxElevationM} m
          </span>
        </div>

        <div className={styles.heroGrid}>
          <div className={styles.heroStatement}>
            <h1 id="hero-title" className={styles.heroTitle}>
              Twelve houses, <em>drawn</em> before they are built.
            </h1>
            <p className={styles.heroLede}>
              Asteria is a single limestone ridge twenty-two kilometres west of Lisbon, and twelve
              houses set along it between 148 and 178 metres. Nothing here is photographed, because
              nothing is finished. Everything here is measured.
            </p>
            <div className={styles.heroActions}>
              <Link href="/residences" className="button">
                See the twelve
              </Link>
              <Link href="/enquire" className="button button--ghost">
                Request a visit
              </Link>
            </div>
          </div>

          <ul className={styles.heroFacts}>
            <li className={styles.heroFact}>
              <span className="annotation">Houses</span>
              <span className={styles.heroFactValue}>
                {facts.total} · {facts.available} available
              </span>
            </li>
            <li className={styles.heroFact}>
              <span className="annotation">Interior area</span>
              <span className={styles.heroFactValue}>
                {facts.minInteriorSqm}–{facts.maxInteriorSqm} m²
              </span>
            </li>
            <li className={styles.heroFact}>
              <span className="annotation">Price band</span>
              <span className={styles.heroFactValue}>
                {compactEur(facts.minPriceEur)}–{compactEur(facts.maxPriceEur)}
              </span>
            </li>
            <li className={styles.heroFact}>
              <span className="annotation">Delivery</span>
              <span className={styles.heroFactValue}>
                {formatQuarter(facts.firstDelivery)} – {formatQuarter(facts.lastDelivery)}
              </span>
            </li>
            <li className={styles.heroFact}>
              <span className="annotation">Central Lisbon</span>
              <span className={styles.heroFactValue}>21.8 km · 28 min</span>
            </li>
          </ul>
        </div>

        <div className={styles.heroDrawing}>
          <RidgeSection residences={residences} animate />
        </div>
      </section>

      {/* 02 — The index of twelve */}
      <section className="page section" aria-labelledby="index-title">
        <div className="section-head">
          <span className="section-index">02</span>
          <h2 id="index-title" className="section-label">
            The index
          </h2>
        </div>

        <div className={styles.indexLayout}>
          <div className={styles.indexTable}>
            <p className="lede" style={{ marginBottom: "var(--space-l)" }}>
              Every house is listed with its real area, its price band and its position on the ridge.
              Sold and reserved houses stay on the list, because a development that hides them is
              harder to judge.
            </p>
            <ul style={{ listStyle: "none", borderTop: "var(--rule-thin) solid var(--ink)" }}>
              {residences.map((r) => (
                <li key={r.id}>
                  <Link href={`/residences/${r.slug}`} className={styles.indexRowLink} prefetch={false}>
                    <article className={styles.residenceRow}>
                      <span className={styles.rowIndex}>{String(r.index).padStart(2, "0")}</span>
                      <div>
                        <h3 className={styles.rowName}>{r.name}</h3>
                        <div className={styles.rowMeta}>
                          <span className="annotation">{residenceTypeLabel(r.type)}</span>
                          <span className="annotation">{r.bedrooms} bed</span>
                          <span className="annotation">{formatSqm(r.interiorAreaSqm)}</span>
                          <span className="annotation">+{r.elevationM} m</span>
                          <span className={`status status--${r.status}`}>{statusLabel(r.status)}</span>
                        </div>
                      </div>
                      <div className={styles.rowFigures}>
                        <span className={styles.rowPrice}>{formatPriceBand(r.priceBandEur)}</span>
                        <span className="annotation">{formatQuarter(r.deliveryQuarter)}</span>
                      </div>
                    </article>
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div className={styles.indexPlan}>
            <SitePlan residences={residences} />
          </div>
        </div>
      </section>

      {/* 03 — Why twelve */}
      <section className="page section" aria-labelledby="thesis-title">
        <div className="section-head">
          <span className="section-index">03</span>
          <span className="section-label">The argument</span>
        </div>

        <div className={styles.thesisGrid}>
          <div className={styles.thesisLead}>
            <h2 id="thesis-title" className={styles.thesisHeading}>
              The plan permits thirty-eight. We drew twelve.
            </h2>
            <p className="annotation thesisNote">
              Site coverage 11% · retained landscape 89% · excavation 8,400 m³
            </p>
          </div>
          <div className={`prose ${styles.thesisBody}`}>
            <p>
              At thirty-eight dwellings the access lane has to be widened to two lanes with a
              footway. That means cutting a two-metre bench along the escarpment for its full
              length, losing the eighteenth-century vineyard terraces and the public vineyard walk
              with them, and moving thirty-one thousand cubic metres of limestone through the
              village over two years.
            </p>
            <p>
              At twelve the cut is contained within the three courtyard plots on the plateau, the
              material is reused on site for terrace retaining, and eighty-nine per cent of the
              ridge stays as it is. The houses cost more per square metre as a direct result,
              because each one carries a larger share of a site that has deliberately been left
              alone.
            </p>
            <p>
              <Link href="/journal/why-twelve-houses">Read the full arithmetic in the journal →</Link>
            </p>
          </div>
        </div>
      </section>

      {/* 04 — Three plan families */}
      <section className="page section" aria-labelledby="typology-title">
        <div className="section-head">
          <span className="section-index">04</span>
          <h2 id="typology-title" className="section-label">
            Three plan families
          </h2>
        </div>
        <ul className={styles.typologies}>
          {typologies.map(({ type, label, items }) => (
            <li key={type} className={styles.typology}>
              <h3 className={styles.typologyName}>
                {label}s <span className={`num ${styles.typologyCount}`}>{items.length}</span>
              </h3>
              <p className={styles.typologyBody}>
                {type === "ridge" &&
                  "Cut into the falling south-west face. Two levels from the lane, one from the valley, with the living floor pressed against the retaining wall."}
                {type === "terrace" &&
                  "Seven point two metres wide, nineteen deep, stepping in half-levels so daylight from the south front reaches the middle of the plan."}
                {type === "courtyard" &&
                  "Single storey on the exposed plateau, turned inward around a walled court because above 170 metres the wind decides the plan."}
              </p>
              <ul className={styles.typologyList}>
                {items.map((r) => (
                  <li key={r.id}>
                    <Link href={`/residences/${r.slug}`} style={{ textDecoration: "none" }} prefetch={false}>
                      <span className="num">{String(r.index).padStart(2, "0")}</span> {r.name}
                    </Link>
                    <span className="annotation">{formatSqm(r.interiorAreaSqm)}</span>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </section>

      {/* 05 — Where it is */}
      <section className="page section" aria-labelledby="location-title">
        <div className="section-head">
          <span className="section-index">05</span>
          <h2 id="location-title" className="section-label">
            Where it is
          </h2>
        </div>
        <ul className={styles.districts}>
          {districts.map((d) => (
            <li key={d.id} className={styles.district}>
              <h3 className={styles.districtName}>
                <Link href={`/location#${d.slug}`} style={{ textDecoration: "none" }}>
                  {d.name}
                </Link>
              </h3>
              <p className={styles.districtSummary}>{d.summary}</p>
              <p className={`annotation ${styles.districtTiming}`}>
                {d.distanceKm === 0 ? "on site" : `${d.distanceKm} km`} · {d.travelMinutes} min
              </p>
            </li>
          ))}
        </ul>
        <p style={{ marginTop: "var(--space-m)" }}>
          <Link href="/location">The full location record →</Link>
        </p>
      </section>

      {/* 06 — Journal */}
      <section className="page section" aria-labelledby="journal-title">
        <div className="section-head">
          <span className="section-index">06</span>
          <h2 id="journal-title" className="section-label">
            From the journal
          </h2>
        </div>
        <ul className={styles.journalList}>
          {journal.map((entry) => (
            <li key={entry.slug} className={styles.journalItem}>
              <p className="annotation">
                {entry.kicker} · {entry.readingMinutes} min
              </p>
              <h3 className={styles.journalTitle}>
                <Link href={`/journal/${entry.slug}`}>{entry.title}</Link>
              </h3>
              <p className={styles.journalDeck}>{entry.deck}</p>
            </li>
          ))}
        </ul>
      </section>

      {/* 07 — The visit */}
      <section className={`page ${styles.closing}`} aria-labelledby="closing-title">
        <div className="section-head">
          <span className="section-index">07</span>
          <span className="section-label">The visit</span>
        </div>
        <div className={styles.closingGrid}>
          <div className={styles.closingLead}>
            <h2 id="closing-title" className={styles.closingHeading}>
              Ninety minutes on the ridge, sturdy shoes.
            </h2>
            <div className={styles.heroActions}>
              <Link href="/enquire" className="button">
                Request a visit
              </Link>
              <a href={`tel:${s.telephone.replace(/\s/g, "")}`} className="button button--ghost">
                {s.telephone}
              </a>
            </div>
          </div>
          <div className={`prose ${styles.closingDetail}`}>
            <p>
              Visits leave from the sales office in Oeiras and take about ninety minutes on foot. You
              will see the plots, the vineyard terraces, the plateau, and the two houses that are
              under construction. You will not see a show home, because there is not one yet.
            </p>
            <p>
              A request submitted through this site is recorded immediately with a reference code
              beginning <span className="num">AST-</span>, and answered by a person within{" "}
              {s.responsePromiseHours} hours.
            </p>
          </div>
        </div>
      </section>

      <JsonLd
        nodes={[
          breadcrumbNode([{ name: "Home", path: "/" }]),
          {
            "@type": "ItemList",
            name: "Asteria Residences — the twelve houses",
            numberOfItems: residences.length,
            itemListElement: residences.map((r) => ({
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
