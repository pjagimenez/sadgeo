# Testes isolados de resolucao do Python. Nao requerem Python, Pester ou acesso a rede.
[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$helper = Join-Path $PSScriptRoot 'python_tools.ps1'
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('sidgeo python tools ' + [guid]::NewGuid().ToString('N'))
$testCount = 0

function Assert-Equal {
    param($Actual, $Expected, [string]$Label)
    if ($Actual -cne $Expected) { throw "$Label : esperado '$Expected'; obtido '$Actual'." }
}

try {
    New-Item -ItemType Directory -Path $tempRoot | Out-Null
    # O mock fica no escopo filho de cada caso; nao modifica o PATH ou os comandos do chamador.
    $real = 'C:\Program Files\Python311\python.exe'
    $other = 'C:\Desenvolvimento\Python312\python.exe'
    $aliasPath = 'D:\Users\teste\AppData\Local\Microsoft\WindowsApps\python.exe'
    foreach ($case in @(
        @{ Paths = @($real, $aliasPath); Expected = $real },
        @{ Paths = @($aliasPath, $real); Expected = $real },
        @{ Paths = @($real, $other); Expected = $real },
        @{ Paths = @($real); Expected = $real },
        @{ Paths = @($aliasPath); Expected = $null },
        @{ Paths = @(); Expected = $null }
    )) {
        & {
            param($Case, [string]$Helper)
            . $Helper
            function Get-Command {
                param($Name, $CommandType, [switch]$All, $ErrorAction)
                foreach ($path in $Case.Paths) { [pscustomobject]@{ Source = $path } }
            }
            if ($null -eq $Case.Expected) {
                $failed = $false
                try { Resolve-Python 'sidgeo-python-not-a-local-file' | Out-Null }
                catch { $failed = $_.Exception.Message -match '-Python' }
                Assert-Equal $failed $true 'Ausencia de Python real deve explicar -Python'
            } else {
                $result = @(Resolve-Python 'sidgeo-python-not-a-local-file')
                Assert-Equal $result.Count 1 'A resolucao deve retornar um unico caminho'
                Assert-Equal ($result[0] -is [string]) $true 'O resultado deve ser uma string'
                Assert-Equal $result[0] $Case.Expected 'Escolha da instalacao real'
            }
        } $case $helper
        $testCount++
    }

    & {
        param([string]$TempRoot, [string]$Helper)
        . $Helper
        $pythonPath = Join-Path $TempRoot 'Python com espacos\python.exe'
        New-Item -ItemType Directory -Path (Split-Path -Parent $pythonPath) | Out-Null
        New-Item -ItemType File -Path $pythonPath | Out-Null
        $result = @(Resolve-Python $pythonPath)
        Assert-Equal $result.Count 1 'Caminho explicito com espacos'
        Assert-Equal $result[0] (Resolve-Path -LiteralPath $pythonPath).ProviderPath 'Caminho explicito preservado'

        $aliasPath = Join-Path $TempRoot 'Microsoft\WindowsApps\python3.exe'
        New-Item -ItemType Directory -Path (Split-Path -Parent $aliasPath) | Out-Null
        New-Item -ItemType File -Path $aliasPath | Out-Null
        $failed = $false
        try { Resolve-Python $aliasPath | Out-Null }
        catch { $failed = $_.Exception.Message -match 'alias do WindowsApps' }
        Assert-Equal $failed $true 'Alias explicito nao deve iniciar a Store'

        $failed = $false
        try { Resolve-Python (Join-Path $TempRoot 'nao-existe\python.exe') | Out-Null }
        catch { $failed = $_.Exception.Message -match 'nao encontrado' }
        Assert-Equal $failed $true 'Caminho inexistente deve gerar erro claro'
    } $tempRoot $helper
    $testCount += 3
    Write-Host "PowerShell: $testCount testes de selecao do Python aprovados."
}
finally {
    if (Test-Path -LiteralPath $tempRoot) { Remove-Item -LiteralPath $tempRoot -Recurse -Force }
}
