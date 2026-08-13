const eur = new Intl.NumberFormat("en-GB", {
  style: "currency",
  currency: "EUR",
  maximumFractionDigits: 0,
});

const num = new Intl.NumberFormat("en-GB");

export function formatPriceBand(band: { from: number; to: number }): string {
  return `${compactEur(band.from)}–${compactEur(band.to)}`;
}

export function compactEur(value: number): string {
  if (value >= 1_000_000) {
    const millions = value / 1_000_000;
    const rendered = millions % 1 === 0 ? millions.toFixed(0) : millions.toFixed(2);
    return `€${rendered}M`;
  }
  return eur.format(value);
}

export function formatEur(value: number): string {
  return eur.format(value);
}

export function formatSqm(value: number): string {
  return `${num.format(value)} m²`;
}

export function formatQuarter(quarter: string): string {
  const [year, q] = quarter.split("-");
  return `${q} ${year}`;
}

export function formatDate(iso: string): string {
  return new Date(`${iso}T00:00:00Z`).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  });
}

export const orientationDegrees: Record<string, number> = {
  N: 0,
  NE: 45,
  E: 90,
  SE: 135,
  S: 180,
  SW: 225,
  W: 270,
  NW: 315,
};

export const orientationName: Record<string, string> = {
  N: "north",
  NE: "north-east",
  E: "east",
  SE: "south-east",
  S: "south",
  SW: "south-west",
  W: "west",
  NW: "north-west",
};
