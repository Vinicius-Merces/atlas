import type { Residence } from "@/lib/content";
import styles from "./drawings.module.css";

type Rect = { x: number; y: number; w: number; h: number };

/**
 * A schematic floor plan produced by a deterministic squarified treemap over
 * the level's room areas. Room proportions on the drawing therefore match the
 * schedule of areas exactly.
 */
function layout(areas: number[], frame: Rect): Rect[] {
  const total = areas.reduce((a, b) => a + b, 0);
  const out: Rect[] = [];
  let rest = { ...frame };
  let remaining = total;

  areas.forEach((area, index) => {
    if (index === areas.length - 1) {
      out.push(rest);
      return;
    }
    const share = area / remaining;
    if (rest.w >= rest.h) {
      const w = rest.w * share;
      out.push({ x: rest.x, y: rest.y, w, h: rest.h });
      rest = { x: rest.x + w, y: rest.y, w: rest.w - w, h: rest.h };
    } else {
      const h = rest.h * share;
      out.push({ x: rest.x, y: rest.y, w: rest.w, h });
      rest = { x: rest.x, y: rest.y + h, w: rest.w, h: rest.h - h };
    }
    remaining -= area;
  });

  return out;
}

export function FloorPlan({
  residence,
  levelIndex,
}: {
  residence: Residence;
  levelIndex: number;
}) {
  const level = residence.plan.find((l) => l.levelIndex === levelIndex) ?? residence.plan[0]!;
  const W = 800;
  const H = 600;
  const frame: Rect = { x: 40, y: 56, w: W - 80, h: H - 116 };
  const rects = layout(
    level.rooms.map((r) => r.areaSqm),
    frame,
  );

  return (
    <figure className={styles.figure}>
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className={`drawing ${styles.floor}`}
        role="img"
        aria-labelledby={`plan-title-${residence.id}-${levelIndex} plan-desc-${residence.id}-${levelIndex}`}
        preserveAspectRatio="xMidYMid meet"
      >
        <title id={`plan-title-${residence.id}-${levelIndex}`}>
          {`${level.level} plan of ${residence.name}`}
        </title>
        <desc id={`plan-desc-${residence.id}-${levelIndex}`}>
          {`Room areas on the ${level.level.toLowerCase()}: ` +
            level.rooms.map((r) => `${r.name}, ${r.areaSqm} square metres`).join("; ") +
            ". The same figures appear in the schedule of areas below."}
        </desc>

        {rects.map((rect, i) => {
          const room = level.rooms[i]!;
          const small = rect.w < 96 || rect.h < 54;
          return (
            <g key={room.name}>
              <rect
                x={rect.x}
                y={rect.y}
                width={rect.w}
                height={rect.h}
                className={i % 2 === 0 ? styles.room : styles.roomAlt}
              />
              {!small && (
                <>
                  <text x={rect.x + 10} y={rect.y + 20} className={styles.roomLabel}>
                    {room.name}
                  </text>
                  <text x={rect.x + 10} y={rect.y + 35} className={styles.roomArea}>
                    {`${room.areaSqm} m²`}
                  </text>
                </>
              )}
              {small && (
                <text x={rect.x + 5} y={rect.y + 15} className={styles.roomArea}>
                  {room.areaSqm}
                </text>
              )}
            </g>
          );
        })}

        <text x={40} y={36} className={styles.roomLabel}>
          {level.level}
        </text>
        <text x={W - 40} y={36} textAnchor="end" className={styles.roomArea}>
          {`${level.rooms.reduce((s, r) => s + r.areaSqm, 0)} m² on this level`}
        </text>
        <text x={40} y={H - 26} className={styles.roomArea}>
          Areas proportional · indicative arrangement
        </text>
      </svg>
      <figcaption className="drawing-caption">
        <span className="annotation">
          Fig. 04 — {residence.name}, {level.level.toLowerCase()}
        </span>
        <span className="annotation">Areas to scale</span>
      </figcaption>
    </figure>
  );
}
