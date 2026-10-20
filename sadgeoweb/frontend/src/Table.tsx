import {
  useEffect,
  useRef,
  useState,
  type ReactNode,
  type CSSProperties,
} from "react";
import {
  columnLabel,
  dayColumns,
  displayValue,
  numericColumn,
} from "./dashboard";
export type Row = Record<string, string | number | null>;
export type TableSort = { field: string; desc: boolean };
type Server = {
  total: number;
  page: number;
  onPage: (page: number) => void;
  query: string;
  onQuery: (query: string) => void;
  sort?: TableSort;
  onSort?: (sort: TableSort) => void;
};
const widths: Record<string, string> = {
  ano: "6ch",
  anoLevantamento: "6ch",
  mesLevantamento: "5ch",
  campanha: "10ch",
  uf: "3ch",
  situacao: "20ch",
  projeto: "14ch",
  municipio: "20ch",
  uorgOrigem: "10ch",
  seq: "10ch",
  dataLevantamento: "12ch",
  tipoLocal: "12ch",
  contagem: "10ch",
};
export default function Table({
  title,
  rows,
  searchable = true,
  pageSize = 20,
  defaultSort,
  server,
  compact = false,
  dense = false,
  showTitle = true,
  showCount = true,
  filters,
  topScroll = false,
  groupDays = false,
}: {
  title: string;
  rows: Row[];
  searchable?: boolean;
  pageSize?: number;
  defaultSort?: string;
  server?: Server;
  compact?: boolean;
  dense?: boolean;
  showTitle?: boolean;
  showCount?: boolean;
  filters?: ReactNode;
  topScroll?: boolean;
  groupDays?: boolean;
}) {
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(0);
  const [sort, setSort] = useState<TableSort | undefined>(
    defaultSort ? { field: defaultSort, desc: true } : undefined,
  );
  const activeSort = server?.sort ?? sort;
  const rawColumns = Object.keys(rows[0] ?? {});
  const days = groupDays ? rawColumns.filter((key) => dayColumns[key]) : [];
  const columns = groupDays
    ? [...rawColumns.filter((key) => !dayColumns[key]), ...days]
    : rawColumns;
  const filtered = server
    ? rows
    : rows.filter((row) =>
        Object.values(row).some((value) =>
          String(value ?? "")
            .toLocaleLowerCase("pt-BR")
            .includes(query.toLocaleLowerCase("pt-BR")),
        ),
      );
  const sorted =
    !server && activeSort
      ? [...filtered].sort((a, b) => {
          const av = a[activeSort.field],
            bv = b[activeSort.field];
          const compare =
            typeof av === "number" && typeof bv === "number"
              ? av - bv
              : String(av ?? "").localeCompare(String(bv ?? ""), "pt-BR", {
                  numeric: true,
                });
          return activeSort.desc ? -compare : compare;
        })
      : filtered;
  const total = server?.total ?? filtered.length,
    pages = Math.max(1, Math.ceil(total / pageSize));
  const current = Math.min(server?.page ?? page, pages - 1);
  const visible = server
    ? sorted
    : sorted.slice(current * pageSize, current * pageSize + pageSize);
  const changePage = server?.onPage ?? setPage;
  const bodyRef = useRef<HTMLDivElement>(null),
    topRef = useRef<HTMLDivElement>(null);
  const [scrollWidth, setScrollWidth] = useState(0);
  useEffect(() => {
    if (!topScroll) return;
    const element = bodyRef.current!;
    const update = () => setScrollWidth(element.scrollWidth);
    update();
    const observer =
      typeof ResizeObserver === "undefined"
        ? undefined
        : new ResizeObserver(update);
    observer?.observe(element);
    if (element.firstElementChild) observer?.observe(element.firstElementChild);
    window.addEventListener("resize", update);
    return () => {
      observer?.disconnect();
      window.removeEventListener("resize", update);
    };
  }, [rows, topScroll]);
  function toggle(field: string) {
    const next = {
      field,
      desc: activeSort?.field === field ? !activeSort.desc : true,
    };
    if (server?.onSort) server.onSort(next);
    else setSort(next);
    if (!server) setPage(0);
  }
  function header(key: string, rowSpan = 1) {
    const label =
      groupDays && dayColumns[key] ? dayColumns[key] : columnLabel(key);
    return (
      <th
        key={key}
        scope="col"
        rowSpan={rowSpan}
        className={numericColumn(key, rows) ? "numeric-column" : undefined}
        aria-sort={
          activeSort?.field === key
            ? activeSort.desc
              ? "descending"
              : "ascending"
            : "none"
        }
      >
        {!server || server.onSort ? (
          <button
            className="column-sort"
            aria-label={`Ordenar por ${label}`}
            title={columnLabel(key)}
            onClick={() => toggle(key)}
          >
            {label}
            {activeSort?.field === key ? (activeSort.desc ? " ↓" : " ↑") : ""}
          </button>
        ) : (
          label
        )}
      </th>
    );
  }
  return (
    <section
      aria-label={title}
      className={`panel ${compact ? "chart-data-table" : ""} ${dense || compact ? "dense-table" : ""}`}
    >
      {showTitle && <h2>{title}</h2>}
      {filters}
      {searchable && (
        <label className="table-search">
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
      {showCount && (
        <p className="table-count">{total.toLocaleString("pt-BR")} registros</p>
      )}
      {topScroll && (
        <div
          ref={topRef}
          className="table-scroll-top"
          aria-label={`Rolagem horizontal de ${title}`}
          tabIndex={0}
          onScroll={(e) => {
            if (
              bodyRef.current &&
              bodyRef.current.scrollLeft !== e.currentTarget.scrollLeft
            )
              bodyRef.current.scrollLeft = e.currentTarget.scrollLeft;
          }}
        >
          <div style={{ width: scrollWidth, height: 1 }} />
        </div>
      )}
      <div
        className="table-scroll"
        ref={bodyRef}
        onScroll={(e) => {
          if (
            topRef.current &&
            topRef.current.scrollLeft !== e.currentTarget.scrollLeft
          )
            topRef.current.scrollLeft = e.currentTarget.scrollLeft;
        }}
      >
        <table>
          <colgroup>
            {columns.map((key) => (
              <col
                key={key}
                style={{
                  width: widths[key] ?? (dayColumns[key] ? "15ch" : undefined),
                }}
              />
            ))}
          </colgroup>
          <thead>
            {days.length ? (
              <>
                <tr>
                  {columns
                    .filter((key) => !dayColumns[key])
                    .map((key) => header(key, 2))}
                  <th
                    scope="colgroup"
                    colSpan={days.length}
                    className="day-column-group"
                  >
                    {days.some((key) => key.startsWith("media"))
                      ? "Médias de dias entre…"
                      : "Dias entre…"}
                  </th>
                </tr>
                <tr>{days.map((key) => header(key))}</tr>
              </>
            ) : (
              <tr>{columns.map((key) => header(key))}</tr>
            )}
          </thead>
          <tbody>
            {visible.map((row, index) => (
              <tr key={String(row.seq ?? index)}>
                {columns.map((key) => (
                  <td
                    key={key}
                    style={
                      dense || compact
                        ? ({
                            "--column-width":
                              widths[key] ??
                              (dayColumns[key] ? "15ch" : "10ch"),
                          } as CSSProperties)
                        : undefined
                    }
                    className={
                      numericColumn(key, rows) ? "numeric-column" : undefined
                    }
                  >
                    {displayValue(key, row[key])}
                  </td>
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
