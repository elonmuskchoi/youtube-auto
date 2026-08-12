$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $repoRoot 'config\final-v3-inputs.json'
$manifest = Get-Content -Raw -Encoding UTF8 $manifestPath | ConvertFrom-Json
$missing = [System.Collections.Generic.List[string]]::new()
$mismatch = [System.Collections.Generic.List[string]]::new()

foreach ($item in $manifest.required_private_files) {
    $path = Join-Path $repoRoot $item.path
    if (-not (Test-Path -LiteralPath $path)) {
        $missing.Add($item.path)
        continue
    }
    if ($item.sha256_reference) {
        $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -ne $item.sha256_reference) {
            $mismatch.Add("$($item.path): expected $($item.sha256_reference), got $actual")
        }
    }
}

foreach ($name in $manifest.required_captures) {
    $path = Join-Path $repoRoot (Join-Path 'assets\landing' $name)
    if (-not (Test-Path -LiteralPath $path)) { $missing.Add("assets/landing/$name") }
}

if (-not $env:TYPECAST_API_KEY) {
    Write-Warning 'TYPECAST_API_KEY is not set. Existing audio may still be rendered, but narration cannot be regenerated.'
}

if ($missing.Count -or $mismatch.Count) {
    if ($missing.Count) { Write-Host "Missing inputs:`n - $($missing -join "`n - ")" -ForegroundColor Yellow }
    if ($mismatch.Count) { Write-Host "Hash mismatches:`n - $($mismatch -join "`n - ")" -ForegroundColor Red }
    exit 1
}

Write-Host 'Final v3 preflight passed.' -ForegroundColor Green
