$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repo '.venv\Scripts\python.exe'
$avatar = Join-Path $repo 'work\heygen-avatar-iii-typecast-v4-long.mp4'
$base = Join-Path $repo 'work\base-long-v4-noavatar.mp4'

if (-not (Test-Path -LiteralPath $avatar)) {
    throw 'HeyGen Avatar III 결과가 없습니다: work/heygen-avatar-iii-typecast-v4-long.mp4'
}
if (-not (Test-Path -LiteralPath $base)) {
    throw '화면·자막 베이스가 없습니다: work/base-long-v4-noavatar.mp4'
}

& $python (Join-Path $PSScriptRoot 'compose_final_v4.py')
& $python (Join-Path $PSScriptRoot 'mix_master_v4.py')

Write-Host 'Created outputs/youtube-auto-final-v4-avatar3-bgm-sfx.mp4' -ForegroundColor Green
