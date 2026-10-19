export type Screen = {
  label: string;
  path: string;
  kind:
    | "dashboard"
    | "records"
    | "table"
    | "pending"
    | "reports"
    | "integrations"
    | "help";
  context?: string;
  campanha?: string;
  table?: string;
  note?: string;
  milestone?: string;
};
export type MenuGroup = { label: string; items: Screen[] };
export const menus: MenuGroup[] = [
  {
    label: "Planejamento",
    items: [
      {
        label: "Campanha",
        path: "/planejamento/campanha",
        kind: "table",
        table: "campanha",
      },
    ],
  },
  {
    label: "Levantamento de Campo",
    items: [
      {
        label: "Recepção de Lotes",
        path: "/campo/lotes",
        kind: "pending",
        milestone: "M03",
      },
      {
        label: "Receber SIGCVEG",
        path: "/campo/sigcveg",
        kind: "pending",
        milestone: "M03",
      },
      {
        label: "Novo Registro",
        path: "/campo/novo-registro",
        kind: "pending",
        milestone: "M02",
      },
      {
        label: "Documentos da Estação",
        path: "/campo/documentos",
        kind: "pending",
        milestone: "M03",
      },
      {
        label: "Acompanhamento",
        path: "/campo/acompanhamento",
        kind: "pending",
        milestone: "M04",
      },

      {
        label: "Importar SIDGEO",
        path: "/campo/importar-sidgeo",
        kind: "pending",
        note: "A importação exige o contrato de arquivo e as regras de integração SIDGEO.",
      },
      {
        label: "Carregar Imagens",
        path: "/campo/imagens",
        kind: "pending",
        note: "O carregamento exige definir armazenamento, vínculo com estações e limites de arquivo.",
      },
      {
        label: "Crítica de Dados",
        path: "/campo/critica",
        kind: "records",
        context: "critica",
      },
    ],
  },
  {
    label: "Homologação",
    items: [
      {
        label: "Cadastro da Solicitação",
        path: "/homologacao/solicitacao",
        kind: "pending",
      },
      {
        label: "Registro de Processamento",
        path: "/homologacao/processamento",
        kind: "pending",
      },
      {
        label: "Realizar Homologação",
        path: "/homologacao/realizar",
        kind: "pending",
      },
    ],
  },
  {
    label: "Análise",
    items: [
      {
        label: "Altimetria",
        path: "/analise/altimetria",
        kind: "records",
        context: "altimetria",
        campanha: "medA",
      },
      {
        label: "Gravimetria",
        path: "/analise/gravimetria",
        kind: "records",
        context: "gravimetria",
        campanha: "medG",
      },
      {
        label: "Planimetria",
        path: "/analise/planimetria",
        kind: "records",
        context: "planimetria",
        campanha: "medP",
      },
      {
        label: "VRF",
        path: "/analise/vrf",
        kind: "records",
        context: "vrf",
        campanha: "vrf",
      },
      {
        label: "VEG",
        path: "/analise/veg",
        kind: "records",
        context: "veg",
        campanha: "veg",
      },
      {
        label: "OGR",
        path: "/analise/ogr",
        kind: "records",
        context: "ogr",
        campanha: "ogr",
      },
      {
        label: "Ajustes de Gabinete",
        path: "/analise/gabinete",
        kind: "records",
        context: "gabinete",
        campanha: "gab",
      },
    ],
  },
  {
    label: "Administração",
    items: [
      {
        label: "Auditoria",
        path: "/administracao/auditoria",
        kind: "pending",
        milestone: "M01",
      },
      {
        label: "Integrações",
        path: "/administracao/integracoes",
        kind: "integrations",
      },
      {
        label: "Modelos de Descrição",
        path: "/administracao/modelos",
        kind: "pending",
        milestone: "M02",
      },

      {
        label: "Perfil de Acesso",
        path: "/administracao/perfil",
        kind: "pending",
      },
      { label: "Usuário", path: "/administracao/usuario", kind: "pending" },
      {
        label: "Permissionamento",
        path: "/administracao/permissoes",
        kind: "pending",
      },
    ],
  },

  {
    label: "Integração BDG",
    items: [
      {
        label: "Aguardando Carga",
        path: "/bdg/aguardando",
        kind: "pending",
        milestone: "M06",
      },
      {
        label: "Em Processamento",
        path: "/bdg/processamento",
        kind: "pending",
        milestone: "M06",
      },
      {
        label: "Retornos e Rejeições",
        path: "/bdg/retornos",
        kind: "pending",
        milestone: "M06",
      },
      {
        label: "Reconciliação SADGEO × BDG",
        path: "/bdg/reconciliacao",
        kind: "pending",
        milestone: "M06",
      },
    ],
  },
  {
    label: "Qualidade e Produção",
    items: [
      {
        label: "Pendências e Devoluções",
        path: "/qualidade/pendencias",
        kind: "pending",
        milestone: "M04",
      },
      {
        label: "Ocorrências de Consistência",
        path: "/qualidade/ocorrencias",
        kind: "pending",
        milestone: "M07",
      },
      {
        label: "Verificações Programadas",
        path: "/qualidade/verificacoes",
        kind: "pending",
        milestone: "M07",
      },
      {
        label: "Análise de Produção",
        path: "/qualidade/producao",
        kind: "reports",
      },
      { label: "Exportações", path: "/qualidade/exportacoes", kind: "reports" },
    ],
  },
  {
    label: "Ajuda e Manuais",
    items: [
      { label: "Guia de Uso e Evolução", path: "/ajuda/guia", kind: "help" },
    ],
  },
  {
    label: "Tabelas básicas",
    items: [
      {
        label: "Pendências",
        path: "/tabelas/pendencia",
        kind: "table",
        table: "pendencia",
      },
      {
        label: "Localização",
        path: "/tabelas/localizacao",
        kind: "table",
        table: "localizacao",
      },
      {
        label: "NUE",
        path: "/tabelas/nue",
        kind: "pending",
        note: "Informe a tabela, as colunas e a chave de NUE para habilitar o cadastro.",
      },
      {
        label: "Códigos de Estação",
        path: "/tabelas/codigos-estacao",
        kind: "pending",
        note: "Informe a tabela, as colunas e a chave de Códigos de Estação.",
      },
      {
        label: "Tipo de Ocorrências",
        path: "/tabelas/tipo-ocorrencias",
        kind: "pending",
        note: "Informe a tabela, as colunas e a chave de Tipo de Ocorrências.",
      },
      {
        label: "Tipo de Projeto",
        path: "/tabelas/tipo-projeto",
        kind: "table",
        table: "tipo-projeto",
      },
      {
        label: "Situação do Marco",
        path: "/tabelas/situacao-marco",
        kind: "table",
        table: "situacao-marco",
      },
      {
        label: "Método de Cálculo",
        path: "/tabelas/metodo-calculo",
        kind: "table",
        table: "metodo-calculo",
      },
      {
        label: "Fonte de Coordenada",
        path: "/tabelas/fonte-coordenada",
        kind: "table",
        table: "fonte-coordenada",
      },
      {
        label: "Equipamento",
        path: "/tabelas/equipamento",
        kind: "table",
        table: "equipamento",
      },
      {
        label: "Atividade",
        path: "/tabelas/atividade",
        kind: "table",
        table: "atividade",
      },
      {
        label: "Status",
        path: "/tabelas/status",
        kind: "table",
        table: "status",
      },
      {
        label: "Município",
        path: "/tabelas/municipio",
        kind: "table",
        table: "municipio",
      },
    ],
  },
];
const detailScreens: { group: string; screen: Screen }[] = [
  {
    group: "Levantamento de Campo",
    screen: {
      label: "Mapa de Estações",
      path: "/campo/mapa",
      kind: "pending",
      milestone: "M02",
    },
  },
  {
    group: "Análise",
    screen: {
      label: "Prévia de Clonagem",
      path: "/campo/clonar",
      kind: "pending",
      milestone: "M05",
    },
  },
];
export function screenFor(path: string) {
  const detail = detailScreens.find((d) => d.screen.path === path);
  if (detail) return detail;
  for (const group of menus) {
    const screen = group.items.find((s) => s.path === path);
    if (screen) return { group: group.label, screen };
  }
  return undefined;
}
