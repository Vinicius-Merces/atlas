import Link from "next/link";
import { getSettings, getResidences, getDistricts, getJournalEntries } from "@/lib/content";
import styles from "./site-chrome.module.css";

export function SiteFooter() {
  const s = getSettings();
  const residences = getResidences();
  const districts = getDistricts();
  const journal = getJournalEntries().slice(0, 3);

  return (
    <footer className={styles.footer}>
      <div className={`page ${styles.footerInner}`}>
        <div className={styles.footerBrand}>
          <p className={styles.footerName}>{s.organisation}</p>
          <p className={styles.footerTagline}>{s.tagline}</p>
          <address className={styles.address}>
            {s.salesOffice.street}
            <br />
            {s.salesOffice.postalCode} {s.salesOffice.locality}, {s.salesOffice.country}
            <br />
            <a href={`tel:${s.telephone.replace(/\s/g, "")}`}>{s.telephone}</a>
            <br />
            <a href={`mailto:${s.email}`}>{s.email}</a>
          </address>
          <p className="annotation">{s.openingHours}</p>
        </div>

        <nav className={styles.footerNav} aria-label="Residences">
          <h2 className={styles.footerHeading}>Residences</h2>
          <ul className={styles.footerList}>
            {residences.map((r) => (
              <li key={r.id}>
                <Link href={`/residences/${r.slug}`} prefetch={false}>
                  <span className="num">{String(r.index).padStart(2, "0")}</span> {r.name}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <nav className={styles.footerNav} aria-label="Location and journal">
          <h2 className={styles.footerHeading}>Location</h2>
          <ul className={styles.footerList}>
            {districts.map((d) => (
              <li key={d.id}>
                <Link href={`/location#${d.slug}`} prefetch={false}>{d.name}</Link>
              </li>
            ))}
          </ul>
          <h2 className={styles.footerHeading}>Journal</h2>
          <ul className={styles.footerList}>
            {journal.map((entry) => (
              <li key={entry.slug}>
                <Link href={`/journal/${entry.slug}`} prefetch={false}>{entry.title}</Link>
              </li>
            ))}
            <li>
              <Link href="/journal">All entries</Link>
            </li>
          </ul>
        </nav>

        <nav className={styles.footerNav} aria-label="Legal and contact">
          <h2 className={styles.footerHeading}>Practical</h2>
          <ul className={styles.footerList}>
            <li>
              <Link href="/enquire">Request a visit</Link>
            </li>
            <li>
              <Link href="/contact">Contact and sales office</Link>
            </li>
            <li>
              <Link href="/privacy">Privacy notice</Link>
            </li>
            <li>
              <Link href="/terms">Terms and sales information</Link>
            </li>
          </ul>
        </nav>
      </div>

      <div className={`page ${styles.colophon}`}>
        <p className="annotation">
          © {new Date().getFullYear()} {s.legalName} · Construction licence 2025/AP/0114
        </p>
        <p className="annotation">
          Drawings are indicative. Areas carry a ±2% contractual tolerance.
        </p>
      </div>
    </footer>
  );
}
