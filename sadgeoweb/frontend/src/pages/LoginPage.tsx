import { useEffect, useState, type FormEvent } from "react";
import { Navigate } from "react-router-dom";
import { Alert, Box, Button, CircularProgress, TextField } from "@mui/material";
import { useAuth, type Config } from "../auth/AuthContext";
import SystemTitle from "../components/elements/SystemTitle";
import RodapeView from "../components/layout/RodapeView";
import "../styles/login.css";
export default function LoginPage() {
  const { user, loading, error: sessionError, login, demo } = useAuth();
  const [config, setConfig] = useState<Config>();
  const [usuario, setUsuario] = useState("");
  const [senha, setSenha] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    const c = new AbortController();
    fetch("/api/dashboard/config", { signal: c.signal })
      .then((r) => {
        if (!r.ok) throw new Error("Configuração indisponível.");
        return r.json();
      })
      .then(setConfig)
      .catch((e) => {
        if (!c.signal.aborted) setError(e.message);
      });
    return () => c.abort();
  }, []);
  if (loading)
    return (
      <Box role="status" sx={{ p: 4 }}>
        Verificando sessão…
      </Box>
    );
  if (user) return <Navigate to="/index" replace />;
  async function submit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(usuario, senha);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setSenha("");
      setBusy(false);
    }
  }
  async function enterDemo() {
    setBusy(true);
    setError("");
    try {
      await demo();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <Box className="login-page">
      <Box className="login-body">
        <Box className="login-container">
          <SystemTitle />
          {(error || sessionError) && (
            <Alert severity="error" sx={{ my: 2 }}>
              {error || sessionError}
            </Alert>
          )}
          {config?.demo ? (
            <>
              <Alert severity="info" sx={{ my: 3 }}>
                Modo demonstração: dados fictícios, sem acesso ao Oracle ou à
                rede institucional.
              </Alert>
              <Button
                variant="contained"
                fullWidth
                disabled={busy}
                onClick={enterDemo}
              >
                {busy ? (
                  <CircularProgress size={22} />
                ) : (
                  "Entrar na demonstração"
                )}
              </Button>
            </>
          ) : (
            <Box component="form" onSubmit={submit} className="login-panel">
              <TextField
                label="Login da rede"
                value={usuario}
                onChange={(e) => setUsuario(e.target.value)}
                autoComplete="username"
                required
                disabled={busy || !config?.authConfigured}
              />
              <TextField
                label="Senha da rede"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                type="password"
                autoComplete="current-password"
                required
                disabled={busy || !config?.authConfigured}
              />
              <Button
                type="submit"
                variant="contained"
                disabled={busy || !config?.authConfigured}
              >
                {busy ? "Autenticando…" : "Entrar"}
              </Button>
              {config && !config.authConfigured && (
                <Alert severity="warning">
                  Login institucional ainda não configurado no processo Java.
                  Configure SADGEO_LDAP_HOST e SADGEO_LDAP_DOMAIN na execução do
                  backend e reinicie-o. Consulte AUTH_CONFIG no arquivo
                  logs/sadgeo.log.
                </Alert>
              )}
            </Box>
          )}
        </Box>
      </Box>
      <RodapeView config={config} />
    </Box>
  );
}
