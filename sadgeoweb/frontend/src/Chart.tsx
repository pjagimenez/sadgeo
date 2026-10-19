import { useEffect, useRef } from "react";
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
  categories,
  series,
}: {
  title: string;
  categories: string[];
  series: { name: string; data: number[] }[];
}) {
  const element = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const chart = echarts.init(element.current!);
    chart.setOption({
      tooltip: { trigger: "axis" },
      legend: { type: "scroll", bottom: 0 },
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
        style={{ height: 340 }}
      />
      <details>
        <summary>Consultar dados do gráfico</summary>
        <table>
          <thead>
            <tr>
              <th>Categoria</th>
              {series.map((s) => (
                <th key={s.name}>{s.name}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {categories.map((c, i) => (
              <tr key={c}>
                <th>{c}</th>
                {series.map((s) => (
                  <td key={s.name}>{s.data[i] ?? 0}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </details>
    </section>
  );
}
