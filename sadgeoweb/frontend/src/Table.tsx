import { useState } from "react";
export type Row = Record<string, string | number | null>;
export default function Table({ title, rows }: { title: string; rows: Row[] }) {
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(0);
  const columns = Object.keys(rows[0] ?? {});
  const filtered = rows.filter((row) =>
    Object.values(row).some((value) =>
      String(value ?? "")
        .toLocaleLowerCase("pt-BR")
        .includes(query.toLocaleLowerCase("pt-BR")),
    ),
  );
  const pages = Math.max(1, Math.ceil(filtered.length / 20));
  const current = Math.min(page, pages - 1);
  return (
    <section className="panel">
      <h2>{title}</h2>
      <label>
        Buscar em {title}
        <input
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setPage(0);
          }}
          placeholder="Campanha, UF, projeto…"
        />
      </label>
      <p>{filtered.length.toLocaleString("pt-BR")} registros</p>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              {columns.map((c) => (
                <th key={c}>{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.slice(current * 20, current * 20 + 20).map((r, i) => (
              <tr key={i}>
                {columns.map((c) => (
                  <td key={c}>{r[c] ?? "—"}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {!filtered.length && <p>Nenhum registro encontrado.</p>}
      <div className="pagination">
        <button disabled={current === 0} onClick={() => setPage(current - 1)}>
          Anterior
        </button>
        <span>
          Página {current + 1} de {pages}
        </span>
        <button
          disabled={current >= pages - 1}
          onClick={() => setPage(current + 1)}
        >
          Próxima
        </button>
      </div>
    </section>
  );
}
