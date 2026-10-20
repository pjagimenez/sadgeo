// @vitest-environment jsdom
import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";
import { defaultYear } from "./dashboard";
import Table from "./Table";
import DashboardTables from "./components/DashboardTables";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
it("uses previous year through March and current year from April in Brasilia", () => {
  expect(defaultYear(new Date("2026-03-31T20:00:00Z"))).toBe("2025");
  expect(defaultYear(new Date("2026-04-01T02:00:00Z"))).toBe("2025");
  expect(defaultYear(new Date("2026-04-01T03:00:00Z"))).toBe("2026");
});
it("sorts descending by year, paginates 10 chart rows and allows column sorting", async () => {
  render(
    <Table
      title="Dados do gráfico"
      rows={Array.from({ length: 12 }, (_, i) => ({
        ano: 2000 + i,
        contagem: i,
      }))}
      pageSize={10}
      defaultSort="ano"
    />,
  );
  expect(screen.getAllByRole("row")[1].textContent).toBe("201111");
  expect(screen.queryByText("2000")).toBeNull();
  await userEvent.click(screen.getByRole("button", { name: "Próxima" }));
  expect(screen.getByText("2000")).toBeTruthy();
  await userEvent.click(screen.getByRole("button", { name: /Ano/ }));
  expect(screen.getAllByRole("row")[1].textContent).toBe("20000");
});
it("requests facts by page and resets dependent project/month/municipality filters", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn(async (url: string) => ({
      ok: true,
      json: async () =>
        url.includes("fatos-filtros")
          ? {
              ano: ["2025", "2026"],
              mes: ["1", "2"],
              campanha: ["medA", "medG"],
              projeto: ["A", "G"],
              uf: ["RJ", "SP"],
              municipio: ["Rio", "São Paulo"],
              uorgOrigem: ["DGC"],
            }
          : { items: [{ seq: "1", anoLevantamento: 2026 }], total: 60 },
    })),
  );
  render(
    <DashboardTables
      analytical={[
        { ano: 2026, projeto: "A", campanha: "medA", situacao: "Liberado" },
      ]}
      refresh={0}
    />,
  );
  await screen.findByText("1", { selector: "td" });
  const project = screen.getAllByLabelText("Projeto")[1] as HTMLSelectElement;
  expect(project.disabled).toBe(true);
  const campaign = screen.getAllByLabelText("Campanha")[1];
  await userEvent.selectOptions(campaign, "medA");
  await userEvent.selectOptions(project, "A");
  await userEvent.selectOptions(campaign, "medG");
  expect(project.value).toBe("");
  const uf = screen.getByLabelText("UF");
  await userEvent.selectOptions(uf, "RJ");
  await userEvent.selectOptions(screen.getByLabelText("Município"), "Rio");
  await userEvent.selectOptions(uf, "SP");
  expect((screen.getByLabelText("Município") as HTMLSelectElement).value).toBe(
    "",
  );
  const panel = screen
    .getByText("Fatos do painel", { selector: "h2" })
    .closest("section")!;
  await vi.waitFor(() =>
    expect(
      (
        within(panel).getByRole("button", {
          name: "Próxima",
        }) as HTMLButtonElement
      ).disabled,
    ).toBe(false),
  );
  await userEvent.click(within(panel).getByRole("button", { name: "Próxima" }));
  await vi.waitFor(() =>
    expect(
      vi
        .mocked(fetch)
        .mock.calls.some(
          ([url]) =>
            String(url).includes("page=1") && String(url).includes("size=25"),
        ),
    ).toBe(true),
  );
  expect(
    vi
      .mocked(fetch)
      .mock.calls.every(([url]) => !String(url).endsWith("/fatos")),
  ).toBe(true);
});

it("formats numeric chart cells with thousands and groups mean-day headers", async () => {
  render(
    <Table
      title="Resumo"
      rows={[
        {
          ano: 2026,
          campanha: "medA",
          contagem: 12345,
          mediaDiasLevantamentoAteEntrada: 1234.5,
          mediaDiasEntradaAteCritica: 20,
          mediaDiasEntradadiasAtePublicacao: 30,
          mediaDiasLevantamentoAteCalculoCoordenadas: 40,
        },
      ]}
      dense
      groupDays
      topScroll
    />,
  );
  expect(screen.getByText("12.345").className).toContain("numeric-column");
  expect(screen.getByText("1.234,5").className).toContain("numeric-column");
  expect(
    screen
      .getByRole("columnheader", { name: "Médias de dias entre…" })
      .getAttribute("colspan"),
  ).toBe("4");
  expect(screen.getByLabelText("Rolagem horizontal de Resumo")).toBeTruthy();
});
it("requests server ordering for all fact columns instead of sorting just the current page", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn(async (url: string) => ({
      ok: true,
      json: async () =>
        url.includes("fatos-filtros")
          ? {}
          : {
              items: [{ seq: "1", anoLevantamento: 2026, contagem: 50 }],
              total: 100,
            },
    })),
  );
  render(<DashboardTables analytical={[]} refresh={0} />);
  const column = await screen.findByRole("button", {
    name: "Ordenar por Quantidade",
  });
  await userEvent.click(column);
  await vi.waitFor(() =>
    expect(
      vi
        .mocked(fetch)
        .mock.calls.some(
          ([url]) =>
            String(url).includes("sort=contagem") &&
            String(url).includes("direction=desc") &&
            String(url).includes("page=0"),
        ),
    ).toBe(true),
  );
});
