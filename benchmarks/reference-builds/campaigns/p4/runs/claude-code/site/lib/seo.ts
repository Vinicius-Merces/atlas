import type { Metadata } from "next";
import { getSettings } from "./content";

export function origin(): string {
  return getSettings().origin.replace(/\/$/, "");
}

export function absolute(path: string): string {
  return `${origin()}${path.startsWith("/") ? path : `/${path}`}`;
}

/**
 * Every public route declares its canonical explicitly (seo-technical-audit).
 * `noindex` is opt-in per route and is never left to a default.
 */
export function pageMetadata(input: {
  title: string;
  description: string;
  path: string;
  noindex?: boolean;
  type?: "website" | "article";
  publishedTime?: string;
  modifiedTime?: string;
}): Metadata {
  const settings = getSettings();
  const url = absolute(input.path);
  return {
    title: input.title,
    description: input.description,
    alternates: { canonical: url },
    robots: input.noindex
      ? { index: false, follow: true }
      : { index: true, follow: true, googleBot: { index: true, follow: true, "max-image-preview": "large" } },
    openGraph: {
      type: input.type ?? "website",
      title: input.title,
      description: input.description,
      url,
      siteName: settings.organisation,
      locale: settings.locale.replace("-", "_"),
      ...(input.publishedTime ? { publishedTime: input.publishedTime } : {}),
      ...(input.modifiedTime ? { modifiedTime: input.modifiedTime } : {}),
    },
    twitter: {
      card: "summary_large_image",
      title: input.title,
      description: input.description,
    },
  };
}
