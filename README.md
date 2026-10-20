# SADGEO — versão 0.2.0

Portal React + Material UI + TypeScript, API REST JSON Spring Boot 3.5 e persistência Oracle. O build gera **um único JAR**, com API e interface no mesmo endereço. JDK 17, Maven 3.9+ e Node.js 22.12+ (ou 24 LTS) com npm são necessários para compilar. Para executar o JAR pronto, basta Java.

## 1. Executar sem Oracle (demonstração)

Na raiz do repositório:

```sh
cd sadgeoweb
mvn clean verify
java -jar target/sadgeo-0.2.0.jar --spring.profiles.active=demo
```

O Maven executa `npm ci`, compila o React e copia o resultado para o JAR. Abra o endereço da aplicação na porta **8080** em sua máquina. O perfil `demo` não conecta ao banco e exibe um aviso permanente de **dados fictícios**. Não use esse perfil para conferir indicadores reais. Na página de login, clique em **Entrar na demonstração**; não informe credenciais.

O portal incorpora o layout de `sadgeo-react-web.7z`: login pêssego/violeta, cabeçalho, menu lateral, ajuda, tema/projeto, rodapé e grade Material UI com seleção e detalhes. Rotas: `/login`, `/index` e `/registros`. Crítica de Dados e Análise usam o mesmo template de consulta, com filtros e paginação no servidor; o dashboard apresenta os totais gerais. A grade consulta os fatos analíticos, não edita estações.

Verificação por terminal:

```sh
curl --fail http://127.0.0.2:8080/api/dashboard/config
# Sem sessão, esta consulta retorna HTTP 401:
curl -i http://127.0.0.2:8080/api/dashboard/resumo
curl --fail http://127.0.0.2:8080/actuator/health
```

## 2. Executar com o Oracle existente

A configuração não armazena credenciais. Defina as variáveis no terminal, IDE ou gerenciador de segredos do ambiente:

```sh
export SADGEO_DB_URL='jdbc:oracle:thin:@//HOST:1521/SERVICE_NAME'
export SADGEO_DB_USERNAME='seu_usuario'
read -rsp 'Senha Oracle: ' SADGEO_DB_PASSWORD; echo
export SADGEO_DB_PASSWORD
export SADGEO_DB_SCHEMA='BDG_VALIDA'
java -jar target/sadgeo-0.2.0.jar --spring.profiles.active=prod
```

No PowerShell, use `$env:SADGEO_DB_URL = '...'` e defina as demais variáveis pelo mecanismo seguro da sua organização. Não coloque senhas em arquivos versionados nem em argumentos de execução.

É necessário alcançar o Oracle pela rede e ter permissão de leitura nas tabelas/views já mapeadas em `dominio`. O Hibernate usa `ddl-auto=validate`: **não cria nem migra o banco**. Os mapeamentos existentes fixam o schema `BDG_VALIDA`; mudar apenas `SADGEO_DB_SCHEMA` não remapeia entidades que declaram esse schema explicitamente.

Sem conexão, credenciais ou objetos corretos, a aplicação pode falhar na inicialização. Nenhum erro do Oracle ativa dados demonstrativos automaticamente.

### Login institucional

Toda a conexão AD/LDAPS é configurada por variáveis de ambiente, assim como o Oracle:

| ENVVAR | Uso | Padrão |
|---|---|---|
| `SADGEO_LDAP_HOST` | Servidor/FQDN, sem protocolo ou porta | vazio |
| `SADGEO_LDAP_PORT` | Porta LDAPS | `636` |
| `SADGEO_LDAP_DOMAIN` | Domínio AD/UPN, por exemplo `example.org` | vazio |
| `SADGEO_LDAP_BASE_DN` | Base de busca, por exemplo `DC=example,DC=org` | derivada do domínio quando vazia |
| `SADGEO_LDAP_CONNECT_TIMEOUT_MS` | Timeout de conexão, em milissegundos | `5000` |
| `SADGEO_LDAP_READ_TIMEOUT_MS` | Timeout de leitura, em milissegundos | `10000` |
| `SADGEO_LDAP_URL` | Override opcional `ldaps://servidor:porta`, compatível com a configuração anterior | vazio |

