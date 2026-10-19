# SADGEO — versão 0.1.0

Portal React + Material UI + TypeScript, API REST JSON Spring Boot 3.5 e persistência Oracle. O build gera **um único JAR**, com API e interface no mesmo endereço. Java 17 ou 21, Maven 3.9+ e Node.js 22.12+ (ou 24 LTS) com npm são necessários para compilar. Para executar o JAR pronto, basta Java.

## 1. Executar sem Oracle (demonstração)

Na raiz do repositório:

```sh
cd sadgeoweb
mvn clean verify
java -jar target/sadgeo-0.1.0.jar --spring.profiles.active=demo
```

O Maven executa `npm ci`, compila o React e copia o resultado para o JAR. Abra o endereço da aplicação na porta **8080** em sua máquina. O perfil `demo` não conecta ao banco e exibe um aviso permanente de **dados fictícios**. Não use esse perfil para conferir indicadores reais. Na página de login, clique em **Entrar na demonstração**; não informe credenciais.

O portal incorpora o layout de `sadgeo-react-web.7z`: login pêssego/violeta, cabeçalho, menu lateral, ajuda, tema/projeto, rodapé e grade Material UI com seleção e detalhes. Rotas: `/login`, `/index` e `/registros`. O tema filtra os registros; o dashboard apresenta os totais gerais. A grade consulta os fatos analíticos, não edita estações.

Verificação por terminal:

```sh
curl --fail http://127.0.0.1:8080/api/dashboard/config
# Sem sessão, esta consulta retorna HTTP 401:
curl -i http://127.0.0.1:8080/api/dashboard/resumo
curl --fail http://127.0.0.1:8080/actuator/health
```

## 2. Executar com o Oracle existente

A configuração não armazena credenciais. Defina as variáveis no terminal, IDE ou gerenciador de segredos do ambiente:

```sh
export SADGEO_DB_URL='jdbc:oracle:thin:@//HOST:1521/SERVICE_NAME'
export SADGEO_DB_USERNAME='seu_usuario'
read -rsp 'Senha Oracle: ' SADGEO_DB_PASSWORD; echo
export SADGEO_DB_PASSWORD
export SADGEO_DB_SCHEMA='BDG_VALIDA'
java -jar target/sadgeo-0.1.0.jar --spring.profiles.active=prod
```

No PowerShell, use `$env:SADGEO_DB_URL = '...'` e defina as demais variáveis pelo mecanismo seguro da sua organização. Não coloque senhas em arquivos versionados nem em argumentos de execução.

É necessário alcançar o Oracle pela rede e ter permissão de leitura nas tabelas/views já mapeadas em `dominio`. O Hibernate usa `ddl-auto=validate`: **não cria nem migra o banco**. Os mapeamentos existentes fixam o schema `BDG_VALIDA`; mudar apenas `SADGEO_DB_SCHEMA` não remapeia entidades que declaram esse schema explicitamente.

Sem conexão, credenciais ou objetos corretos, a aplicação pode falhar na inicialização. Nenhum erro do Oracle ativa dados demonstrativos automaticamente.

### Login institucional

Configure também `SADGEO_LDAP_URL` (por exemplo, `ldaps://SERVIDOR_AD:636`) e `SADGEO_LDAP_DOMAIN` com os dados fornecidos pela instituição. O JDK precisa confiar no certificado do AD; use o truststore institucional, sem desabilitar TLS. O login faz bind do próprio usuário por Spring Security, sem credenciais fixas. Sem configuração, o formulário fica desabilitado e o backend recusa o login. A integração ainda precisa ser validada com o AD real.

Consultas exigem sessão no servidor. O cliente obtém CSRF em `GET /api/auth/csrf`, envia credenciais por `POST /api/auth/login` (formulário URL-encoded), consulta `GET /api/auth/me` e encerra em `POST /api/auth/logout`. Respostas são JSON; logout retorna 204. A entrada `POST /api/auth/demo` só funciona no perfil demo. Senhas e tokens não são salvos em localStorage. Use HTTPS em produção. A autorização por módulo ainda não foi implementada; usuários autenticados têm acesso de consulta.

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
cp target/sadgeo-0.1.0.jar target/ocp/
oc start-build sadgeo --from-dir=target/ocp --follow
```

Isso pressupõe um BuildConfig `sadgeo` existente, login no cluster e acesso à imagem interna Java 17. Configure `SADGEO_DB_*` por Secret/configuração do deployment. O processo é `java -jar /deployments/app.jar`, porta 8080. Processos locais de desenvolvimento não são necessários em produção.

**A versão 0.1 é uma base interna de leitura.** Consultas exigem sessão e CSRF permanece ativo. O login LDAPS depende da configuração e validação institucional; a autorização detalhada por módulo precisa ser definida antes de ampliar o acesso. Credenciais presentes no histórico antigo do Git devem ser rotacionadas pelos responsáveis.

## Escopo da migração

- Vaadin, seus plugins, bundles e classes de interface foram removidos.
- O template anterior foi adaptado à API 0.1. Componentes/contextos ausentes foram reconstruídos. A imagem `back7.jpg` não estava no arquivo original; usa-se fundo CSS. Nenhum mock antigo autentica usuários em produção.
- React preserva indicadores de situação, evolução anual, gráfico ano/campanha, resumo analítico e fatos, com busca e paginação local.
- Serviços, DTOs, entidades, repositórios Oracle e estrutura OLAP Java foram mantidos.
- Esta versão cobre o **dashboard**. As páginas de levantamento, análise, homologação, relatórios e administração do Vaadin eram esboços e não viraram módulos funcionais. O esboço de cadastro/edição de estação também não está disponível na interface 0.1; seus serviços e entidades foram preservados para a próxima etapa.
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
