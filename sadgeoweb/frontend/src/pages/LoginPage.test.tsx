// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import LoginPage from "./LoginPage";
const auth = vi.hoisted(() => ({
  user: null,
  loading: false,
  error: "",
  login: vi.fn(),
  demo: vi.fn(),
}));
vi.mock("../auth/AuthContext", () => ({ useAuth: () => auth }));
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
beforeEach(() => {
  auth.demo.mockReset();
  auth.login.mockReset();
});
function config(demo: boolean, authConfigured = false) {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ demo, authConfigured, version: "0.2.0" }),
    }),
  );
  render(
    <MemoryRouter>
      <LoginPage />
    </MemoryRouter>,
  );
}
it("enters demo explicitly without requesting or inventing a password", async () => {
  config(true);
  await userEvent.click(
    await screen.findByRole("button", { name: "Entrar na demonstração" }),
  );
  expect(auth.demo).toHaveBeenCalledOnce();
  expect(screen.queryByLabelText("Senha da rede")).toBeNull();
});
it("disables institutional login until backend authentication is configured", async () => {
  config(false);
  await screen.findByText(/Login institucional ainda não configurado/);
  expect(
    (screen.getByRole("button", { name: "Entrar" }) as HTMLButtonElement)
      .disabled,
  ).toBe(true);
});
it("shows a failed demo request without entering the portal", async () => {
  auth.demo.mockRejectedValue(new Error("Serviço indisponível"));
  config(true);
  await userEvent.click(
    await screen.findByRole("button", { name: "Entrar na demonstração" }),
  );
  expect(await screen.findByText("Serviço indisponível")).toBeTruthy();
});
