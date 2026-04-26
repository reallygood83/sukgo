#!/usr/bin/env bash
# sukgo — 한 번에 설치 스크립트
# 사용: ./install.sh
#
# 작업: Python 의존성 설치 + 실행 권한 + ~/.local/bin/sukgo 심볼릭 링크

set -e

# 색상
G='\033[0;32m'   # green
B='\033[0;34m'   # blue
Y='\033[1;33m'   # yellow
R='\033[0;31m'   # red
D='\033[2m'      # dim
N='\033[0m'      # no color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo
echo -e "${B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo -e "${B}              s u k g o   설 치${N}"
echo -e "${B}             결정의 기술 CLI${N}"
echo -e "${B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo

# ─── 1. Python 확인 ─────────────────────────────────────────
echo -e "${B}[1/4]${N} Python 환경 확인..."
if ! command -v python3 &> /dev/null; then
    echo -e "      ${R}❌ Python 3 이 설치되지 않았습니다.${N}"
    echo -e "      ${D}설치: https://www.python.org/downloads/${N}"
    exit 1
fi
PY_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "      ${G}✅${N} Python $PY_VERSION"

# ─── 2. 의존성 설치 ──────────────────────────────────────────
echo
echo -e "${B}[2/4]${N} 의존성 설치 (yfinance, FinanceDataReader, requests)..."
if [[ -f "$SCRIPT_DIR/requirements.txt" ]]; then
    if python3 -m pip install --user --quiet --upgrade -r "$SCRIPT_DIR/requirements.txt" 2>&1 | tail -5; then
        echo -e "      ${G}✅${N} 의존성 설치 완료"
    else
        echo -e "      ${Y}⚠${N}  일부 패키지 설치 실패 — 데이터 페처 일부 비활성"
    fi
else
    echo -e "      ${Y}⚠${N}  requirements.txt 없음 — 데이터 페처 비활성"
fi

# ─── 3. 실행 권한 ────────────────────────────────────────────
echo
echo -e "${B}[3/4]${N} 실행 권한 부여..."
chmod +x "$SCRIPT_DIR/poc.py"
echo -e "      ${G}✅${N} chmod +x poc.py"

# ─── 4. PATH 등록 ────────────────────────────────────────────
echo
echo -e "${B}[4/4]${N} sukgo 명령어 등록..."
mkdir -p "$HOME/.local/bin"
ln -sf "$SCRIPT_DIR/poc.py" "$HOME/.local/bin/sukgo"
echo -e "      ${G}✅${N} ~/.local/bin/sukgo → $SCRIPT_DIR/poc.py"

# ─── PATH 체크 ──────────────────────────────────────────────
PATH_OK=0
case ":$PATH:" in
    *":$HOME/.local/bin:"*) PATH_OK=1 ;;
esac

echo
echo -e "${G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo -e "${G}              ✅ 설치 완료!${N}"
echo -e "${G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo

if [[ $PATH_OK -eq 0 ]]; then
    echo -e "${Y}⚠ ~/.local/bin 이 PATH에 없습니다.${N}"
    echo -e "  다음 한 줄을 실행하면 자동 추가됩니다:"
    echo
    SHELL_RC="$HOME/.zshrc"
    [[ "$SHELL" == */bash ]] && SHELL_RC="$HOME/.bashrc"
    echo -e "  ${G}echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> $SHELL_RC && source $SHELL_RC${N}"
    echo
fi

echo -e "  ${B}시작:${N}    ${G}sukgo${N}"
echo -e "  ${B}README:${N}  ${G}cat $SCRIPT_DIR/README.md${N}"
echo -e "  ${B}보안:${N}    ${G}cat $SCRIPT_DIR/docs/SECURITY.md${N}"
echo
echo -e "  ${D}made by 배움의 달인 ✨${N}"
echo
