import { journalEntrySchema, type JournalEntry } from "./schema";

const raw = [
  {
    slug: "why-twelve-houses",
    status: "published",
    kicker: "Development",
    title: "Why twelve houses and not forty",
    deck: "The ridge could carry three times the density under the local plan. The arithmetic of why it does not is the whole argument of the project.",
    publishedAt: "2026-02-11",
    updatedAt: "2026-05-04",
    author: { name: "Inês Vidal Ferrão", role: "Principal architect" },
    readingMinutes: 6,
    tags: ["development", "planning", "landscape"],
    body: [
      {
        kind: "paragraph",
        text: "The Alto da Pedra plan permits 38 dwellings on the ridge. We drew 12. The decision was not sentimental: at 38 units the access lane has to be widened to two lanes with a footway, which means cutting a two-metre bench along the escarpment for its full length, which means losing the vineyard terraces and the vineyard walk with them.",
      },
      { kind: "heading", text: "What the density costs" },
      {
        kind: "paragraph",
        text: "Once the bench is cut, the retained landscape drops from 89 per cent of the site to 54 per cent, the two public paths become a single road-adjacent footway, and every plot loses its direct relationship to the ground. The houses would still be good houses. The site would no longer be the reason to buy one.",
      },
      {
        kind: "dataTable",
        caption: "Two densities on the same site",
        columns: ["Measure", "12 houses (built)", "38 houses (permitted)"],
        rows: [
          ["Site coverage", "11%", "34%"],
          ["Retained landscape", "89%", "54%"],
          ["Access lane width", "3.5 m single with passing bays", "6.0 m with footway"],
          ["Vineyard terraces retained", "2.1 ha", "0.4 ha"],
          ["Public paths retained", "2", "1"],
          ["Excavation volume", "8,400 m³", "31,200 m³"],
        ],
      },
      {
        kind: "paragraph",
        text: "The excavation number is the one that decided it. Cutting 31,200 cubic metres out of a limestone escarpment is a two-year operation with a haulage route through the village, and it produces a ridge that is visibly a construction site from the valley for the whole of that time. At 8,400 cubic metres the cut is contained within the three courtyard plots on the plateau and the material is reused on site for the terrace retaining.",
      },
      {
        kind: "pullquote",
        text: "You cannot sell a view of a landscape you removed in order to build the houses that look at it.",
        attribution: "Inês Vidal Ferrão",
      },
      {
        kind: "paragraph",
        text: "The consequence for a buyer is straightforward and worth stating plainly: these houses cost more per square metre than the same houses would on a denser scheme, because each one carries a larger share of a site that has deliberately been left alone.",
      },
    ],
    relatedResidences: ["A03", "A12"],
    relatedDistricts: ["D1"],
  },
  {
    slug: "reading-the-section",
    status: "published",
    kicker: "Architecture",
    title: "How to read the ridge section",
    deck: "Every drawing on this site is pegged to one line: the measured section through the escarpment. Here is how to use it.",
    publishedAt: "2026-03-02",
    author: { name: "Inês Vidal Ferrão", role: "Principal architect" },
    readingMinutes: 5,
    tags: ["architecture", "drawings"],
    body: [
      {
        kind: "paragraph",
        text: "The line running under the twelve markers on the home page is not decoration. It is the surveyed profile of the ridge from the western access at 148 metres to the eastern rock shelf at 178 metres, and each marker sits at the actual elevation of that plot.",
      },
      { kind: "heading", text: "What the section tells you that a photograph could not" },
      {
        kind: "list",
        items: [
          "Which houses are cut into the slope and which sit on the plateau: below 160 m the section is steep enough to bury a floor, above it the ground flattens.",
          "Why the ridge houses have two levels and the courtyard houses have one.",
          "Why the terrace houses step in half-levels: the fall across a 19 m deep plot is 3.1 m, which is exactly two half-levels.",
          "Where the wind comes from. Above 170 m the escarpment stops sheltering you, which is why houses 10, 11 and 12 turn inward.",
        ],
      },
      {
        kind: "paragraph",
        text: "It also tells you what you are buying before the building exists. The elevation of your plot, its position relative to its neighbours, and the direction the ground falls are the three facts that a completed house cannot change, and they are all in the section.",
      },
      {
        kind: "pullquote",
        text: "The building is a proposal. The ground is a fact.",
      },
      {
        kind: "paragraph",
        text: "On every residence page the same section reappears with that plot highlighted, alongside a plan and an elevation drawn from the same survey. All three come from the same data as the numbers in the specification table, so if the table says 154 metres the drawing puts the house at 154 metres.",
      },
    ],
    relatedResidences: ["A01", "A05", "A10"],
    relatedDistricts: ["D1"],
  },
  {
    slug: "buying-off-plan-honestly",
    status: "published",
    kicker: "Buying",
    title: "Buying off-plan, honestly",
    deck: "What is fixed, what can still change, what protects your deposit, and the four questions worth asking any off-plan developer including us.",
    publishedAt: "2026-04-18",
    author: { name: "Miguel Andrade", role: "Sales director" },
    readingMinutes: 8,
    tags: ["buying", "process"],
    body: [
      {
        kind: "paragraph",
        text: "Every house on this site is sold before it is built. That is normal for a development of this kind and it is also the part of the process where buyers are least well served, so this entry sets out our terms in the same detail we would give you in the sales office.",
      },
      { kind: "heading", text: "What is fixed at reservation" },
      {
        kind: "list",
        items: [
          "The plot, its boundaries, and its elevation.",
          "The gross interior and exterior areas, with a contractual tolerance of ±2 per cent.",
          "The price. It is fixed in the promissory contract and is not indexed to construction costs.",
          "The external envelope: cladding, openings, roof geometry and orientation.",
          "The delivery quarter, with a contractual long-stop six months beyond it.",
        ],
      },
      { kind: "heading", text: "What can still change" },
      {
        kind: "list",
        items: [
          "Internal non-structural partitions, up to the point of first fix.",
          "Kitchen and bathroom specification, from the published schedule or by substitution at cost.",
          "Floor finishes and joinery timber, from the published palette.",
          "Named suppliers, where a product is discontinued; substitution must be of equal or better specification and is notified in writing.",
        ],
      },
      { kind: "heading", text: "What protects the deposit" },
      {
        kind: "dataTable",
        caption: "Payment structure and protection",
        columns: ["Stage", "Share of price", "Protection"],
        rows: [
          ["Reservation", "1%", "Refundable in full for 21 days"],
          ["Promissory contract", "19%", "Bank guarantee for the full amount paid"],
          ["Structure complete", "20%", "Bank guarantee maintained"],
          ["Envelope complete", "20%", "Bank guarantee maintained"],
          ["Completion (deed)", "40%", "Title transfer"],
        ],
      },
      {
        kind: "paragraph",
        text: "The bank guarantee is the part to check with any developer. Ours is issued per unit by the project's lending bank and covers every euro paid before the deed, which means a failure of the developer returns your money rather than putting you in a creditors' queue. Ask for the guarantee wording before you sign anything, not after.",
      },
      { kind: "heading", text: "Four questions worth asking" },
      {
        kind: "list",
        items: [
          "Is the price indexed to construction cost inflation? (Here: no.)",
          "Who issues the deposit guarantee and does it cover pre-deed payments in full?",
          "What is the contractual long-stop date and what happens if it passes?",
          "What is the defects liability period and who holds it after the developer dissolves?",
        ],
      },
      {
        kind: "paragraph",
        text: "Our answers are, in order: no; the project's lending bank, in full; the published delivery quarter plus six months, after which you may rescind and recover with interest; five years structural and two years non-structural, held by the developer entity which is contracted to remain in existence for the duration.",
      },
    ],
    relatedResidences: ["A02", "A08"],
    relatedDistricts: [],
  },
  {
    slug: "the-energy-strategy",
    status: "published",
    kicker: "Systems",
    title: "Where the A+ rating actually comes from",
    deck: "Eleven of the twelve houses are rated A+. The rating is mostly fabric, not equipment, and the difference matters for what you pay in year ten.",
    publishedAt: "2026-05-27",
    author: { name: "Rui Sacadura", role: "Building services engineer" },
    readingMinutes: 7,
    tags: ["systems", "energy"],
    body: [
      {
        kind: "paragraph",
        text: "It is easy to buy an energy rating with equipment: put a large enough heat pump and a large enough photovoltaic array on a mediocre building and the certificate improves. It is also the version that degrades, because equipment has a fifteen-year life and fabric has a sixty-year one.",
      },
      { kind: "heading", text: "The fabric first" },
      {
        kind: "dataTable",
        caption: "Envelope performance against the Portuguese regulatory minimum",
        columns: ["Element", "Regulatory maximum", "Asteria"],
        rows: [
          ["External wall U-value", "0.40 W/m²K", "0.16 W/m²K"],
          ["Roof U-value", "0.35 W/m²K", "0.13 W/m²K"],
          ["Glazing U-value", "2.20 W/m²K", "0.90 W/m²K"],
          ["Air permeability", "not regulated", "1.4 m³/h·m² at 50 Pa"],
          ["Thermal bridging at slab edge", "common", "eliminated by continuous external insulation"],
        ],
      },
      {
        kind: "paragraph",
        text: "The air permeability figure is the one worth dwelling on. At 1.4 the house holds its temperature overnight without running anything, which is why the heat pumps here are sized at roughly half what a comparable villa of this area would need.",
      },
      { kind: "heading", text: "Then the equipment" },
      {
        kind: "list",
        items: [
          "Air-to-water heat pumps on the ridge and terrace houses; a shared ground-source array for the three courtyard houses, where the plateau geology allows 90 m bores.",
          "Mechanical ventilation with 85–88 per cent heat recovery, with summer bypass.",
          "Photovoltaic arrays sized to the roof, 4.8 to 12.6 kWp, with batteries on the larger houses.",
          "Underfloor circuits used for cooling as well as heating, at 18 °C flow with dew-point control.",
        ],
      },
      {
        kind: "paragraph",
        text: "House 08 is rated A rather than A+ and we have not hidden it. Its roof takes 4.8 kWp because it is the narrowest plan in the terrace row and it is overshadowed by the rock face at the north-east corner in winter. The fabric is identical to its neighbours; the array is smaller. That is the honest reason, and it is reflected in the price.",
      },
      {
        kind: "pullquote",
        text: "A certificate describes a building on the day it is tested. Fabric describes it in year thirty.",
        attribution: "Rui Sacadura",
      },
    ],
    relatedResidences: ["A08", "A10", "A11"],
    relatedDistricts: [],
  },
  {
    slug: "the-vineyard-agreement",
    status: "published",
    kicker: "Landscape",
    title: "Who farms the vineyard after we leave",
    deck: "Two point one hectares of retained terraces need someone to work them for longer than a developer exists. The mechanism is a 30-year management agreement, and here is how it is funded.",
    publishedAt: "2026-06-30",
    author: { name: "Inês Vidal Ferrão", role: "Principal architect" },
    readingMinutes: 5,
    tags: ["landscape", "governance"],
    body: [
      {
        kind: "paragraph",
        text: "Retaining a vineyard in a marketing drawing is easy. Keeping it farmed for thirty years after the developer has been dissolved is a governance problem, and it is the kind of promise that quietly fails on most schemes of this type.",
      },
      { kind: "heading", text: "The mechanism" },
      {
        kind: "list",
        items: [
          "The 2.1 ha of terraces are held by the owners' association, not by individual plots, so no single owner can withdraw them.",
          "A 30-year management agreement with the Quinta da Pedra cooperative covers pruning, harvest and terrace-wall maintenance.",
          "The agreement is funded by a fixed annual charge of €1,850 per house, index-linked to Portuguese CPI, disclosed in the promissory contract.",
          "The cooperative takes the fruit; the association takes no revenue and carries no commercial risk.",
        ],
      },
      {
        kind: "paragraph",
        text: "The charge is disclosed at reservation because it is a real running cost and a buyer comparing this development against another should be comparing the total. The equivalent charge on a scheme with a communal pool and gated security is typically three to four times higher; we have neither.",
      },
      {
        kind: "paragraph",
        text: "The terrace walls are the expensive part. There are 1,340 linear metres of dry-stone terracing on the south-west face, some of it eighteenth century, and it needs a mason for roughly twenty days a year. That is the single largest line in the annual charge and it is the reason the charge is fixed rather than assessed year by year.",
      },
    ],
    relatedResidences: ["A03"],
    relatedDistricts: ["D1", "D2"],
  },
  {
    slug: "material-samples-autumn",
    status: "draft",
    kicker: "Materials",
    title: "Autumn material samples (draft, not published)",
    deck: "An unpublished entry retained in the content set so the draft/published editorial state has a real instance to exercise rather than a hypothetical one.",
    publishedAt: "2026-09-01",
    author: { name: "Inês Vidal Ferrão", role: "Principal architect" },
    readingMinutes: 3,
    tags: ["materials"],
    body: [
      { kind: "paragraph", text: "This entry is in draft state and must never appear in the journal index, the sitemap, or a direct URL fetch in production." },
      { kind: "paragraph", text: "It exists so that the draft-exclusion behaviour described in the content model is verified against real content rather than asserted." },
      { kind: "paragraph", text: "If this text is ever visible on the deployed site, the editorial state model has failed and the defect is in lib/content.ts." },
    ],
    relatedResidences: [],
    relatedDistricts: [],
  },
] satisfies unknown[];

export const journalEntries: JournalEntry[] = raw.map((entry) => journalEntrySchema.parse(entry));
