[CmdletBinding()]
param(
    [string]$Python = '',
    [switch]$SkipGui,
    [switch]$NoTranscript
)
. "$PSScriptRoot\scripts\python_tools.ps1"
Push-Location $PSScriptRoot
$transcriptStarted = $false
try {
    New-Item -ItemType Directory -Force -Path 'logs' | Out-Null
    if (-not $NoTranscript) {
        Start-Transcript -Path (Join-Path $PSScriptRoot 'logs\resultado-testes.txt') -Force | Out-Null
        $transcriptStarted = $true
    }
    & "$PSScriptRoot\scripts\test_python_tools.ps1"
    if (-not $Python) {
        $Python = if (Test-Path '.venv\Scripts\python.exe') { '.venv\Scripts\python.exe' } else { 'python' }
    }
    $pythonExe = Resolve-Python $Python
    Write-Host "Python: $pythonExe"
    # O script de build instala as ferramentas. Este script nunca altera o ambiente.
    Invoke-Python $pythonExe @('-m', 'pip', 'check')
    Invoke-Python $pythonExe @('testebuild.py')
    Invoke-Python $pythonExe @('-m', 'pylint', 'sidgeo', '--disable=all', '--enable=E,F', '--ignore=extras,imagem')
    Invoke-Python $pythonExe @('-m', 'pyright', '--pythonpath', $pythonExe)
    $pytestArgs = @('-m', 'pytest', '-q')
    if ($SkipGui) { $pytestArgs += @('-m', 'not gui') } else { $pytestArgs += '--require-gui' }
    Invoke-Python $pythonExe $pytestArgs
    if ($NoTranscript) { Write-Host 'Verificacoes concluidas.' }
    else { Write-Host 'Testes concluidos. Relatorio: logs\resultado-testes.txt' }
}
finally {
    if ($transcriptStarted) { Stop-Transcript | Out-Null }
    Pop-Location
}
