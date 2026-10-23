file: /sidgeo/sidgeo.py
Created on Tue Feb 25 16:04:38 2025
@author: pjag

Resumo
------
Interface gráfica principal do SIDGEO, construída em Tkinter. Este módulo contém
a classe :class:`Aplicativo`, que orquestra os frames de UI, integra-se ao
repositório de dados (:class:`RepositorioDados`) e oferece fluxos de importação,
exportação, consulta e edição de registros (instâncias de ``Registro`` criadas
por :class:`RegistroFactory`).

Colaboradores (POO)
-------------------
- **RepositorioDados**: serviço de persistência e manipulação do dataset (pandas).
- **RegistroFactory**: fabrica objetos de domínio ``Registro`` a partir de dicts.
- **InfoBasicasFrame**: frame (Tk) que gerencia campos básicos do registro.
- **CoordenadasFrame**: frame (Tk) para coleta/edição de coordenadas.
- **ObservacoesFrame**: frame (Tk) para textos livres e anotações.
- **RegistroFrame**: frame (Tk) com controles (Salvar/Excluir/Limpar/Buscar) e listbox.
- **DatasetFrame**: frame (Tk) com operações de importação/exportação/visualização.
- **IntegradorSadgeo**: diálogo (Tk) para integração e ingestão via SADGEO.

I/O Externo
-----------
- Arquivos: leitura e escrita de CSV/JSON via :class:`RepositorioDados`.
- Logs: arquivo rotativo em ``<UserLogDir>/<APP_SIGLA>/sidgeo.log``.
- UI: janelas e diálogos Tkinter (modais e não-modais).

Como gerar o executável (PyInstaller)
-------------------------------------
Atualizar bibliotecas do Python::

    python -m pip install --upgrade pip
    pip install tkcalendar pandas pyinstaller charset_normalizer
    pip install -r requirements.txt
    pip install platformdirs

Gerar o SIDGEO.EXE::

    python -m PyInstaller --onefile --windowed --hidden-import=tkcalendar \
        --hidden-import=pandas --hidden-import=charset_normalizer \
        --hidden-import=babel.numbers --collect-submodules platformdirs \
        --collect-all pandas sidgeo.py

ou::

    pyinstaller sidgeo.spec

Distribuição::

    dist\\sidgeo.exe
    (*) leve um sidgeo.csv em branco (1ª crítica) ou preenchido (2ª crítica).

Notas de Estilo
---------------
- Docstrings no **padrão Google** (PEP 257 + Google Style).
- Comentários curtos com ``#`` para trechos específicos de implementação.
- Os tipos são informativos (``typing``) para melhorar legibilidade/IDE.
"""