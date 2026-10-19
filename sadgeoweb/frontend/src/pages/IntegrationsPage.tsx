import { useEffect, useState } from "react";
import { Alert, Box, Button, Chip, Paper, Typography } from "@mui/material";
import type { Config } from "../auth/AuthContext";
export default function IntegrationsPage() {
  const [data, setData] = useState<Config>();
  const [health, setHealth] = useState("Verificando");
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    const c = new AbortController();
    setError("");
    fetch("/api/dashboard/config", { signal: c.signal })
      .then((r) => {
        if (!r.ok) throw new Error("Configuração indisponível");
        return r.json();
      })
      .then(setData)
      .catch((e) => {
        if (!c.signal.aborted) setError(e.message);
      });
    fetch("/actuator/health", { signal: c.signal })
      .then(async (r) => {
        const h = await r.json();
        setHealth(h.status ?? `HTTP ${r.status}`);
      })
      .catch(() => {
        if (!c.signal.aborted) setHealth("Indisponível");
      });
    return () => c.abort();
  }, [attempt]);
  return (
    <Box component="main" className="portal-content">
      <Typography className="eyebrow">Administração</Typography>
      <Typography component="h1" variant="h4">
        Integrações
      </Typography>
      <Button sx={{ my: 2 }} onClick={() => setAttempt((a) => a + 1)}>
        Atualizar estado
      </Button>
      {error && <Alert severity="error">{error}</Alert>}
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))",
          gap: 2,
        }}
      >
        {[
          ["Aplicação", health, "Saúde geral informada pelo backend."],
          [
            "Oracle",
            data?.demo
              ? "Não utilizado no demo"
              : "Validação institucional necessária",
            "O estado geral UP não substitui a conferência dos objetos e permissões Oracle.",
          ],
          [
            "AD / LDAPS",
            data?.authConfigured ? "Configuração presente" : "Não configurado",
            "A presença de configuração não comprova autenticação ou conectividade.",
          ],
          [
            "SIDGEO / SIGCVEG",
            "Pendente — M03",
            "Contrato e recebimento de lotes ainda não implementados.",
          ],
          [
            "GEDLivre",
            "Pendente — M03",
            "Consulta e gravação dependem do contrato institucional.",
          ],
          [
            "BDG",
            "Pendente — M06",
            "Fila, confirmação e reconciliação ainda não conectadas.",
          ],
        ].map(([name, status, note]) => (
          <Paper variant="outlined" sx={{ p: 2 }} key={name}>
            <Typography variant="h6">{name}</Typography>
            <Chip label={status} size="small" sx={{ my: 1 }} />
            <Typography variant="body2">{note}</Typography>
          </Paper>
        ))}
      </Box>
      <Alert severity="info" sx={{ my: 2 }}>
        Esta tela não exibe senhas, tokens ou configurações sensíveis.
      </Alert>
    </Box>
  );
}