```sh
export SADGEO_LDAP_HOST='ad.example.org'
export SADGEO_LDAP_PORT='636'
export SADGEO_LDAP_DOMAIN='example.org'
export SADGEO_LDAP_BASE_DN='DC=example,DC=org'
export SADGEO_LDAP_CONNECT_TIMEOUT_MS='5000'
export SADGEO_LDAP_READ_TIMEOUT_MS='10000'
# Deixe SADGEO_LDAP_URL sem valor para usar HOST + PORT:
unset SADGEO_LDAP_URL
java -jar target/sadgeo-0.2.0.jar --spring.profiles.active=prod
```

No Eclipse: **Run Configurations → Environment**. No VS Code: seção `env`/`envFile` da configuração de execução Java. No OpenShift: variáveis do deployment/ConfigMap; credenciais Oracle devem ficar em Secret. `sadgeoweb/.env.example` lista as variáveis, mas o Spring Boot não carrega `.env` automaticamente; configure a IDE ou exporte-as antes de iniciar.

`SADGEO_LDAP_DOMAIN` é o domínio do usuário AD, não o endereço de um servidor DNS. O hostname é resolvido pelo DNS do sistema operacional/cluster; se ele não resolver, ajuste a configuração de rede/DNS da máquina ou do pod. A aplicação não altera o resolver do host. Use um FQDN compatível com o certificado TLS do AD.

`SADGEO_LDAP_URL`, quando preenchida, tem prioridade sobre HOST/PORT. Apenas `ldaps://` é aceito; não inclua usuário, senha ou Base DN na URL. Configuração parcial, porta inválida ou timeouts não positivos geram erro claro na inicialização. Sem nenhuma configuração, o formulário fica desabilitado e o backend recusa o login.

O JDK precisa confiar no certificado do AD. É possível selecionar o truststore institucional pela ENVVAR padrão da JVM `JAVA_TOOL_OPTIONS`, por exemplo `-Djavax.net.ssl.trustStore=/caminho/truststore.p12 -Djavax.net.ssl.trustStoreType=PKCS12`. Não desabilite TLS nem validação de hostname. O bind usa o usuário e a senha digitados no login; não há credenciais fixas de administrador. A conexão com AD real ainda precisa ser validada na instituição.

Consultas exigem sessão no servidor. O cliente obtém CSRF em `GET /api/auth/csrf`, envia credenciais por `POST /api/auth/login` (formulário URL-encoded), consulta `GET /api/auth/me` e encerra em `POST /api/auth/logout`. Respostas são JSON; logout retorna 204. A entrada `POST /api/auth/demo` só funciona no perfil demo. Senhas e tokens não são salvos em localStorage. Use HTTPS em produção. A autorização por módulo ainda não foi implementada; usuários autenticados têm acesso de consulta. A manutenção dos cadastros Oracle exige também a lista `SADGEO_CATALOG_WRITERS`.

## 3. Desenvolver com atualização automática do React

Primeiro execute o build da etapa 1. Depois abra dois terminais.

Backend, em `sadgeoweb`:

```sh
mvn spring-boot:run -Dexec.skip=true -Dspring-boot.run.profiles=demo
```

Para dados reais, configure as variáveis da etapa 2 e troque `demo` por `dev`.

Frontend, em `sadgeoweb/frontend`:

```sh
npm ci
npm run dev
```

Abra a porta **5173** na sua máquina. O Vite encaminha `/api` para a porta 8080, sem precisar liberar CORS. Ao acessar a porta 8080, será exibido o último frontend compilado; as alterações instantâneas ficam na porta 5173.

## 4. Testar e empacotar

Em `sadgeoweb/frontend`:

```sh
npm test
npm run build
```

Em `sadgeoweb`:

```sh
mvn clean verify
```

Os testes Java usam fixtures ou mocks, sem Oracle/AD. Verificam contratos JSON, proteção de consultas, sessão, CSRF, logout, rotas SPA e bloqueio de demo fora desse perfil. Os testes React verificam login, configuração ausente, carregamento, erro/repetição, busca e paginação. A validação com Oracle real deve ser feita no ambiente da instituição; os testes demonstrativos não a substituem.

## 5. Implantar no OpenShift

