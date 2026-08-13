import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getLegalDocument, getLegalDocuments } from "@/lib/content";
import { formatDate } from "@/lib/format";
import { Blocks } from "@/components/Blocks";
import { pageMetadata } from "@/lib/seo";
import { JsonLd, breadcrumbNode } from "@/lib/jsonld";
import styles from "./legal.module.css";

export function generateStaticParams() {
  return getLegalDocuments().map((doc) => ({ legal: doc.slug }));
}

export const dynamicParams = false;

export async function generateMetadata({
  params,
}: {
  params: Promise<{ legal: string }>;
}): Promise<Metadata> {
  const { legal } = await params;
  const doc = getLegalDocument(legal);
  if (!doc) return pageMetadata({ title: "Not found", description: "", path: `/${legal}`, noindex: true });
  return pageMetadata({
    title: doc.title,
    description: doc.summary,
    path: `/${doc.slug}`,
    noindex: doc.noindex,
  });
}

export default async function LegalPage({ params }: { params: Promise<{ legal: string }> }) {
  const { legal } = await params;
  const doc = getLegalDocument(legal);
  if (!doc) notFound();

  return (
    <article className={`page ${styles.wrap}`}>
      <div className="section-head">
        <span className="section-index">—</span>
        <span className="section-label">
          Effective {formatDate(doc.effectiveDate)}
        </span>
      </div>
      <h1 className={styles.title}>{doc.title}</h1>
      <p className="lede" style={{ marginTop: "var(--space-s)", marginBottom: "var(--space-xl)" }}>
        {doc.summary}
      </p>
      <Blocks blocks={doc.body} />

      <JsonLd
        nodes={[
          breadcrumbNode([
            { name: "Home", path: "/" },
            { name: doc.title, path: `/${doc.slug}` },
          ]),
        ]}
      />
    </article>
  );
}
