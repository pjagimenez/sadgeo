# Manual do SADGEO

Sistematização e Análise de Dados Geodésicos

## Painel de Controle

A tela inicial é pública. Os totais aparecem em duas linhas de indicadores no desktop. O botão Atualizar dados refaz as consultas.

## Gráficos

Evolução anual e Consolidado por Ano e Campanha ignoram anos com todas as séries zeradas. Consulte os nomes das campanhas nas dicas da legenda. Consultar dados do gráfico abre a tabela, ordenada por ano decrescente, com dez linhas por página.

## Resumo analítico

Selecione ano, projeto, campanha e situação. Somente o ano inicia selecionado: janeiro a março usam o ano anterior; de abril em diante, o ano corrente. A busca textual permanece disponível e a tabela tem 25 linhas por página. Os filtros ficam em uma linha antes da busca. Clique no título de uma coluna para ordenar. As médias de dias estão agrupadas em quatro subcolunas. A rolagem horizontal superior acompanha a tabela.

## Fatos do Painel

Os registros são carregados por demanda, em páginas de 25 linhas, ordenados por ano e mês decrescentes. Use ano, mês, campanha, projeto, UF, município e UORG de origem, além da busca textual. Os filtros ficam em duas linhas, incluindo Situação, e os meses aparecem como JAN, FEV etc. Escolha ano antes do mês, campanha antes do projeto e UF antes do município. Clique em qualquer coluna para ordenar o resultado completo no servidor. Ao alterar o filtro pai, a seleção dependente é limpa.

## Navegação

Planejamento reúne Campanha, NUE e Códigos de Estação. Os grupos do menu podem permanecer abertos simultaneamente e compartilham uma área de rolagem. Ajuda desta tela explica o contexto atual; este Manual fica acima da ajuda no cabeçalho e o Guia de Uso e Evolução está no ícone junto à versão no rodapé.

## Login e manutenção

Faça login no cabeçalho para consultar módulos operacionais ou manter cadastros. Para sair, use Sair. Nunca informe credenciais institucionais na entrada de demonstração. Gravação de estações, crítica definitiva, importação, GED e carga BDG dependem dos milestones e não são executadas pelas prévias locais.

## Diagnóstico de login

Se o login estiver desabilitado, confira SADGEO_LDAP_HOST e SADGEO_LDAP_DOMAIN no processo Java. Reinicie o backend após alterar as ENVVARs. Consulte AUTH_CONFIG no console ou em logs/sadgeo.log. Uma falha de autenticação mostra a referência e a categoria correspondentes ao evento no log. Senhas e tokens não são incluídos no diagnóstico.
