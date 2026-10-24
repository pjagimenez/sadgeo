[CmdletBinding()]
param(
    [string]$Python = 'python',
    [switch]$InstallDependencies,
    [switch]$Run
)
. "$PSScriptRoot\scripts\python_tools.ps1"
Push-Location $PSScriptRoot
$transcriptStarted = $false
try {
    New-Item -ItemType Directory -Force -Path 'logs' | Out-Null
    Start-Transcript -Path (Join-Path $PSScriptRoot 'logs\resultado-build.txt') -Force | Out-Null
    $transcriptStarted = $true
    if (-not (Test-Path '.venv\Scripts\python.exe')) {
        $bootstrapPython = Resolve-Python $Python
        Write-Host "Python selecionado para criar .venv: $bootstrapPython"
        Invoke-Python $bootstrapPython @('-m', 'venv', '.venv')
    }
    $pythonExe = (Resolve-Path '.venv\Scripts\python.exe').Path
    Write-Host "Python do ambiente: $pythonExe"
    Invoke-Python $pythonExe @('--version')
    $hashInput = ((Get-FileHash 'requirements.txt', 'requirements-dev.txt' -Algorithm SHA256).Hash -join ':')
    $marker = Join-Path $PSScriptRoot '.venv\.sidgeo-dependencies.sha256'
    $previousHash = if (Test-Path $marker) { (Get-Content $marker -Raw).Trim() } else { '' }
    if ($InstallDependencies -or $previousHash -ne $hashInput) {
        Invoke-Python $pythonExe @('-m', 'pip', 'install', '-r', 'requirements.txt', '-r', 'requirements-dev.txt')
        Set-Content -Path $marker -Value $hashInput -Encoding ASCII
    } else {
        Write-Host 'Dependencias sem alteracao; instalacao dispensada.'
    }
    # Falhas de testes interrompem a geracao do executavel.
    & "$PSScriptRoot\testes.ps1" -Python $pythonExe -NoTranscript
    Invoke-Python $pythonExe @('-m', 'PyInstaller', '--noconfirm', '--clean', 'sidgeo.spec')
    $exe = Join-Path $PSScriptRoot 'dist\sidgeo.exe'
    if (-not (Test-Path $exe -PathType Leaf)) { throw 'Executavel nao encontrado apos o build.' }
    # Start-Process -Wait tambem aguarda executaveis Windows sem console.
    $process = Start-Process -FilePath $exe -ArgumentList '--smoke-test' -Wait -PassThru
    if ($process.ExitCode -ne 0) { throw "Falha na inicializacao do executavel (codigo $($process.ExitCode))." }
    Write-Host "Build e teste do executavel concluidos: $exe"
    if ($Run) { Start-Process -FilePath $exe | Out-Null }
}
finally {
    if ($transcriptStarted) { Stop-Transcript | Out-Null }
    Pop-Location
}
