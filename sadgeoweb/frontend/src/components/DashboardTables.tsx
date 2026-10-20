import { useEffect, useState } from "react";
import Table, { type Row, type TableSort } from "../Table";
import DashboardFilters from "./DashboardFilters";
import {
  defaultYear,
  matches,
  newestFirst,
  type FilterValues,
} from "../dashboard";
const analyticalFields: [string, string][] = [
  ["ano", "Ano"],
  ["projeto", "Projeto"],
  ["campanha", "Campanha"],
  ["situacao", "Situação"],
];
const factFields: [string, string][] = [
  ["ano", "Ano"],
  ["mes", "Mês"],
  ["uf", "UF"],
  ["municipio", "Município"],
  ["uorgOrigem", "UORG de origem"],
  ["campanha", "Campanha"],
  ["projeto", "Projeto"],
  ["situacao", "Situação"],
];
export default function DashboardTables({
  analytical,
  refresh,
}: {
  analytical: Row[];
  refresh: number;
}) {
  const [summaryFilters, setSummaryFilters] = useState<FilterValues>({
    ano: defaultYear(),
  });
  const [filters, setFilters] = useState<FilterValues>({ ano: defaultYear() });
  const [options, setOptions] = useState<Record<string, string[]>>({});
  const [page, setPage] = useState(0);
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState<TableSort>({
    field: "anoLevantamento",
    desc: true,
  });
  const [result, setResult] = useState<{ items: Row[]; total: number }>();
  const [error, setError] = useState("");
  const [facetError, setFacetError] = useState("");
  const optionsQuery = new URLSearchParams(
    Object.entries(filters).filter(([, value]) => !!value),
  ).toString();
  useEffect(() => {
    const c = new AbortController();
    setFacetError("");
    fetch("/api/dashboard/fatos-filtros?" + optionsQuery, { signal: c.signal })
      .then((r) => {
        if (!r.ok) throw Error(`Filtros indisponíveis (HTTP ${r.status})`);
        return r.json();
      })
      .then(setOptions)
      .catch((e) => {
        if (!c.signal.aborted) setFacetError(e.message);
      });
    return () => c.abort();
  }, [optionsQuery, refresh]);
  useEffect(() => {
    const c = new AbortController();
    setResult(undefined);
    setError("");
    const timer = setTimeout(() => {
      fetch(
        "/api/dashboard/fatos-pagina?" +
          new URLSearchParams({
            ...filters,
            page: String(page),
            size: "25",
            q: query,
            sort: sort.field,
            direction: sort.desc ? "desc" : "asc",
          }),
        { signal: c.signal },
      )
        .then((r) => {
          if (!r.ok) throw Error(`Fatos indisponíveis (HTTP ${r.status})`);
          return r.json();
        })
        .then(setResult)
        .catch((e) => {
          if (!c.signal.aborted) setError(e.message);
        });
    }, 200);
    return () => {
      clearTimeout(timer);
      c.abort();
    };
  }, [filters, page, query, refresh, sort]);
  const summaryOptions = Object.fromEntries(
    analyticalFields.map(([key]) => [
      key,
      [
        ...new Set(
          analytical.map((row) => String(row[key] ?? "")).filter(Boolean),
        ),
      ],
    ]),
  );
  function change(key: string, value: string) {
    setPage(0);
    setFilters((previous) => ({
      ...previous,
      [key]: value,
      ...(key === "ano"
        ? {
            mes: "",
            campanha: "",
            projeto: "",
            uf: "",
            municipio: "",
            uorgOrigem: "",
            situacao: "",
          }
        : {}),
      ...(key === "campanha" ? { projeto: "" } : {}),
      ...(key === "uf" ? { municipio: "" } : {}),
    }));
  }
  return (
    <div className="dashboard-tables">
      <div className="dashboard-table-column">
        <Table
          title="Resumo analítico"
          rows={newestFirst(
            analytical.filter((row) => matches(row, summaryFilters)),
          )}
          pageSize={25}
          defaultSort="ano"
          dense
          topScroll
          groupDays
          filters={
            <DashboardFilters
              layout="summary"
              fields={analyticalFields}
              values={summaryFilters}
              options={summaryOptions}
              onChange={(key, value) =>
                setSummaryFilters((previous) => ({ ...previous, [key]: value }))
              }
            />
          }
        />
      </div>
      <div className="dashboard-table-column">
        <Table
          title="Fatos do painel"
          rows={result?.items ?? []}
          pageSize={25}
          dense
          topScroll
          groupDays
          filters={
            <>
              <DashboardFilters
                layout="facts"
                fields={factFields}
                values={filters}
                options={options}
                onChange={change}
              />
              {facetError && <p role="alert">{facetError}</p>}
              {error && <p role="alert">{error}</p>}
              {!result && !error && <p role="status">Carregando fatos…</p>}
            </>
          }
          server={{
            total: result?.total ?? 0,
            page,
            onPage: setPage,
            query,
            onQuery: (value) => {
              setQuery(value);
              setPage(0);
            },
            sort,
            onSort: (next) => {
              setSort(next);
              setPage(0);
            },
          }}
        />
      </div>
    </div>
  );
}
