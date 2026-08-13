import type { Residence } from "@/lib/content";
import styles from "./drawings.module.css";

/**
 * The measured section through the Alto da Pedra escarpment, with each of the
 * twelve plots pegged at its real elevation. This is the site's signature
 * drawing: it is structural information, not decoration, and every number in it
 * comes from the residence records.
 */
export function RidgeSection({
  residences,
  activeId,
  animate = false,
  compact = false,
}: {
  residences: Residence[];
  activeId?: string;
  animate?: boolean;
  compact?: boolean;
}) {
  const W = 1200;
  const H = compact ? 300 : 420;
  const padX = 56;
  const padTop = compact ? 44 : 76;
  const padBottom = 58;

  const elevations = residences.map((r) => r.elevationM);
  const minE = Math.min(...elevations) - 14;
  const maxE = Math.max(...elevations) + 12;

  const x = (t: number) => padX + t * (W - padX * 2);
  const y = (elevationM: number) =>
    H - padBottom - ((elevationM - minE) / (maxE - minE)) * (H - padTop - padBottom);

  // Ground profile: the surveyed line, sampled through the plot elevations.
  const points = residences.map((r) => ({ px: x(r.plotX), py: y(r.elevationM) }));
  const ground = [
    `M ${padX} ${y(minE + 6)}`,
    ...points.map((p, i) => {
      const prev = i === 0 ? { px: padX, py: y(minE + 6) } : points[i - 1]!;
      const cx = (prev.px + p.px) / 2;
      return `C ${cx} ${prev.py} ${cx} ${p.py} ${p.px} ${p.py}`;
    }),
    `L ${W - padX} ${y(maxE - 8)}`,
  ].join(" ");

  const gridSteps = 4;

  return (
    <figure className={styles.figure}>
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className={`drawing ${styles.ridge}`}
        role="img"
        aria-labelledby="ridge-title ridge-desc"
        preserveAspectRatio="xMidYMid meet"
      >
        <title id="ridge-title">
          Measured section through the Alto da Pedra ridge showing all twelve plots
        </title>
        <desc id="ridge-desc">
          {`The ground rises from ${Math.min(...elevations)} metres at the western access to ` +
            `${Math.max(...elevations)} metres at the eastern rock shelf. ` +
            residences
              .map((r) => `Plot ${String(r.index).padStart(2, "0")} at ${r.elevationM} metres`)
              .join(", ") +
            "."}
        </desc>

        {/* Elevation datum grid */}
        {Array.from({ length: gridSteps + 1 }, (_, i) => {
          const value = Math.round(minE + ((maxE - minE) / gridSteps) * i);
          return (
            <g key={value} className={styles.datum}>
              <line x1={padX} x2={W - padX} y1={y(value)} y2={y(value)} />
              <text x={padX - 10} y={y(value) + 4} textAnchor="end">
                {value}
              </text>
            </g>
          );
        })}

        {/* Ground */}
        <path
          d={ground}
          className={`${styles.ground} ${animate ? styles.groundAnimated : ""}`}
          fill="none"
        />

        {/* Plot markers */}
        {residences.map((r) => {
          const px = x(r.plotX);
          const py = y(r.elevationM);
          const active = r.id === activeId;
          return (
            <g
              key={r.id}
              className={`${styles.plot} ${active ? styles.plotActive : ""}`}
              data-residence={r.id}
            >
              <line x1={px} x2={px} y1={py} y2={H - padBottom} className={styles.plotStem} />
              <rect x={px - 7} y={py - 7} width={14} height={14} className={styles.plotMark} />
              <text x={px} y={py - 16} textAnchor="middle" className={styles.plotIndex}>
                {String(r.index).padStart(2, "0")}
              </text>
              {!compact && (
                <text x={px} y={H - padBottom + 20} textAnchor="middle" className={styles.plotElev}>
                  {r.elevationM}
                </text>
              )}
            </g>
          );
        })}

        {/* Baseline */}
        <line
          x1={padX}
          x2={W - padX}
          y1={H - padBottom}
          y2={H - padBottom}
          className={styles.baseline}
        />
        <text x={padX} y={H - 16} className={styles.axisLabel}>
          West access
        </text>
        <text x={W - padX} y={H - 16} textAnchor="end" className={styles.axisLabel}>
          East rock shelf
        </text>
        <text x={padX - 10} y={padTop - 18} textAnchor="end" className={styles.axisLabel}>
          m
        </text>
      </svg>
      <figcaption className="drawing-caption">
        <span className="annotation">Fig. 01 — Ridge section, 1:2000, elevations in metres</span>
        <span className="annotation">Survey datum: valley floor 96 m</span>
      </figcaption>
    </figure>
  );
}
