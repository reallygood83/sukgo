#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# sukgo 똑똑한 설치 스크립트
#
# 어떤 환경이든 안전하게 작동하도록 모든 케이스 처리:
#   ✅ Python 자동 탐지 (python3 / brew python / system python)
#   ✅ 격리된 venv 자동 생성 (사용자 다른 환경과 충돌 X)
#   ✅ pip 자동 업그레이드 (구버전 pip 패키지 못 찾는 문제 해결)
#   ✅ 정확한 PyPI 이름 사용 (finance-datareader 등)
#   ✅ Wrapper script (sukgo 명령어가 자기 venv 자동 사용)
#   ✅ 친절한 검증 + 진단 메시지
#
# 사용:  ./install.sh
# ═══════════════════════════════════════════════════════════════════

set -e

# ─── 색상 ──────────────────────────────────────────────────────────
G='\033[0;32m'   # green
B='\033[0;34m'   # blue
Y='\033[1;33m'   # yellow
R='\033[0;31m'   # red
P='\033[0;35m'   # purple
D='\033[2m'      # dim
W='\033[1m'      # bold
N='\033[0m'      # no color

# ─── 경로 ──────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUKGO_HOME="$HOME/.sukgo"
VENV_DIR="$SUKGO_HOME/venv"
BIN_DIR="$HOME/.local/bin"
WRAPPER="$BIN_DIR/sukgo"

# ─── 헤더 ──────────────────────────────────────────────────────────
clear
echo
echo -e "${P}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo
echo -e "                  ${W}s u k g o${N}  ${D}설치${N}"
echo -e "                ${D}결정의 기술 CLI${N}"
echo
echo -e "${P}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo
echo -e "  ${D}이 스크립트는 모든 의존성을 격리된 환경에 설치하여${N}"
echo -e "  ${D}사용자님의 다른 Python 작업과 충돌하지 않도록 합니다.${N}"
echo

# ─── 1. Python 탐지 ────────────────────────────────────────────────
echo -e "${B}[1/5]${N} ${W}Python 탐지${N}"

PYTHON=""
for cmd in python3.12 python3.11 python3.10 python3 python; do
    if command -v "$cmd" &> /dev/null; then
        VERSION=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
        MAJOR=$(echo "$VERSION" | cut -d. -f1)
        MINOR=$(echo "$VERSION" | cut -d. -f2)
        if [[ "$MAJOR" -eq 3 && "$MINOR" -ge 9 ]]; then
            PYTHON=$(command -v "$cmd")
            PY_VERSION="$VERSION"
            break
        fi
    fi
done

if [[ -z "$PYTHON" ]]; then
    echo -e "      ${R}❌ Python 3.9 이상이 필요합니다.${N}"
    echo
    echo -e "  ${D}macOS:${N}    ${G}brew install python@3.11${N}"
    echo -e "  ${D}Linux:${N}    ${G}sudo apt install python3.11${N}"
    echo -e "  ${D}공식:${N}     ${G}https://www.python.org/downloads/${N}"
    exit 1
fi
echo -e "      ${G}✅${N} Python ${PY_VERSION} 발견  ${D}($PYTHON)${N}"

# ─── 2. 격리된 venv 생성 ────────────────────────────────────────────
echo
echo -e "${B}[2/5]${N} ${W}sukgo 전용 가상환경 준비${N}"

mkdir -p "$SUKGO_HOME"
if [[ -d "$VENV_DIR" ]]; then
    echo -e "      ${D}기존 venv 발견. 그대로 사용 (의존성만 업데이트)${N}"
else
    echo -e "      ${D}깨끗한 venv 생성 중... (~/.sukgo/venv)${N}"
    "$PYTHON" -m venv "$VENV_DIR" 2>/dev/null
    echo -e "      ${G}✅${N} venv 생성 완료"
fi

# venv의 python·pip 경로
VENV_PY="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

# ─── 3. pip 업그레이드 + 의존성 설치 ──────────────────────────────────
echo
echo -e "${B}[3/5]${N} ${W}의존성 설치${N}"
echo -e "      ${D}pip 업그레이드 중...${N}"
"$VENV_PY" -m pip install --quiet --upgrade pip 2>/dev/null

