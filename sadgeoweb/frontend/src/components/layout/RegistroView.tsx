// Grade e seleção adaptadas de RegistroView.tsx da versão anterior.
import { useState } from "react";
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Typography,
} from "@mui/material";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import { ptBR } from "@mui/x-data-grid/locales";
import RecordDetails from "./RecordDetails";
import type { Row } from "../../Table";
export default function RegistroView({
  rows,
  total,
  page,
  size,
  loading,
  onPageChange,
}: {
  rows: Row[];
  total: number;
  page: number;
  size: number;
  loading: boolean;
  onPageChange: (page: number, size: number) => void;
}) {
  const [selected, setSelected] = useState<Row | null>(null);
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
    <Box>
      <Box sx={{ height: 520, width: "100%", bgcolor: "background.paper" }}>
        <DataGrid
          rows={rows}
          columns={columns}
          getRowId={(r) => String(r.seq)}
          localeText={ptBR.components.MuiDataGrid.defaultProps.localeText}
          pageSizeOptions={[10, 25, 50, 100]}
          paginationMode="server"
          rowCount={total}
          loading={loading}
          paginationModel={{ page, pageSize: size }}
          onPaginationModelChange={(m) => onPageChange(m.page, m.pageSize)}
          disableRowSelectionOnClick
          onRowClick={(p) => setSelected(p.row as Row)}
          onCellKeyDown={(p, e) => {
            if (e.key === "Enter") setSelected(p.row as Row);
          }}
        />
      </Box>
      <Dialog
        open={!!selected}
        onClose={() => setSelected(null)}
        fullWidth
        maxWidth="lg"
      >
        <DialogTitle>Detalhes do registro {selected?.seq}</DialogTitle>
        <DialogContent>
          {selected && (
            <RecordDetails key={String(selected.seq)} row={selected} />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSelected(null)}>Fechar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
