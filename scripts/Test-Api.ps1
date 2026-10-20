# PowerShell 7+ (Windows/Linux). Uses a cookie session and CSRF; never writes to Oracle.
param(
    [string]$BaseUrl = 'http://127.0.0.1:8080',
    [switch]$Crud
)
$ErrorActionPreference = 'Stop'
Import-Module Microsoft.PowerShell.Utility
$BaseUrl = $BaseUrl.TrimEnd('/')
$session = [Microsoft.PowerShell.Commands.WebRequestSession]::new()
$created = $false
$testCode = $null
function Invoke-Api {
    param([string]$Method, [string]$Path, [int]$Expected = 200, $Data = $null, [switch]$Form)
    $headers = @{}
    if ($Method -ne 'GET') {
        $csrf = Invoke-RestMethod -Uri "$BaseUrl/api/auth/csrf" -WebSession $session -TimeoutSec 60
        $headers[$csrf.headerName] = $csrf.token
    }
    $arguments = @{ Uri = "$BaseUrl$Path"; Method = $Method; WebSession = $session; Headers = $headers; TimeoutSec = 60; SkipHttpErrorCheck = $true }
    if ($null -ne $Data) {
        if ($Form) { $arguments.Body = $Data; $arguments.ContentType = 'application/x-www-form-urlencoded' }
        else { $arguments.Body = [Text.Encoding]::UTF8.GetBytes(($Data | ConvertTo-Json -Depth 10 -Compress)); $arguments.ContentType = 'application/json; charset=utf-8' }
    }
    $response = Invoke-WebRequest @arguments
    if ([int]$response.StatusCode -ne $Expected) { throw "FAIL $Method $Path : HTTP $($response.StatusCode), esperado $Expected. $($response.Content)" }
    if ($response.Content) { return ($response.Content | ConvertFrom-Json) }
}
try {
    $null = Invoke-Api GET '/actuator/health'
    $config = Invoke-Api GET '/api/dashboard/config'
    if ($Crud -and -not $config.demo) { throw '-Crud só é permitido em demo; o script não altera Oracle real.' }
    $null = Invoke-Api GET '/api/dashboard/resumo'
    $facts = Invoke-Api GET '/api/dashboard/fatos-pagina?size=2'
    if ($facts.size -ne 2 -or $facts.items.Count -gt 2 -or $facts.total -lt $facts.items.Count) { throw 'Paginacao de fatos invalida.' }
    $null = Invoke-Api GET '/api/dashboard/fatos-filtros'
    $null = Invoke-Api GET '/api/registros/critica' 401
    if ($config.demo) { $null = Invoke-Api POST '/api/auth/demo' }
    else {
        $credential = Get-Credential -Message 'Login institucional do SADGEO'
        if ($null -eq $credential) { throw 'Login cancelado.' }
        $login = @{ username = $credential.UserName; password = $credential.GetNetworkCredential().Password }
        try { $null = Invoke-Api POST '/api/auth/login' 200 $login -Form }
        finally { $login.Clear(); $credential = $null }
    }
    $null = Invoke-Api GET '/api/auth/me'
    $null = Invoke-Api GET '/api/dashboard/resumo'
    $null = Invoke-Api GET '/api/registros/critica'
    $contexts = [ordered]@{ altimetria='medA'; gravimetria='medG'; planimetria='medP'; vrf='vrf'; veg='veg'; ogr='ogr'; gabinete='gab' }
    foreach ($entry in $contexts.GetEnumerator()) {
        $result = Invoke-Api GET "/api/registros/$($entry.Key)?size=100&campanha=tentativa-de-troca"
        if ($result.campanha -cne $entry.Value) { throw "Filtro incorreto: $($entry.Key)" }
        foreach ($row in $result.items) { if ($row.campanha -cne $entry.Value) { throw "Campanha indevida em $($entry.Key)" } }
        if ($config.demo -and $result.total -le 0) { throw "Demo sem registros para $($entry.Key)" }
        Write-Host "OK filtro $($entry.Key) = $($entry.Value)"
    }
    $null = Invoke-Api GET '/api/registros/critica?size=999' 400
    $null = Invoke-Api GET '/api/registros/desconhecido' 404
    $null = Invoke-Api GET '/api/tabelas'
    $locations = Invoke-Api GET '/api/tabelas/localizacao'
    if (($locations.meta.keys -join ',') -ne 'TIPO_LOCAL') { throw 'PK Localização inesperada.' }
    $campaign = Invoke-Api GET '/api/tabelas/campanha/meta'
    if (($campaign.keys | Sort-Object) -join ',' -ne 'COD_CAMPANHA,COD_INSTITUICAO,COD_PROJETO') { throw 'PK Campanha inesperada.' }
    $null = Invoke-Api GET '/api/tabelas/pendencia'
    if ($Crud) {
        foreach ($candidate in @('Z9','Z8','Z7','Z6','Z5','Z4','Z3','Z2','Z1','Z0')) {
            $existing = Invoke-Api GET "/api/tabelas/localizacao?q=$candidate"
            if ($existing.total -eq 0) { $testCode = $candidate; break }
        }
        if (-not $testCode) { throw 'Nenhum código livre para o teste.' }
        $null = Invoke-Api POST '/api/tabelas/localizacao' 201 @{ TIPO_LOCAL=$testCode; DESCRICAO='Teste automatizado' }
        $created = $true
        $null = Invoke-Api PUT '/api/tabelas/localizacao' 200 @{ key=@{ TIPO_LOCAL=$testCode }; values=@{ DESCRICAO='Teste atualizado' } }
        $row = Invoke-Api GET "/api/tabelas/localizacao/item?TIPO_LOCAL=$testCode"
        if ($row.DESCRICAO -ne 'Teste atualizado') { throw 'Atualização não confirmada.' }
        $null = Invoke-Api DELETE '/api/tabelas/localizacao' 204 @{ key=@{ TIPO_LOCAL=$testCode } }
        $created = $false
        $null = Invoke-Api GET "/api/tabelas/localizacao/item?TIPO_LOCAL=$testCode" 404
        Write-Host 'OK CRUD Localização (demo), com limpeza do registro criado'
    }
    $null = Invoke-Api POST '/api/auth/logout' 204
    $null = Invoke-Api GET '/api/dashboard/resumo'
    $facts = Invoke-Api GET '/api/dashboard/fatos-pagina?size=2'
    if ($facts.size -ne 2 -or $facts.items.Count -gt 2 -or $facts.total -lt $facts.items.Count) { throw 'Paginacao de fatos invalida.' }
    $null = Invoke-Api GET '/api/dashboard/fatos-filtros'
    $null = Invoke-Api GET '/api/registros/critica' 401
    Write-Host 'PASS: saúde, login, sessão, dashboard, campanhas, catálogos e logout'
}
finally {
    if ($created) {
        try { $null = Invoke-Api DELETE '/api/tabelas/localizacao' 204 @{ key=@{ TIPO_LOCAL=$testCode } } }
        catch { Write-Warning "Não foi possível limpar o código de teste $testCode" }
    }
}
