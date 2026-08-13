import Link from "next/link";
import type { Residence } from "@/lib/content";
import styles from "./drawings.module.css";

/**
 * The site plan, drawn as the constellation the development is named for:
 * twelve nodes at their surveyed positions, connected in ridge order.
 * Each node is a real link to its residence, so the drawing is also navigation.
 */
export function SitePlan({
  residences,
  activeId,
  interactive = true,
}: {
  residences: Residence[];
  activeId?: string;
  interactive?: boolean;
}) {
  const W = 1200;
  const H = 560;
  const pad = 70;

  const x = (t: number) => pad + t * (W - pad * 2);
  const y = (t: number) => pad + (0.12 + t * 0.72) * (H - pad * 2);

  const ordered = [...residences].sort((a, b) => a.index - b.index);

  return (
    <figure className={styles.figure}>
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className={`drawing ${styles.plan}`}
        /*
         * When the hit layer is present the drawing contains focusable links,
         * so `role="img"` would be a nested-interactive violation: the correct
         * role for a labelled container of interactive children is `group`.
         */
        role={interactive ? "group" : "img"}
        aria-labelledby="siteplan-title siteplan-desc"
        preserveAspectRatio="xMidYMid meet"
      >
        <title id="siteplan-title">Site plan of the twelve plots on the Alto da Pedra ridge</title>
        <desc id="siteplan-desc">
          {`Twelve numbered plots run west to east along the ridge. ` +
            ordered
              .map(
                (r) =>
                  `Plot ${String(r.index).padStart(2, "0")}, ${r.name}, ${r.status}, plot area ${r.plotAreaSqm} square metres`,
              )
              .join(". ") +
            ". The plateau path and the vineyard walk cross the site and remain public."}
        </desc>

        {/* Ridge edge and contours */}
        <path
          d={`M ${pad} ${y(0.86)} C ${W * 0.3} ${y(0.72)}, ${W * 0.62} ${y(0.46)}, ${W - pad} ${y(0.2)}`}
          className={styles.planEdge}
        />
        {[0.1, 0.22, 0.34].map((offset) => (
          <path
            key={offset}
            d={`M ${pad} ${y(0.86 + offset)} C ${W * 0.3} ${y(0.72 + offset)}, ${W * 0.62} ${y(0.46 + offset)}, ${W - pad} ${y(0.2 + offset)}`}
            className={styles.planContour}
          />
        ))}

        {/* Plateau path */}
        <path
          d={`M ${pad} ${y(0.62)} C ${W * 0.35} ${y(0.5)}, ${W * 0.65} ${y(0.26)}, ${W - pad} ${y(0.08)}`}
          className={styles.planPathLine}
        />
        <text x={W - pad} y={y(0.08) - 10} textAnchor="end" className={styles.planLegend}>
          Plateau path
        </text>

        {/* Connectors in ridge order */}
        {ordered.slice(0, -1).map((r, i) => {
          const next = ordered[i + 1]!;
          return (
            <line
              key={`${r.id}-link`}
              x1={x(r.plotX)}
              y1={y(r.plotY)}
              x2={x(next.plotX)}
              y2={y(next.plotY)}
              className={styles.planLink}
            />
          );
        })}

        {/* Plot marks. Always drawn, never themselves interactive. */}
        {ordered.map((r) => (
          <g
            key={r.id}
            className={`${styles.planLinkGroup} ${r.id === activeId ? styles.planActive : ""}`}
            data-plot={r.id}
          >
            <circle cx={x(r.plotX)} cy={y(r.plotY)} r={13} className={styles.planNode} />
            <text
              x={x(r.plotX)}
              y={y(r.plotY) + 4}
              textAnchor="middle"
              className={styles.planNodeLabel}
            >
              {String(r.index).padStart(2, "0")}
            </text>
          </g>
        ))}

        {/*
          Hit layer. The drawing is a supplementary way to reach a residence;
          the authoritative tap path is the residence list on the same page.
          Below 48rem this layer is display:none — removed from the tab order
          and from the accessibility tree — because at phone scale a plot node
          cannot reach a 24 px target without the twelve nodes colliding.
          Above 48rem each target is a 40-unit radius circle, comfortably past
          24 CSS px at every rendered width.
        */}
        {interactive && (
          <g className={styles.planHits}>
            {ordered.map((r) => (
              <Link
                key={`${r.id}-hit`}
                href={`/residences/${r.slug}`}
                prefetch={false}
                aria-label={`${r.name}, plot ${String(r.index).padStart(2, "0")}, ${r.status}`}
              >
                <circle
                  cx={x(r.plotX)}
                  cy={y(r.plotY)}
                  r={40}
                  fill="transparent"
                  className={styles.planHit}
                  data-plot-hit={r.id}
                />
              </Link>
            ))}
          </g>
        )}

        <text x={pad} y={H - 26} className={styles.planLegend}>
          West
        </text>
        <text x={W - pad} y={H - 26} textAnchor="end" className={styles.planLegend}>
          East · plateau
        </text>
      </svg>
      <figcaption className="drawing-caption">
        <span className="annotation">Fig. 02 — Site plan, 1:2500</span>
        <span className="annotation">12 plots · 11% site coverage</span>
      </figcaption>
    </figure>
  );
}
