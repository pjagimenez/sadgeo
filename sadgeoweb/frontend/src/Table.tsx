import { useState } from "react";
import { columnLabel } from "./dashboard";
export type Row = Record<string, string | number | null>;
type Server = {
  total: number;
  page: number;
  onPage: (page: number) => void;
  query: string;
  onQuery: (query: string) => void;
};
export default function Table({
  title,
  rows,
  searchable = true,
  pageSize = 20,
  defaultSort,
  server,
  compact = false,
}: {
  title: string;
  rows: Row[];
  searchable?: boolean;
  pageSize?: number;
  defaultSort?: string;
  server?: Server;
  compact?: boolean;
}) {
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(0);
  const [sort, setSort] = useState<
    { field: string; desc: boolean } | undefined
  >(defaultSort ? { field: defaultSort, desc: true } : undefined);
  const columns = Object.keys(rows[0] ?? {});
  const filtered = server
    ? rows
    : rows.filter((row) =>
        Object.values(row).some((value) =>
          String(value ?? "")
            .toLocaleLowerCase("pt-BR")
            .includes(query.toLocaleLowerCase("pt-BR")),
        ),
      );
  const sorted = sort
    ? [...filtered].sort((a, b) => {
        const av = a[sort.field],
          bv = b[sort.field];
        const comparison =
          typeof av === "number" && typeof bv === "number"
            ? av - bv
            : String(av ?? "").localeCompare(String(bv ?? ""), "pt-BR", {
                numeric: true,
              });
        return sort.desc ? -comparison : comparison;
      })
    : filtered;
  const total = server?.total ?? filtered.length;
  const pages = Math.max(1, Math.ceil(total / pageSize));
  const current = Math.min(server?.page ?? page, pages - 1);
  const visible = server
    ? sorted
    : sorted.slice(current * pageSize, current * pageSize + pageSize);
  const changePage = server?.onPage ?? setPage;
  return (
    <section className={`panel ${compact ? "chart-data-table" : ""}`}>
      <h2>{title}</h2>
      {searchable && (
        <label>
          Buscar em {title}
          <input
            value={server?.query ?? query}
            onChange={(e) => {
              if (server) server.onQuery(e.target.value);
              else {
                setQuery(e.target.value);
                setPage(0);
              }
            }}
            placeholder="Campanha, UF, projeto…"
          />
        </label>
      )}
      <p>{total.toLocaleString("pt-BR")} registros</p>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              {columns.map((c) => (
                <th
                  key={c}
                  className={c.startsWith("mediaDias") || c.startsWith("diasAte") ? "metric-column" : undefined}
                  aria-sort={
                    sort?.field === c
                      ? sort.desc
                        ? "descending"
                        : "ascending"
                      : "none"
                  }
                >
                  {server ? (
                    <span>{columnLabel(c)}</span>
                  ) : (
                    <button
                      className="column-sort"
                      onClick={() => {
                        setSort({
                          field: c,
                          desc: sort?.field === c ? !sort.desc : true,
                        });
                        setPage(0);
                      }}
                    >
                      {columnLabel(c)}
                      {sort?.field === c ? (sort.desc ? " ↓" : " ↑") : ""}
                    </button>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {visible.map((row, i) => (
              <tr key={String(row.seq ?? i)}>
                {columns.map((c) => (
                  <td key={c}>{row[c] ?? "—"}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {!total && <p>Nenhum registro encontrado.</p>}
      <div className="pagination">
        <button
          disabled={current === 0}
          onClick={() => changePage(current - 1)}
        >
          Anterior
        </button>
        <span>
          Página {current + 1} de {pages}
        </span>
        <button
          disabled={current >= pages - 1}
          onClick={() => changePage(current + 1)}
        >
          Próxima
        </button>
      </div>
    </section>
  );
}
