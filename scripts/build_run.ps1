[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('demo', 'dev', 'prod')]
    [string]$Profile,

    [string]$JavaHome = $(if ($env:OS -eq 'Windows_NT') { 'C:\Desenvolvimento\jdk-17.0.20.1+1' } else { $env:JAVA_HOME }),
    [string]$CaCertificateFile,
    [ValidateRange(1, 65535)]
    [int]$Port = 8080,
    [switch]$SkipBuild
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$previousNodeExtraCa = $env:NODE_EXTRA_CA_CERTS

function Invoke-Checked {
    param([string]$Command, [string[]]$Arguments)
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao executar $Command (codigo $LASTEXITCODE)."
    }
}

Push-Location $repoRoot
try {
    if (![string]::IsNullOrWhiteSpace($CaCertificateFile)) {
        $caPath = (Resolve-Path -LiteralPath $CaCertificateFile).Path
        $pem = Get-Content -LiteralPath $caPath -Raw
        if ($pem -notmatch '-----BEGIN CERTIFICATE-----') {
            throw 'CaCertificateFile deve conter certificado(s) de CA em formato PEM/Base-64, sem chave privada.'
        }
        if ($pem -match 'PRIVATE KEY') { throw 'Informe somente certificados publicos de CA, sem chave privada.' }
        $env:NODE_EXTRA_CA_CERTS = $caPath
        Write-Host 'CA adicional configurada para Node/npm; validacao TLS permanece ativa.'
    }
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

    $hostPresent = ![string]::IsNullOrWhiteSpace($env:SADGEO_LDAP_HOST)
    $domainPresent = ![string]::IsNullOrWhiteSpace($env:SADGEO_LDAP_DOMAIN)
    $urlPresent = ![string]::IsNullOrWhiteSpace($env:SADGEO_LDAP_URL)
    Write-Host "LDAPS nesta sessao: SADGEO_LDAP_HOST informado=$hostPresent | SADGEO_LDAP_DOMAIN informado=$domainPresent | SADGEO_LDAP_URL informado=$urlPresent"
    if ($Profile -ne 'demo' -and (!$domainPresent -or (!$hostPresent -and !$urlPresent))) {
        Write-Warning 'Login institucional depende das propriedades recebidas pelo Java. Configure SADGEO_LDAP_HOST e SADGEO_LDAP_DOMAIN nesta sessao ou nas configuracoes Spring. .env nao e carregado automaticamente.'
    }
    Set-Location (Join-Path $repoRoot 'sadgeoweb')
    $logPath = if ([string]::IsNullOrWhiteSpace($env:SADGEO_LOG_FILE)) { Join-Path (Get-Location) 'logs/sadgeo.log' } else { $env:SADGEO_LOG_FILE }
    Write-Host "Log da aplicacao: $logPath"
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
    $env:NODE_EXTRA_CA_CERTS = $previousNodeExtraCa
    Pop-Location
}
