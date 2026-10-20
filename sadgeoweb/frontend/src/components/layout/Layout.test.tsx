// @vitest-environment jsdom
import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import RodapeView from "./RodapeView";
import HeaderActions from "./HeaderActions";
import MenuAcaoView from "./MenuAcaoView";
import PrincipalPage from "../../pages/PrincipalPage";
import type { Config, User } from "../../auth/AuthContext";
const auth = vi.hoisted(() => ({
  user: null as User | null,
  loading: false,
  logout: vi.fn(),
}));
vi.mock("../../auth/AuthContext", () => ({ useAuth: () => auth }));
const config: Config = {
  demo: false,
  version: "0.2.20261019-16",
  profile: "prod",
  profileLabel: "Produção",
  hostname: "sadgeo-pod-123",
  authConfigured: true,
};
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
beforeEach(() => {
  auth.user = null;
  auth.logout.mockReset();
});
it("places copyright, profile/hostname and version in their footer slots", () => {
  render(<RodapeView config={config} />);
  const footer = screen.getByRole("contentinfo");
  expect(within(footer).getByText(/IBGE-DGC\/CGED\/GSD/).className).toContain(
    "footer-copyright",
  );
  expect(
    within(footer).getByText("Produção (prod) • sadgeo-pod-123").className,
  ).toContain("footer-environment");
  expect(
    within(footer).getByText("Versão 0.2.20261019-16").parentElement!.className,
  ).toContain("footer-version");
});
it("keeps user identity, profile and logout together in header actions", async () => {
  auth.user = {
    login: "usuario123",
    nome: "Usuário",
    description: "Equipe de Geodésia <campo>",
    perfil: "Consulta",
    demo: false,
  };
  render(
    <MemoryRouter>
      <HeaderActions />
    </MemoryRouter>,
  );
  const account = screen.getByLabelText(
    "Identificação do usuário",
  ).parentElement!;
  expect(account.className).toContain("header-account");
  expect(within(account).getByText("Identificador: usuario123")).toBeTruthy();
  expect(within(account).getByText("Perfil: Consulta")).toBeTruthy();
  expect(within(account).getByText("Descrição: Equipe de Geodésia <campo>")).toBeTruthy();
  expect(account.querySelector('campo')).toBeNull();
  await userEvent.click(within(account).getByRole("button", { name: "Sair" }));
  expect(auth.logout).toHaveBeenCalledOnce();
});
it("renders the public dashboard outlet for visitors with account actions in the header", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({ ok: true, json: async () => config }),
  );
  render(
    <MemoryRouter initialEntries={["/index"]}>
      <Routes><Route element={<PrincipalPage />}>
        <Route path="/index" element={<div>Dashboard público</div>} />
      </Route></Routes>
    </MemoryRouter>,
  );
  expect(screen.getByText("Visitante")).toBeTruthy();
  expect(screen.getByText("Dashboard público")).toBeTruthy();
  expect(
    screen.getByRole("banner").querySelector('a[href="/login"]'),
  ).toBeTruthy();
  expect(
    await screen.findByText("Produção (prod) • sadgeo-pod-123"),
  ).toBeTruthy();
  expect(
    vi
      .mocked(fetch)
      .mock.calls.every(([url]) => url === "/api/dashboard/config"),
  ).toBe(true);
});

it("expands multiple menu groups independently without nested scroll containers", async () => {
  render(<MemoryRouter><MenuAcaoView /></MemoryRouter>);
  const nav = screen.getByRole("navigation", { name: "Navegação principal" });
  await userEvent.click(within(nav).getByRole("button", { name: /Planejamento/ }));
  await userEvent.click(within(nav).getByRole("button", { name: /Tabelas básicas/i }));
  expect(within(nav).getByRole("link", { name: "Campanha" })).toBeTruthy();
  expect(within(nav).getByRole("link", { name: "Localização" })).toBeTruthy();
  expect(nav.querySelectorAll("details").length).toBe(0);
  expect(within(nav).queryByText("Visitante")).toBeNull();
});
