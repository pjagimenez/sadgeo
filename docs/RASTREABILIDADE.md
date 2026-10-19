# Rastreabilidade das propostas e pendências de especificação

## Fontes analisadas

Os documentos recebidos foram usados como material de requisitos e referência AS-IS. Referências internas, links e instruções neles contidos não foram executados. Os arquivos originais e as capturas com dados identificáveis não foram adicionados ao GitHub.

| Referência | Documento enviado | Uso |
|---|---|---|
| R | `SADGEO_01_ListaDeRequisitos.docx` | ReqF01–14, ReqNF01–05; histórico indica revisão 1.1 em 12/11/2024 |
| E | `SADGEO_02_EstágiosProcessoDeProdução.docx` | Cinco estágios, delimitação dentro/fora do sistema |
| U | `SADGEO_03_CasosDeUso.docx` | UC01–19, atores, fluxos e exceções |
| W | `SADGEO_WireFrame_Visão_AS-IS 2.docx` | Telas de lista/detalhe, inserção por registro/arquivo, documentos, mapas, fotos, exportação, exclusão, clonagem e comparação de coordenadas; dez imagens analisadas/inventariadas |
| Q | `Quebra-telas-SADGEO 1.odt` | Hipóteses sobre IDs, abas e modais; não é contrato funcional confirmado |
| S | Solicitações desta conversa | Menus, códigos CAMPANHA, tabelas/PK Campanha, Pendências, layout e cinco estágios reiterados pelo usuário |
| L | `sadgeoweb/TODO.md` legado | Observações históricas de importação SIDGEO, fotos, responsividade e abas; não comprova implementação |

Os estágios e requisitos de 2024 são a base de análise; a versão documental “2.x” não altera o nome da versão técnica 0.2 do novo aplicativo.

## Requisitos funcionais

“Parcial” indica uma base demonstrável, sem equivaler ao aceite operacional completo. “Proposto” indica operação no backlog; a 0.2 já gera a tela correspondente quando não depende de efeitos no processo. M00–M08 e a trilha H estão descritos no [TODO](../TODO.md).

| Requisito | UC relacionado | Situação na 0.2 | Evolução e tela | Marco |
|---|---|---|---|---|
| ReqF01 — Inserção descritiva | UC02 | Proposto; CRUD de códigos não cadastra estação | Editor por abas, busca BDG, modelos descritivos, recepção SIGCVEG | M02–M03 |
| ReqF02 — Validação/crítica | UC03 | Consulta, sem comandos de crítica | Salvar, complementar, reter/devolver/liberar e histórico | M01/M04/M05 |
| ReqF03 — Acesso | UC01/17 | Parcial: sessão/demo e AD configurável | Validar LDAPS real, timeout institucional e escopos | M00–M01 |
| ReqF04 — Perfis | UC10/18 | Proposto; allowlist de cadastros é provisória | Perfis/unidades/temas; PROJ e acompanhamento somente leitura | M01/M04/M05 |
| ReqF05 — Visualização | UC04 | Parcial: busca, projeto, campanha e paginação | Filtros cumulativos por unidade/status/atributos e contagem autorizada | M02/M04 |
| ReqF06 — Exportação | UC05 | CSV de consulta na 0.2; formatos oficiais propostos | TXT, KMZ, relatório simplificado e CoordDalti | M05 |
| ReqF07 — Fotos | UC06/12 | Prévia local e abas; associação/upload propostos | Galeria por categoria, upload/substituição e validações | M03 |
| ReqF08 — Mapa | UC07 | Proposto | Visualização e comparação espacial do registro | M02 |
| ReqF09 — Qualidade em duas instâncias | UC03 | Proposto | Fluxo com atores distintos, bloqueios e transições auditadas | M01/M04/M05 |
| ReqF10 — BDGMapaWeb | UC07 (complemento) | Proposto | Consulta de estações/camadas, contrato a confirmar | M02; complemento posterior se necessário |
| ReqF11 — GEDLivre | UC08/13 | Proposto | Fichas/cadernetas; escrita depende de contrato específico | M03 |
| ReqF12 — Consistência pós-produção | UC09 | Proposto | Agenda de verificações, ocorrências e relatório de evidências | M07 |
| ReqF13 — Clonagem | UC15 | Proposto | Prévia, origem/destino, whitelist de campos e permissão PROJ | M05 |
| ReqF14 — Exclusão de registro | UC14 | Proposto; exclusão em código básico é outra operação | Dependências, confirmação, justificativa e trilha | M02/M05 |

