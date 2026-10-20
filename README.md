# SADGEO — versão 0.2.0

**SADGEO — Sistematização e Análise de Dados Geodésicos.**

Portal React + Material UI + TypeScript, API REST JSON Spring Boot 3.5 e persistência Oracle. O build gera **um único JAR**, com API e interface no mesmo endereço. JDK 17, Maven 3.9+ e Node.js 22.12+ (ou 24 LTS) com npm são necessários para compilar. Para executar o JAR pronto, basta Java.

## 1. Executar sem Oracle (demonstração)

Na raiz do repositório:

```sh
cd sadgeoweb
mvn clean verify
java -jar target/sadgeo-0.2.0.jar --spring.profiles.active=demo
```

O Maven verifica as dependências frontend, executa `npm ci` quando necessário, compila o React e copia o resultado para o JAR. Abra o endereço da aplicação na porta **8080** em sua máquina. O perfil `demo` não conecta ao banco e exibe um aviso permanente de **dados fictícios**. Não use esse perfil para conferir indicadores reais. Na página de login, clique em **Entrar na demonstração**; não informe credenciais.

O portal incorpora o layout de `sadgeo-react-web.7z`: login pêssego/violeta, cabeçalho, menu lateral, ajuda, tema/projeto, rodapé e grade Material UI com seleção e detalhes. Rotas: `/login`, `/index` e `/registros`. Crítica de Dados e Análise usam o mesmo template de consulta, com filtros e paginação no servidor; o dashboard apresenta os totais gerais. A grade consulta os fatos analíticos, não edita estações.

Verificação por terminal:

