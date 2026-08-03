# Elsewhere API PowerShell Wrapper
# Equivalent to elsewhere-api.sh but runs natively on Windows

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Route,

    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$QueryArgs
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$EnvFile = Join-Path $ScriptDir ".env"

# Auto-load ELSEWHERE_KEY from .env if not already set
if (-not ($env:ELSEWHERE_KEY -match '^els_live_') -and (Test-Path $EnvFile)) {
    $envContent = Get-Content $EnvFile -Encoding UTF8
    foreach ($line in $envContent) {
        if ($line -match '^ELSEWHERE_KEY=(.+)$') {
            $env:ELSEWHERE_KEY = $Matches[1].Trim()
            break
        }
    }
}

$BaseUrl = "https://elsewhere.news/api/v1"

# Validate ELSEWHERE_KEY for non-check-version routes
if ($Route -ne "check-version") {
    if (-not ($env:ELSEWHERE_KEY -match '^els_live_[A-Za-z0-9_-]{43}$')) {
        Write-Error "ELSEWHERE_AUTH=missing_or_invalid: bind a personal key as ELSEWHERE_KEY"
        exit 11
    }
}

# Validate route against allowlist
$AllowedRoutes = @(
    '^/search/chunks$',
    '^/entities/(find|search)$',
    '^/relation-keys$',
    '^/topics$',
    '^/personas$',
    '^/me/(context|content-views|annotations|sessions|topics|whats-new)$',
    '^/entities/[A-Za-z0-9_-]+/(card|edges)$',
    '^/content/(article|podcast)/[A-Za-z0-9_-]+$',
    '^/(topics|personas)/[A-Za-z0-9_-]+$',
    '^/me/sessions/[A-Za-z0-9_-]+$'
)

$RouteAllowed = $false
foreach ($pattern in $AllowedRoutes) {
    if ($Route -match $pattern) {
        $RouteAllowed = $true
        break
    }
}

if (-not $RouteAllowed -and $Route -ne "check-version") {
    Write-Error "ELSEWHERE_REQUEST=invalid: route is not on the read-only allowlist"
    exit 2
}

if ($Route -eq "check-version") {
    # Anonymous version check
    $savedKey = $env:ELSEWHERE_KEY
    $env:ELSEWHERE_KEY = ""
    $env:AUTH_HEADER = ""
    $env:CURL_HOME = ""
    $env:SSLKEYLOGFILE = ""
    
    try {
        $response = Invoke-RestMethod -Uri "https://elsewhere.news/.well-known/elsewhere-skill.json" -Method GET -Headers @{"Accept"="application/json"} -ErrorAction Stop
        $env:ELSEWHERE_KEY = $savedKey
        $response | ConvertTo-Json -Compress
        exit 0
    } catch {
        $env:ELSEWHERE_KEY = $savedKey
        Write-Error "ELSEWHERE_VERSION=unavailable"
        exit 14
    }
}

# Build query string
$queryParams = @{}
foreach ($arg in $QueryArgs) {
    if ($arg -match '^([A-Za-z][A-Za-z0-9_]*)=(.*)$') {
        $queryParams[$Matches[1]] = $Matches[2]
    }
}

# Build URL
$fullUrl = "$BaseUrl$Route"
if ($queryParams.Count -gt 0) {
    $qs = ($queryParams.GetEnumerator() | ForEach-Object { "$($_.Key)=$([System.Uri]::EscapeDataString($_.Value))" }) -join "&"
    $fullUrl += "?$qs"
}

# Make authenticated API call
$headers = @{
    "Authorization" = "Bearer $($env:ELSEWHERE_KEY)"
    "Accept" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri $fullUrl -Method GET -Headers $headers -ErrorAction Stop
    $response | ConvertTo-Json -Depth 20 -Compress
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 401) {
        Write-Error "ELSEWHERE_AUTH=unauthorized"
        exit 12
    } elseif ($statusCode -eq 429) {
        Write-Error "ELSEWHERE_API=rate_or_quota_limited"
        exit 13
    } else {
        Write-Error "ELSEWHERE_API=http_error: $statusCode"
        exit 14
    }
}
