import type { Residence } from "@/lib/content";
import styles from "./drawings.module.css";

export function MaterialSwatches({ materials }: { materials: Residence["materials"] }) {
  return (
    <ul className={styles.swatches}>
      {materials.map((material) => (
        <li key={material.name} className={styles.swatch}>
          <div className={styles.swatchChip} style={{ background: material.hex }} aria-hidden="true" />
          <div className={styles.swatchBody}>
            <p className={styles.swatchName}>{material.name}</p>
            <p className={styles.swatchUse}>{material.application}</p>
          </div>
        </li>
      ))}
    </ul>
  );
}
