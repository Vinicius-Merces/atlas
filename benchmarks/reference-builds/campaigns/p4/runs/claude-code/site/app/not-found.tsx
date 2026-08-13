import Link from "next/link";
import { getResidences } from "@/lib/content";

export default function NotFound() {
  const residences = getResidences().slice(0, 4);
  return (
    <div className="page" style={{ paddingTop: "var(--space-2xl)", paddingBottom: "var(--space-3xl)" }}>
      <p className="annotation">Error 404</p>
      <h1 style={{ fontSize: "var(--step-4)", marginTop: "var(--space-s)", maxWidth: "18ch" }}>
        That page is not on the ridge.
      </h1>
      <p className="prose" style={{ marginTop: "var(--space-m)" }}>
        The address you followed does not exist here. Nothing has been removed: every residence page
        stays published even after the house is sold, so a broken link is a wrong address rather than
        a withdrawn one.
      </p>
      <ul style={{ listStyle: "none", marginTop: "var(--space-l)", borderTop: "var(--rule-thin) solid var(--ink)" }}>
        {residences.map((r) => (
          <li key={r.id} style={{ padding: "0.6rem 0", borderBottom: "var(--rule-hair) solid var(--rule-color)" }}>
            <Link href={`/residences/${r.slug}`}>
              <span className="num">{String(r.index).padStart(2, "0")}</span> {r.name}
            </Link>
          </li>
        ))}
      </ul>
      <p style={{ marginTop: "var(--space-l)", display: "flex", gap: "var(--space-2xs)", flexWrap: "wrap" }}>
        <Link href="/" className="button">Home</Link>
        <Link href="/residences" className="button button--ghost">All twelve residences</Link>
        <Link href="/enquire" className="button button--ghost">Request a visit</Link>
      </p>
    </div>
  );
}
