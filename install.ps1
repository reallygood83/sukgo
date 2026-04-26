# ═══════════════════════════════════════════════════════════════════
# sukgo Windows 설치 스크립트 (install.sh의 PowerShell 포팅)
#
# 동작:
#   ✅ Python 3.9+ 자동 탐지 (py launcher / python / python3)
#   ✅ 격리된 venv 생성 (%USERPROFILE%\.sukgo\venv)
#   ✅ pip 업그레이드 + 의존성 설치
#   ✅ Wrapper(sukgo.cmd) → %USERPROFILE%\.sukgo\bin
#   ✅ User PATH 자동 추가
#
# 사용:  powershell -ExecutionPolicy Bypass -File install.ps1
# ═══════════════════════════════════════════════════════════════════

$ErrorActionPreference = 'Stop'

# ─── 한글 출력 인코딩 (Korean Windows / cp949 환경 대응) ──────────────
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding           = [System.Text.Encoding]::UTF8
    chcp 65001 > $null
} catch { }

# ─── 경로 ──────────────────────────────────────────────────────────
$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$SukgoHome  = Join-Path $env:USERPROFILE '.sukgo'
$VenvDir    = Join-Path $SukgoHome 'venv'
$BinDir     = Join-Path $SukgoHome 'bin'
$WrapperCmd = Join-Path $BinDir 'sukgo.cmd'
$WrapperPs1 = Join-Path $BinDir 'sukgo.ps1'

# ─── 헤더 ──────────────────────────────────────────────────────────
function Write-Header($t)  { Write-Host "`n[$t]" -ForegroundColor Blue -NoNewline }
function Write-OK($t)      { Write-Host "      [OK] $t" -ForegroundColor Green }
function Write-Warn($t)    { Write-Host "      [!]  $t" -ForegroundColor Yellow }
function Write-Err($t)     { Write-Host "      [X]  $t" -ForegroundColor Red }
function Write-Info($t)    { Write-Host "      $t" -ForegroundColor DarkGray }

Clear-Host
Write-Host ""
Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host ""
Write-Host "                  s u k g o  설치" -ForegroundColor White
Write-Host "                결정의 기술 CLI"   -ForegroundColor DarkGray
Write-Host ""
Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host ""
Write-Info "이 스크립트는 모든 의존성을 격리된 환경에 설치하여"
Write-Info "사용자님의 다른 Python 작업과 충돌하지 않도록 합니다."

# ─── 1. Python 탐지 ────────────────────────────────────────────────
Write-Header "1/5"; Write-Host " Python 탐지" -ForegroundColor White

$PyCmd = $null
$PyVer = $null

# py launcher 우선 (Windows 표준)
$candidates = @(
    @{ exe = 'py';      args = @('-3.12') },
    @{ exe = 'py';      args = @('-3.11') },
    @{ exe = 'py';      args = @('-3.10') },
    @{ exe = 'py';      args = @('-3') },
    @{ exe = 'python';  args = @() },
    @{ exe = 'python3'; args = @() }
)

foreach ($c in $candidates) {
    if (-not (Get-Command $c.exe -ErrorAction SilentlyContinue)) { continue }
    try {
        $checkArgs = @($c.args) + @('-c', "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        $ver = & $c.exe @checkArgs 2>$null
        if ($LASTEXITCODE -ne 0) { continue }
        $parts = $ver.Trim().Split('.')
        if ([int]$parts[0] -eq 3 -and [int]$parts[1] -ge 9) {
            $PyCmd = $c
            $PyVer = $ver.Trim()
            break
        }
    } catch { continue }
}

if (-not $PyCmd) {
    Write-Err "Python 3.9 이상이 필요합니다."
    Write-Host ""
    Write-Host "  공식 다운로드: " -NoNewline; Write-Host "https://www.python.org/downloads/" -ForegroundColor Green
    Write-Host "  또는 winget:   " -NoNewline; Write-Host "winget install Python.Python.3.12" -ForegroundColor Green
    Write-Host ""
    exit 1
}

$PyDisplay = "$($PyCmd.exe) $($PyCmd.args -join ' ')".Trim()
Write-OK "Python $PyVer 발견 ($PyDisplay)"

# ─── 2. 격리된 venv 생성 ────────────────────────────────────────────
Write-Header "2/5"; Write-Host " sukgo 전용 가상환경 준비" -ForegroundColor White

New-Item -ItemType Directory -Path $SukgoHome -Force | Out-Null

if (Test-Path $VenvDir) {
    Write-Info "기존 venv 발견. 그대로 사용 (의존성만 업데이트)"
} else {
    Write-Info "깨끗한 venv 생성 중... ($VenvDir)"
    $venvArgs = @($PyCmd.args) + @('-m', 'venv', $VenvDir)
    & $PyCmd.exe @venvArgs
    if ($LASTEXITCODE -ne 0) { Write-Err "venv 생성 실패"; exit 1 }
    Write-OK "venv 생성 완료"
}

$VenvPy = Join-Path $VenvDir 'Scripts\python.exe'
if (-not (Test-Path $VenvPy)) {
    Write-Err "venv python.exe 를 찾을 수 없습니다: $VenvPy"
    exit 1
}

# ─── 3. pip 업그레이드 + 의존성 설치 ──────────────────────────────────
Write-Header "3/5"; Write-Host " 의존성 설치" -ForegroundColor White

Write-Info "pip 업그레이드 중..."
& $VenvPy -m pip install --quiet --upgrade pip 2>&1 | Out-Null

$Reqs = Join-Path $ScriptDir 'requirements.txt'
if (Test-Path $Reqs) {
    Write-Info "패키지 설치 중... (1~2분 소요)"
    $LogFile = Join-Path $env:TEMP 'sukgo_install.log'
    & $VenvPy -m pip install --quiet -r $Reqs 2>&1 | Tee-Object -FilePath $LogFile | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-OK "yfinance, finance-datareader, requests 설치 완료"
    } else {
        Write-Warn "일부 패키지 설치 실패 (자세히):"
        Get-Content $LogFile -Tail 5 | ForEach-Object { Write-Info $_ }
        Write-Info "Investment 도구 일부 기능 제한됨"
    }
    Remove-Item $LogFile -ErrorAction SilentlyContinue
}

