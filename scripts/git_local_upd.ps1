[CmdletBinding()]
param(
    [string]$Destination = (Split-Path -Parent $PSScriptRoot)
)

# Somente Git: nao compila, nao executa Java e nao altera ENVVARs.
$ErrorActionPreference = 'Stop'
$repository = 'https://github.com/pjagimenez/sadgeo.git'
$destinationPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Destination)

function Invoke-GitChecked {
    param([string[]]$Arguments)
    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falha no Git (codigo $LASTEXITCODE). Operacao interrompida."
    }
}

Get-Command git -ErrorAction Stop | Out-Null
if (!(Test-Path -LiteralPath $destinationPath)) {
    Invoke-GitChecked -Arguments @('clone', '--branch', 'main', '--single-branch', $repository, $destinationPath)
}
else {
    if (!(Test-Path -LiteralPath (Join-Path $destinationPath '.git'))) {
        throw 'O destino existe mas nao e um checkout Git. Escolha uma pasta nova com -Destination.'
    }
    Push-Location $destinationPath
    try {
        $origin = & git remote get-url origin
        if ($LASTEXITCODE -ne 0 -or $origin -notmatch '^(https://github\.com/|git@github\.com:)pjagimenez/sadgeo(?:\.git)?/?$') {
            throw 'O origin do destino nao corresponde a pjagimenez/sadgeo. Nenhuma atualizacao realizada.'
        }
        $changes = & git status --porcelain
        if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel consultar o estado do checkout.' }
        if ($changes) {
            $label = 'sadgeo-antes-update-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0, 8)
            Write-Host 'Guardando alteracoes locais e arquivos nao rastreados no stash...'
            # save is compatible with older Git versions, including those without git switch.
            Invoke-GitChecked -Arguments @('stash', 'save', '--include-untracked', $label)
            $stashCommit = & git rev-parse --verify refs/stash
            if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel confirmar o stash. Atualizacao interrompida.' }
            Write-Host "Alteracoes preservadas no stash: $stashCommit ($label)"
            Write-Host "Para recuperar depois: git stash apply $stashCommit"
            Write-Host 'O stash nao sera reaplicado nem removido automaticamente, mesmo se a atualizacao falhar.'
            $remaining = & git status --porcelain
            if ($LASTEXITCODE -ne 0 -or $remaining) {
                throw 'O checkout ainda possui alteracoes apos o stash. Atualizacao interrompida; confira git status.'
            }
        }
        Invoke-GitChecked -Arguments @('checkout', 'main')
        Invoke-GitChecked -Arguments @('pull', '--ff-only', 'origin', 'main')
    }
    finally {
        Pop-Location
    }
}
Write-Host "SADGEO baixado/atualizado em: $destinationPath"
