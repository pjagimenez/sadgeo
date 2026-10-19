# Menus, campanhas e cadastros — SADGEO 0.2

## Navegação

A tela inicial autenticada é **Painel de Controle** (`/index`). `/registros` redireciona para `/campo/critica`.

| Grupo | Tela / rota | Comportamento |
|---|---|---|
| Planejamento | Campanha — `/planejamento/campanha` | CRUD de `T_CAMPANHA` |
| Levantamento de Campo | Importar SIDGEO, Carregar Imagens | Template de área de trabalho; operações de importação/armazenamento pendentes |
| Levantamento de Campo | Crítica de Dados — `/campo/critica` | Template de consulta, todas as campanhas |
| Homologação | Cadastro da Solicitação, Registro de Processamento, Realizar Homologação | Rotas e template; regras e operações pendentes |
| Análise | Altimetria, Gravimetria, Planimetria, VRF, VEG, OGR, Ajustes de Gabinete | Mesmo template de consulta, com campanha fixa |
| Administração | Perfil de Acesso, Usuário, Permissionamento | Rotas e template; manutenção de permissões institucionais pendente |
| Tabelas básicas | Cadastros abaixo | CRUD por metadados, sujeito à PK e autorização |
| Tabelas básicas | NUE, Códigos de Estação, Tipo de Ocorrências | Aguardam nomes das tabelas, colunas e chaves; não são associados a tabelas por suposição |

O menu hierárquico conserva o bloco de usuário/login/logout na parte inferior. O template de registros reúne busca, filtro adicional por projeto, paginação no servidor e detalhes da linha. Ele consulta os fatos do painel; não implementa ainda gravação de crítica ou edição de estação.

## Filtros implícitos de CAMPANHA

| Contexto | Tela | Campanha fixa |
|---|---|---|
| `critica` | Crítica de Dados | Todas |
| `altimetria` | Altimetria | `medA` |
| `gravimetria` | Gravimetria | `medG` |
| `planimetria` | Planimetria | `medP` |
| `vrf` | VRF | `vrf` |
| `veg` | VEG | `veg` |
| `ogr` | OGR | `ogr` |
| `gabinete` | Ajustes de Gabinete | `gab` |

`GET /api/registros/{contexto}?page=0&size=25&q=texto&projeto=PROJETO` retorna `items`, `total`, `page`, `size`, `totalPages` e `campanha`. Tamanho máximo: 100. O backend escolhe a campanha pelo contexto, sem aceitar substituição por query string. Busca e projeto são filtros adicionais, sem remover o filtro fixo. A propriedade Java `campanha` usa o mapeamento existente `DIM_CAMPANHA` da view `V_FATO_SADGEO_PAINEL`; confirme que a view retorna os códigos indicados ao validar com o Oracle real.

## Cadastros disponíveis

| Identificador API | Tabela Oracle | Referência de chave no demo |
|---|---|---|
| `localizacao` | `T_LOCALIZACAO` | `TIPO_LOCAL` |
| `tipo-projeto` | `T_TIPO_PROJETO` | `TIPO_PROJETO` |
| `situacao-marco` | `T_TIPO_SITUACAO_MARCO` | `COD_SITUACAO_MARCO` |
| `metodo-calculo` | `T_METODO_CALCULO` | `COD_METODO_CALCULO` |
| `fonte-coordenada` | `T_FONTE_COORDENADA` | `CD_FONTE_COORDENADA` |
| `equipamento` | `T_EQUIPAMENTO` | `CODIGO` |
| `campanha` | `T_CAMPANHA` | `COD_CAMPANHA`, `COD_PROJETO`, `COD_INSTITUICAO` |
| `atividade` | `T_ATIVIDADE` | `COD_ATIVIDADE` |
| `status` | `T_STATUS` | `STATUS` |
| `municipio` | `T_MUNICIPIO` | `COD_UF`, `COD_MUNICIPIO` |
| `pendencia` | `T_PENDENCIA_SADGEO` | `COD_PEND` |

Os campos, limites e nulabilidade fornecidos estão em `sadgeoweb/src/main/resources/catalogo.json`. Em produção, as PKs são consultadas no metadado Oracle; não se considera a primeira coluna automaticamente como chave. Se não houver PK confirmada, a manutenção fica desabilitada. Para `T_CAMPANHA`, a chave deve coincidir com os três campos confirmados pelo usuário. Campos de chave não podem ser modificados na edição.

Os cadastros usam Controller → Service → Repository JDBC, consultas parametrizadas e uma lista fixa de tabelas/colunas. Não criam tabelas, sequences, PKs nem migrations; `ddl-auto=validate` continua ativo nas entidades JPA. O schema JDBC usa `SADGEO_DB_SCHEMA`, mas as entidades JPA antigas ainda declaram `BDG_VALIDA` explicitamente.

