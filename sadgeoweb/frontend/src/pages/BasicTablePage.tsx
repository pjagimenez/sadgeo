import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import { ptBR } from "@mui/x-data-grid/locales";
import { request } from "../api";
type Values = Record<string, string | null>;
type Field = {
  name: string;
  label: string;
  type: string;
  maxLength: number;
  nullable: boolean;
};
type Meta = {
  id: string;
  title: string;
  table: string;
  fields: Field[];
  keys: string[];
  canWrite: boolean;
};
type Page = {
  meta: Meta;
  items: Values[];
  total: number;
  page: number;
  size: number;
};
function inputValue(value: string | null | undefined, field: Field) {
  if (value == null) return "";
  if (field.type === "date" && value.length === 10) return value + "T00:00";
  return String(value);
}
export default function BasicTablePage({
  table,
  group,
}: {
  table: string;
  group: string;
}) {
  const [data, setData] = useState<Page>();
  const [q, setQ] = useState("");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const [size, setSize] = useState(25);
  const [attempt, setAttempt] = useState(0);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editing, setEditing] = useState<Values | null | undefined>(undefined);
  const [values, setValues] = useState<Record<string, string>>({});
  const [removing, setRemoving] = useState<Values>();
  const [busy, setBusy] = useState(false);
  const [formError, setFormError] = useState("");
  useEffect(() => {
    let active = true;
    setError("");
    request<Page>(
      `/api/tabelas/${table}?${new URLSearchParams({ page: String(page), size: String(size), q: search })}`,
    )
      .then((d) => {
        if (active) setData(d);
      })
      .catch((e) => {
        if (active) setError(e.message);
      });
    return () => {
      active = false;
    };
  }, [table, page, size, search, attempt]);
  const meta = data?.meta;
  function key(row: Values) {
    return Object.fromEntries((meta?.keys ?? []).map((k) => [k, row[k]]));
  }
  function open(row: Values | null) {
    if (!meta) return;
    setEditing(row);
    setFormError("");
    setValues(
      Object.fromEntries(
        meta.fields.map((f) => [f.name, inputValue(row?.[f.name], f)]),
      ),
    );
  }
  async function save() {
    if (!meta) return;
    setBusy(true);
    setFormError("");
    try {
      const payload = Object.fromEntries(
        meta.fields
          .filter((f) =>
            editing
              ? !meta.keys.includes(f.name) &&
                values[f.name] !== inputValue(editing[f.name], f)
              : values[f.name] !== "" || !f.nullable,
          )
          .map((f) => [f.name, values[f.name] === "" ? null : values[f.name]]),
      );
      await request(
        `/api/tabelas/${table}`,
        editing ? "PUT" : "POST",
        editing ? { key: key(editing), values: payload } : payload,
      );
      setEditing(undefined);
      setSuccess("Registro salvo com sucesso.");
      setAttempt((a) => a + 1);
    } catch (e) {
      setFormError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function remove() {
    if (!removing) return;
    setBusy(true);
    setFormError("");
    try {
      await request(`/api/tabelas/${table}`, "DELETE", { key: key(removing) });
      setRemoving(undefined);
      setSuccess("Registro excluído.");
      setAttempt((a) => a + 1);
    } catch (e) {
      setFormError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  const columns: GridColDef[] = (meta?.fields ?? []).map((f) => ({
    field: f.name,
    headerName: f.label,
    width: f.name.includes("DSC") || f.name === "DESCRICAO" ? 260 : 170,
  }));
  columns.push({
    field: "_actions",
    headerName: "Ações",
    width: 220,
    sortable: false,
    renderCell: (p) => (
      <Box>
        <Button onClick={() => open(p.row)}>
          {meta?.canWrite ? "Editar" : "Consultar"}
        </Button>
        {meta?.canWrite && (
          <Button
            color="error"
            onClick={() => {
              setRemoving(p.row);
              setFormError("");
            }}
          >
            Excluir
          </Button>
        )}
      </Box>
    ),
  });
  return (
    <Box component="main" className="portal-content">
      <Typography className="eyebrow">{group}</Typography>
      <Typography component="h1" variant="h4">
        {meta?.title ?? "Cadastro"}
      </Typography>
      {meta && (
        <Paper variant="outlined" sx={{ p: 2, my: 2 }}>
          <Typography variant="body2">{meta.table}</Typography>
          <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", my: 1 }}>
            {meta.keys.map((k) => (
              <Chip key={k} label={`Chave: ${k}`} size="small" />
            ))}
          </Box>
          {!meta.canWrite && (
            <Alert severity="info">
              Consulta disponível. Manutenção exige chave primária confirmada e
              usuário autorizado.
            </Alert>
          )}
        </Paper>
      )}
      {error && (
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
      )}
      {success && (
        <Alert severity="success" onClose={() => setSuccess("")} sx={{ my: 2 }}>
          {success}
        </Alert>
      )}
      <Box
        component="form"
        onSubmit={(e) => {
          e.preventDefault();
          setSearch(q);
          setPage(0);
        }}
        sx={{ display: "flex", gap: 2, flexWrap: "wrap", my: 2 }}
      >
        <TextField
          label="Buscar no cadastro"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          size="small"
        />
        <Button type="submit">Pesquisar</Button>
        {meta?.canWrite && (
          <Button variant="contained" onClick={() => open(null)}>
            Novo registro
          </Button>
        )}
      </Box>
      <Box sx={{ height: 530, width: "100%", bgcolor: "background.paper" }}>
        <DataGrid
          rows={(data?.items ?? []).map((r, i) => ({
            ...r,
            _gridId: meta?.keys.length ? JSON.stringify(key(r)) : String(i),
          }))}
          columns={columns}
          getRowId={(r) => r._gridId}
          localeText={ptBR.components.MuiDataGrid.defaultProps.localeText}
          paginationMode="server"
          rowCount={data?.total ?? 0}
          paginationModel={{ page, pageSize: size }}
          pageSizeOptions={[10, 25, 50, 100]}
          onPaginationModelChange={(m) => {
            setPage(m.page);
            setSize(m.pageSize);
          }}
          disableRowSelectionOnClick
          loading={!data && !error}
        />
      </Box>
      <Dialog
        open={editing !== undefined}
        onClose={() => {
          if (!busy) setEditing(undefined);
        }}
        fullWidth
        maxWidth="md"
      >
        <DialogTitle>
          {editing
            ? meta?.canWrite
              ? "Editar"
              : "Consultar"
            : "Novo registro"}{" "}
          — {meta?.title}
        </DialogTitle>
        <Box
          component="form"
          onSubmit={(e) => {
            e.preventDefault();
            save();
          }}
        >
          <DialogContent>
            {formError && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {formError}
              </Alert>
            )}
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr" },
                gap: 2,
                pt: 1,
              }}
            >
              {meta?.fields.map((f) => (
                <TextField
                  key={f.name}
                  label={f.label}
                  helperText={
                    f.name + (meta.keys.includes(f.name) ? " • chave" : "")
                  }
                  value={values[f.name] ?? ""}
                  onChange={(e) =>
                    setValues({ ...values, [f.name]: e.target.value })
                  }
                  required={!f.nullable}
                  type={f.type === "date" ? "datetime-local" : "text"}
                  slotProps={{
                    inputLabel: { shrink: true },
                    htmlInput: {
                      maxLength: f.type === "text" ? f.maxLength : undefined,
                      inputMode: ["number", "money", "integer"].includes(f.type)
                        ? "decimal"
                        : undefined,
                    },
                  }}
                  disabled={
                    busy ||
                    !meta.canWrite ||
                    (!!editing && meta.keys.includes(f.name))
                  }
                />
              ))}
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setEditing(undefined)} disabled={busy}>
              Fechar
            </Button>
            {meta?.canWrite && (
              <Button type="submit" variant="contained" disabled={busy}>
                Salvar
              </Button>
            )}
          </DialogActions>
        </Box>
      </Dialog>
      <Dialog
        open={!!removing}
        onClose={() => {
          if (!busy) setRemoving(undefined);
        }}
      >
        <DialogTitle>Excluir registro?</DialogTitle>
        <DialogContent>
          {formError && <Alert severity="error">{formError}</Alert>}Confirme a
          exclusão em {meta?.title}: {removing && JSON.stringify(key(removing))}
          . Registros referenciados por outras tabelas podem impedir a operação.
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRemoving(undefined)} disabled={busy}>
            Cancelar
          </Button>
          <Button color="error" disabled={busy} onClick={remove}>
            Confirmar exclusão
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
