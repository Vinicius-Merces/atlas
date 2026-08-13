"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./site-chrome.module.css";

const NAV = [
  { href: "/residences", label: "Residences" },
  { href: "/location", label: "Location" },
  { href: "/journal", label: "Journal" },
  { href: "/contact", label: "Contact" },
];

export function SiteHeader() {
  const pathname = usePathname();

  return (
    <header className={styles.header}>
      <div className={`page ${styles.headerInner}`}>
        <Link href="/" className={styles.wordmark} aria-label="Asteria Residences, home">
          <span className={styles.wordmarkGlyph} aria-hidden="true">
            <svg viewBox="0 0 40 24" width="40" height="24" focusable="false" aria-hidden="true">
              <line x1="2" y1="20" x2="38" y2="6" stroke="currentColor" strokeWidth="0.75" />
              {[0, 1, 2, 3, 4, 5].map((i) => (
                <rect
                  key={i}
                  x={2 + i * 7.2 - 2}
                  y={20 - i * 2.8 - 2}
                  width="4"
                  height="4"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1"
                />
              ))}
            </svg>
          </span>
          <span className={styles.wordmarkText}>
            Asteria
            <span className={styles.wordmarkSub}>Residences</span>
          </span>
        </Link>

        <nav className={styles.nav} aria-label="Primary">
          <ul className={styles.navList}>
            {NAV.map((item) => {
              const current = pathname === item.href || pathname.startsWith(`${item.href}/`);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={styles.navLink}
                    aria-current={current ? "page" : undefined}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        <Link href="/enquire" className={`button ${styles.headerCta}`}>
          Request a visit
        </Link>
      </div>
    </header>
  );
}
