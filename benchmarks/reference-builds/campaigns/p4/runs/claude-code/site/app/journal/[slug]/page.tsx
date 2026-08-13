import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import styles from "../journal.module.css";
import { getJournalEntries, getJournalEntry, getResidenceById, getDistrict, getDistricts } from "@/lib/content";
import { formatDate } from "@/lib/format";
import { Blocks } from "@/components/Blocks";
import { pageMetadata } from "@/lib/seo";
import { JsonLd, breadcrumbNode, journalNode } from "@/lib/jsonld";

export function generateStaticParams() {
  return getJournalEntries().map((entry) => ({ slug: entry.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const entry = getJournalEntry(slug);
  if (!entry) {
    return pageMetadata({ title: "Not found", description: "", path: `/journal/${slug}`, noindex: true });
  }
  return pageMetadata({
    title: entry.title,
    description: entry.deck,
    path: `/journal/${entry.slug}`,
    type: "article",
    publishedTime: entry.publishedAt,
    modifiedTime: entry.updatedAt,
  });
}

export default async function JournalEntryPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const entry = getJournalEntry(slug);
  if (!entry) notFound();

  const related = entry.relatedResidences
    .map((id) => getResidenceById(id))
    .filter((r): r is NonNullable<typeof r> => Boolean(r));
  const relatedDistricts = entry.relatedDistricts
    .map((id) => getDistricts().find((d) => d.id === id) ?? getDistrict(id))
    .filter((d): d is NonNullable<typeof d> => Boolean(d));
  const others = getJournalEntries().filter((e) => e.slug !== entry.slug).slice(0, 2);

  return (
    <article className={`page ${styles.entry}`}>
      <nav aria-label="Breadcrumb">
        <ol className="annotation" style={{ display: "flex", gap: "0.5rem", listStyle: "none", flexWrap: "wrap", marginBottom: "var(--space-m)" }}>
          <li>
            <Link href="/">Asteria</Link> /
          </li>
          <li>
            <Link href="/journal">Journal</Link> /
          </li>
          <li aria-current="page">{entry.kicker}</li>
        </ol>
      </nav>

      <h1 className={styles.entryTitle}>{entry.title}</h1>
      <p className={styles.entryDeck}>{entry.deck}</p>

      <div className={styles.entryLayout}>
        <aside className={styles.entryMeta} aria-label="Entry details">
          <div className={styles.metaItem}>
            <span className="annotation">Written by</span>
            <span className={styles.metaValue}>{entry.author.name}</span>
            <span className="annotation">{entry.author.role}</span>
          </div>
          <div className={styles.metaItem}>
            <span className="annotation">Published</span>
            <span className={styles.metaValue}>
              <time dateTime={entry.publishedAt}>{formatDate(entry.publishedAt)}</time>
            </span>
          </div>
          {entry.updatedAt && (
            <div className={styles.metaItem}>
              <span className="annotation">Updated</span>
              <span className={styles.metaValue}>
                <time dateTime={entry.updatedAt}>{formatDate(entry.updatedAt)}</time>
              </span>
            </div>
          )}
          <div className={styles.metaItem}>
            <span className="annotation">Reading time</span>
            <span className={styles.metaValue}>{entry.readingMinutes} minutes</span>
          </div>
          <ul className={styles.tags}>
            {entry.tags.map((tag) => (
              <li key={tag} className={styles.tag}>
                {tag}
              </li>
            ))}
          </ul>
        </aside>

        <div className={styles.entryBody}>
          <Blocks blocks={entry.body} />

          {(related.length > 0 || relatedDistricts.length > 0) && (
            <section className={styles.related} aria-labelledby="related-title">
              <h2 id="related-title" className="annotation">
                Referenced in this entry
              </h2>
              <ul className={styles.relatedList}>
                {related.map((r) => (
                  <li key={r.id}>
                    <Link href={`/residences/${r.slug}`}>
                      <span className="num">{String(r.index).padStart(2, "0")}</span> {r.name}
                    </Link>
                  </li>
                ))}
                {relatedDistricts.map((d) => (
                  <li key={d.id}>
                    <Link href={`/location#${d.slug}`}>{d.name}</Link>
                  </li>
                ))}
              </ul>
            </section>
          )}

          <section className={styles.related} aria-labelledby="more-title">
            <h2 id="more-title" className="annotation">
              More from the journal
            </h2>
            <ul className={styles.relatedList}>
              {others.map((other) => (
                <li key={other.slug}>
                  <Link href={`/journal/${other.slug}`}>{other.title}</Link>
                </li>
              ))}
              <li>
                <Link href="/enquire">Request a visit →</Link>
              </li>
            </ul>
          </section>
        </div>
      </div>

      <JsonLd
        nodes={[
          breadcrumbNode([
            { name: "Home", path: "/" },
            { name: "Journal", path: "/journal" },
            { name: entry.title, path: `/journal/${entry.slug}` },
          ]),
          journalNode(entry),
        ]}
      />
    </article>
  );
}
