# SADGEO 0.2.0

A 0.2 preserva a base React + Spring Boot e acrescenta o menu operacional, cadastros, consultas e interfaces propostas nos documentos. **Telas geradas não equivalem a integrações concluídas.**

## Funcionalidades disponíveis

- Painel de Controle padrão, rodapé `0.2.YYYYMMDD-HH`, profile/hostname e identificação/login/logout no menu inferior.
- Crítica de Dados e sete análises no mesmo template, com filtro CAMPANHA fixo aplicado pela API, pesquisa e paginação.
- Detalhe em abas: Dados Gerais, Coordenadas, Fotos, Documentos, Pendências e Histórico. Os dados disponíveis são os fatos atuais; abas sem contrato de dados mostram indisponibilidade.
- Campanha com chave composta e dez tabelas básicas, incluindo Localização e Pendências, com CRUD, validação, CSRF e restrição de manutenção Oracle.
- Análise de Produção e Exportações: filtros cumulativos por campanha, período anual e texto; CSV de todos os grupos filtrados. Registro e página de consulta também podem ser exportados em CSV.
- CSV com campos delimitados/escapados e proteção contra fórmulas de planilha; precisão de números grandes preservada como texto.
- Estado das integrações: health da aplicação e presença de configuração LDAPS, distinguindo “configurado” de “conectado”. Nenhuma senha/token é retornada.
- Guia de Uso e Evolução, com links de navegação e TODO.
- Scripts de testes curl e PowerShell 7+ que usam sessão/CSRF e só fazem CRUD automatizado em demo.

## Novas telas geradas, sem executar mudanças no processo

| Área | O que pode ser feito na 0.2 | O que permanece pendente |
|---|---|---|
| Recepção de Lotes / SIDGEO / SIGCVEG | Selecionar arquivo local e conferir nome/tamanho; visualizar etapas e tabela de resultados | Ler/validar formato, deduplicar e importar — M03 |
| Novo Registro | Preencher e pré-visualizar rascunho local | Salvar estação e aplicar regras de negócio — M01/M02 |
| Imagens | Selecionar JPEG/PNG/WebP e visualizar localmente por categoria | Upload, associação, substituição e metadados persistentes — M03 |
| Documentos | Campos de contexto e estrutura para fichas/cadernetas | Consulta/escrita GEDLivre — M03 |
| Coordenadas / mapa | Abas, comparação visual preparada e área do mapa sem marcadores fictícios | Coordenadas, SRID, provedor, cálculo e confirmação — M02 |
| Clonagem / modelos | Prévia local de campos/texto e referência de origem | Copiar/gravar/aplicar automaticamente — M02/M05 |
| Acompanhamento | Estrutura de filtros e resultado | Escopo por unidade e etapas liberadas — M01/M04 |
| Homologação | Três telas, etapas, filtros/campos e estrutura de resultados | Fluxo próprio e decisões — Trilha H |
| BDG | Quatro telas de fila, processamento, retorno e reconciliação | Envio, reenvio, confirmação e atualização — M06 |
| Qualidade e pendências operacionais | Telas de ocorrências, devoluções e programação | Regras, agenda, responsáveis e tratamento persistente — M04/M07 |
| Administração / auditoria | Telas de usuário, perfil, permissionamento e eventos | Modelo institucional, concessão de direitos e auditoria persistente — M01 |
| NUE / Códigos de Estação / Tipo de Ocorrências | Formulários e tabela visual | Nomes/colunas/chaves para conexão Oracle |

Prévia local é descartada ao sair da tela: não faz upload, não salva em localStorage e não muda Oracle. Os botões definitivos ficam desabilitados, com o milestone indicado. Dados indisponíveis não aparecem como contagens zero de filas reais.

## Limites da entrega

- Não grava, libera, retém, devolve, clona nem exclui registros de estação. O CRUD disponível é de códigos básicos/Campanha.
- Não executa carga ou publicação BDG, escrita GEDLivre nem importação SIDGEO/SIGCVEG.
- Não inventa coordenadas, fotos vinculadas, histórico ou eventos operacionais.
- CSV é uma exportação da consulta, não os formatos oficiais TXT/KMZ/relatório simplificado/CoordDalti.
- Planejamento e execução física de campo continuam externos. A tela Campanha é cadastro de referência.
- Oracle/AD/BDG institucionais ainda precisam de validação real. Demonstração, mocks e H2 não comprovam essas integrações.

## Como executar

```sh
cd sadgeoweb
mvn clean verify
java -jar target/sadgeo-0.2.0.jar --spring.profiles.active=demo
```

Em outro terminal, na raiz do checkout:

```sh
bash scripts/test-api.sh http://127.0.0.1:8080 --crud
```

Ou:

```powershell
pwsh -NoProfile -File scripts/Test-Api.ps1 -BaseUrl http://127.0.0.1:8080 -Crud
```

Para dados institucionais, siga as ENVVARs e pré-requisitos do [README](../README.md). O [TODO](../TODO.md) mantém os marcos de impacto, as dependências e os critérios de aceite.
