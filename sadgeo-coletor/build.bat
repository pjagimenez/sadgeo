@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -File "%~dp0build.ps1" %*
exit /b %errorlevel%