```sh
curl --fail http://127.0.0.2:8080/api/dashboard/config
# Dashboard público: esta consulta retorna HTTP 200 mesmo sem sessão:
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

O Dashboard e seus dados de consulta são públicos. Registros operacionais e cadastros exigem sessão no servidor. O cliente obtém CSRF em `GET /api/auth/csrf`, envia credenciais por `POST /api/auth/login` (formulário URL-encoded), consulta `GET /api/auth/me` e encerra em `POST /api/auth/logout`. Respostas são JSON; logout retorna 204. A entrada `POST /api/auth/demo` só funciona no perfil demo. Senhas e tokens não são salvos em localStorage. Use HTTPS em produção. A autorização por módulo ainda não foi implementada; usuários autenticados têm acesso de consulta. A manutenção dos cadastros Oracle exige também a lista `SADGEO_CATALOG_WRITERS`.

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

### Trabalhar com Spring Tools for Eclipse e Visual Studio Code

Use as duas IDEs no **mesmo checkout**, com o backend Java no Spring Tools e o frontend React no VS Code.

| Ferramenta | Pasta | Responsabilidade |
|---|---|---|
| Spring Tools for Eclipse | `sadgeoweb` | Java, Spring Boot, API REST e persistência |
| Visual Studio Code | `sadgeoweb/frontend` | React, TypeScript, componentes e estilos |

**Backend no Spring Tools**

1. Importe por **File → Import → Maven → Existing Maven Projects**, selecionando a pasta `sadgeoweb` que contém o `pom.xml`.
2. Configure o projeto com **JavaSE-17**, compiler compliance **17** e o JDK portátil `C:\Desenvolvimento\jdk-17.0.20.1+1`.
3. Abra **Run → Run Configurations → Spring Boot App** e selecione a classe principal `SadgeoApplication`.
4. Na aba **JRE**, selecione o JDK 17. Em **Arguments → Program arguments**, informe:

   ```text
   --spring.profiles.active=demo
   ```

5. Inicie com **Run** ou **Debug**. O backend usa a porta **8080** por padrão. Para dados institucionais, use `dev` ou `prod` e configure as ENVVARs de Oracle/LDAPS na aba **Environment**, conforme as seções anteriores.

Se o Eclipse indicar compliance 25 incompatível com JDK 17, ajuste **Window → Preferences → Java → Compiler** e **Project → Properties → Java Compiler** para **17**. Depois execute **Maven → Update Project** e **Project → Clean**. A JVM que inicia a própria IDE pode ser mais recente se a versão do Spring Tools exigir.

**Frontend no VS Code**

Abra `sadgeoweb/frontend` e execute no terminal PowerShell integrado:

```powershell
npm.cmd ci --include=dev --bin-links=true
npm.cmd run dev
```

Acesse **http://localhost:5173**. O Vite encaminha as chamadas `/api` para o backend em **8080**. Alterações React aparecem automaticamente; não é necessário gerar o JAR a cada alteração. Não use Live Server para executar esse frontend.

Durante o desenvolvimento, depure Java com breakpoints no Spring Tools e inspecione o React pelas ferramentas do navegador ou pelo depurador do VS Code. Alterações Java podem exigir reiniciar o backend. Os dois editores compartilham os mesmos arquivos e o mesmo histórico Git.

**Testar a aplicação empacotada**

Para conferir React e API no mesmo JAR, encerre primeiro o backend iniciado pelo Spring Tools, liberando a porta 8080. Na raiz do checkout:

```powershell
.\scripts\build_run.ps1 -Profile demo
```

Acesse **http://localhost:8080**. Esse comando compila, testa e executa o JAR; o React servido nessa porta corresponde ao último build. No trabalho diário com alterações automáticas das telas, mantenha o backend no Spring Tools e o Vite no VS Code, acessando **5173**.

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

**A versão 0.2 inclui consultas e manutenção dos cadastros descritos.** O Dashboard é público; consultas operacionais e cadastros exigem sessão, e CSRF permanece ativo. O login LDAPS depende da configuração e validação institucional; a autorização detalhada por módulo precisa ser definida antes de ampliar o acesso. Credenciais presentes no histórico antigo do Git devem ser rotacionadas pelos responsáveis.

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

Todos são GET, sob `/api/dashboard`. As consultas listadas são públicas, inclusive para visitantes:

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

No canto superior direito do cabeçalho ficam Ajuda, nome, identificador, perfil e Sair. Sem sessão, aparecem Visitante e Fazer login. O menu lateral fica dedicado à navegação, com grupos independentes e uma única área de rolagem. O Dashboard é a página inicial pública; registros operacionais e cadastros continuam exigindo autenticação. Em telas pequenas, o rodapé distribui os três blocos em linhas para preservar a leitura.

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

Se o destino ja existir, deve ser checkout de `pjagimenez/sadgeo`. Antes de atualizar, o script guarda automaticamente alteracoes locais e arquivos nao rastreados em um stash identificado por data e codigo unico. Ele confirma o stash e o checkout limpo antes de prosseguir, e usa `git checkout` para compatibilidade com Git antigo. Para a primeira copia sem scripts locais, use `git clone https://github.com/pjagimenez/sadgeo.git`.

### Eclipse/STS: compiler compliance 25 versus JDK 17

Cadastrar o JDK 17 nao muda automaticamente o nivel do compilador. Em **Window > Preferences > Java > Compiler**, selecione **Compiler compliance level: 17**. Se houver configuracao especifica do projeto, em **Project > Properties > Java Compiler**, marque **Enable project specific settings** e selecione **17**. Depois ajuste **Java Build Path > Libraries > JRE System Library** para **JavaSE-17**, associado ao JDK portatil em **Installed JREs > Execution Environments**. Execute **Maven > Update Project** e **Project > Clean**. Nas configuracoes **Spring Boot App** e **Maven Build**, a aba **JRE** tambem deve apontar para JDK 17. Nao altere a JVM que inicia a propria IDE se a versao do STS exigir Java mais recente.

### Frontend: `tsc` nao reconhecido no Windows

TypeScript e Vite sao dependencias locais de compilacao em `devDependencies`. O build precisa delas mesmo quando o perfil Spring e `prod`. Quando precisa reinstalar os pacotes, o Maven usa `npm ci --include=dev --bin-links=true`, para instala-las inclusive quando `NODE_ENV=production` ou uma configuracao npm omite dependencias de desenvolvimento/desativa os executaveis em `node_modules/.bin`. Nao e necessario instalar TypeScript globalmente.