# ─── 4. Wrapper 등록 ───────────────────────────────────────────────
Write-Header "4/5"; Write-Host " sukgo 명령어 등록" -ForegroundColor White

New-Item -ItemType Directory -Path $BinDir -Force | Out-Null

# sukgo.cmd — cmd.exe / PowerShell 양쪽에서 모두 동작
# (cmd.exe 호환을 위해 영문 주석 + ASCII 인코딩 사용)
$CmdContent = @"
@echo off
chcp 65001 >nul
REM sukgo wrapper - run via isolated venv python
"$VenvPy" "$ScriptDir\poc.py" %*
"@
Set-Content -Path $WrapperCmd -Value $CmdContent -Encoding ASCII

# sukgo.ps1 — PowerShell 네이티브
$Ps1Content = @"
# sukgo wrapper (PowerShell)
& "$VenvPy" "$ScriptDir\poc.py" @args
exit `$LASTEXITCODE
"@
Set-Content -Path $WrapperPs1 -Value $Ps1Content -Encoding UTF8

Write-OK "sukgo 명령어 → $WrapperCmd"
Write-Info "(자체 venv의 Python을 자동 사용 — 다른 환경 영향 X)"

# ─── 5. PATH 검증 + 의존성 점검 ──────────────────────────────────────
Write-Header "5/5"; Write-Host " 검증" -ForegroundColor White

$UserPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$PathParts = $UserPath -split ';' | Where-Object { $_ -and ($_.TrimEnd('\') -eq $BinDir.TrimEnd('\')) }
$PathNote = ''

if (-not $PathParts) {
    Write-Warn "$BinDir 가 User PATH 에 없습니다. 자동 추가 중..."
    $NewPath = if ($UserPath) { "$UserPath;$BinDir" } else { $BinDir }
    [Environment]::SetEnvironmentVariable('Path', $NewPath, 'User')
    Write-OK "User PATH 에 추가됨"
    $PathNote = "[!] 새 PowerShell/터미널을 열어야 'sukgo' 명령이 인식됩니다."
} else {
    Write-OK "PATH OK"
}

# 의존성 검증
$DepsCheck = & $VenvPy -c @"
try:
    import yfinance, FinanceDataReader, requests
    print('OK')
except ImportError as e:
    print(f'MISSING: {e.name}')
"@ 2>&1

if ($DepsCheck.Trim() -eq 'OK') {
    Write-OK "모든 의존성 확인됨"
} else {
    Write-Warn $DepsCheck
}

# ─── 완료 ──────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""
Write-Host "                  ✅ 설치 완료!" -ForegroundColor Green
Write-Host ""
Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""

if ($PathNote) {
    Write-Host "  $PathNote" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "  바로 시작:" -ForegroundColor White
Write-Host "    sukgo" -ForegroundColor Green -NoNewline
Write-Host "                          # 메인 메뉴" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  업데이트:" -ForegroundColor White
Write-Host "    sukgo update" -ForegroundColor Green
Write-Host ""
Write-Host "  도움말:" -ForegroundColor White
Write-Host "    https://github.com/reallygood83/sukgo" -ForegroundColor Green
Write-Host ""
Write-Host "  made by 배움의 달인 ✨" -ForegroundColor DarkGray
Write-Host ""
