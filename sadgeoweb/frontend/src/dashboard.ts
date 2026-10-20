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

export const monthNames = [
  "JAN",
  "FEV",
  "MAR",
  "ABR",
  "MAI",
  "JUN",
  "JUL",
  "AGO",
  "SET",
  "OUT",
  "NOV",
  "DEZ",
];
export const dayColumns: Record<string, string> = {
  mediaDiasLevantamentoAteEntrada: "Levant. → Entrada",
  mediaDiasEntradaAteCritica: "Entrada → Crítica",
  mediaDiasEntradadiasAtePublicacao: "Entrada → Publicação",
  mediaDiasEntradaAtePublicacao: "Entrada → Publicação",
  mediaDiasLevantamentoAteCalculoCoordenadas: "Levant. → Cálc. coord.",
  diasAteEntrada: "Levant. → Entrada",
  diasAteCritica: "Entrada → Crítica",
  diasAtePublicacao: "Entrada → Publicação",
  diasAteCalculoCoord: "Levant. → Cálc. coord.",
};
export function numericColumn(key: string, rows: Row[]) {
  return (
    ["ano", "anoLevantamento", "mesLevantamento"].includes(key) ||
    rows.some((row) => typeof row[key] === "number")
  );
}
export function displayValue(key: string, value: Row[string]) {
  if (value == null) return "—";
  if (key === "mesLevantamento")
    return monthNames[Number(value) - 1] ?? String(value);
  if (typeof value === "number" && !["ano", "anoLevantamento"].includes(key))
    return value.toLocaleString("pt-BR", { maximumFractionDigits: 2 });
  return String(value);
}
export function brazilianDate(value: Row[string] | undefined) {
  const match = String(value ?? "").match(/^(\d{4})-(\d{2})-(\d{2})/);
  return match ? `${match[3]}/${match[2]}/${match[1]}` : "—";
}
