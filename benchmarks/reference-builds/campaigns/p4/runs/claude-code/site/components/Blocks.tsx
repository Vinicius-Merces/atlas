import type { Block } from "@/lib/content";
import styles from "./blocks.module.css";

/**
 * The frontend rendering contract for editorial blocks
 * (planning/03-content-model.md). The switch is exhaustive over the union and
 * returns null for anything unknown, so a future block type published by an
 * editor cannot break a page.
 */
function renderBlock(block: Block, index: number) {
  switch (block.kind) {
    case "heading":
      return (
        <h2 key={index} className={styles.heading}>
          {block.text}
        </h2>
      );
    case "paragraph":
      return (
        <p key={index} className={styles.paragraph}>
          {block.text}
        </p>
      );
    case "list":
      return (
        <ul key={index} className={styles.list}>
          {block.items.map((item: string) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      );
    case "pullquote":
      return (
        <figure key={index} className={styles.pullquote}>
          <blockquote>
            <p>{block.text}</p>
          </blockquote>
          {block.attribution && <figcaption className="annotation">{block.attribution}</figcaption>}
        </figure>
      );
    case "dataTable":
      return (
        <div key={index} className={styles.tableWrap}>
          <table className="data-table">
            <caption>{block.caption}</caption>
            <thead>
              <tr>
                {block.columns.map((column: string, i: number) => (
                  <th key={column} scope="col" className={i > 0 ? "numeric" : undefined}>
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {block.rows.map((row: string[]) => (
                <tr key={row.join("|")}>
                  {row.map((cell: string, i: number) =>
                    i === 0 ? (
                      <th key={i} scope="row" style={{ fontWeight: 400 }}>
                        {cell}
                      </th>
                    ) : (
                      <td key={i} className="numeric">
                        {cell || <span aria-label="not applicable">—</span>}
                      </td>
                    ),
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    default:
      return null;
  }
}

export function Blocks({ blocks }: { blocks: Block[] }) {
  return <div className={styles.body}>{blocks.map(renderBlock)}</div>;
}
