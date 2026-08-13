import { districtSchema, type District } from "./schema";

const raw = [
  {
    id: "D1",
    slug: "the-ridge",
    name: "The ridge itself",
    kind: "Immediate setting",
    distanceKm: 0,
    travelMinutes: 1,
    mode: "on foot",
    summary:
      "A 1.4 km limestone escarpment at 148–178 m, carrying the twelve plots, a retained vineyard and an orchard.",
    narrative: [
      "Alto da Pedra is a single limestone escarpment running roughly east–west, with a plateau at its eastern end and a steep south-west face falling to the valley. The development occupies the upper 1.4 km of it and builds on eleven per cent of the site area; the rest is retained as vineyard, orchard, and native ridge planting.",
      "Two paths cross the site. The plateau path runs east–west along the top and reaches the village in eleven minutes on foot. The vineyard walk drops south-west from Ridge House 03 and joins the valley road below. Both existed before the development and both stay public.",
    ],
    highlights: [
      "Eleven per cent site coverage; 89% retained landscape",
      "Two pre-existing public paths preserved",
      "Retained vineyard of 2.1 hectares under a 30-year management agreement",
      "No gates on the ridge itself; parking and services are below the building line",
    ],
  },
  {
    id: "D2",
    slug: "the-village",
    name: "Pedra Alta village",
    kind: "Everyday",
    distanceKm: 1.2,
    travelMinutes: 11,
    mode: "on foot by the plateau path",
    summary:
      "The nearest settlement: a square, a weekly market, a pharmacy, two restaurants, a bakery and the primary school.",
    narrative: [
      "Pedra Alta is small enough to walk across in five minutes and old enough to have a market that predates the road. The Saturday market runs from 08:00 to 13:00 in the square. There is a pharmacy, a health post open on weekday mornings, a bakery, a hardware shop, two restaurants and a primary school with 140 places.",
      "The village is the reason the plateau path matters. From Courtyard House 12 at the eastern end it is eleven minutes on foot, downhill in the evening and uphill on the way home, which is the correct order.",
    ],
    highlights: [
      "Saturday market, 08:00–13:00, in the village square",
      "Primary school, 140 places, 1.4 km",
      "Pharmacy and weekday health post",
      "Two restaurants and a bakery on the square",
    ],
  },
  {
    id: "D3",
    slug: "oeiras-and-the-coast",
    name: "Oeiras and the coast",
    kind: "Services and sea",
    distanceKm: 9.4,
    travelMinutes: 16,
    mode: "by car",
    summary:
      "The nearest town centre and the Atlantic: supermarkets, international schools, the marina, and the coast road west.",
    narrative: [
      "Oeiras carries everything the village does not: full supermarkets, the international schools most buyers ask about, medical specialists, the marina, and the train that runs along the river into central Lisbon every twenty minutes.",
      "The coast road west from Oeiras reaches Cascais in twenty-five minutes and Guincho in forty. The nearest swimming beach to the ridge is Santo Amaro, sixteen minutes door to sand.",
    ],
    highlights: [
      "Two international schools within 12 km",
      "Marina and coastal promenade",
      "Rail to Lisbon Cais do Sodré, every 20 minutes",
      "Nearest beach 16 minutes by car",
    ],
  },
  {
    id: "D4",
    slug: "lisbon",
    name: "Central Lisbon",
    kind: "The city",
    distanceKm: 21.8,
    travelMinutes: 28,
    mode: "by car outside peak hours",
    summary:
      "Twenty-two kilometres east: the reason the ridge is commutable and the reason it is quiet.",
    narrative: [
      "The A5 entry is 4.8 km from the ridge and central Lisbon is twenty-eight minutes from there outside peak hours, forty-five in the worst of the morning. Humberto Delgado airport is thirty-four minutes by the same road.",
      "The distance is the point. The ridge is close enough that a buyer keeps the city in their week and far enough that the loudest thing on the plateau in the evening is the wind in the carob trees.",
    ],
    highlights: [
      "A5 motorway entry 4.8 km",
      "Central Lisbon 28 minutes off-peak",
      "Airport 34 minutes",
      "No flight path over the ridge",
    ],
  },
] satisfies unknown[];

export const districts: District[] = raw.map((entry) => districtSchema.parse(entry));
