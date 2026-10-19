import { useState } from "react";
import { Link } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  Chip,
  Tab,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";
import type { Row } from "../../Table";
import { downloadCsv } from "../../export";
const tabs = [
  "Dados gerais",
  "Coordenadas",
  "Fotos",
  "Documentos",
  "Pendências",
  "Histórico",
];
const labels: Record<string, string> = {
  seq: "Sequência do registro",
  campanha: "Campanha",
  projeto: "Projeto",
  uf: "UF",
  municipio: "Município",
  situacao: "Situação",
  tipoLocal: "Tipo de local",
  uorgOrigem: "Unidade de origem",
  anoLevantamento: "Ano do levantamento",
  mesLevantamento: "Mês",
  dataLevantamento: "Data do levantamento",
  contagem: "Contagem",
  diasAteEntrada: "Dias até entrada",
  diasAteCritica: "Dias até crítica",
  diasAtePublicacao: "Dias até publicação",
  diasAteCalculoCoord: "Dias até cálculo de coordenadas",
};
export default function RecordDetails({ row }: { row: Row }) {
  const [tab, setTab] = useState(0);
  const query = `?registro=${encodeURIComponent(String(row.seq))}`;
  return (
    <>
      <Box sx={{ display: "flex", gap: 1, mb: 2, flexWrap: "wrap" }}>
        <Chip label={`Campanha: ${row.campanha ?? "Não informada"}`} />
        <Chip
          label="Consulta — nenhuma alteração no registro"
          variant="outlined"
        />
      </Box>
      <Tabs
        value={tab}
        onChange={(_, v) => setTab(v)}
        variant="scrollable"
        scrollButtons="auto"
        aria-label="Abas do registro"
      >
        {tabs.map((t, i) => (
          <Tab
            key={t}
            label={t}
            id={`registro-tab-${i}`}
            aria-controls={`registro-panel-${i}`}
          />
        ))}
      </Tabs>
      <Box
        role="tabpanel"
        id={`registro-panel-${tab}`}
        aria-labelledby={`registro-tab-${tab}`}
        sx={{ py: 2 }}
      >
        {tab === 0 && (
          <>
            <Box
              component="dl"
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr" },
                gap: 2,
              }}
            >
              {Object.entries(row).map(([k, v]) => (
                <Box key={k}>
                  <Typography component="dt" variant="caption">
                    {labels[k] ?? k}
                  </Typography>
                  <Typography component="dd" sx={{ m: 0 }}>
                    {v ?? "—"}
                  </Typography>
                </Box>
              ))}
            </Box>
            <Button
              onClick={() =>
                downloadCsv([row], `sadgeo-registro-${row.seq}.csv`)
              }
            >
              Exportar registro CSV
            </Button>
          </>
        )}
        {tab === 1 && (
          <>
            <Alert severity="info">
              A consulta atual de fatos não fornece coordenadas nem a versão do
              BDG. Comparação e mapa dependem do milestone M02.
            </Alert>
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr" },
                gap: 2,
                my: 2,
              }}
            >
              {["BDG", "SADGEO"].map((source) => (
                <Box key={source}>
                  <Typography variant="h6">{source}</Typography>
                  {[
                    "Latitude",
                    "Longitude",
                    "Datum / SRID",
                    "Fonte e data",
                  ].map((f) => (
                    <TextField
                      disabled
                      fullWidth
                      size="small"
                      key={f}
                      label={f}
                      placeholder="Indisponível"
                      slotProps={{ inputLabel: { shrink: true } }}
                      sx={{ my: 1 }}
                    />
                  ))}
                </Box>
              ))}
            </Box>
            <Typography>
              Diferença: não calculada — dados de comparação indisponíveis.
            </Typography>
            <Button disabled>Comparar coordenadas</Button>
            <Button component={Link} to={"/campo/mapa" + query}>
              Abrir área do mapa
            </Button>
          </>
        )}
        {tab === 2 && (
          <>
            <Alert severity="info">
              Fotos do registro ainda não são fornecidas pela API. Galeria
              vinculada e substituição: M03.
            </Alert>
            <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", my: 2 }}>
              {["Panorâmica", "Chapa", "BDG", "Situação (VEG)"].map((c) => (
                <Chip key={c} label={c} variant="outlined" />
              ))}
            </Box>
            <Button component={Link} to={"/campo/imagens" + query}>
              Abrir prévia de imagens
            </Button>
          </>
        )}
        {tab === 3 && (
          <>
            <Alert severity="info">
              Acesso a fichas e cadernetas no GEDLivre depende de contrato
              institucional — M03.
            </Alert>
            <Button component={Link} to={"/campo/documentos" + query}>
              Abrir área de documentos
            </Button>
          </>
        )}
        {tab === 4 && (
          <>
            <Typography sx={{ mb: 2 }}>
              Situação informada na consulta: {row.situacao ?? "Não informada"}.
            </Typography>
            <Alert severity="info">
              Pendências operacionais e devoluções ainda não estão vinculadas ao
              registro. O cadastro de códigos de pendência é uma função
              separada.
            </Alert>
            <Button component={Link} to={"/qualidade/pendencias" + query}>
              Abrir área de pendências
            </Button>
          </>
        )}
        {tab === 5 && (
          <>
            <Alert severity="info">
              Histórico persistente de alterações e decisões previsto em
              M01/M02. Nenhum evento de auditoria fictício é apresentado.
            </Alert>
            <Typography sx={{ my: 2 }}>
              Data de levantamento informada:{" "}
              {row.dataLevantamento ?? "Não informada"}.
            </Typography>
          </>
        )}
      </Box>
      <Box
        sx={{
          display: "flex",
          gap: 1,
          flexWrap: "wrap",
          borderTop: 1,
          borderColor: "divider",
          pt: 2,
        }}
      >
        <Button disabled>Salvar rascunho</Button>
        <Button disabled>Devolver / Reter</Button>
        <Button disabled>Liberar</Button>
        <Button disabled>Clonar</Button>
        <Button disabled>Excluir registro</Button>
        <Button component={Link} to={"/campo/clonar" + query}>
          Prévia de clonagem
        </Button>
      </Box>
      <Typography variant="caption">
        Comandos do registro dependem da autorização, trilha e transições dos
        milestones M01–M05.
      </Typography>
    </>
  );
}
