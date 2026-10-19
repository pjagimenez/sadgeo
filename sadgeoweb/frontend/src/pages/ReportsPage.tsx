import { useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Chip,
  MenuItem,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import Table, { type Row } from "../Table";
import { downloadCsv } from "../export";
export default function ReportsPage({ title }: { title: string }) {
  const [rows, setRows] = useState<Row[]>();
  const [error, setError] = useState("");
  const [campanha, setCampanha] = useState("");
  const [search, setSearch] = useState("");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    const c = new AbortController();
    setError("");
    fetch("/api/dashboard/analitico", { signal: c.signal })
      .then((r) => {
        if (!r.ok)
          throw new Error(`Falha na consulta de produção (HTTP ${r.status}).`);
        return r.json();
      })
      .then(setRows)
      .catch((e) => {
        if (!c.signal.aborted) setError(e.message);
      });
    return () => c.abort();
  }, [attempt]);
  const filtered = useMemo(
    () =>
      (rows ?? []).filter(
        (r) =>
          (!campanha || r.campanha === campanha) &&
          (!start || Number(r.ano) >= Number(start)) &&
          (!end || Number(r.ano) <= Number(end)) &&
          (!search ||
            Object.values(r).some((v) =>
              String(v ?? "")
                .toLocaleLowerCase("pt-BR")
                .includes(search.toLocaleLowerCase("pt-BR")),
            )),
      ),
    [rows, campanha, start, end, search],
  );
  const invalid = !!start && !!end && Number(start) > Number(end);
  const campaigns = [
    ...new Set((rows ?? []).map((r) => String(r.campanha ?? ""))),
  ]
    .filter(Boolean)
    .sort();
  return (
    <Box component="main" className="portal-content">
      <Typography className="eyebrow">Qualidade e Produção</Typography>
      <Typography component="h1" variant="h4">
        {title}
      </Typography>
      <Alert severity="info" sx={{ my: 2 }}>
        Consulta aos resumos analíticos existentes. O CSV contém somente as
        linhas exibidas pelo filtro; não é o layout oficial TXT, KMZ ou
        CoordDalti, previstos no milestone M05.
      </Alert>
      <Paper
        variant="outlined"
        sx={{ p: 2, my: 2, display: "flex", gap: 2, flexWrap: "wrap" }}
      >
        <TextField
          label="Projeto, UF ou texto"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          size="small"
        />
        <TextField
          label="Campanha"
          select
          value={campanha}
          onChange={(e) => setCampanha(e.target.value)}
          size="small"
          sx={{ minWidth: 180 }}
        >
          <MenuItem value="">Todas</MenuItem>
          {campaigns.map((c) => (
            <MenuItem key={c} value={c}>
              {c}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          type="number"
          label="Ano inicial"
          value={start}
          onChange={(e) => setStart(e.target.value)}
          size="small"
        />
        <TextField
          type="number"
          label="Ano final"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
          size="small"
        />
        <Button
          onClick={() => {
            setCampanha("");
            setSearch("");
            setStart("");
            setEnd("");
          }}
        >
          Limpar
        </Button>
        <Button
          variant="contained"
          disabled={!!error || !rows || invalid || !filtered.length}
          onClick={() => downloadCsv(filtered, "sadgeo-producao-0.2.csv")}
        >
          Exportar consulta CSV
        </Button>
      </Paper>
      <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", mb: 2 }}>
        {[
          "Exportar TXT",
          "Exportar KMZ",
          "CoordDalti (Altimetria)",
          "Relatório simplificado",
        ].map((label) => (
          <Button disabled key={label}>
            {label}
          </Button>
        ))}
      </Box>
      {error ? (
        <Alert
          severity="error"
          action={
            <Button onClick={() => setAttempt((a) => a + 1)}>
              Tentar novamente
            </Button>
          }
        >
          {error}
        </Alert>
      ) : invalid ? (
        <Alert severity="warning">
          O ano inicial deve ser menor ou igual ao ano final.
        </Alert>
      ) : !rows ? (
        <p role="status">Carregando produção…</p>
      ) : (
        <>
          <Box sx={{ display: "flex", gap: 2, my: 2 }}>
            <Chip label={`${filtered.length} grupos analíticos`} />
            <Chip
              label={`${filtered.reduce((n, r) => n + Number(r.contagem ?? 0), 0).toLocaleString("pt-BR")} registros contabilizados`}
            />
          </Box>
          <Table
            title="Produção por ano, campanha, projeto e UF"
            rows={filtered}
            searchable={false}
          />
        </>
      )}
    </Box>
  );
}
