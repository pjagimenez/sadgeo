# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 6: executar a partir de build.ps1 (Windows) ou python -m PyInstaller sidgeo.spec.
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

project_path = Path(SPECPATH)
a = Analysis(
    [str(project_path / 'app.py')],
    pathex=[str(project_path)],
    binaries=[],
    datas=collect_data_files('babel'),
    hiddenimports=['babel.numbers', 'tkcalendar', 'tables'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas.tests'],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='sidgeo', debug=False, bootloader_ignore_signals=False,
    strip=False, upx=False, console=False,
)
