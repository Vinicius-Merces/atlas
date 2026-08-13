import { z } from "zod";

/**
 * Content schemas. These are the CMS-boundary contract described in
 * planning/03-content-model.md: every content module is parsed through these
 * schemas, and no UI component may read raw content.
 */

export const orientationSchema = z.enum(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]);
export type Orientation = z.infer<typeof orientationSchema>;

export const residenceStatusSchema = z.enum(["available", "reserved", "sold"]);
export type ResidenceStatus = z.infer<typeof residenceStatusSchema>;

export const residenceTypeSchema = z.enum(["ridge", "terrace", "courtyard"]);
export type ResidenceType = z.infer<typeof residenceTypeSchema>;

export const roomSchema = z.object({
  name: z.string().min(1),
  areaSqm: z.number().positive(),
});

export const levelPlanSchema = z.object({
  level: z.string().min(1),
  levelIndex: z.number().int(),
  rooms: z.array(roomSchema).min(1),
});

export const materialSchema = z.object({
  name: z.string().min(1),
  hex: z.string().regex(/^#[0-9a-f]{6}$/),
  application: z.string().min(1),
});

export const featureGroupSchema = z.object({
  group: z.string().min(1),
  items: z.array(z.string().min(1)).min(1),
});

export const residenceSchema = z.object({
  id: z.string().regex(/^A(0[1-9]|1[0-2])$/),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  index: z.number().int().min(1).max(12),
  name: z.string().min(1),
  type: residenceTypeSchema,
  status: residenceStatusSchema,
  interiorAreaSqm: z.number().positive(),
  outdoorAreaSqm: z.number().positive(),
  plotAreaSqm: z.number().positive(),
  bedrooms: z.number().int().positive(),
  bathrooms: z.number().int().positive(),
  levels: z.number().int().positive(),
  parking: z.number().int().min(0),
  orientation: orientationSchema,
  aspect: z.string().min(1),
  elevationM: z.number(),
  plotX: z.number().min(0).max(1),
  plotY: z.number().min(0).max(1),
  priceBandEur: z.object({ from: z.number().positive(), to: z.number().positive() }),
  deliveryQuarter: z.string().regex(/^20\d{2}-Q[1-4]$/),
  energyRating: z.string().min(1),
  summary: z.string().min(20).max(220),
  narrative: z.array(z.string().min(40)).min(2),
  features: z.array(featureGroupSchema).min(2),
  materials: z.array(materialSchema).min(2),
  plan: z.array(levelPlanSchema).min(1),
});
export type Residence = z.infer<typeof residenceSchema>;

export const districtSchema = z.object({
  id: z.string().min(1),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  name: z.string().min(1),
  kind: z.string().min(1),
  distanceKm: z.number().nonnegative(),
  travelMinutes: z.number().int().positive(),
  mode: z.string().min(1),
  summary: z.string().min(20).max(240),
  narrative: z.array(z.string().min(40)).min(1),
  highlights: z.array(z.string().min(3)).min(2),
});
export type District = z.infer<typeof districtSchema>;

const paragraphBlock = z.object({ kind: z.literal("paragraph"), text: z.string().min(1) });
const headingBlock = z.object({ kind: z.literal("heading"), text: z.string().min(1) });
const listBlock = z.object({ kind: z.literal("list"), items: z.array(z.string().min(1)).min(1) });
const pullquoteBlock = z.object({
  kind: z.literal("pullquote"),
  text: z.string().min(1),
  attribution: z.string().optional(),
});
const dataTableBlock = z.object({
  kind: z.literal("dataTable"),
  caption: z.string().min(1),
  columns: z.array(z.string().min(1)).min(2),
  rows: z.array(z.array(z.string()).min(2)).min(1),
});

export const blockSchema = z.discriminatedUnion("kind", [
  paragraphBlock,
  headingBlock,
  listBlock,
  pullquoteBlock,
  dataTableBlock,
]);
export type Block = z.infer<typeof blockSchema>;

export const journalEntrySchema = z.object({
  slug: z.string().regex(/^[a-z0-9-]+$/),
  status: z.enum(["draft", "published"]),
  kicker: z.string().min(1),
  title: z.string().min(1),
  deck: z.string().min(20).max(260),
  publishedAt: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  updatedAt: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  author: z.object({ name: z.string().min(1), role: z.string().min(1) }),
  readingMinutes: z.number().int().positive(),
  tags: z.array(z.string().min(1)).min(1),
  body: z.array(blockSchema).min(3),
  relatedResidences: z.array(z.string()).default([]),
  relatedDistricts: z.array(z.string()).default([]),
});
export type JournalEntry = z.infer<typeof journalEntrySchema>;

export const legalDocumentSchema = z.object({
  slug: z.string().regex(/^[a-z0-9-]+$/),
  title: z.string().min(1),
  effectiveDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  summary: z.string().min(20).max(240),
  noindex: z.boolean().default(false),
  body: z.array(blockSchema).min(2),
});
export type LegalDocument = z.infer<typeof legalDocumentSchema>;

export const siteSettingsSchema = z.object({
  organisation: z.string().min(1),
  legalName: z.string().min(1),
  tagline: z.string().min(1),
  locale: z.string().min(2),
  origin: z.string().url(),
  developmentLocality: z.string().min(1),
  developmentRegion: z.string().min(1),
  developmentCountry: z.string().min(1),
  geo: z.object({ latitude: z.number(), longitude: z.number() }),
  salesOffice: z.object({
    street: z.string().min(1),
    locality: z.string().min(1),
    postalCode: z.string().min(1),
    country: z.string().min(1),
  }),
  telephone: z.string().min(1),
  email: z.string().email(),
  openingHours: z.string().min(1),
  responsePromiseHours: z.number().int().positive(),
  totalResidences: z.number().int().positive(),
  architect: z.string().min(1),
  developer: z.string().min(1),
  completion: z.string().min(1),
});
export type SiteSettings = z.infer<typeof siteSettingsSchema>;
