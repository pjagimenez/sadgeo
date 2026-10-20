import { useEffect, useState } from "react";
import Chart from "../Chart";
import type { Row } from "../Table";
import DashboardTables from "../components/DashboardTables";
import { campaignNames, brazilianDate } from "../dashboard";
const statuses: [string, string][] = [
  ["naoCriticado", "Não criticado"],
  ["retidoCampo", "Retido campo"],
  ["liberadoCampo", "Liberado campo"],
  ["criticadoCampo", "Criticado campo"],
  ["atualizadoBdg", "Atualizado BDG"],
  ["reservadoGabinete", "Reservado gabinete"],
  ["retidoProjeto", "Retido projeto"],
  ["liberadoProjeto", "Liberado projeto"],
  ["criticadoProjeto", "Criticado projeto"],
];
type Dashboard = {
  config: { demo: boolean; version: string };
  resumo: Row;
  anual: Row[];
  analitico: Row[];
  pivot: { categorias: string[]; series: Record<string, number[]> };
};
async function get<T>(section: string, signal: AbortSignal): Promise<T> {
  const response = await fetch(`/api/dashboard/${section}`, { signal });
  if (!response.ok)
    throw new Error(
      `Não foi possível carregar ${section} (HTTP ${response.status}). Verifique o backend e a conexão com o Oracle.`,
    );
  return response.json();
}
export default function DashboardPage() {
  const [data, setData] = useState<Dashboard>();
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    setError("");
    setData(undefined);
    Promise.all([
      get<Dashboard["config"]>("config", controller.signal),
      get<Row>("resumo", controller.signal),
      get<Row[]>("evolucao-anual", controller.signal),
      get<Row[]>("analitico", controller.signal),
      get<Dashboard["pivot"]>("pivot", controller.signal),
    ])
      .then(([config, resumo, anual, analitico, pivot]) =>
        setData({ config, resumo, anual, analitico, pivot }),
      )
      .catch((e) => {
        if (!controller.signal.aborted) setError(e.message);
      });
    return () => controller.abort();
  }, [attempt]);
  return (
    <>
      {" "}
      <main>
        <div className="heading dashboard-heading">
          <div>
            <p className="eyebrow">VISÃO GERAL</p>
            <h1>Painel de Controle</h1>
          </div>
          <button
            className="dashboard-refresh"
            onClick={() => setAttempt((a) => a + 1)}
          >
            Atualizar dados
          </button>
          <div className="dashboard-subline">
            <p>
              Acompanhamento de levantamentos, campanhas e situação dos
              registros.
            </p>
            {data && (
              <p className="period">
                Período {brazilianDate(data.resumo.dtPrimeiroLevantamento)} a{" "}
                {brazilianDate(data.resumo.dtUltimoLevantamento)}
              </p>
            )}
          </div>
        </div>
        {error ? (
          <div role="alert" className="error">
            {error}
            <button onClick={() => setAttempt((a) => a + 1)}>
              Tentar novamente
            </button>
          </div>
        ) : !data ? (
          <p role="status">Carregando indicadores…</p>
        ) : (
          <>
            <section className="dashboard-indicators" aria-label="Indicadores">
              <article className="indicator indicator-total">
                <span className="indicator-label">Total de registros</span>
                <strong className="indicator-value">
                  <span>
                    {Number(data.resumo.total ?? 0).toLocaleString("pt-BR")}
                  </span>
                </strong>
              </article>
              {statuses.map(([key, label]) => (
                <article className={`indicator indicator-${key}`} key={key}>
                  <span className="indicator-label">{label}</span>
                  <strong className="indicator-value">
                    <span>
                      {Number(data.resumo[key] ?? 0).toLocaleString("pt-BR")}
                    </span>
                  </strong>
                </article>
              ))}
            </section>
            <div className="charts">
              <Chart
                title="Evolução anual"
                categories={data.anual.map((r) => String(r.ano))}
                series={statuses.map(([key, name]) => ({
                  name,
                  data: data.anual.map((r) => Number(r[key] ?? 0)),
                }))}
              />
              <Chart
                title="Consolidado por Ano e Campanha"
                hints={campaignNames}
                categories={data.pivot.categorias}
                series={Object.entries(data.pivot.series).map(
                  ([name, values]) => ({ name, data: values }),
                )}
              />
            </div>
            <DashboardTables analytical={data.analitico} refresh={attempt} />
          </>
        )}
      </main>
    </>
  );
}
