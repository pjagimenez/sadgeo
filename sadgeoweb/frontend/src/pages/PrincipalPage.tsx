import { useEffect, useState } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import { Alert, Box, Button, Typography } from "@mui/material";
import { useAuth, type Config } from "../auth/AuthContext";
import MenuAcaoView from "../components/layout/MenuAcaoView";
import HeaderActions from "../components/layout/HeaderActions";
import RodapeView from "../components/layout/RodapeView";
export default function PrincipalPage() {
  const { user, loading } = useAuth();
  const { pathname } = useLocation();
  const [config, setConfig] = useState<Config>();
  useEffect(() => {
    const c = new AbortController();
    fetch("/api/dashboard/config", { signal: c.signal })
      .then((r) => {
        if (!r.ok) throw new Error("Ambiente indisponível");
        return r.json();
      })
      .then(setConfig)
      .catch(() => {});
    return () => c.abort();
  }, []);
  if (loading) return <p role="status">Verificando sessão…</p>;
  return (
    <Box className="portal-shell">
      <Box component="header" className="portal-header">
        <div>
          <Typography component="div" variant="h5" fontWeight={800}>
            SADGEO
          </Typography>
          <Typography variant="body2">
            Sistema de Administração de Dados Geodésicos de Execução Operacional
          </Typography>
        </div>
        <HeaderActions />
      </Box>
      {(config?.demo || user?.demo) && (
        <Alert severity="info">
          Modo demonstração — dados fictícios. Nenhuma conexão com o Oracle.
        </Alert>
      )}
      <Box className="portal-body">
        <MenuAcaoView />
        <Box className="portal-workspace">
          {!user && pathname !== "/index" && pathname !== "/ajuda/guia" ? (
            <Box component="main" className="portal-content">
              <Typography component="h1" variant="h4">
                Acesso ao módulo
              </Typography>
              <Alert severity="info" sx={{ my: 2 }}>
                Faça login para acessar este módulo. O Painel de Controle é público.
              </Alert>
              <Button component={Link} to="/login" variant="contained">
                Fazer login
              </Button>
            </Box>
          ) : (
            <Outlet />
          )}
        </Box>
      </Box>
      <RodapeView config={config} />
    </Box>
  );
}
