import { useEffect, useState, useRef } from "react";
import {
  Alert,
  Box,
  Button,
  Chip,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import RegistroView from "../components/layout/RegistroView";
import { downloadCsv } from "../export";
import type { Row } from "../Table";
import type { Screen } from "../navigation";
type Page = {
  items: Row[];
  total: number;
  page: number;
  size: number;
  campanha: string;
};
export default function RecordsPage({
  screen,
  group,
}: {
  screen: Screen;
  group: string;
}) {
  const [q, setQ] = useState("");
  const [project, setProject] = useState("");
  const [filter, setFilter] = useState({ q: "", projeto: "" });
  const [page, setPage] = useState(0);
  const [size, setSize] = useState(25);
  const [data, setData] = useState<Page>();
  const total = useRef(0);
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    const c = new AbortController();
    setError("");
    setData(undefined);
    const query = new URLSearchParams({
      page: String(page),
      size: String(size),
      ...filter,
    });
    fetch(`/api/registros/${screen.context}?${query}`, { signal: c.signal })
      .then((r) => {
        if (!r.ok)
          throw new Error(
            `Não foi possível consultar os registros (HTTP ${r.status}).`,
          );
        return r.json();
      })
      .then((d) => {
        total.current = d.total;
        setData(d);
      })
      .catch((e) => {
        if (!c.signal.aborted) setError(e.message);
      });
    return () => c.abort();
  }, [screen.context, page, size, filter, attempt]);
  return (
    <Box component="main" className="portal-content">
      <Typography className="eyebrow">{group}</Typography>
      <Typography component="h1" variant="h4">
        {screen.label}
      </Typography>
      <Paper variant="outlined" sx={{ p: 2, my: 2 }}>
        <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", mb: 2 }}>
          <Chip
            label={
              screen.campanha
                ? `CAMPANHA = ${screen.campanha}`
                : "Todas as campanhas"
            }
            color="primary"
          />
          <Chip label="Template de consulta e crítica" variant="outlined" />
        </Box>
        <Box
          component="form"
          onSubmit={(e) => {
            e.preventDefault();
            setPage(0);
            setFilter({ q, projeto: project });
          }}
          sx={{ display: "flex", gap: 2, flexWrap: "wrap" }}
        >
          <TextField
            label="Buscar registros"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            size="small"
          />
          <TextField
            label="Projeto"
            value={project}
            onChange={(e) => setProject(e.target.value)}
            size="small"
          />
          <Button type="submit" variant="contained">
            Pesquisar
          </Button>
          <Button
            onClick={() => {
              setQ("");
              setProject("");
              setFilter({ q: "", projeto: "" });
              setPage(0);
            }}
          >
            Limpar filtros
          </Button>
        </Box>
      </Paper>
      <Alert severity="info" sx={{ mb: 2 }}>
        Consulta aos fatos do painel. O filtro de campanha é aplicado pela API e
        permanece ativo ao pesquisar. Edição de estações e ações de crítica
        ainda dependem das regras específicas.
      </Alert>
      <Button
        disabled={!data?.items.length}
        onClick={() =>
          data &&
          downloadCsv(
            data.items,
            `sadgeo-${screen.context}-pagina-${page + 1}.csv`,
          )
        }
        sx={{ mb: 2 }}
      >
        Exportar página CSV
      </Button>
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
      ) : (
        <RegistroView
          rows={data?.items ?? []}
          total={data?.total ?? total.current}
          page={page}
          size={size}
          loading={!data}
          onPageChange={(p, s) => {
            setPage(p);
            setSize(s);
          }}
        />
      )}
    </Box>
  );
}
