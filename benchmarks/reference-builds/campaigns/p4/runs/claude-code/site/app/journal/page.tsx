import Link from "next/link";
import type { Metadata } from "next";
import styles from "./journal.module.css";
import { getJournalEntries } from "@/lib/content";
import { formatDate } from "@/lib/format";
import { pageMetadata } from "@/lib/seo";
import { JsonLd, breadcrumbNode, journalNode } from "@/lib/jsonld";

export const metadata: Metadata = pageMetadata({
  title: "Journal",
  description:
    "Notes from the people building Asteria: why the scheme is twelve houses and not thirty-eight, how to read the ridge section, what off-plan terms actually protect, and where the energy rating comes from.",
  path: "/journal",
});

export default function JournalPage() {
  const entries = getJournalEntries();

  return (
    <>
      <section className={`page ${styles.intro}`}>
        <div className="section-head">
          <span className="section-index">06</span>
          <span className="section-label">Journal · {entries.length} entries</span>
        </div>
        <h1 className={styles.title}>What we would tell you in the sales office</h1>
        <p className="lede" style={{ marginTop: "var(--space-m)" }}>
          Written by the architect, the services engineer and the sales director, with the numbers
          left in. If an entry makes a claim, the figures behind it are on the page.
        </p>
      </section>

      <section className="page section" aria-label="Journal entries">
        <ol className={styles.list}>
          {entries.map((entry, index) => (
            <li key={entry.slug} className={styles.item}>
              <span className={styles.itemIndex}>{String(index + 1).padStart(2, "0")}</span>
              <div>
                <p className="annotation">
                  {entry.kicker} · {formatDate(entry.publishedAt)} · {entry.readingMinutes} min read
                </p>
                <h2 className={styles.itemTitle}>
                  <Link href={`/journal/${entry.slug}`}>{entry.title}</Link>
                </h2>
                <p className={styles.itemDeck}>{entry.deck}</p>
                <p className="annotation">
                  {entry.author.name} · {entry.author.role}
                </p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <JsonLd
        nodes={[
          breadcrumbNode([
            { name: "Home", path: "/" },
            { name: "Journal", path: "/journal" },
          ]),
          {
            "@type": "Blog",
            name: "Asteria Journal",
            blogPost: entries.map(journalNode),
          },
        ]}
      />
    </>
  );
}
