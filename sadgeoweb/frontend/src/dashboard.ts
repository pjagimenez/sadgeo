import type { Row } from "./Table";
export const campaignNames: Record<string, string> = {
  cons: "Construção",
  medA: "Medição altimétrica",
  medG: "Medição gravimétrica",
  medP: "Medição planimétrica",
  gab: "Ajustes de gabinete",
  vrf: "VRF",
  veg: "VEG",
  ogr: "OGR",
};
export function defaultYear(date = new Date()) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: "America/Sao_Paulo",
    year: "numeric",
    month: "numeric",
  }).formatToParts(date);
  const year = Number(parts.find((p) => p.type === "year")!.value),
    month = Number(parts.find((p) => p.type === "month")!.value);
  return String(year - (month <= 3 ? 1 : 0));
}
export function newestFirst(rows: Row[], field = "ano") {
  return [...rows].sort(
    (a, b) => Number(b[field] ?? 0) - Number(a[field] ?? 0),
  );
}
export const fieldLabels: Record<string, string> = {
  ano: "Ano",
  anoLevantamento: "Ano",
  mesLevantamento: "Mês",
  campanha: "Campanha",
  projeto: "Projeto",
  uf: "UF",
  municipio: "Município",
  situacao: "Situação",
  uorgOrigem: "UORG de origem",
  seq: "Identificador",
  contagem: "Quantidade",
  dataLevantamento: "Data do levantamento",
  tipoLocal: "Tipo de local",
  mediaDiasLevantamentoAteEntrada:
    "Média de dias do levantamento até a entrada",
  mediaDiasEntradaAteCritica: "Média de dias da entrada até a crítica",
  mediaDiasEntradadiasAtePublicacao:
    "Média de dias da entrada até a publicação",
  mediaDiasEntradaAtePublicacao: "Média de dias da entrada até a publicação",
  mediaDiasLevantamentoAteCalculoCoordenadas:
    "Média de dias do levantamento até o cálculo de coordenadas",
  diasAteEntrada: "Dias até a entrada",
  diasAteCritica: "Dias até a crítica",
  diasAtePublicacao: "Dias até a publicação",
  diasAteCalculoCoord: "Dias até o cálculo de coordenadas",
};
export function columnLabel(key: string) {
  return fieldLabels[key] ?? key.replace(/([a-z])([A-Z])/g, "$1 $2");
}
export type FilterValues = Record<string, string>;
export function matches(row: Row, filters: FilterValues) {
  return Object.entries(filters).every(
    ([field, value]) => !value || String(row[field] ?? "") === value,
  );
}