Depois de atualizar o checkout, execute novamente `scripts/build_run.ps1 -Profile demo`. Para diagnosticar ou compilar somente o frontend, em PowerShell:

```powershell
Set-Location .\sadgeoweb\frontend
npm.cmd ci --include=dev --bin-links=true
if ($LASTEXITCODE -ne 0) { throw 'Falha na instalacao npm' }
npm.cmd ls typescript vite
npm.cmd run build
```

`npm ci` baixa/reinstala os pacotes; a primeira execucao pode demorar conforme a rede. O aviso `whatwg-encoding deprecated` nao e a causa do erro `tsc`. Avisos de vulnerabilidades precisam de analise separada; nao execute `npm audit fix --force` automaticamente, pois pode introduzir atualizacoes incompativeis.

### Evitar reinstalar os pacotes frontend em todo build

A etapa Maven `frontend-install` verifica a instalacao antes de executar `npm ci`. Se `package.json`, `package-lock.json`, `.npmrc`, o script de instalacao, a versao do Node e a plataforma permanecerem iguais, e a instalacao local estiver presente, reutiliza `node_modules`. O marcador fica dentro de `node_modules`, fora do Git; `mvn clean` nao o remove. A primeira execucao apos esta atualizacao reinstala os pacotes e cria o marcador. Mudancas no codigo React nao exigem reinstalacao dos pacotes.

Para forcar uma reinstalacao, na raiz do repositorio:

```powershell
Remove-Item .\sadgeoweb\frontend\node_modules\.sadgeo-install.json -ErrorAction SilentlyContinue
.\scripts\build_run.ps1 -Profile demo
```

A compilacao React e os testes Maven continuam sendo executados para incorporar e verificar as alteracoes. Para apenas executar um JAR ja pronto, use `build_run.ps1 -Profile demo -SkipBuild`. No desenvolvimento diario das telas, use Vite (`npm.cmd run dev`) para atualizacao automatica.

### Recuperacao npm: TAR_ENTRY_ERROR ENOENT e instalacao incompleta

Se o npm informa falhas de extracao e o build acusa ferramentas ausentes, o log nao comprova a causa. Cache, bloqueios/permissoes, instalacoes simultaneas e protecao de endpoint podem interferir. Primeiro encerre Vite e outros builds desse checkout. Na raiz do repositorio, o procedimento abaixo remove apenas dependencias geradas e tenta a instalacao com um novo cache de usuario, mantendo o lockfile:

```powershell
Remove-Item -LiteralPath .\sadgeoweb\frontend\node_modules -Recurse -Force -ErrorAction Stop
$oldNpmCache = $env:npm_config_cache
try {
    $env:npm_config_cache = Join-Path $env:LOCALAPPDATA ('sadgeo-npm-cache-' + [guid]::NewGuid().ToString('N'))
    node .\sadgeoweb\frontend\scripts\install-dependencies.cjs
    if ($LASTEXITCODE -ne 0) { throw 'Instalacao npm ainda incompleta; confira os arquivos ausentes e erros acima.' }
} finally {
    $env:npm_config_cache = $oldNpmCache
}
.\scripts\build_run.ps1 -Profile demo
```

Se `node_modules` nao existir, pule a remocao. Se a remocao falhar, interrompa e investigue o bloqueio/permissao. Se os erros persistirem mesmo com cache novo e sem builds paralelos, encaminhe o log ao suporte para verificar acesso ao diretorio e eventos de protecao de endpoint; nao desative o antivirus. O script lista os arquivos de ferramentas que faltam. Nao apague `package-lock.json` nem use `npm audit fix --force` para resolver erros de extracao. Em PowerShell, comandos npm manuais devem usar `npm.cmd`, inclusive `npm.cmd fund`; `fund` apenas informa financiamento e nao corrige o build.

### Downloads HTTPS com CA institucional / proxy corporativo

