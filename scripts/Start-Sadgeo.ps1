[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('demo', 'dev', 'prod')]
    [string]$Profile,

    [string]$JavaHome = $env:JAVA_HOME,
    [ValidateRange(1, 65535)]
    [int]$Port = 8080,
    [switch]$Update,
    [switch]$SkipBuild
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

function Invoke-Checked {
    param([string]$Command, [string[]]$Arguments)
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao executar $Command (codigo $LASTEXITCODE)."
    }
}

Push-Location $repoRoot
try {
    if ([string]::IsNullOrWhiteSpace($JavaHome)) {
        throw 'Informe -JavaHome ou configure JAVA_HOME apontando para o JDK 17.'
    }
    $javaName = if ($env:OS -eq 'Windows_NT') { 'java.exe' } else { 'java' }
    $java = Join-Path $JavaHome "bin/$javaName"
    $releaseFile = Join-Path $JavaHome 'release'
    if (!(Test-Path $java) -or !(Test-Path $releaseFile)) {
        throw 'JavaHome deve apontar para uma instalacao valida do JDK 17.'
    }
    $release = Get-Content $releaseFile -Raw
    if ($release -notmatch '(?m)^JAVA_VERSION="17(?:\.|\")') {
        throw 'SADGEO requer JDK 17. Ajuste -JavaHome ou JAVA_HOME.'
    }
    $env:JAVA_HOME = (Resolve-Path $JavaHome).Path
    $java = Join-Path $env:JAVA_HOME "bin/$javaName"
    $env:PATH = "$(Join-Path $env:JAVA_HOME 'bin')$([IO.Path]::PathSeparator)$env:PATH"

    if ($Update) {
        $changes = & git status --porcelain
        if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel consultar o checkout Git.' }
        if ($changes) { throw 'Ha alteracoes locais. Salve-as antes de usar -Update.' }
        Invoke-Checked -Command 'git' -Arguments @('checkout', 'main')
        Invoke-Checked -Command 'git' -Arguments @('pull', '--ff-only', 'origin', 'main')
    }

    Set-Location (Join-Path $repoRoot 'sadgeoweb')
    if (!$SkipBuild) {
        $maven = if ($env:OS -eq 'Windows_NT') { 'mvn.cmd' } else { 'mvn' }
        Invoke-Checked -Command $maven -Arguments @('clean', 'verify')
    }
    [xml]$pom = Get-Content 'pom.xml' -Raw
    $version = [string]$pom.project.version
    $jar = Join-Path 'target' "sadgeo-$version.jar"
    if (!(Test-Path $jar)) { throw "JAR ausente: $jar. Execute sem -SkipBuild." }

    Write-Host "Iniciando SADGEO $version | profile=$Profile | porta=$Port | JDK 17"
    Invoke-Checked -Command $java -Arguments @('-jar', $jar, "--spring.profiles.active=$Profile", "--server.port=$Port")
}
finally {
    Pop-Location
}
