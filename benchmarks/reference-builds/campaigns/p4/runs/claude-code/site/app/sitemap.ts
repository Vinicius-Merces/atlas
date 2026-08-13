import type { MetadataRoute } from "next";
import { getResidences, getJournalEntries, getLegalDocuments } from "@/lib/content";
import { absolute } from "@/lib/seo";

/**
 * Only indexable, published routes appear. Draft journal entries are excluded
 * because getJournalEntries() never returns them, and /enquire/received is
 * excluded because it is a per-submission confirmation surface.
 */
export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();

  const staticRoutes: MetadataRoute.Sitemap = [
    { url: absolute("/"), lastModified: now, changeFrequency: "monthly", priority: 1 },
    { url: absolute("/residences"), lastModified: now, changeFrequency: "weekly", priority: 0.9 },
    { url: absolute("/location"), lastModified: now, changeFrequency: "monthly", priority: 0.7 },
    { url: absolute("/journal"), lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    { url: absolute("/enquire"), lastModified: now, changeFrequency: "yearly", priority: 0.8 },
  ];

  const residences: MetadataRoute.Sitemap = getResidences().map((r) => ({
    url: absolute(`/residences/${r.slug}`),
    lastModified: now,
    changeFrequency: "weekly",
    priority: 0.8,
  }));

  const journal: MetadataRoute.Sitemap = getJournalEntries().map((entry) => ({
    url: absolute(`/journal/${entry.slug}`),
    lastModified: new Date(`${entry.updatedAt ?? entry.publishedAt}T00:00:00Z`),
    changeFrequency: "yearly",
    priority: 0.5,
  }));

  const legal: MetadataRoute.Sitemap = getLegalDocuments()
    .filter((doc) => !doc.noindex)
    .map((doc) => ({
      url: absolute(`/${doc.slug}`),
      lastModified: new Date(`${doc.effectiveDate}T00:00:00Z`),
      changeFrequency: "yearly",
      priority: 0.3,
    }));

  return [...staticRoutes, ...residences, ...journal, ...legal];
}
