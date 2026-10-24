Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-Python {
    param([string]$Executable, [string[]]$Arguments)
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falha no Python (codigo $LASTEXITCODE): $($Arguments -join ' ')"
    }
}

function Test-WindowsPythonAlias {
    param([string]$Path)
    # Atalhos do App Execution Alias nao sao a instalacao real do Python.
    return $Path -match '[\\/]Microsoft[\\/]WindowsApps[\\/]python(?:\d+(?:\.\d+)?)?\.exe$'
}

function Resolve-Python {
    param([string]$Executable)
    if (Test-Path -LiteralPath $Executable -PathType Leaf) {
        $resolved = (Resolve-Path -LiteralPath $Executable).ProviderPath
        if (Test-WindowsPythonAlias $resolved) {
            throw "O caminho '$resolved' e um alias do WindowsApps. Informe o Python real com -Python 'C:\pasta\python.exe'."
        }
        return [string]$resolved
    }
    if ($Executable -match '[\\/]') {
        throw "Executavel Python nao encontrado: '$Executable'. Confira o caminho informado em -Python."
    }
    # Get-Command pode retornar varias instalacoes. Escolhe apenas uma, na ordem do PATH,
    # sem juntar seus caminhos nem executar os atalhos da Microsoft Store.
    $commands = @(Get-Command -Name $Executable -CommandType Application -All -ErrorAction SilentlyContinue)
    $command = $commands | Where-Object {
        $_.Source -and -not (Test-WindowsPythonAlias $_.Source)
    } | Select-Object -First 1
    if ($null -eq $command) {
        throw "Python real nao encontrado no PATH (aliases WindowsApps sao ignorados). Use -Python 'C:\pasta\python.exe'."
    }
    return [string]$command.Source
}
