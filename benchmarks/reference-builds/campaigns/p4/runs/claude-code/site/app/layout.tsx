import type { Metadata, Viewport } from "next";
import "@fontsource-variable/fraunces";
import "@fontsource-variable/newsreader";
import "@fontsource/ibm-plex-mono/400.css";
import "./globals.css";
import { SiteHeader } from "@/components/SiteHeader";
import { SiteFooter } from "@/components/SiteFooter";
import { getSettings } from "@/lib/content";
import { JsonLd, organisationNode, websiteNode, developmentNode } from "@/lib/jsonld";
import { absolute } from "@/lib/seo";

const settings = getSettings();

export const metadata: Metadata = {
  metadataBase: new URL(settings.origin),
  title: {
    default: `${settings.organisation} — ${settings.tagline}`,
    template: `%s · ${settings.organisation}`,
  },
  description:
    "Twelve architect-designed houses on the Alto da Pedra ridge, 22 km from central Lisbon. Areas, plans, prices and delivery dates published in full. Visits by appointment.",
  applicationName: settings.organisation,
  authors: [{ name: settings.legalName }],
  alternates: { canonical: absolute("/") },
  robots: { index: true, follow: true },
  formatDetection: { telephone: true, address: false, email: false },
};

export const viewport: Viewport = {
  themeColor: "#f4f1ea",
  colorScheme: "light",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang={settings.locale}>
      <body>
        <a className="skip-link" href="#main">
          Skip to content
        </a>
        <SiteHeader />
        <main id="main">{children}</main>
        <SiteFooter />
        <JsonLd nodes={[organisationNode(), websiteNode(), developmentNode()]} />
      </body>
    </html>
  );
}
