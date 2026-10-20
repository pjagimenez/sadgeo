import { useEffect, useRef, useMemo } from "react";
import Table from "./Table";
import * as echarts from "echarts/core";
import { BarChart } from "echarts/charts";
import {
  GridComponent,
  LegendComponent,
  TooltipComponent,
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
echarts.use([
  BarChart,
  GridComponent,
  LegendComponent,
  TooltipComponent,
  CanvasRenderer,
]);
export default function Chart({
  title,
  categories: inputCategories,
  series: inputSeries,
  hints = {},
}: {
  title: string;
  categories: string[];
  series: { name: string; data: number[] }[];
  hints?: Record<string, string>;
}) {
  const valid = inputCategories
    .map((_, index) => index)
    .filter((index) =>
      inputSeries.some((s) => Number(s.data[index] ?? 0) !== 0),
    );
  const categories = valid.map((index) => inputCategories[index]);
  const series = inputSeries.map((s) => ({
    ...s,
    data: valid.map((index) => s.data[index] ?? 0),
  }));
  const rows = useMemo(
    () =>
      valid
        .map((index) =>
          Object.fromEntries([
            ["ano", inputCategories[index]],
            ...inputSeries.map((s) => [s.name, s.data[index] ?? 0]),
          ]),
        )
        .sort((a, b) => Number(b.ano) - Number(a.ano)),
    [inputCategories, inputSeries],
  );
  const element = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const chart = echarts.init(element.current!);
    chart.setOption({
      tooltip: {
        trigger: "axis",
        valueFormatter: (value: unknown) => String(value),
        formatter: (
          params: {
            axisValue: string;
            seriesName: string;
            value: number;
            marker: string;
          }[],
        ) =>
          params
            .map(
              (p, index) =>
                `${index === 0 ? `${echarts.format.encodeHTML(p.axisValue)}<br/>` : ""}${echarts.format.encodeHTML(p.seriesName)}${hints[p.seriesName] ? ` — ${echarts.format.encodeHTML(hints[p.seriesName])}` : ""}: ${p.value}`,
            )
            .join("<br/>"),
      },
      legend: {
        type: "scroll",
        bottom: 0,
        tooltip: {
          show: true,
          formatter: (p: { name: string }) =>
            hints[p.name] ? `${p.name} — ${hints[p.name]}` : p.name,
        },
      },
      grid: { top: 20, bottom: 75, left: 65, right: 20 },
      xAxis: { type: "category", data: categories },
      yAxis: { type: "value" },
      series: series.map((s) => ({ ...s, type: "bar", stack: "total" })),
    });
    const observer = new ResizeObserver(() => chart.resize());
    observer.observe(element.current!);
    return () => {
      observer.disconnect();
      chart.dispose();
    };
  }, [categories, series]);
  return (
    <section className="panel">
      <h2>{title}</h2>
      <div
        role="img"
        aria-label={title}
        ref={element}
        style={{ height: 255 }}
      />
      {Object.keys(hints).length > 0 && (
        <p className="campaign-hints">
          {series.map((s) => (
            <abbr key={s.name} title={hints[s.name] ?? s.name}>
              {s.name}
            </abbr>
          ))}
        </p>
      )}
      <details>
        <summary>Consultar dados do gráfico</summary>
        <Table
          title={`Dados — ${title}`}
          rows={rows}
          searchable={false}
          pageSize={10}
          defaultSort="ano"
          compact
        />
      </details>
    </section>
  );
}
