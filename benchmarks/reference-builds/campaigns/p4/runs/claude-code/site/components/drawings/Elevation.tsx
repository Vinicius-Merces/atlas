import type { Residence } from "@/lib/content";
import styles from "./drawings.module.css";

/**
 * A schematic elevation generated from the residence's own dimensional data:
 * footprint width from the plan family, storey count from `levels`, opening
 * rhythm from bedroom count. The drawing cannot contradict the specification
 * table because it is drawn from the same fields.
 */
export function Elevation({ residence }: { residence: Residence }) {
  const W = 900;
  const H = 600;
  const groundY = 470;

  const footprint =
    residence.type === "courtyard" ? 620 : residence.type === "ridge" ? 520 : 340;
  const storeyHeight = residence.type === "courtyard" ? 118 : 104;
  const storeys = residence.type === "terrace" ? 2 : residence.levels;
  const buriedLevel = residence.type !== "courtyard";

  const left = (W - footprint) / 2;
  const bodyTop = groundY - storeys * storeyHeight;

  const openings = Math.max(3, Math.min(7, residence.bedrooms + 1));
  const openingWidth = footprint / (openings * 2 + 1);

  // The ground line falls across the plot for the cut-in types.
  const fall = buriedLevel ? 62 : 10;

  return (
    <figure className={styles.figure}>
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className={`drawing ${styles.elevation}`}
        role="img"
        aria-labelledby={`elev-title-${residence.id} elev-desc-${residence.id}`}
        preserveAspectRatio="xMidYMid meet"
      >
        <title id={`elev-title-${residence.id}`}>
          {`Schematic elevation of ${residence.name}`}
        </title>
        <desc id={`elev-desc-${residence.id}`}>
          {`${residence.name} is a ${residence.levels}-level ${residence.type} house of ` +
            `${residence.interiorAreaSqm} square metres interior area, facing ${residence.orientation}, ` +
            `set at ${residence.elevationM} metres above the valley datum. ` +
            (buriedLevel
              ? "The lower level is cut into the falling ground and opens at grade to the garden side."
              : "The house is single storey, wrapped around an enclosed courtyard.")}
        </desc>

        {/* Mass. On the cut-in types the lower level continues below the
            uphill ground line, which is what "two storeys from the lane and one
            from the valley" means in section. */}
        <rect
          x={left}
          y={bodyTop}
          width={footprint}
          height={storeys * storeyHeight + (buriedLevel ? 26 : 0)}
          className={styles.elevMass}
        />

        {/* Ground: falls left (uphill, cut) to right (downhill, at grade). */}
        {(() => {
          const y0 = groundY - fall;
          const y1 = groundY + 14;
          const ground = (t: number) => y0 + (y1 - y0) * (t * t * 0.55 + t * 0.45);
          const steps = 40;
          const pts = Array.from({ length: steps + 1 }, (_, i) => {
            const t = i / steps;
            return { x: 30 + t * (W - 60), y: ground(t) };
          });
          return (
            <g>
              <polyline
                points={pts.map((p) => `${p.x},${p.y}`).join(" ")}
                className={styles.elevGround}
              />
              {pts
                .filter((_, i) => i % 2 === 0)
                .map((p) => (
                  <line
                    key={p.x}
                    x1={p.x}
                    y1={p.y + 3}
                    x2={p.x - 11}
                    y2={p.y + 16}
                    className={styles.elevHatch}
                  />
                ))}
            </g>
          );
        })()}

        {/* Storey division lines */}
        {Array.from({ length: storeys - 1 }, (_, i) => (
          <line
            key={i}
            x1={left}
            x2={left + footprint}
            y1={bodyTop + (i + 1) * storeyHeight}
            y2={bodyTop + (i + 1) * storeyHeight}
            className={styles.elevHatch}
          />
        ))}

        {/* Roof plane / canopy */}
        <line
          x1={left - (residence.type === "ridge" ? 34 : 12)}
          x2={left + footprint + (residence.type === "ridge" ? 34 : 12)}
          y1={bodyTop}
          y2={bodyTop}
          stroke="var(--ink)"
          strokeWidth={2}
        />

        {/* Openings */}
        {Array.from({ length: storeys }, (_, level) =>
          Array.from({ length: openings }, (_, i) => {
            const ox = left + openingWidth * (i * 2 + 1);
            const oy = bodyTop + level * storeyHeight + 26;
            return (
              <rect
                key={`${level}-${i}`}
                x={ox}
                y={oy}
                width={openingWidth}
                height={storeyHeight - 46}
                className={styles.elevOpening}
              />
            );
          }),
        )}

        {/* Dimension line */}
        <g>
          <line
            x1={left}
            x2={left + footprint}
            y1={groundY + 46}
            y2={groundY + 46}
            className={styles.elevDim}
          />
          <line x1={left} x2={left} y1={groundY + 40} y2={groundY + 52} className={styles.elevDim} />
          <line
            x1={left + footprint}
            x2={left + footprint}
            y1={groundY + 40}
            y2={groundY + 52}
            className={styles.elevDim}
          />
          <text
            x={left + footprint / 2}
            y={groundY + 68}
            textAnchor="middle"
            className={styles.elevDimText}
          >
            {`${residence.interiorAreaSqm} m² interior`}
          </text>
        </g>

        <text x={40} y={44} className={styles.elevDimText}>
          {`${residence.orientation} elevation · +${residence.elevationM} m`}
        </text>
      </svg>
      <figcaption className="drawing-caption">
        <span className="annotation">
          Fig. 03 — {residence.name}, schematic elevation, indicative
        </span>
        <span className="annotation">{residence.levels} level(s)</span>
      </figcaption>
    </figure>
  );
}
