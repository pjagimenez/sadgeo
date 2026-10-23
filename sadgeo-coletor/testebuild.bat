@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -File "%~dp0testes.ps1" %*
exit /b %errorlevel%
