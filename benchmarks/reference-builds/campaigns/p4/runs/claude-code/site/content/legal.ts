import { legalDocumentSchema, type LegalDocument } from "./schema";

const raw = [
  {
    slug: "privacy",
    title: "Privacy notice",
    effectiveDate: "2026-01-15",
    summary:
      "What Asteria Residences collects when you request a visit, why, how long it is kept, and how to have it deleted.",
    noindex: false,
    body: [
      { kind: "heading", text: "Who is responsible" },
      {
        kind: "paragraph",
        text: "Asteria Ridge Development, Lda., Rua da Pedreira 12, 2780-158 Oeiras, Portugal, is the controller for personal data collected through this website. Data protection enquiries: privacy@asteria-residences.example.",
      },
      { kind: "heading", text: "What we collect and why" },
      {
        kind: "dataTable",
        caption: "Data collected through the visit request form",
        columns: ["Data", "Purpose", "Lawful basis", "Retention"],
        rows: [
          ["Name, email, telephone", "To answer your visit request", "Consent, given on the form", "24 months from last contact"],
          ["Residence of interest, timeframe, purchase context", "To prepare a useful conversation", "Consent", "24 months from last contact"],
          ["Message text", "To answer what you asked", "Consent", "24 months from last contact"],
          ["Preferred dates", "To schedule a visit", "Consent", "12 months"],
          ["IP address, in hashed form", "Rate limiting and abuse prevention only", "Legitimate interest", "30 days"],
          ["Submission timestamp and reference code", "Record of the request and audit", "Legitimate interest", "24 months"],
        ],
      },
      { kind: "heading", text: "What we do not do" },
      {
        kind: "list",
        items: [
          "We do not use third-party advertising or analytics scripts. There is no tracking pixel on this site.",
          "We do not set any cookie that is not strictly necessary. The site sets no cookie at all unless you submit the form, and then only a session identifier used to deduplicate funnel events.",
          "We do not sell, rent or share your details with anyone outside the named recipients below.",
          "We do not add you to a marketing list because you requested a visit. Marketing contact requires a separate, explicit opt-in that this form does not ask for.",
        ],
      },
      { kind: "heading", text: "Who else sees it" },
      {
        kind: "paragraph",
        text: "Your request is passed to the appointed sales broker for the development in order to arrange the visit. Hosting is within the European Economic Area. No transfer outside the EEA takes place.",
      },
      { kind: "heading", text: "Your rights" },
      {
        kind: "paragraph",
        text: "You may request access, rectification, erasure, restriction, portability, or withdraw consent at any time by writing to privacy@asteria-residences.example, quoting the reference code shown when you submitted the form. We respond within 30 days. You may also complain to the Comissão Nacional de Proteção de Dados.",
      },
    ],
  },
  {
    slug: "terms",
    title: "Terms and sales information",
    effectiveDate: "2026-01-15",
    summary:
      "The status of the information published on this site, including what is indicative and what is contractual.",
    noindex: false,
    body: [
      { kind: "heading", text: "Status of published information" },
      {
        kind: "paragraph",
        text: "Asteria Residences is a development under construction. Every drawing on this site is derived from the current planning and technical design and is indicative until the corresponding element is built. Areas are stated as gross areas from the approved drawings and carry a contractual tolerance of ±2 per cent at completion.",
      },
      { kind: "heading", text: "Prices and availability" },
      {
        kind: "list",
        items: [
          "Prices are published as bands, not as fixed figures, because the final figure depends on specification choices made at reservation.",
          "The price for a specific residence is fixed in the promissory contract and is not indexed to construction cost.",
          "Availability shown on this site is updated when a reservation is countersigned and may lag a same-day change. The sales office holds the authoritative position.",
          "Nothing on this website constitutes an offer capable of acceptance.",
        ],
      },
      { kind: "heading", text: "Drawings and imagery" },
      {
        kind: "paragraph",
        text: "This site contains no photographs and no computer-generated impressions of completed interiors, because the buildings do not yet exist. All drawings are line drawings generated directly from the published dimensional data for each residence. Where a drawing and a stated dimension disagree, the stated dimension governs.",
      },
      { kind: "heading", text: "Licensing and regulatory" },
      {
        kind: "paragraph",
        text: "Construction licence 2025/AP/0114, Câmara Municipal de Oeiras. Energy certificates are issued per unit on completion; the ratings published here are the design-stage assessments. Asteria Ridge Development, Lda. is registered under NIPC 517 000 000.",
      },
    ],
  },
  {
    slug: "contact",
    title: "Contact and sales office",
    effectiveDate: "2026-01-15",
    summary:
      "How to reach Asteria Residences directly, including sales office address, opening hours and telephone.",
    noindex: false,
    body: [
      { kind: "heading", text: "Sales office" },
      {
        kind: "paragraph",
        text: "Rua da Pedreira 12, 2780-158 Oeiras, Portugal. Open Monday to Saturday, 10:00–18:00. Visits to the ridge itself leave from the sales office and take approximately ninety minutes; sturdy shoes are genuinely necessary.",
      },
      { kind: "heading", text: "Direct contact" },
      {
        kind: "list",
        items: [
          "Telephone: +351 210 000 120",
          "Visit requests and general enquiries: visits@asteria-residences.example",
          "Data protection: privacy@asteria-residences.example",
          "Press and media: press@asteria-residences.example",
        ],
      },
      { kind: "heading", text: "What happens after you write" },
      {
        kind: "paragraph",
        text: "A visit request submitted through this site is recorded immediately with a reference code beginning AST-. Quote that code in any follow-up. A member of the sales team answers within one working day; if you have not heard from us within that time, telephone the office rather than resubmitting the form.",
      },
    ],
  },
] satisfies unknown[];

export const legalDocuments: LegalDocument[] = raw.map((entry) => legalDocumentSchema.parse(entry));
