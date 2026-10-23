# SIDGEO — Coletor de campo

Aplicativo desktop Python/Tkinter para preparar e revisar registros de estações geodésicas. Versão **v1.0.261023**, independente da versão do portal `sadgeoweb`.

A tela segue a paleta e a organização do [DynAdjustWeb](https://github.com/pjagimenez/DynAdjustWeb): cabeçalho verde escuro, painéis claros, botões compactos e destaque para a ação principal. Na resolução **1366 × 768**, a janela reserva espaço para a barra de tarefas. Os campos estão em três abas, com rolagem quando necessário:

- **Identificação e campanha:** estação, situação, informante, projeto, campanha e datas.
- **Coordenadas:** latitude/longitude, fonte, atualização e possibilidade de ocupação.
- **Descrição e acesso:** descrição, localização, itinerário e observação.

A listagem e os botões Salvar, Limpar, Coordenadas BDG e Excluir ficam visíveis à direita. Importar/exportar arquivos, consultar SADGEO e ver/zerar a base ficam na barra inferior. Aplicar coordenadas do BDG altera o formulário; clique em **Salvar registro** para persistir.

![Coletor em uma tela de 1366 × 768](docs/sidgeo-1366x768.png)

## Build no Windows com PowerShell

Use Python **3.11 ou superior, com Tkinter e suporte a `venv`/`pip`**; a validação nesta alteração usou Python 3.12. Uma distribuição portátil completa pode ficar em uma pasta gravável, sem instalação administrativa. O pacote *embeddable* mínimo do Python não inclui todos esses componentes.

Depois de atualizar o repositório, entre na pasta do coletor:

```powershell
cd .\sadgeo-coletor
.\build.ps1
```

Se o Python não estiver no PATH, informe o executável para criar o ambiente:

```powershell
.\build.ps1 -Python 'C:\Desenvolvimento\Python312\python.exe'
```

O script cria `.venv`, instala dependências quando os arquivos `requirements*.txt` mudam, verifica imports, Pylint, Pyright e testes automatizados, gera **`dist\sidgeo.exe`** e executa um teste de inicialização do próprio executável com uma base temporária. Qualquer falha interrompe o processo. Não é necessário ativar o `venv` nem ter permissão administrativa.

Nas execuções seguintes, a instalação é dispensada se os requisitos não mudaram. Para reinstalar as dependências ou abrir a aplicação ao terminar:

```powershell
.\build.ps1 -InstallDependencies
.\build.ps1 -Run
```

`-Python` seleciona o Python usado para **criar** `.venv`; um ambiente já criado continua sendo reutilizado. O executável Windows deve ser gerado **no Windows**. A primeira extração de um executável `onefile` pode demorar alguns segundos.

Se a política institucional bloquear scripts, use o procedimento autorizado pelo administrador. Os scripts não alteram a política de execução, o Git, certificados ou configurações globais.

## Rodar durante o desenvolvimento

Depois de preparar o ambiente com o build:

```powershell
.\.venv\Scripts\python.exe app.py
```

Para preparar apenas as dependências, sem gerar o executável:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.\.venv\Scripts\python.exe app.py
```

A entrada atual é **`app.py`** e o empacotamento oficial usa **`sidgeo.spec`**, compatível com PyInstaller 6. Os arquivos `build.bat` e `testebuild.bat` encaminham para os scripts PowerShell e propagam seu código de erro.

## Testar sem gerar o executável

```powershell
.\testes.ps1
# Ou selecionar outro ambiente já preparado:
.\testes.ps1 -Python 'C:\Ambientes\sidgeo\Scripts\python.exe'
# Sem uma sessão gráfica (omite explicitamente os testes de tela):
.\testes.ps1 -SkipGui
```

O teste completo exige sessão gráfica e cobre abertura e dimensionamento em 1366 × 768, abas, edição, listagem, exclusão com confirmação, importação/exportação, diálogos de arquivo, comparação BDG e encerramento. Também verifica reabertura do HDF5, zeros à esquerda e preservação da base quando uma gravação falha. Os testes usam dados sintéticos e diretórios temporários, sem acessar a base de trabalho ou as APIs institucionais.

Para executar diretamente em Linux, com Tkinter e sessão gráfica disponíveis:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m pytest -q --require-gui
.venv/bin/python -m PyInstaller --noconfirm --clean sidgeo.spec
./dist/sidgeo --smoke-test
```

## Logs e dados locais

| Arquivo | Conteúdo |
|---|---|
| `logs\resultado-build.txt` | Instalação, verificações, empacotamento e resultado do build |
| `logs\resultado-testes.txt` | Execução avulsa de `testes.ps1` |
| `sidgeo.log`, no diretório de logs do usuário | Eventos e exceções da aplicação, inclusive callbacks Tkinter; rotação de até três arquivos de 500 KB |
| `sidgeo.h5`, no diretório de dados do usuário | Base de trabalho local |

Os caminhos da aplicação são definidos por `platformdirs`. Para ver os caminhos exatos no seu computador:

```powershell
.\.venv\Scripts\python.exe -c "import platformdirs; print('Dados:', platformdirs.user_data_dir('SIDGEO', appauthor=False, roaming=False)); print('Logs:', platformdirs.user_log_dir('SIDGEO', appauthor=False))"
```

A base é salva após cada alteração e não fica dentro do executável. Faça backup antes de substituir uma versão em uso. Falhas de leitura preservam o arquivo original e são reportadas; falhas de escrita preservam o último arquivo salvo. **Zerar base local** exige confirmação. CSV usa `;` como separador; JSON usa uma lista de registros. A chave lógica continua sendo `cod_estacao`: importar a mesma estação atualiza seu registro. Uma importação com registros inválidos informa quantos foram processados e mantém os válidos já gravados.

## Integrações e certificados

As URLs BDG/SADGEO estão em `sidgeo/util/settings.py`; os contratos das APIs reais precisam ser validados na rede institucional. Os testes automatizados não enviam dados a esses serviços.

Se houver uma autoridade certificadora interna, configure o certificado PEM aprovado para cada ferramenta, sem desativar a validação HTTPS:

```powershell
# Downloads de pacotes pelo pip, quando necessário:
$env:PIP_CERT = 'C:\Certificados\cadeia-institucional.pem'
# Consultas HTTPS da aplicação via requests, quando necessário:
$env:REQUESTS_CA_BUNDLE = 'C:\Certificados\cadeia-institucional.pem'
```

Se os downloads e as consultas funcionam normalmente, essas variáveis não precisam ser definidas.

## Organização

`view` contém os widgets e diálogos; `application` coordena os casos de uso; `domain` contém registro, validação e mapeamento; `infra` implementa persistência, arquivos, logs e clientes HTTP. `tests` contém os testes de regressão; `typings/tkcalendar` descreve a API utilizada dessa biblioteca para a análise estrita do Pyright. As pastas `old`, `extras` e `imagem` contêm material legado ou experimental e não compõem a aplicação empacotada.

## Validação desta alteração

Foram executados **30 testes**, incluindo a interface em display virtual de 1366 × 768 e com fontes ampliadas, além da análise estrita do Pyright (zero erros/avisos), Pylint nas categorias de erro e verificação de imports. `testes.ps1` foi executado com PowerShell 7.4; a sintaxe dos scripts, argumentos com espaços e interrupção por código de erro também foram verificados.

O empacotamento PyInstaller 6 e o teste `--smoke-test` foram validados em Linux/Python 3.12. A geração e a execução do **`.exe` Windows** devem ser validadas no Windows com `build.ps1`; esta sessão não dispõe desse sistema operacional. Os scripts usam comandos compatíveis com Windows PowerShell 5.1.
