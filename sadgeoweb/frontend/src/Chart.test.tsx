// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";
const mock = vi.hoisted(() => ({ setOption: vi.fn() }));
vi.mock("echarts/core", () => ({
  use: vi.fn(),
  init: () => ({
    setOption: mock.setOption,
    resize: vi.fn(),
    dispose: vi.fn(),
  }),
  format: { encodeHTML: (value: unknown) => String(value) },
}));
import Chart from "./Chart";
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
it("uses 255px charts, removes all-zero years and sorts the data table descending in pages of ten", async () => {
  vi.stubGlobal(
    "ResizeObserver",
    class {
      observe() {}
      disconnect() {}
    },
  );
  render(
    <Chart
      title="Campanhas"
      categories={Array.from({ length: 13 }, (_, i) => String(2000 + i))}
      series={[{ name: "cons", data: Array.from({ length: 13 }, (_, i) => i) }]}
      hints={{ cons: "Construção" }}
    />,
  );
  expect(screen.getByRole("img").style.height).toBe("255px");
  expect(screen.getByTitle("Construção")).toBeTruthy();
  const option = mock.setOption.mock.calls.at(-1)![0];
  expect(option.xAxis.data).not.toContain("2000");
  await userEvent.click(screen.getByText("Consultar dados do gráfico"));
  expect(screen.getAllByRole("row")).toHaveLength(11);
  expect(screen.getAllByRole("row")[1].textContent).toBe("201212");
  expect(screen.queryByText("2000")).toBeNull();
  await userEvent.click(screen.getByRole("button", { name: "Próxima" }));
  expect(screen.getByText("2001")).toBeTruthy();
});
