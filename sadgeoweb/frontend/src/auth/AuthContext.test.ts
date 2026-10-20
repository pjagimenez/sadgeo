import { afterEach, expect, it, vi } from "vitest";
import { authRequest } from "./AuthContext";
afterEach(() => vi.unstubAllGlobals());
it("shows the diagnostic reference and safe failure category returned by the backend", async () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ headerName: "X-CSRF-TOKEN", token: "test-only" }),
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 503,
        json: async () => ({
          message: "Consulte o diagnóstico no log.",
          diagnosticId: "test-reference",
          reason: "LDAP_DNS",
        }),
      }),
  );
  await expect(
    authRequest(
      "login",
      new URLSearchParams({ username: "test", password: "test-only" }),
    ),
  ).rejects.toThrow("Referência: test-reference. Motivo: LDAP_DNS.");
});
