import type { MetadataRoute } from "next";
import { absolute } from "@/lib/seo";

/**
 * Explicit crawl behaviour for every public route family
 * (fixture constraint: "Public production routes must have explicit
 * crawl/index/canonical behavior").
 */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: [
          "/api/",
          "/enquire/received",
          "/residences?",
        ],
      },
    ],
    sitemap: absolute("/sitemap.xml"),
    host: absolute("/"),
  };
}