Solicite ao suporte o certificado publico da **CA raiz institucional** e, quando necessario, as intermediarias, em formato **PEM/Base-64**. A extensao pode ser `.pem` ou `.cer`, mas o conteudo precisa ter `-----BEGIN CERTIFICATE-----`. Nao use chave privada. Confirme a origem/impressao digital com o suporte antes de confiar no arquivo. Nao versione certificados institucionais no checkout.

Para os downloads Node/npm no build:

```powershell
.\scripts\build_run.ps1 -Profile demo -CaCertificateFile 'C:\Desenvolvimento\certificados\ca-institucional.pem'
```

O parametro configura `NODE_EXTRA_CA_CERTS` antes de iniciar Node/npm e restaura o valor anterior ao encerrar. Sem o parametro, preserva a configuracao da sessao. Ele nao altera o truststore Java nem o Git. Se npm ja possui `cafile`/`ca` explicito, confirme com o suporte que esse bundle tambem contem a CA institucional, pois configuracoes explicitas de CA podem prevalecer sobre as CAs adicionais do Node.

Para instalar manualmente as dependencias ou executar Vite, configure antes de iniciar o processo:

```powershell
$env:NODE_EXTRA_CA_CERTS = 'C:\Desenvolvimento\certificados\ca-institucional.pem'
```

Para Git, quando o proprio Git indicar erro de certificado, uma configuracao por comando e:

```powershell
git -c http.sslCAInfo='C:/Desenvolvimento/certificados/ca-institucional.pem' pull --ff-only origin main
```

Java/Maven e LDAPS usam outro mecanismo: um truststore Java com a cadeia institucional, conforme a secao LDAPS. Ele pode ficar em uma pasta do usuario e ser selecionado via `JAVA_TOOL_OPTIONS`, sem instalacao administrativa. O suporte deve fornecer/orientar um truststore que preserve as CAs publicas necessarias. Nao desative HTTPS com `strict-ssl=false`, `NODE_TLS_REJECT_UNAUTHORIZED=0` ou `http.sslVerify=false`.

Erros como `SELF_SIGNED_CERT_IN_CHAIN`, `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` e `PKIX path building failed` indicam problemas de confianca TLS. `TAR_ENTRY_ERROR ENOENT`, isoladamente, nao comprova falha de certificado.

### Atualizacao com stash automatico

`git_local_upd.ps1` guarda as alteracoes rastreadas (inclusive staged) e os arquivos nao rastreados antes de mudar para `main` e executar o pull. Usa `git stash save --include-untracked` para funcionar tambem em versoes antigas do Git. Arquivos ignorados, como `.env`, `node_modules` e `target`, nao entram no stash e permanecem no disco.

```powershell
.\scripts\git_local_upd.ps1
.\scripts\build_run.ps1 -Profile demo
```

O script mostra o identificador completo do stash e o comando de recuperacao. As alteracoes **nao sao reaplicadas automaticamente**, para nao substituir os scripts atualizados ou causar conflitos durante a atualizacao. O stash fica preservado mesmo se o pull falhar.

```powershell
git stash list
# Consulte ou recupere usando o SHA mostrado pelo script:
git stash show --stat SHA-DO-STASH
git stash apply SHA-DO-STASH
```

A recuperacao pode gerar conflitos; `apply` mantem a copia no stash. Stash e armazenamento local neste checkout, nao um backup enviado ao GitHub.

### Dashboard público e navegação compacta

`/` abre o Painel de Controle (`/index`), sem exigir login. Os GETs existentes `/api/dashboard/config`, `/resumo`, `/evolucao-anual`, `/analitico`, `/fatos` e `/pivot` são públicos. As APIs `/api/registros/**` e `/api/tabelas/**` continuam protegidas; login, manutenção e logout preservam sessão/CSRF.

Ajuda e identificação/login/logout ficam no canto superior direito do cabeçalho. O menu usa grupos expansíveis independentes, permite manter vários grupos abertos e possui uma única área de rolagem; os textos quebram linha. Os dez indicadores do Dashboard usam células compactas com rótulo e valor em losango: cinco colunas e duas linhas no desktop amplo, com adaptação para telas menores. Cores complementam os rótulos, sem substituí-los.
