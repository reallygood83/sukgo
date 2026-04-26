# ═══════════════════════════════════════════════════════════════════
# sukgo Windows 한 줄 설치 (PowerShell)
#
# 사용:
#   irm https://raw.githubusercontent.com/reallygood83/sukgo/main/get.ps1 | iex
#
# 동작:
#   1. %USERPROFILE%\.sukgo\source\ 에 GitHub 코드 다운로드 (또는 업데이트)
#   2. install.ps1 자동 실행 (격리된 venv + 의존성 + wrapper)
#   3. sukgo 명령어 사용 가능
#
# 환경 변수:
#   $env:SUKGO_BRANCH   기본 main  (특정 브랜치 설치)
# ═══════════════════════════════════════════════════════════════════

$ErrorActionPreference = 'Stop'

# ─── 한글 출력 인코딩 (Korean Windows / cp949 환경 대응) ──────────────
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding           = [System.Text.Encoding]::UTF8
    chcp 65001 > $null
} catch { }

$RepoUrl   = 'https://github.com/reallygood83/sukgo.git'
$SukgoHome = Join-Path $env:USERPROFILE '.sukgo'
$SourceDir = Join-Path $SukgoHome 'source'
$Branch    = if ($env:SUKGO_BRANCH) { $env:SUKGO_BRANCH } else { 'main' }

Write-Host ""
Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host ""
Write-Host "                  s u k g o" -ForegroundColor White
Write-Host "                한 줄 설치 (Windows)" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host ""

# ─── 사전 점검 ────────────────────────────────────────────────────
Write-Host "[사전 점검]" -ForegroundColor Blue

# git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "  [X] git 이 필요합니다." -ForegroundColor Red
    Write-Host ""
    Write-Host "  Windows: " -NoNewline; Write-Host "winget install Git.Git" -ForegroundColor Green
    Write-Host "  공식:    " -NoNewline; Write-Host "https://git-scm.com/download/win" -ForegroundColor Green
    exit 1
}
Write-Host "  [OK] git" -ForegroundColor Green

# Python (py launcher 또는 python)
$PyOK = $false
foreach ($exe in @('py', 'python', 'python3')) {
    if (Get-Command $exe -ErrorAction SilentlyContinue) {
        try {
            $v = & $exe --version 2>&1
            if ($LASTEXITCODE -eq 0) { $PyOK = $true; Write-Host "  [OK] $v" -ForegroundColor Green; break }
        } catch {}
    }
}

if (-not $PyOK) {
    Write-Host "  [X] Python 3.9+ 가 필요합니다." -ForegroundColor Red
    Write-Host ""
    Write-Host "  winget:  " -NoNewline; Write-Host "winget install Python.Python.3.12" -ForegroundColor Green
    Write-Host "  공식:    " -NoNewline; Write-Host "https://www.python.org/downloads/" -ForegroundColor Green
    Write-Host ""
    Write-Host "  ※ 설치 시 'Add Python to PATH' 옵션을 반드시 체크하세요." -ForegroundColor Yellow
    exit 1
}

# ─── 1. 다운로드 ──────────────────────────────────────────────────
Write-Host ""
Write-Host "[1/2] " -ForegroundColor Blue -NoNewline; Write-Host "sukgo 코드 가져오기" -ForegroundColor White

New-Item -ItemType Directory -Path $SukgoHome -Force | Out-Null

if (Test-Path (Join-Path $SourceDir '.git')) {
    Write-Host "  기존 설치 발견 → 최신으로 업데이트" -ForegroundColor DarkGray
    Push-Location $SourceDir
    try {
        git fetch --quiet origin
        git checkout --quiet $Branch 2>$null
        if ($LASTEXITCODE -ne 0) {
            git checkout --quiet -b $Branch "origin/$Branch"
        }
        git reset --hard --quiet "origin/$Branch"
        Write-Host "  [OK] 업데이트 완료 ($SourceDir)" -ForegroundColor Green
    } finally {
        Pop-Location
    }
} else {
    Write-Host "  다운로드 중... ($SourceDir)" -ForegroundColor DarkGray
    git clone --quiet --branch $Branch $RepoUrl $SourceDir
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  [X] git clone 실패" -ForegroundColor Red
        exit 1
    }
    Write-Host "  [OK] 다운로드 완료" -ForegroundColor Green
}

# ─── 2. install.ps1 실행 ──────────────────────────────────────────
Write-Host ""
Write-Host "[2/2] " -ForegroundColor Blue -NoNewline; Write-Host "설치 스크립트 실행" -ForegroundColor White
Write-Host ""

$InstallPs1 = Join-Path $SourceDir 'install.ps1'
& powershell -NoProfile -ExecutionPolicy Bypass -File $InstallPs1
exit $LASTEXITCODE
