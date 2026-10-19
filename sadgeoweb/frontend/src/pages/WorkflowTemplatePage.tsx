import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Chip,
  MenuItem,
  Paper,
  Step,
  StepLabel,
  Stepper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { useLocation } from "react-router-dom";
import type { Screen } from "../navigation";
type Blueprint = {
  intro: string;
  fields: string[];
  columns: string[];
  action: string;
  steps?: string[];
};
function blueprint(screen: Screen, group: string): Blueprint {
  const path = screen.path;
  if (path === "/campo/clonar")
    return {
      intro:
        "Prévia local de clonagem. Origem/destino e campos copiáveis precisam de autorização; nenhum identificador, histórico ou liberação será copiado nesta versão.",
      fields: [
        "Registro de origem (sequência)",
        "Estação de destino",
        "Campos propostos",
        "Justificativa",
      ],
      columns: ["Campo", "Origem", "Destino"],
      action: "Confirmar clonagem",
    };
  if (path === "/campo/mapa")
    return {
      intro:
        "Área visual do mapa da estação. Sem coordenadas e referência espacial no contrato atual, não são desenhados marcadores nem acessadas camadas externas.",
      fields: ["Registro", "Campanha", "Datum / SRID", "Fonte"],
      columns: ["Registro", "Latitude", "Longitude", "Referência"],
      action: "Carregar mapa",
    };
  if (path === "/campo/novo-registro")
    return {
      intro:
        "Preparação visual do editor de estação. A prévia fica somente nesta tela e não cadastra nem altera uma estação.",
      fields: [
        "Código da Estação",
        "Campanha",
        "Projeto",
        "UF",
        "Município",
        "Descrição",
      ],
      columns: ["Estação", "Campanha", "Situação"],
      action: "Salvar estação no Oracle",
      steps: ["Dados gerais", "Coordenadas", "Anexos", "Validação"],
    };
  if (path === "/administracao/modelos")
    return {
      intro:
        "Prévia local de modelo descritivo por tipo de monumento. A tabela e as regras de aplicação dos modelos ainda precisam ser confirmadas.",
      fields: ["Tipo de Monumento", "Descrição-base"],
      columns: ["Tipo", "Modelo", "Versão"],
      action: "Publicar modelo",
    };
  if (
    ["/campo/lotes", "/campo/importar-sidgeo", "/campo/sigcveg"].includes(path)
  )
    return {
      intro:
        "Área de recepção e conferência de lotes. É possível selecionar um arquivo local para conferir nome e tamanho; ele não será enviado, processado nem importado.",
      fields: ["Projeto", "Campanha", "Instituição", "Unidade de origem"],
      columns: ["Linha", "Estação", "Campanha", "Validação", "Mensagem"],
      action: "Confirmar importação",
      steps: ["Origem", "Leitura e prévia", "Validação", "Confirmação"],
    };
  if (path === "/campo/imagens")
    return {
      intro:
        "Prévia local de foto e categoria. A imagem não é enviada ao servidor; associação, substituição e extração de metadados dependem do fluxo de anexos.",
      fields: ["Código da Estação", "Legenda"],
      columns: ["Categoria", "Arquivo", "Origem", "Data"],
      action: "Enviar imagem",
    };
  if (path === "/campo/documentos")
    return {
      intro:
        "Área preparada para fichas e cadernetas vinculadas à estação. Não há consulta nem escrita no GEDLivre nesta versão.",
      fields: ["Código da Estação", "Tipo de Documento"],
      columns: ["Documento", "Tipo", "Origem", "Identificador GED"],
      action: "Abrir GEDLivre",
    };
  if (path === "/campo/acompanhamento")
    return {
      intro:
        "Área de acompanhamento da unidade, somente consulta. A seleção de unidade e estágios exige a matriz de permissões e o mapeamento do fluxo; nenhum total fictício é apresentado.",
      fields: ["Unidade", "Campanha", "Etapa", "Período"],
      columns: [
        "Estação",
        "Unidade",
        "Etapa",
        "Última liberação",
        "Atualização BDG",
      ],
      action: "Carregar acompanhamento",
    };
  if (group === "Integração BDG")
    return {
      intro:
        "Fila preparada para integrar o retorno oficial do BDG. Sem contrato e confirmação de carga, esta tela não envia registros nem os marca como atualizados.",
      fields: ["Campanha", "Lote", "Situação"],
      columns: [
        "Registro",
        "Lote",
        "Tentativa",
        "Protocolo",
        "Resultado",
        "Mensagem",
      ],
      action: path.endsWith("retornos")
        ? "Reprocessar lote"
        : "Executar operação BDG",
      steps: ["Elegível", "Enviado", "Processado", "Confirmado"],
    };
  if (group === "Qualidade e Produção")
    return {
      intro:
        "Área de tratamento de ocorrências e verificação de consistência. Regras, responsáveis e armazenamento de resultados serão implementados no marco indicado.",
      fields: ["Campanha", "Unidade", "Regra", "Prioridade"],
      columns: [
        "Registro",
        "Regra / Pendência",
        "Evidência",
        "Responsável",
        "Situação",
      ],
      action: path.endsWith("verificacoes")
        ? "Agendar verificação"
        : "Registrar tratamento",
    };
  if (group === "Homologação")
    return {
      intro:
        "Fluxo visual de homologação. A relação com solicitação, processamento, crítica e carga precisa ser definida com a área de negócio antes de executar decisões.",
      fields: [
        "Solicitação",
        "Estação",
        "Processamento",
        "Responsável",
        "Observação",
      ],
      columns: ["Solicitação", "Estação", "Processamento", "Situação", "Data"],
      action: "Confirmar homologação",
      steps: ["Solicitação", "Processamento", "Análise", "Decisão"],
    };
  if (group === "Administração")
    return {
      intro:
        "Estrutura da administração institucional. Esta tela não cria usuários, não concede perfis e não apresenta eventos de auditoria que ainda não foram registrados.",
      fields: path.endsWith("auditoria")
        ? ["Usuário", "Ação", "Registro", "Período"]
        : ["Usuário institucional", "Perfil", "Unidade", "Tema"],
      columns: path.endsWith("auditoria")
        ? ["Data/hora", "Usuário", "Ação", "Registro", "Motivo"]
        : ["Usuário", "Perfil", "Unidade", "Tema", "Permissão"],
      action: path.endsWith("auditoria")
        ? "Consultar auditoria"
        : "Aplicar permissões",
    };
  return {
    intro:
      screen.note ??
      "Cadastro preparado visualmente; falta confirmar a tabela e os campos antes de conectar ao Oracle.",
    fields: ["Código", "Descrição"],
    columns: ["Código", "Descrição"],
    action: "Salvar cadastro",
  };
}
export default function WorkflowTemplatePage({
  screen,
  group,
}: {
  screen: Screen;
  group: string;
}) {
  const reference = new URLSearchParams(useLocation().search).get("registro");
  const model = blueprint(screen, group);
  const milestone =
    screen.milestone ??
    (group === "Homologação"
      ? "Trilha H"
      : group === "Administração"
        ? "M01"
        : "Definição de tabela");
  const [values, setValues] = useState<Record<string, string>>({});
  const [preview, setPreview] = useState(false);
  const [file, setFile] = useState<File>();
  const [imageUrl, setImageUrl] = useState("");
  const [error, setError] = useState("");
  const [category, setCategory] = useState("Panorâmica");
  const image = screen.path === "/campo/imagens";
  const intake = [
    "/campo/lotes",
    "/campo/importar-sidgeo",
    "/campo/sigcveg",
  ].includes(screen.path);
  const draft = [
    "/campo/novo-registro",
    "/administracao/modelos",
    "/campo/clonar",
  ].includes(screen.path);
  useEffect(() => {
    if (!file || !image) {
      setImageUrl("");
      return;
    }
    const url = URL.createObjectURL(file);
    setImageUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file, image]);
  function selectFile(f?: File) {
    setError("");
    if (
      f &&
      image &&
      !["image/jpeg", "image/png", "image/webp"].includes(f.type)
    ) {
      setError("Para a prévia local, selecione JPEG, PNG ou WebP.");
      setFile(undefined);
      return;
    }
    setFile(f);
  }
  return (
    <Box component="main" className="portal-content">
      <Typography className="eyebrow">{group}</Typography>
      <Typography component="h1" variant="h4">
        {screen.label}
      </Typography>
      <Box sx={{ display: "flex", gap: 1, my: 2, flexWrap: "wrap" }}>
        <Chip
          label="Template disponível • integração pendente"
          color="warning"
        />
        <Chip label={`Milestone: ${milestone}`} variant="outlined" />
      </Box>
      {reference && (
        <Chip label={`Registro de referência: ${reference}`} sx={{ mb: 2 }} />
      )}
      <Alert severity="info">{model.intro}</Alert>
      {screen.path === "/campo/mapa" && (
        <Paper
          variant="outlined"
          sx={{
            my: 2,
            p: 4,
            minHeight: 240,
            display: "grid",
            placeItems: "center",
            backgroundImage:
              "linear-gradient(#dfe4ec 1px,transparent 1px),linear-gradient(90deg,#dfe4ec 1px,transparent 1px)",
            backgroundSize: "24px 24px",
          }}
        >
          <Alert severity="info">
            Mapa não conectado — aguardando coordenadas, SRID e provedor.
          </Alert>
        </Paper>
      )}
      {model.steps && (
        <Stepper
          activeStep={0}
          alternativeLabel
          sx={{ my: 3, overflowX: "auto" }}
        >
          {model.steps.map((s) => (
            <Step key={s}>
              <StepLabel>{s}</StepLabel>
            </Step>
          ))}
        </Stepper>
      )}
      <Paper variant="outlined" sx={{ p: 2, my: 2 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          {draft ? "Rascunho local" : "Contexto da operação"}
        </Typography>
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
            gap: 2,
          }}
        >
          {model.fields.map((field) => (
            <TextField
              key={field}
              label={field}
              value={values[field] ?? ""}
              onChange={(e) =>
                setValues({ ...values, [field]: e.target.value })
              }
              multiline={field.includes("Descrição") || field === "Observação"}
              minRows={field.includes("Descrição") ? 3 : 1}
              size="small"
            />
          ))}
        </Box>
        {image && (
          <TextField
            select
            label="Categoria da foto"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            size="small"
            sx={{ my: 2, minWidth: 220 }}
          >
            {["Panorâmica", "Chapa", "Atual do BDG", "Situação (VEG)"].map(
              (c) => (
                <MenuItem key={c} value={c}>
                  {c}
                </MenuItem>
              ),
            )}
          </TextField>
        )}
        {(image || intake) && (
          <Box sx={{ my: 2 }}>
            <Button component="label" variant="outlined">
              Selecionar arquivo local
              <input
                aria-label="Arquivo para prévia local"
                type="file"
                hidden
                accept={image ? "image/jpeg,image/png,image/webp" : undefined}
                onChange={(e) => selectFile(e.target.files?.[0])}
              />
            </Button>
            {file && (
              <Typography sx={{ mt: 1 }}>
                {file.name} • {file.size.toLocaleString("pt-BR")} bytes • não
                enviado
              </Typography>
            )}
          </Box>
        )}
        {error && <Alert severity="error">{error}</Alert>}
        {imageUrl && (
          <Box component="figure" sx={{ m: 0, my: 2 }}>
            <Box
              component="img"
              src={imageUrl}
              alt={`Prévia local: ${category}`}
              sx={{ maxWidth: "100%", maxHeight: 360, objectFit: "contain" }}
            />
            <Typography component="figcaption" variant="caption">
              Prévia local — não vinculada nem gravada.
            </Typography>
          </Box>
        )}
        <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", mt: 2 }}>
          {draft && (
            <Button variant="outlined" onClick={() => setPreview(true)}>
              Pré-visualizar rascunho
            </Button>
          )}
          <Button disabled variant="contained">
            {model.action}
          </Button>
          <Button
            onClick={() => {
              setValues({});
              setFile(undefined);
              setPreview(false);
              setError("");
            }}
          >
            Limpar prévia
          </Button>
        </Box>
        <Typography variant="caption" component="p" sx={{ mt: 2 }}>
          A operação definitiva depende de {milestone}. Os campos desta prévia
          não são persistidos e são descartados ao sair da tela.
        </Typography>
      </Paper>
      {draft && preview && (
        <Paper variant="outlined" sx={{ p: 2, my: 2 }}>
          <Typography variant="h6">Prévia do rascunho — não salvo</Typography>
          <Box component="dl">
            {model.fields.map((f) => (
              <Box key={f} sx={{ my: 1 }}>
                <Typography component="dt" fontWeight={600}>
                  {f}
                </Typography>
                <Typography
                  component="dd"
                  sx={{ m: 0, whiteSpace: "pre-wrap" }}
                >
                  {values[f] || "Não informado"}
                </Typography>
              </Box>
            ))}
          </Box>
        </Paper>
      )}
      <Paper variant="outlined" sx={{ p: 2, overflowX: "auto" }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Área de resultados
        </Typography>
        <Table size="small">
          <TableHead>
            <TableRow>
              {model.columns.map((c) => (
                <TableCell key={c}>{c}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell colSpan={model.columns.length}>
                Resultados indisponíveis: integração ainda não implementada.
                Esta tabela não representa uma fila vazia no sistema de origem.
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Paper>
    </Box>
  );
}
