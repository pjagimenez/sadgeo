// @vitest-environment jsdom
import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import RodapeView from "./RodapeView";
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
  version: "0.1.20261019-16",
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
    within(footer).getByText("Versão 0.1.20261019-16").className,
  ).toContain("footer-version");
});
it("keeps user identity, profile and logout together at the bottom of the menu", async () => {
  auth.user = {
    login: "usuario123",
    nome: "Usuário",
    perfil: "Consulta",
    demo: false,
  };
  render(
    <MemoryRouter>
      <MenuAcaoView tema="" setTema={() => {}} temas={[]} />
    </MemoryRouter>,
  );
  const account = screen.getByLabelText(
    "Identificação do usuário",
  ).parentElement!;
  expect(account.className).toContain("portal-account");
  expect(within(account).getByText("Identificador: usuario123")).toBeTruthy();
  expect(within(account).getByText("Perfil: Consulta")).toBeTruthy();
  await userEvent.click(within(account).getByRole("button", { name: "Sair" }));
  expect(auth.logout).toHaveBeenCalledOnce();
});
it("shows a visitor shell and login action without requesting protected data", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({ ok: true, json: async () => config }),
  );
  render(
    <MemoryRouter>
      <PrincipalPage />
    </MemoryRouter>,
  );
  expect(screen.getByText("Visitante")).toBeTruthy();
  expect(
    screen.getByRole("complementary").querySelector('a[href="/login"]'),
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
