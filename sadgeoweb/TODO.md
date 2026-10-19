# Notas legadas — preservadas para referência

O plano vigente de evolução está em [TODO / milestones](../TODO.md), com status e critérios de aceite. As anotações abaixo são históricas, inclusive referências ao Vaadin/EAP; não indicam que essas tecnologias devam ser reinstaladas ou que os itens já estejam implementados.

---


Geral
   -- Incluir o -javaagent:/opt/eap/modules/com/microsoft/applicationinsights/main/applicationinsights-agent-3.1.1.jar na imagem Docker
   
MainLayout
  - Incluir cabeçalho com login/logout
  - Incluir rodape com versão e copyright
  - Incluir logo SADGEO
  - Teste de responsividade Notebook, Celular, Browsers
  
DashboardView
  - ajustar PainelResumo para ter espaço H entre os badge, reduzir tamanhos e fonte em 50%
  - colocar um hr 
  - grafico de cubo te, que ter moldura (borda) reduzir altura em 25%. Melhorar o padrão dos combos (Style)
  - tabela de fatos não aparece no grid. Pode excluir.
  - tabela de resumo analitico está com rolagem e apenas 1 registro visivel, colocar 5 linhas,  ajustar H do cabeçalho eduzir 15%
  
NEW Login/Logout
  - DTO, Entity, View BD, Repository para usuario, perfis,
  - Classe Service Autenticação LDAP  
  - Classe service 
  

NEW Levantamento de campo -> Importar SIDGEO
  - vai como status_vrf =1.     somente mesmo projeto e campanha.    Anotador/ ue é do arquvio sidgeo.     Validar os dados.
  - Ver campos ausentes SIDGEO <-> SADGEO para essa etapa.  
  - Previsualizar antes de salvar na base.
    
NEW Levantamento de campo -> Importar Imagem
  - Permitir trocar imagem. Tem que extrair metadados.
  
NEW Editar Itens Levantamento

registro
├── EstacaoItemCampanhaView
│
├── component
│   ├── EstacaoDrawer
│   ├── DadosGeraisTab
│   ├── CoordenadasTab
│   ├── FotosTab
│   ├── DocumentosTab
│   └── HistoricoTab
│
├── dto
│   ├── EstacaoGridDTO
│   └── EstacaoFiltroDTO
│
├── entity
│   └── SadgeoEntity
│
├── repository
│   └── SadgeoRepository
│
└── service
    └── EstacaoConsultaService
  