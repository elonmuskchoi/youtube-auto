$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

& (Join-Path $PSScriptRoot 'preflight_final_v3.ps1')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$python = Join-Path $repoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    throw 'Missing .venv. Create it and install requirements.txt first.'
}

$bundledFfmpeg = Get-ChildItem -Path (Join-Path $repoRoot 'work\ffmpeg') -Recurse -Filter ffmpeg.exe -ErrorAction SilentlyContinue | Select-Object -First 1
$ffmpeg = if ($bundledFfmpeg) { $bundledFfmpeg.FullName } else { (Get-Command ffmpeg -ErrorAction Stop).Source }

& $python scripts\render_synced_video.py `
    --captures assets\landing `
    --proofs work\proofs `
    --audio audio\narration-long-v3.wav `
    --timings audio\word-timings-long-v3.json `
    --output work\base-long-v3-noavatar.mp4 `
    --ffmpeg $ffmpeg
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $python scripts\compose_final_v3.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host 'Created outputs/youtube-auto-final-v3-avatar3-typecast.mp4' -ForegroundColor Green