O usuário Oracle deve ter permissões nas tabelas solicitadas. Violações de chave/referência retornam HTTP 409; a exclusão não realiza cascata. As gravações preservam defaults do banco quando campos opcionais são omitidos. Valores vazios explícitos tornam-se NULL. `NUMBER(38,0)` é transmitido como texto para preservar a precisão no JavaScript; valores numéricos recebidos são convertidos para `BigDecimal`. Datas Oracle DATE usam data/hora local sem timezone. Limites BYTE de textos são validados como UTF-8; valide a compatibilidade com o charset real do banco. Fonte de coordenada numérica com um dígito é completada à esquerda (`9` → `09`).

## Permissões de gravação

- Em `demo`, usuários da sessão demonstrativa podem alterar somente as fixtures em memória. Tudo é reiniciado com o processo.
- Em `dev`/`prod`, o padrão é consulta. Para liberar manutenção, defina `SADGEO_CATALOG_WRITERS` com identificadores autenticados separados por vírgulas, iguais ao `login` retornado por `/api/auth/me`.
- Essa lista não implementa os futuros cadastros de perfil/permissionamento. Usuários fora da lista recebem 403 mesmo se chamarem a API diretamente.
- CSRF é obrigatório em POST, PUT e DELETE.

## Contratos REST

Todas as rotas abaixo exigem sessão:

```text
GET    /api/tabelas                         Catálogo de tabelas
GET    /api/tabelas/{id}?page=0&size=25&q=    Lista paginada com metadados
GET    /api/tabelas/{id}/meta                Campos, PK efetiva e canWrite
GET    /api/tabelas/{id}/item?TIPO_LOCAL=XX   Registro por chave completa
POST   /api/tabelas/{id}                    Criação (201)
PUT    /api/tabelas/{id}                    Alteração (200)
DELETE /api/tabelas/{id}                    Exclusão (204)
```

Criação em Localização:

```json
{"TIPO_LOCAL":"XX","DESCRICAO":"Descrição"}
```

Alteração:

```json
{"key":{"TIPO_LOCAL":"XX"},"values":{"DESCRICAO":"Nova descrição"}}
```

Exclusão:

```json
{"key":{"TIPO_LOCAL":"XX"}}
```

Em Campanha, envie os três campos no objeto `key` e todos os campos obrigatórios na criação. Para consultar uma linha, envie os três nomes na query string de `/item`. Não altere o código de uma chave existente.

## Testes externos reproduzíveis

Primeiro compile e inicie o demo, a partir da raiz do checkout:

```sh
cd sadgeoweb
mvn clean verify
java -jar target/sadgeo-0.2.0.jar --spring.profiles.active=demo
```

Em outro terminal, na raiz do checkout, execute uma das opções.

**Bash + curl + Python 3:**

```sh
bash scripts/test-api.sh http://127.0.0.2:8080
bash scripts/test-api.sh http://127.0.0.2:8080 --crud
```

**PowerShell 7+ (Windows ou Linux):**

```powershell
pwsh -NoProfile -File scripts/Test-Api.ps1 -BaseUrl http://127.0.0.2:8080
pwsh -NoProfile -File scripts/Test-Api.ps1 -BaseUrl http://127.0.0.2:8080 -Crud
```

Os scripts validam saúde, bloqueio sem sessão, login, sessão, dashboard, as sete campanhas, metadados de Localização/Campanha, Pendências e logout. Guardam cookies e obtêm CSRF automaticamente; saem com erro se uma verificação falhar. Na versão real, solicitam usuário/senha sem incluí-los na linha de comando. Não compartilhe a saída com tracing de credenciais habilitado.

`--crud`/`-Crud` só funciona quando o backend informa `demo=true`. Escolhe um código de teste livre, cria, consulta, altera e exclui uma Localização. Nunca modifica um registro que já existia e tenta limpar o registro criado em caso de falha. Os scripts não executam gravações no Oracle real.

Os testes Java usam fixtures e H2 em modo Oracle para exercitar SQL JDBC e descoberta de PK. Isso não substitui a validação com Oracle/LDAPS reais, ainda pendente por ausência de conexão institucional neste ambiente.

## Telas adicionais da 0.2

A 0.2 acrescenta recepção/SIGCVEG, rascunho de registro, prévia local de fotos, documentos, acompanhamento, filas BDG, qualidade, auditoria, modelos e ajuda. Detalhes têm abas e links de contexto. A produção permite filtros e CSV; CSV não substitui formatos oficiais. A tela de integrações consulta somente configuração não sensível e saúde geral. Operações não implementadas ficam desabilitadas, sem retorno fictício de sucesso. Consulte [RELEASE-0.2](RELEASE-0.2.md) e [TODO](../TODO.md).
