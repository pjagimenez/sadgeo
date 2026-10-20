import { campaignNames, monthNames, type FilterValues } from "../dashboard";
export default function DashboardFilters({
  fields,
  layout = "summary",
  values,
  options,
  onChange,
}: {
  fields: [string, string][];
  layout?: "summary" | "facts";
  values: FilterValues;
  options: Record<string, string[]>;
  onChange: (key: string, value: string) => void;
}) {
  return (
    <div
      className={`dashboard-filters dashboard-filters-${layout}`}
      aria-label={
        layout === "summary"
          ? "Filtros do Resumo analítico"
          : "Filtros dos Fatos do painel"
      }
    >
      {fields.map(([key, label]) => {
        const choices = [
          ...new Set([
            ...(options[key] ?? []),
            ...(values[key] ? [values[key]] : []),
          ]),
        ].sort((a, b) =>
          key === "ano" || key === "mes"
            ? Number(b) - Number(a)
            : a.localeCompare(b, "pt-BR"),
        );
        return (
          <label key={key} className={`filter-${key}`}>
            {label}
            <select
              aria-label={label}
              value={values[key] ?? ""}
              disabled={
                (key === "mes" && !values.ano) ||
                (key === "municipio" && !values.uf) ||
                (key === "projeto" &&
                  fields.some(([f]) => f === "mes") &&
                  !values.campanha)
              }
              onChange={(e) => onChange(key, e.target.value)}
            >
              <option value="">Todos</option>
              {choices.map((value) => (
                <option key={value} value={value}>
                  {key === "mes"
                    ? (monthNames[Number(value) - 1] ?? value)
                    : value}
                  {key === "campanha" && campaignNames[value]
                    ? ` — ${campaignNames[value]}`
                    : ""}
                </option>
              ))}
            </select>
          </label>
        );
      })}
    </div>
  );
}
