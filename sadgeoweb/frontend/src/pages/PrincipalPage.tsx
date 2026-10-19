import { useEffect, useState } from "react";
import { Navigate, Outlet, useOutletContext } from "react-router-dom";
import { Alert, Box, Button, Typography } from "@mui/material";
import { useAuth } from "../auth/AuthContext";
import MenuAcaoView from "../components/layout/MenuAcaoView";
import RodapeView from "../components/layout/RodapeView";
import RegistroView from "../components/layout/RegistroView";
import type { Row } from "../Table";
type PortalContext = {
  rows: Row[];
  tema: string;
  error: string;
  loading: boolean;
  retry: () => void;
};
export function RegistrosPage() {
  const { rows, tema, error, loading, retry } =
    useOutletContext<PortalContext>();
  return error ? (
    <Alert
      severity="error"
      action={<Button onClick={retry}>Tentar novamente</Button>}
    >
      {error}
    </Alert>
  ) : loading ? (
    <p role="status">Carregando registros…</p>
  ) : (
    <RegistroView rows={rows} tema={tema} />
  );
}
export default function PrincipalPage() {
  const { user, loading } = useAuth();
  const [rows, setRows] = useState<Row[]>([]);
  const [tema, setTema] = useState("");
  const [error, setError] = useState("");
  const [fetching, setFetching] = useState(true);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    if (!user) return;
    const c = new AbortController();
    setFetching(true);
    setError("");
    fetch("/api/dashboard/fatos", { signal: c.signal })
      .then((r) => {
        if (!r.ok)
          throw new Error(`Falha ao consultar registros (HTTP ${r.status}).`);
        return r.json();
      })
      .then(setRows)
      .catch((e) => {
        if (!c.signal.aborted) setError(e.message);
      })
      .finally(() => {
        if (!c.signal.aborted) setFetching(false);
      });
    return () => c.abort();
  }, [user, attempt]);
  if (loading) return <p role="status">Verificando sessão…</p>;
  if (!user) return <Navigate to="/login" replace />;
  const temas = [
    ...new Set(
      rows
        .map((r) => r.projeto)
        .filter((p): p is string => typeof p === "string" && !!p),
    ),
  ].sort();
  return (
    <Box className="portal-shell">
      <Box component="header" className="portal-header">
        <div>
          <Typography component="div" variant="h5" fontWeight={800}>
            SADGEO
          </Typography>
          <Typography variant="body2">
            Sistema de acompanhamento de dados geodésicos
          </Typography>
        </div>
        <Typography variant="caption">
          {user.demo ? "DEMONSTRAÇÃO" : "PORTAL INSTITUCIONAL"} • 0.1
        </Typography>
      </Box>
      {user.demo && (
        <Alert severity="info">
          Modo demonstração — dados fictícios. Nenhuma conexão com o Oracle.
        </Alert>
      )}
      <Box className="portal-body">
        <MenuAcaoView tema={tema} setTema={setTema} temas={temas} />
        <Box className="portal-workspace">
          <Outlet
            context={
              {
                rows,
                tema,
                error,
                loading: fetching,
                retry: () => setAttempt((a) => a + 1),
              } satisfies PortalContext
            }
          />
        </Box>
      </Box>
      <RodapeView demo={user.demo} />
    </Box>
  );
}
