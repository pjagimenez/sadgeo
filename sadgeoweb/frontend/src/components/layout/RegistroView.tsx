// Grade e seleção adaptadas de RegistroView.tsx da versão anterior.
import { useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Typography,
} from "@mui/material";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import { ptBR } from "@mui/x-data-grid/locales";
import type { Row } from "../../Table";
export default function RegistroView({
  rows,
  tema,
}: {
  rows: Row[];
  tema: string;
}) {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Row | null>(null);
  const filtered = useMemo(
    () =>
      rows.filter(
        (r) =>
          (!tema || r.projeto === tema) &&
          Object.values(r).some((v) =>
            String(v ?? "")
              .toLocaleLowerCase("pt-BR")
              .includes(query.toLocaleLowerCase("pt-BR")),
          ),
      ),
    [rows, tema, query],
  );
  const columns: GridColDef[] = [
    ["seq", "Sequência"],
    ["campanha", "Campanha"],
    ["projeto", "Projeto"],
    ["municipio", "Município"],
    ["uf", "UF"],
    ["situacao", "Situação"],
    ["dataLevantamento", "Levantamento"],
    ["contagem", "Contagem"],
  ].map(([field, headerName]) => ({
    field,
    headerName,
    width: field === "municipio" ? 190 : 150,
  }));
  return (
    <Box component="main" className="portal-content">
      <Typography component="h1" variant="h4">
        Registros
      </Typography>
      <Alert severity="info" sx={{ my: 2 }}>
        Consulta aos fatos do painel. Cadastro e edição de estações ainda não
        estão disponíveis na API 0.1.
      </Alert>
      <TextField
        label="Buscar registros"
        placeholder="Campanha, município, UF…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        size="small"
        sx={{ my: 2, width: "min(100%,400px)" }}
      />
      <Box sx={{ height: 520, width: "100%", bgcolor: "background.paper" }}>
        <DataGrid
          rows={filtered}
          columns={columns}
          getRowId={(r) => String(r.seq)}
          localeText={ptBR.components.MuiDataGrid.defaultProps.localeText}
          pageSizeOptions={[10, 25, 50, 100]}
          initialState={{
            pagination: { paginationModel: { page: 0, pageSize: 25 } },
          }}
          disableRowSelectionOnClick
          onRowClick={(p) => setSelected(p.row as Row)}
          onCellKeyDown={(p, e) => {
            if (e.key === "Enter") setSelected(p.row as Row);
          }}
        />
      </Box>
      <Dialog open={!!selected} onClose={() => setSelected(null)} fullWidth>
        <DialogTitle>Detalhes do registro {selected?.seq}</DialogTitle>
        <DialogContent>
          <Box component="dl">
            {Object.entries(selected ?? {}).map(([k, v]) => (
              <Box key={k} sx={{ mb: 1 }}>
                <Typography component="dt" fontWeight={700}>
                  {k}
                </Typography>
                <Typography component="dd" sx={{ m: 0 }}>
                  {v ?? "—"}
                </Typography>
              </Box>
            ))}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSelected(null)}>Fechar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
