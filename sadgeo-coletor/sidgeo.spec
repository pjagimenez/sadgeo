#sidgeo.spec
# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files


project_path = os.path.abspath('.')  # ou o caminho absoluto do projeto

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[project_path],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkcalendar',
        'pandas',
        'charset_normalizer',
        'babel.numbers',
        'platformdirs',
        'jinja2'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

# Coleta todos os submódulos de pandas e platformdirs
a.datas += collect_all('pandas')[1]
a.datas += collect_all('platformdirs')[1]
a.datas += collect_all('charset_normalizer')[1]
a.datas += collect_all('babel')[1]

# Inclui todos os submódulos e dados do pacote sidgeo
a.hiddenimports += collect_submodules('sidgeo')

# Exclui testes desnecessários
a.excludes += ['pandas.tests']

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    [],  # ← runtime_hooks (mesmo vazio, precisa estar aqui)
    a.datas,
    name='sidgeo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False  # Altere para True se quiser ver o console
)
