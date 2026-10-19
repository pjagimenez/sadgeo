// @vitest-environment jsdom
import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";
import App from "./pages/DashboardPage";
import Table from "./Table";
vi.mock("./Chart", () => ({ default: () => <div>Gráfico</div> }));
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
it("reports API failures and retries without silently using demo data", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 503 }));
  render(<App />);
  expect((await screen.findByRole("alert")).textContent).toContain("HTTP 503");
  const count = vi.mocked(fetch).mock.calls.length;
  await userEvent.click(screen.getByText("Tentar novamente"));
  await waitFor(() =>
    expect(vi.mocked(fetch).mock.calls.length).toBeGreaterThan(count),
  );
});
it("renders dashboard totals from the API", async () => {
  const data: Record<string, unknown> = {
    config: { demo: true, version: "0.1.0" },
    resumo: { total: 123 },
    "evolucao-anual": [],
    analitico: [],
    fatos: [],
    pivot: { categorias: [], series: {} },
  };
  vi.stubGlobal(
    "fetch",
    vi.fn(async (url: string) => ({
      ok: true,
      json: async () => data[url.split("/").pop()!],
    })),
  );
  render(<App />);
  expect(await screen.findByText("123")).toBeTruthy();
});
it("paginates and filters analytical rows", async () => {
  render(
    <Table
      title="Fatos"
      rows={Array.from({ length: 25 }, (_, i) => ({
        campanha: `Campanha ${i}`,
      }))}
    />,
  );
  expect(screen.queryByText("Campanha 24")).toBeNull();
  await userEvent.click(screen.getByText("Próxima"));
  expect(screen.getByText("Campanha 24")).toBeTruthy();
  await userEvent.type(screen.getByRole("textbox"), "Campanha 3");
  expect(screen.getByText("Campanha 3")).toBeTruthy();
  expect(screen.queryByText("Campanha 24")).toBeNull();
});
