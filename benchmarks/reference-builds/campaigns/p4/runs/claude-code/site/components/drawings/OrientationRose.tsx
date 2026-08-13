import { orientationDegrees, orientationName } from "@/lib/format";
import styles from "./drawings.module.css";

export function OrientationRose({ orientation }: { orientation: string }) {
  const size = 200;
  const c = size / 2;
  const r = 74;
  const degrees = orientationDegrees[orientation] ?? 180;
  const rad = ((degrees - 90) * Math.PI) / 180;
  const nx = c + Math.cos(rad) * r;
  const ny = c + Math.sin(rad) * r;

  const letters = ["N", "E", "S", "W"];

  return (
    <svg
      viewBox={`0 0 ${size} ${size}`}
      className={styles.rose}
      role="img"
      aria-label={`Principal aspect faces ${orientationName[orientation] ?? orientation}`}
    >
      <circle cx={c} cy={c} r={r} className={styles.roseRing} />
      <circle cx={c} cy={c} r={r - 12} className={styles.roseRing} />
      {Array.from({ length: 16 }, (_, i) => {
        const a = ((i * 22.5 - 90) * Math.PI) / 180;
        const inner = i % 4 === 0 ? r - 20 : r - 8;
        return (
          <line
            key={i}
            x1={c + Math.cos(a) * inner}
            y1={c + Math.sin(a) * inner}
            x2={c + Math.cos(a) * r}
            y2={c + Math.sin(a) * r}
            className={styles.roseTick}
          />
        );
      })}
      <line x1={c} y1={c} x2={nx} y2={ny} className={styles.roseNeedle} />
      <circle cx={c} cy={c} r={3} fill="var(--accent)" />
      {letters.map((letter, i) => {
        const a = ((i * 90 - 90) * Math.PI) / 180;
        return (
          <text
            key={letter}
            x={c + Math.cos(a) * (r + 14)}
            y={c + Math.sin(a) * (r + 14) + 4}
            textAnchor="middle"
            className={styles.roseLetter}
          >
            {letter}
          </text>
        );
      })}
    </svg>
  );
}
