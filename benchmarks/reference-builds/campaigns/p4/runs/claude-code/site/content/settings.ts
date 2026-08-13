import { siteSettingsSchema, type SiteSettings } from "./schema";

const raw = {
  organisation: "Asteria Residences",
  legalName: "Asteria Ridge Development, Lda.",
  tagline: "Twelve houses on the Alto da Pedra ridge",
  locale: "en-GB",
  origin: process.env.ASTERIA_ORIGIN ?? "https://asteria-residences.example",
  developmentLocality: "Alto da Pedra",
  developmentRegion: "Lisbon District",
  developmentCountry: "Portugal",
  geo: { latitude: 38.7412, longitude: -9.2986 },
  salesOffice: {
    street: "Rua da Pedreira 12",
    locality: "Oeiras",
    postalCode: "2780-158",
    country: "Portugal",
  },
  telephone: "+351 210 000 120",
  email: "visits@asteria-residences.example",
  openingHours: "Monday to Saturday, 10:00–18:00",
  responsePromiseHours: 24,
  totalResidences: 12,
  architect: "Vidal Ferrão Arquitectos",
  developer: "Asteria Ridge Development, Lda.",
  completion: "Phased delivery, 2027 Q2 to 2028 Q1",
} satisfies Record<string, unknown>;

export const settings: SiteSettings = siteSettingsSchema.parse(raw);
