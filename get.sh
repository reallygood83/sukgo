#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# sukgo 한 줄 설치 (One-line installer)
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/reallygood83/sukgo/main/get.sh | bash
#
# 동작:
#   1. ~/.sukgo/source/ 에 GitHub 코드 다운로드 (또는 업데이트)
#   2. install.sh 자동 실행 (격리된 venv + 의존성 + wrapper)
#   3. sukgo 명령어 사용 가능
#
# 환경 변수:
#   SUKGO_HOME     기본 ~/.sukgo  (소스·venv 위치)
#   SUKGO_BRANCH   기본 main      (특정 브랜치 설치)
# ═══════════════════════════════════════════════════════════════════

set -e

REPO_URL="https://github.com/reallygood83/sukgo.git"
SUKGO_HOME="${SUKGO_HOME:-$HOME/.sukgo}"
SOURCE_DIR="$SUKGO_HOME/source"
BRANCH="${SUKGO_BRANCH:-main}"

# 색상
G='\033[0;32m'
B='\033[0;34m'
Y='\033[1;33m'
R='\033[0;31m'
P='\033[0;35m'
W='\033[1m'
D='\033[2m'
N='\033[0m'

echo
echo -e "${P}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo
echo -e "                  ${W}s u k g o${N}"
echo -e "                ${D}한 줄 설치 (1-line install)${N}"
echo
echo -e "${P}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo

# ─── 사전 점검 ────────────────────────────────────────────────────
echo -e "${B}[사전 점검]${N}"

# git
if ! command -v git &> /dev/null; then
    echo -e "  ${R}❌${N} git 이 필요합니다."
    echo
    echo -e "  ${D}macOS:${N}    ${G}brew install git${N}"
    echo -e "  ${D}Linux:${N}    ${G}sudo apt install git${N}"
    echo -e "  ${D}Windows:${N}  ${G}https://git-scm.com/download/win${N}"
    exit 1
fi
echo -e "  ${G}✅${N} git"

# python3
if ! command -v python3 &> /dev/null; then
    echo -e "  ${R}❌${N} Python 3.9+ 가 필요합니다."
    echo
    echo -e "  ${D}macOS:${N}    ${G}brew install python@3.11${N}"
    echo -e "  ${D}Linux:${N}    ${G}sudo apt install python3.11 python3-venv${N}"
    echo -e "  ${D}공식:${N}     ${G}https://www.python.org/downloads/${N}"
    exit 1
fi
echo -e "  ${G}✅${N} $(python3 --version)"

# ─── 1. 다운로드 ──────────────────────────────────────────────────
echo
echo -e "${B}[1/2]${N} ${W}sukgo 코드 가져오기${N}"

mkdir -p "$SUKGO_HOME"

if [ -d "$SOURCE_DIR/.git" ]; then
    echo -e "  ${D}기존 설치 발견 → 최신으로 업데이트${N}"
    cd "$SOURCE_DIR"
    git fetch --quiet origin
    git checkout --quiet "$BRANCH" 2>/dev/null || git checkout --quiet -b "$BRANCH" "origin/$BRANCH"
    git reset --hard --quiet "origin/$BRANCH"
    echo -e "  ${G}✅${N} 업데이트 완료 ($SOURCE_DIR)"
else
    echo -e "  ${D}다운로드 중... ($SOURCE_DIR)${N}"
    git clone --quiet --branch "$BRANCH" "$REPO_URL" "$SOURCE_DIR"
    echo -e "  ${G}✅${N} 다운로드 완료"
fi

# ─── 2. install.sh 실행 ───────────────────────────────────────────
echo
echo -e "${B}[2/2]${N} ${W}설치 스크립트 실행${N}"
echo

# install.sh 가 자체 출력을 가지므로 그대로 실행
bash "$SOURCE_DIR/install.sh"

# install.sh 가 자체 완료 메시지 출력함
