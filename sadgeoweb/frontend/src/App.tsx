import { useEffect, useState } from 'react';
import Chart from './Chart';
import Table, { type Row } from './Table';
const statuses: [string,string][] = [['naoCriticado','Não criticado'],['retidoCampo','Retido campo'],['liberadoCampo','Liberado campo'],['criticadoCampo','Criticado campo'],['retidoProjeto','Retido projeto'],['liberadoProjeto','Liberado projeto'],['criticadoProjeto','Criticado projeto'],['atualizadoBdg','Atualizado BDG'],['reservadoGabinete','Reservado gabinete']];
type Dashboard = { config: { demo: boolean; version: string }; resumo: Row; anual: Row[]; analitico: Row[]; fatos: Row[]; pivot: { categorias: string[]; series: Record<string,number[]> } };
async function get<T>(section: string, signal: AbortSignal): Promise<T> {
  const response = await fetch(`/api/dashboard/${section}`, { signal });
  if (!response.ok) throw new Error(`Não foi possível carregar ${section} (HTTP ${response.status}). Verifique o backend e a conexão com o Oracle.`);
  return response.json();
}
export default function App() {
  const [data,setData] = useState<Dashboard>(); const [error,setError] = useState(''); const [attempt,setAttempt] = useState(0);
  useEffect(() => {
    const controller = new AbortController(); setError(''); setData(undefined);
    Promise.all([get<Dashboard['config']>('config',controller.signal), get<Row>('resumo',controller.signal),get<Row[]>('evolucao-anual',controller.signal),get<Row[]>('analitico',controller.signal),get<Row[]>('fatos',controller.signal),get<Dashboard['pivot']>('pivot',controller.signal)])
      .then(([config,resumo,anual,analitico,fatos,pivot]) => setData({config,resumo,anual,analitico,fatos,pivot}))
      .catch(e => { if (!controller.signal.aborted) setError(e.message); });
    return () => controller.abort();
  },[attempt]);
  return <><header><div><strong>SADGEO</strong><span>Sistema de acompanhamento de dados geodésicos</span></div><small>Versão {data?.config.version ?? '0.1.0'}</small></header>
    <main><div className="heading"><div><p className="eyebrow">VISÃO GERAL</p><h1>Painel resumo</h1><p>Acompanhamento de levantamentos, campanhas e situação dos registros.</p></div><button onClick={() => setAttempt(a=>a+1)}>Atualizar dados</button></div>
    {error ? <div role="alert" className="error">{error}<button onClick={() => setAttempt(a=>a+1)}>Tentar novamente</button></div> : !data ? <p role="status">Carregando indicadores…</p> : <>
      {data.config.demo && <p className="notice" role="status">Modo demonstração — dados fictícios. Nenhuma conexão com o Oracle.</p>}
      <section className="cards" aria-label="Indicadores"><article className="card total"><span>Total de registros</span><strong>{Number(data.resumo.total ?? 0).toLocaleString('pt-BR')}</strong></article>{statuses.map(([key,label]) => <article className="card" key={key}><span>{label}</span><strong>{Number(data.resumo[key] ?? 0).toLocaleString('pt-BR')}</strong></article>)}</section>
      <p className="period">Período dos levantamentos: {data.resumo.dtPrimeiroLevantamento ?? '—'} a {data.resumo.dtUltimoLevantamento ?? '—'}</p>
      <div className="charts"><Chart title="Evolução anual" categories={data.anual.map(r=>String(r.ano))} series={statuses.map(([key,name])=>({name,data:data.anual.map(r=>Number(r[key]??0))}))}/><Chart title="Registros por ano e campanha" categories={data.pivot.categorias} series={Object.entries(data.pivot.series).map(([name,values])=>({name,data:values}))}/></div>
      <Table title="Resumo analítico" rows={data.analitico}/><Table title="Fatos do painel" rows={data.fatos}/>
    </>}</main><footer>SADGEO 0.1 • React + Spring Boot</footer></>;
}
