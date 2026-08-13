import { residences } from "@/content/residences";
import { districts } from "@/content/districts";
import { journalEntries } from "@/content/journal";
import { legalDocuments } from "@/content/legal";
import { settings } from "@/content/settings";
import type {
  Block,
  District,
  JournalEntry,
  LegalDocument,
  Residence,
  SiteSettings,
} from "@/content/schema";

/**
 * The CMS boundary (planning/03-content-model.md).
 *
 * This module is the ONLY place allowed to import from `content/`. Swapping the
 * repository-authored source for a headless CMS is a change to this file alone;
 * every exported function below is the stable contract components rely on.
 */

export type { Block, District, JournalEntry, LegalDocument, Residence, SiteSettings };

export function getSettings(): SiteSettings {
  return settings;
}

export function getResidences(): Residence[] {
  return [...residences].sort((a, b) => a.index - b.index);
}

export function getResidence(slug: string): Residence | undefined {
  return residences.find((r) => r.slug === slug);
}

export function getResidenceById(id: string): Residence | undefined {
  return residences.find((r) => r.id === id);
}

export function getAvailableResidences(): Residence[] {
  return getResidences().filter((r) => r.status === "available");
}

export function getDistricts(): District[] {
  return districts;
}

export function getDistrict(slug: string): District | undefined {
  return districts.find((d) => d.slug === slug);
}

/** Published entries only. Draft entries never leave this module. */
export function getJournalEntries(): JournalEntry[] {
  return journalEntries
    .filter((entry) => entry.status === "published")
    .sort((a, b) => (a.publishedAt < b.publishedAt ? 1 : -1));
}

export function getJournalEntry(slug: string): JournalEntry | undefined {
  return getJournalEntries().find((entry) => entry.slug === slug);
}

export function getLegalDocuments(): LegalDocument[] {
  return legalDocuments;
}

export function getLegalDocument(slug: string): LegalDocument | undefined {
  return legalDocuments.find((doc) => doc.slug === slug);
}

/** Derived facts used by the home page and structured data. */
export function getDevelopmentFacts() {
  const all = getResidences();
  const available = all.filter((r) => r.status === "available");
  const interior = all.map((r) => r.interiorAreaSqm);
  const prices = all.map((r) => r.priceBandEur.from);
  return {
    total: all.length,
    available: available.length,
    reserved: all.filter((r) => r.status === "reserved").length,
    sold: all.filter((r) => r.status === "sold").length,
    minInteriorSqm: Math.min(...interior),
    maxInteriorSqm: Math.max(...interior),
    minPriceEur: Math.min(...prices),
    maxPriceEur: Math.max(...all.map((r) => r.priceBandEur.to)),
    minElevationM: Math.min(...all.map((r) => r.elevationM)),
    maxElevationM: Math.max(...all.map((r) => r.elevationM)),
    firstDelivery: all.map((r) => r.deliveryQuarter).sort()[0],
    lastDelivery: all.map((r) => r.deliveryQuarter).sort().at(-1)!,
  };
}

export function residenceTypeLabel(type: Residence["type"]): string {
  return { ridge: "Ridge house", terrace: "Terrace house", courtyard: "Courtyard house" }[type];
}

export function statusLabel(status: Residence["status"]): string {
  return { available: "Available", reserved: "Reserved", sold: "Sold" }[status];
}

export function planTotalSqm(residence: Residence): number {
  return residence.plan.reduce(
    (total, level) => total + level.rooms.reduce((sum, room) => sum + room.areaSqm, 0),
    0,
  );
}