UC11 (painel) é parcialmente atendido pelo painel atual, mas falta personalização autorizada por unidade/tema. UC16 (histórico) tem aba visual, mas eventos persistentes permanecem em M01/M02. UC19 tem consulta analítica e CSV na 0.2; ampliar a análise por escopo e produção permanece em M05/M07. UC18 não deve ser considerado concluído apenas porque o usuário clica num menu de campanha: falta escopo, limpeza da seleção e aplicação de permissões.

## Requisitos não funcionais

| Requisito | Evidência atual | Aceite futuro necessário |
|---|---|---|
| ReqNF01 — Segurança | Sessão, CSRF, LDAPS configurável, manutenção de cadastros restrita | Autorização por registro/unidade/tema, auditoria, expiração e teste institucional |
| ReqNF02 — Usabilidade | Material UI, template compartilhado, responsividade básica testada | Sessões de uso por cadastrador/crítico/PROJ, teclado e fluxos completos |
| ReqNF03 — Desempenho | Paginação na nova consulta e nos cadastros | Volume e concorrência representativos; metas acordadas antes de medir |
| ReqNF04 — Disponibilidade | Health e build reproduzível | Operação 24/7, manutenção programada, recuperação e monitoração; não comprovadas por teste local |
| ReqNF05 — Escalabilidade | Frontend estático no JAR e API separável | Testes de carga e estratégia de sessão/replicação, filas e tarefas agendadas |

## Divergências a resolver com a área de negócio

| ID | Evidência | Encaminhamento proposto |
|---|---|---|
| D01 | E, estágio 3, menciona “segunda e terceira crítica”; ReqF09 e UC03 descrevem duas | Planejar duas instâncias inicialmente; terceira só após definição formal de ator, condição e retorno |
| D02 | UC03 impede que quem inseriu/criticou anteriormente faça a crítica; estágio 3 atribui primeira crítica a agentes de campo | Confirmar separação de pessoas dentro da mesma unidade e eventuais exceções; não liberar autoaprovação por conveniência |
| D03 | UC08/13 citam ReqF10 para GEDLivre; em R, ReqF10 é BDGMapaWeb e ReqF11 é GEDLivre | Manter os IDs originais; usar ReqF11 como mapeamento proposto e registrar a correção documental |
| D04 | UC13 descreve gravar no GEDLivre, mas seu fluxo lista visualizar/download | Separar consulta de escrita e só implementar escrita após confirmar contrato, permissão e identificador de retorno |
| D05 | UC12 é “Visualizar Fotos”, mas inclui upload, já previsto em UC06 | Uma galeria comum, distinguindo permissão de visualizar/manter; não atribuir upload a todos os leitores |
| D06 | UC14 remete a ReqF09, mas R define exclusão em ReqF14 | Rastrear a exclusão por ReqF14 e registrar a divergência original |
| D07 | Q usa “possivelmente/provavelmente”; `#signup` é hipótese de inscrição | Não criar autocadastro público nem inferir tabelas de usuário por IDs HTML |
| D08 | Planejamento/execução são externos em E; a conversa solicita menu Planejamento/Campanha | Manter cadastro e referências da campanha; módulo completo de áreas/equipes é opcional, dependente de integração e necessidade |
| D09 | Homologação está no menu solicitado, sem fluxo detalhado nas fontes R/U | Especificar trilha H; não usar “Homologar” como sinônimo de liberar 2ª crítica ou carregar BDG |
| D10 | ReqF04 permite leitura de outros temas para PROJ, com clonagem como única ação adicional | Modelar permissões de origem/destino e escopo; nunca conceder edição irrestrita por trocar o filtro |
| D11 | UC17 cita inatividade não superior a 2h; o parâmetro operacional ainda não foi acordado | Definir timeout configurável dentro do limite e testar expiração; não marcar como implementado apenas por existir logout |
| D12 | ReqF08 menciona Google Maps; ReqF10 adiciona BDGMapaWeb | Confirmar provedor, contrato, política de acesso e uso de coordenadas/SRID antes de escolher SDK/licença |

## Rastreabilidade dos estágios e ações

- Estágio 1: cadastro de campanha existente; planejamento real e coleta permanecem externos.
- Estágio 2: M02/M03 — edição, recepção, prévia, fotos e documentos; SIGCVEG é citado em ReqF01, SIDGEO no AS-IS/solicitação/notas legadas.
- Estágio 3: M01/M04/M05 — permissões, auditoria, duas instâncias e acompanhamento. Fonte principal: ReqF02/04/09 e UC03.
- Estágio 4: M05/M06 — exportações e fila de carga/retorno; publicação depende de política institucional. Estágio não prova a existência de uma API BDG específica.
- Estágio 5: M07/M08 — verificações, operação, recuperação e treinamento.

Os marcos são uma proposta de sequência, não datas, custos ou compromissos com terceiros. A implementação deve começar pelo próximo marco aceito, sem tratar hipóteses documentais como regras de banco confirmadas.
