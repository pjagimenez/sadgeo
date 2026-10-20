import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
export type User = {
  login: string;
  nome: string;
  description?: string;
  perfil: string;
  demo: boolean;
};
export type Config = {
  demo: boolean;
  version: string;
  authConfigured: boolean;
  profile: string;
  profileLabel: string;
  hostname: string;
};
export async function authRequest(path: string, data?: URLSearchParams) {
  const csrf = await fetch("/api/auth/csrf", { credentials: "same-origin" });
  if (!csrf.ok) throw new Error("Não foi possível iniciar uma sessão segura.");
  const token = await csrf.json();
  const response = await fetch(`/api/auth/${path}`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      [token.headerName]: token.token,
      ...(data ? { "Content-Type": "application/x-www-form-urlencoded" } : {}),
    },
    body: data,
  });
  if (!response.ok) {
    const failure = await response.json().catch(() => null);
    const fallback =
      response.status === 401
        ? "Usuário ou senha inválidos."
        : `Não foi possível autenticar ou encerrar a sessão (HTTP ${response.status}).`;
    const message =
      typeof failure?.message === "string" ? failure.message : fallback;
    const reference =
      typeof failure?.diagnosticId === "string"
        ? ` Referência: ${failure.diagnosticId}.`
        : "";
    const reason =
      typeof failure?.reason === "string" ? ` Motivo: ${failure.reason}.` : "";
    throw new Error(message + reference + reason);
  }
}
const AuthContext = createContext<{
  user: User | null;
  loading: boolean;
  error: string;
  login: (u: string, p: string) => Promise<void>;
  demo: () => Promise<void>;
  logout: () => Promise<void>;
} | null>(null);
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  async function refresh() {
    const r = await fetch("/api/auth/me", { credentials: "same-origin" });
    if (r.status === 401) {
      setUser(null);
      return;
    }
    if (!r.ok) throw new Error("Não foi possível verificar a sessão.");
    setUser(await r.json());
  }
  useEffect(() => {
    refresh()
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);
  async function login(u: string, p: string) {
    await authRequest(
      "login",
      new URLSearchParams({ username: u, password: p }),
    );
    await refresh();
    setError("");
  }
  async function demo() {
    await authRequest("demo");
    await refresh();
    setError("");
  }
  async function logout() {
    await authRequest("logout");
    setUser(null);
  }
  return (
    <AuthContext.Provider value={{ user, loading, error, login, demo, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("AuthProvider necessário");
  return value;
}