Execute `mvn clean verify`. O Dockerfile existente em `sadgeoweb/openshift` aceita o JAR. Prepare o contexto:

```sh
mkdir -p target/ocp
cp openshift/Dockerfile target/ocp/
cp target/sadgeo-0.2.0.jar target/ocp/
oc start-build sadgeo --from-dir=target/ocp --follow
```

Isso pressupõe um BuildConfig `sadgeo` existente, login no cluster e acesso à imagem interna Java 17. Configure `SADGEO_DB_*` por Secret/configuração do deployment. O processo é `java -jar /deployments/app.jar`, porta 8080. Processos locais de desenvolvimento não são necessários em produção.

**A versão 0.2 inclui consultas e manutenção dos cadastros descritos.** Consultas exigem sessão e CSRF permanece ativo. O login LDAPS depende da configuração e validação institucional; a autorização detalhada por módulo precisa ser definida antes de ampliar o acesso. Credenciais presentes no histórico antigo do Git devem ser rotacionadas pelos responsáveis.

## Escopo da migração

- Vaadin, seus plugins, bundles e classes de interface foram removidos.
- O template anterior foi adaptado à API 0.2. Componentes/contextos ausentes foram reconstruídos. A imagem `back7.jpg` não estava no arquivo original; usa-se fundo CSS. Nenhum mock antigo autentica usuários em produção.
- React preserva indicadores de situação, evolução anual, gráfico ano/campanha, resumo analítico e fatos, com busca e paginação local.
- Serviços, DTOs, entidades, repositórios Oracle e estrutura OLAP Java foram mantidos.
- A tela inicial é **Painel de Controle**. Crítica de Dados e as sete análises compartilham uma consulta paginada com filtro implícito por campanha. Planejamento/Campanha e 10 tabelas básicas têm CRUD. Importação, imagens, homologação e administração têm rotas/templates, com integração pendente. Edição de estações continua fora do escopo disponível.
- Os endpoints `/fatos` e `/analitico` ainda carregam a coleção inteira, como a implementação anterior. Para volumes grandes, implementar filtros e paginação no servidor antes de ampliar o uso.
- `CubeProvider` mantém o comportamento anterior de carregar o cubo na inicialização; atualizar a página não recarrega esse cubo do banco. A atualização dinâmica é uma evolução separada.
- O deploy deixou de ser acionado automaticamente por `mvn deploy`; use a etapa explícita acima.

## Endpoints

Todos são GET, sob `/api/dashboard`. Apenas `/config` é público; os demais exigem sessão:

| Rota | Resposta |
|---|---|
| `/config` | Versão e identificação do modo demo |
| `/resumo` | Totais por situação e período |
| `/evolucao-anual` | Totais anuais por situação |
| `/campanhas` | Evolução por campanha, projeto e UF |
| `/analitico` | Resumo analítico |
| `/fatos` | Fatos do painel |
| `/pivot` | Categorias e séries de contagem por ano/campanha |

## Estrutura

```text
sadgeoweb/
  frontend/src/                    React, componentes e testes
  src/main/java/.../dashboard/api/ Controllers REST
  src/main/java/.../dashboard/     Serviços e DTOs
  src/main/java/.../dominio/       Entidades e repositórios
  src/main/resources/demo/         Dados fictícios isolados
  src/test/                       Testes de integração HTTP
  pom.xml                         Build integrado React + Java
```

## Validação Oracle Spatial: coluna GEOM

O driver Oracle pode informar `SDO_GEOMETRY` com tipo JDBC `STRUCT`, enquanto o Hibernate Spatial usa o código interno `GEOMETRY`. O campo JTS `Point` permanece espacial; a declaração `columnDefinition = "SDO_GEOMETRY"` usa o mesmo nome não qualificado retornado pelo driver. Isso permite a comparação de tipos do Hibernate sem desativar `ddl-auto=validate`, sem converter a coluna para texto e sem alterar o banco.

Um teste de regressão executa a rotina real de comparação de tipos do Hibernate com esse metadado e também rejeita uma coluna `VARCHAR2`. Isso valida o cenário informado, mas não substitui a inicialização contra o Oracle real. Após atualizar, execute novamente com as ENVVARs Oracle; se outra coluna apresentar divergência, preserve o diagnóstico completo.

