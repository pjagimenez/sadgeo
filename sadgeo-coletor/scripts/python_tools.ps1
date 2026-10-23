Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-Python {
    param([string]$Executable, [string[]]$Arguments)
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falha no Python (codigo $LASTEXITCODE): $($Arguments -join ' ')"
    }
}

function Resolve-Python {
    param([string]$Executable)
    if (Test-Path -LiteralPath $Executable -PathType Leaf) {
        return (Resolve-Path -LiteralPath $Executable).Path
    }
    $command = Get-Command $Executable -CommandType Application -ErrorAction Stop
    return $command.Source
}
