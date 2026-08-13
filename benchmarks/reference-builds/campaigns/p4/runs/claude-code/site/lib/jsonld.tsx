import { getSettings, type District, type JournalEntry, type Residence } from "./content";
import { absolute } from "./seo";

/**
 * Structured data. Every node below is derived from authoritative content
 * fields, so the markup cannot make a claim the visible page does not make
 * (capability: structured-data-validation).
 */

export function organisationNode() {
  const s = getSettings();
  return {
    "@type": "RealEstateAgent",
    "@id": `${absolute("/")}#organisation`,
    name: s.organisation,
    legalName: s.legalName,
    url: absolute("/"),
    telephone: s.telephone,
    email: s.email,
    address: {
      "@type": "PostalAddress",
      streetAddress: s.salesOffice.street,
      addressLocality: s.salesOffice.locality,
      postalCode: s.salesOffice.postalCode,
      addressCountry: s.salesOffice.country,
    },
    areaServed: `${s.developmentLocality}, ${s.developmentRegion}, ${s.developmentCountry}`,
    openingHours: "Mo-Sa 10:00-18:00",
  };
}

export function websiteNode() {
  const s = getSettings();
  return {
    "@type": "WebSite",
    "@id": `${absolute("/")}#website`,
    name: s.organisation,
    url: absolute("/"),
    inLanguage: s.locale,
    publisher: { "@id": `${absolute("/")}#organisation` },
  };
}

export function developmentNode() {
  const s = getSettings();
  return {
    "@type": "Place",
    "@id": `${absolute("/")}#development`,
    name: `${s.organisation}, ${s.developmentLocality}`,
    description: s.tagline,
    geo: {
      "@type": "GeoCoordinates",
      latitude: s.geo.latitude,
      longitude: s.geo.longitude,
    },
    address: {
      "@type": "PostalAddress",
      addressLocality: s.developmentLocality,
      addressRegion: s.developmentRegion,
      addressCountry: s.developmentCountry,
    },
  };
}

/**
 * A residence is only marked with an `offers` node when it is actually
 * available. Reserved and sold units publish the residence without an offer,
 * because advertising an offer for a unit that cannot be bought would be
 * structured data that contradicts the page.
 */
export function residenceNode(residence: Residence) {
  const s = getSettings();
  const url = absolute(`/residences/${residence.slug}`);
  const base: Record<string, unknown> = {
    "@type": "SingleFamilyResidence",
    "@id": `${url}#residence`,
    name: residence.name,
    url,
    description: residence.summary,
    numberOfRooms: residence.bedrooms,
    numberOfBedrooms: residence.bedrooms,
    numberOfBathroomsTotal: residence.bathrooms,
    numberOfFullBathrooms: residence.bathrooms,
    floorSize: {
      "@type": "QuantitativeValue",
      value: residence.interiorAreaSqm,
      unitCode: "MTK",
    },
    lotSize: {
      "@type": "QuantitativeValue",
      value: residence.plotAreaSqm,
      unitCode: "MTK",
    },
    address: {
      "@type": "PostalAddress",
      addressLocality: s.developmentLocality,
      addressRegion: s.developmentRegion,
      addressCountry: s.developmentCountry,
    },
    containedInPlace: { "@id": `${absolute("/")}#development` },
  };

  if (residence.status === "available") {
    base.offers = {
      "@type": "Offer",
      url,
      priceCurrency: "EUR",
      priceSpecification: {
        "@type": "PriceSpecification",
        minPrice: residence.priceBandEur.from,
        maxPrice: residence.priceBandEur.to,
        priceCurrency: "EUR",
        valueAddedTaxIncluded: false,
      },
      availability: "https://schema.org/PreOrder",
      seller: { "@id": `${absolute("/")}#organisation` },
    };
  }

  return base;
}

export function journalNode(entry: JournalEntry) {
  const url = absolute(`/journal/${entry.slug}`);
  return {
    "@type": "Article",
    "@id": `${url}#article`,
    headline: entry.title,
    description: entry.deck,
    url,
    datePublished: entry.publishedAt,
    ...(entry.updatedAt ? { dateModified: entry.updatedAt } : {}),
    author: { "@type": "Person", name: entry.author.name, jobTitle: entry.author.role },
    publisher: { "@id": `${absolute("/")}#organisation` },
    inLanguage: getSettings().locale,
    isPartOf: { "@id": `${absolute("/")}#website` },
    wordCount: entry.body.reduce((count, block) => {
      if (block.kind === "paragraph" || block.kind === "heading") return count + block.text.split(/\s+/).length;
      if (block.kind === "list") return count + block.items.join(" ").split(/\s+/).length;
      if (block.kind === "pullquote") return count + block.text.split(/\s+/).length;
      return count;
    }, 0),
  };
}

export function districtNode(district: District) {
  return {
    "@type": "Place",
    "@id": `${absolute("/location")}#${district.slug}`,
    name: district.name,
    description: district.summary,
  };
}

export function breadcrumbNode(trail: { name: string; path: string }[]) {
  return {
    "@type": "BreadcrumbList",
    itemListElement: trail.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: absolute(item.path),
    })),
  };
}

export function faqNode(items: { question: string; answer: string }[]) {
  return {
    "@type": "FAQPage",
    "@id": `${absolute("/enquire")}#faq`,
    mainEntity: items.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: { "@type": "Answer", text: item.answer },
    })),
  };
}

export function graph(nodes: unknown[]) {
  return { "@context": "https://schema.org", "@graph": nodes };
}

export function JsonLd({ nodes }: { nodes: unknown[] }) {
  return (
    <script
      type="application/ld+json"
      // Content is derived from typed, schema-validated content records.
      dangerouslySetInnerHTML={{ __html: JSON.stringify(graph(nodes)) }}
    />
  );
}
