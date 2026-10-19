// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, it, vi } from "vitest";
import ReportsPage from "./ReportsPage";
import WorkflowTemplatePage from "./WorkflowTemplatePage";
import RecordDetails from "../components/layout/RecordDetails";
import { downloadCsv } from "../export";
vi.mock("../export", () => ({ downloadCsv: vi.fn() }));
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.clearAllMocks();
});
it("exports only production rows matching the visible period and text filters", async () => {
  const rows = [
    { ano: 2024, campanha: "medA", projeto: "P1", uf: "RJ", contagem: 2 },
    { ano: 2026, campanha: "medG", projeto: "P2", uf: "SP", contagem: 3 },
  ];
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({ ok: true, json: async () => rows }),
  );
  render(<ReportsPage title="Análise de Produção" />);
  await screen.findByText("P1");
  await userEvent.type(screen.getByLabelText("Ano inicial"), "2025");
  await userEvent.type(screen.getByLabelText("Projeto, UF ou texto"), "SP");
  await userEvent.click(
    screen.getByRole("button", { name: "Exportar consulta CSV" }),
  );
  expect(downloadCsv).toHaveBeenCalledWith(
    [rows[1]],
    "sadgeo-producao-0.2.csv",
  );
  await userEvent.type(screen.getByLabelText("Ano final"), "2020");
  expect(
    (
      screen.getByRole("button", {
        name: "Exportar consulta CSV",
      }) as HTMLButtonElement
    ).disabled,
  ).toBe(true);
});
it("previews a station draft without persisting or invoking a backend command", async () => {
  vi.stubGlobal("fetch", vi.fn());
  render(
    <MemoryRouter>
      <WorkflowTemplatePage
        screen={{
          label: "Novo Registro",
          path: "/campo/novo-registro",
          kind: "pending",
          milestone: "M02",
        }}
        group="Levantamento de Campo"
      />
    </MemoryRouter>,
  );
  await userEvent.type(screen.getByLabelText("Código da Estação"), "RN-01");
  await userEvent.click(
    screen.getByRole("button", { name: "Pré-visualizar rascunho" }),
  );
  expect(screen.getByText("RN-01")).toBeTruthy();
  expect(
    (
      screen.getByRole("button", {
        name: "Salvar estação no Oracle",
      }) as HTMLButtonElement
    ).disabled,
  ).toBe(true);
  expect(fetch).not.toHaveBeenCalled();
});
it("selects a local intake file but never uploads it", async () => {
  vi.stubGlobal("fetch", vi.fn());
  render(
    <MemoryRouter>
      <WorkflowTemplatePage
        screen={{
          label: "Recepção de Lotes",
          path: "/campo/lotes",
          kind: "pending",
          milestone: "M03",
        }}
        group="Levantamento de Campo"
      />
    </MemoryRouter>,
  );
  await userEvent.upload(
    screen.getByLabelText("Arquivo para prévia local"),
    new File(["dados"], "lote.txt", { type: "text/plain" }),
  );
  expect(screen.getByText(/lote.txt/)).toBeTruthy();
  expect(
    (
      screen.getByRole("button", {
        name: "Confirmar importação",
      }) as HTMLButtonElement
    ).disabled,
  ).toBe(true);
  expect(fetch).not.toHaveBeenCalled();
});
it("opens record tabs with explicit missing data and keeps workflow actions disabled", async () => {
  render(
    <MemoryRouter>
      <RecordDetails
        row={{ seq: "42", campanha: "medA", municipio: "Rio de Janeiro" }}
      />
    </MemoryRouter>,
  );
  await userEvent.click(screen.getByRole("tab", { name: "Fotos" }));
  expect(
    screen
      .getByRole("link", { name: "Abrir prévia de imagens" })
      .getAttribute("href"),
  ).toBe("/campo/imagens?registro=42");
  await userEvent.click(screen.getByRole("tab", { name: "Histórico" }));
  expect(screen.getByText(/Nenhum evento de auditoria fictício/)).toBeTruthy();
  expect(
    (
      screen.getByRole("button", {
        name: "Liberar",
      }) as HTMLButtonElement
    ).disabled,
  ).toBe(true);
});
