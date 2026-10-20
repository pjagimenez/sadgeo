import { campaignNames, type FilterValues } from "../dashboard";
export default function DashboardFilters({
  fields,
  values,
  options,
  onChange,
}: {
  fields: [string, string][];
  values: FilterValues;
  options: Record<string, string[]>;
  onChange: (key: string, value: string) => void;
}) {
  return (
    <div className="dashboard-filters">
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
          <label key={key}>
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
                  {value}
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