## Rodapé, versão e identificação

O rodapé exibe copyright `IBGE-DGC/CGED/GSD` à esquerda, rótulo/profile e hostname do servidor ao centro, e `Versão 0.2.YYYYMMDD-HH` à direita. A data/hora vem do build Maven, no fuso `America/Sao_Paulo`, e permanece igual após reiniciar o mesmo JAR. O artefato Maven continua se chamando `sadgeo-0.2.0.jar`.

O rótulo padrão acompanha o profile (`demo`: Demonstração; `dev`: Desenvolvimento; `prod`: Produção). Para personalizá-lo, defina `SADGEO_PROFILE_LABEL`, por exemplo `Homologação`. Hostname vem da máquina que executa o backend (`HOSTNAME`/`COMPUTERNAME`, com fallback à consulta local); em contêineres, normalmente identifica o pod, não o computador do navegador.

No menu lateral, nome, identificador, perfil e botão Sair ficam no bloco inferior. Sem sessão, o portal mostra Visitante e Fazer login; consultas continuam exigindo autenticação. Em telas pequenas, o rodapé distribui os três blocos em linhas para preservar a leitura.

## Menus, cadastros e testes curl/PowerShell

O [guia de cadastros e testes](docs/CADASTROS-E-TESTES.md) descreve toda a hierarquia, os filtros `medA/medG/medP/vrf/veg/ogr/gab`, os 11 cadastros (incluindo Pendências), as chaves compostas e os contratos REST.

Com o demo em execução, na raiz do checkout:

```sh
bash scripts/test-api.sh http://127.0.0.2:8080 --crud
```

Ou, com PowerShell 7+:

```powershell
pwsh -NoProfile -File scripts/Test-Api.ps1 -BaseUrl http://127.0.0.2:8080 -Crud
```

A opção de CRUD é restrita ao demo; os scripts não gravam no Oracle real. Para manutenção pela interface/API em produção, configure `SADGEO_CATALOG_WRITERS` com os logins autorizados e as permissões correspondentes no banco. NUE, Códigos de Estação e Tipo de Ocorrências aguardam a definição das tabelas e campos.

## Evolução funcional e milestones

- [TODO / milestones](TODO.md): incrementos, dependências, tarefas e critérios de aceite, da base 0.2 à operação de produção.
- [Sugestões de telas e menus](docs/TELAS-E-MENUS.md): cobertura dos cinco estágios, template de estação e propostas que ainda não existem na 0.2.
- [Rastreabilidade](docs/RASTREABILIDADE.md): requisitos/casos de uso dos documentos recebidos e decisões pendentes, incluindo duas versus três instâncias de crítica.

As novas interfaces foram geradas na 0.2, com ações impactantes desabilitadas e identificadas por milestone. O planejamento de campo continua externo; Campanha é um cadastro de referência. Homologação precisa de especificação própria e não é sinônimo de carga no BDG.

## Entrega 0.2

A [nota de versão 0.2](docs/RELEASE-0.2.md) separa funcionalidades, prévias locais e integrações futuras. As novas telas de baixo impacto já foram geradas; mudanças que gravam estações, decidem críticas ou alteram sistemas externos permanecem nos milestones.

### Falha de compilação em `LdapProperties` (getDomain/getBaseDn/timeouts)

Atualize o checkout e execute `mvn clean verify` em `sadgeoweb`. A configuração LDAP tem acessores Java explícitos; o Maven também declara o processador Lombok usado pelas entidades. Confira `mvn -version`: o JDK efetivamente usado pelo Maven pode ser diferente do selecionado na IDE. O JDK obrigatório para este projeto é o 17. Se o erro persistir, confira se há `-proc:none` nas opções locais e atualize o projeto Maven na IDE.

No Windows/PowerShell, configure o JDK 17 antes de compilar (ajuste o caminho da instalação):

```powershell
$env:JAVA_HOME = 'C:\Java\jdk-17'
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
mvn -version
mvn clean verify
```

No Eclipse/STS, selecione JDK 17 em **Installed JREs** e na configuração de execução Maven. No VS Code, selecione JavaSE-17 em **Java: Configure Java Runtime**. O Maven exige a versão `[17,18)`; o bytecode também é compilado para Java 17.