if [[ -f "$SCRIPT_DIR/requirements.txt" ]]; then
    echo -e "      ${D}패키지 설치 중... (1~2분 소요){N}"
    if "$VENV_PY" -m pip install --quiet -r "$SCRIPT_DIR/requirements.txt" 2>/tmp/sukgo_install.log; then
        echo -e "      ${G}✅${N} yfinance, finance-datareader, requests 설치 완료"
    else
        echo -e "      ${Y}⚠${N}  일부 패키지 설치 실패 (자세히):"
        tail -5 /tmp/sukgo_install.log 2>/dev/null
        echo -e "      ${D}   Investment 도구 일부 기능 제한됨${N}"
    fi
    rm -f /tmp/sukgo_install.log
fi

# ─── 4. Wrapper 스크립트 설치 ───────────────────────────────────────
echo
echo -e "${B}[4/5]${N} ${W}sukgo 명령어 등록${N}"

mkdir -p "$BIN_DIR"

# Wrapper script — sukgo 명령어가 자기 venv python을 자동 사용
cat > "$WRAPPER" <<WRAPPER_EOF
#!/usr/bin/env bash
# sukgo wrapper — 격리된 venv의 Python으로 sukgo 실행
# 사용자가 어떤 환경에 있든 (다른 venv 활성화 등) 영향 받지 않음
exec "$VENV_PY" "$SCRIPT_DIR/poc.py" "\$@"
WRAPPER_EOF

chmod +x "$WRAPPER"
echo -e "      ${G}✅${N} ${G}sukgo${N} 명령어 → $WRAPPER"
echo -e "      ${D}   (자체 venv의 Python을 자동 사용 — 다른 환경 영향 X)${N}"

# ─── 5. PATH 검증 + 빠른 테스트 ─────────────────────────────────────
echo
echo -e "${B}[5/5]${N} ${W}검증${N}"

PATH_OK=0
case ":$PATH:" in
    *":$BIN_DIR:"*) PATH_OK=1 ;;
esac

if [[ $PATH_OK -eq 0 ]]; then
    SHELL_RC="$HOME/.zshrc"
    [[ "$SHELL" == */bash ]] && SHELL_RC="$HOME/.bashrc"

    echo -e "      ${Y}⚠${N}  ${W}~/.local/bin 이 PATH에 없습니다.${N}"
    echo -e "      ${D}자동 추가 중...${N}"
    echo '' >> "$SHELL_RC"
    echo '# sukgo PATH (auto-added by install.sh)' >> "$SHELL_RC"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
    echo -e "      ${G}✅${N} $SHELL_RC 에 PATH 추가됨"
    PATH_NOTE="${Y}⚡ 새 터미널을 여시거나 다음 명령 실행:${N} ${G}source $SHELL_RC${N}"
else
    echo -e "      ${G}✅${N} PATH OK"
    PATH_NOTE=""
fi

# 의존성 검증
DEPS_OK=$("$VENV_PY" -c "
try:
    import yfinance, FinanceDataReader, requests
    print('OK')
except ImportError as e:
    print(f'MISSING: {e.name}')
" 2>&1)

if [[ "$DEPS_OK" == "OK" ]]; then
    echo -e "      ${G}✅${N} 모든 의존성 확인됨"
else
    echo -e "      ${Y}⚠${N}  $DEPS_OK"
fi

# ─── 완료 ──────────────────────────────────────────────────────────
echo
echo -e "${G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo
echo -e "                  ${G}${W}✅ 설치 완료!${N}"
echo
echo -e "${G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo

if [[ -n "$PATH_NOTE" ]]; then
    echo -e "  $PATH_NOTE"
    echo
fi

echo -e "  ${W}바로 시작:${N}"
echo -e "    ${G}sukgo${N}                          ${D}# 메인 메뉴${N}"
echo
echo -e "  ${W}도움말:${N}"
echo -e "    ${G}cat $SCRIPT_DIR/README.md${N}"
echo -e "    ${G}https://github.com/reallygood83/sukgo${N}"
echo
echo -e "  ${W}문제가 생기면:${N}"
echo -e "    ${G}cat $SCRIPT_DIR/docs/SECURITY.md${N}"
echo -e "    ${G}https://github.com/reallygood83/sukgo/issues${N}"
echo
echo -e "  ${D}made by 배움의 달인 ✨${N}"
echo