### Executar pelo PowerShell com profile como argumento

Na raiz do checkout, o argumento `-Profile` e obrigatorio (`demo`, `dev` ou `prod`):

```powershell
# Atualizar a main; depois compilar/testar e iniciar a demonstracao
.\scripts\git_local_upd.ps1
.\scripts\build_run.ps1 -Profile demo -JavaHome 'C:\Desenvolvimento\jdk-17.0.20.1+1'

# Iniciar com Oracle/LDAPS configurados nas ENVVARs da sessao
.\scripts\build_run.ps1 -Profile dev -JavaHome 'C:\Program Files\Java\jdk-17'

# Reutilizar o JAR ja compilado e selecionar outra porta
.\scripts\build_run.ps1 -Profile prod -SkipBuild -Port 8081
```

No Windows, `-JavaHome` usa `C:\Desenvolvimento\jdk-17.0.20.1+1` quando omitido; em outros sistemas, usa `JAVA_HOME`. O script exige JDK 17, interrompe em erros e resolve os caminhos a partir de sua propria localizacao. O build nao executa comandos Git; use `git_local_upd.ps1` separadamente para atualizar. Sem `-SkipBuild`, executa `mvn clean verify`. `dev` e `prod` exigem as ENVVARs e conexoes institucionais descritas acima; o script nao carrega `.env`. Encerre com `Ctrl+C`. Pode ser executado no Windows PowerShell 5.1 ou PowerShell 7+.

### Se o Windows so tem JDK 24

Instale tambem o JDK 17 (o 24 pode continuar instalado):

```powershell
winget install --id EclipseAdoptium.Temurin.17.JDK --exact --source winget
```

A instalacao pode solicitar permissao do Windows. Se `winget` nao estiver disponivel, instale o Temurin 17 pelo site oficial <https://adoptium.net/temurin/releases/?version=17> ou solicite a instalacao ao suporte.

Reabra o PowerShell, localize a instalacao e execute a partir da raiz do checkout:

```powershell
Get-ChildItem 'C:\Program Files\Eclipse Adoptium' -Directory
# Substitua pelo caminho exibido:
.\scripts\build_run.ps1 -Profile demo -JavaHome 'C:\Program Files\Eclipse Adoptium\jdk-17.0.x.x-hotspot'
```

Para atualizar manualmente com Git antigo, use `git checkout main` e `git pull --ff-only origin main`. `D:\` isolado nao e um comando de navegacao: use `Set-Location 'D:\caminho\do\repositorio'`. No Windows, consulte a versao do npm com `npm.cmd --version`; o build Maven tambem seleciona `npm.cmd`, evitando o bloqueio de `npm.ps1` sem alterar a politica de execucao.

### Scripts prontos para o JDK portatil informado

No Windows, `build_run.ps1` usa por padrao `C:\Desenvolvimento\jdk-17.0.20.1+1`. Nao instala programas nem exige alterar `JAVA_HOME` permanentemente. `-JavaHome` permite substituir esse caminho. Execute na raiz do repositorio:

```powershell
# Somente atualizar do GitHub (sem Maven, Java ou execucao da aplicacao)
.\scripts\git_local_upd.ps1

# Compilar/testar e executar no perfil escolhido
.\scripts\build_run.ps1 -Profile demo

# Compilar e executar com as ENVVARs institucionais configuradas
.\scripts\build_run.ps1 -Profile dev

# Reutilizar o JAR existente
.\scripts\build_run.ps1 -Profile prod -SkipBuild
```

Para baixar uma nova copia, o script de Git aceita um destino ainda inexistente:

```powershell
.\scripts\git_local_upd.ps1 -Destination 'D:\IBGE\Projetos\gitProjetos\sadgeo-novo'
```

Se o destino ja existir, deve ser checkout de `pjagimenez/sadgeo` e estar limpo, inclusive sem arquivos nao rastreados. O script nao apaga nem sobrescreve alteracoes locais, e usa `git checkout` para compatibilidade com Git antigo. Para a primeira copia sem scripts locais, use `git clone https://github.com/pjagimenez/sadgeo.git`.
