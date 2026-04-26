# sukgo

> **결정의 기술 — AI와 함께 더 잘 생각하기**

검증된 사고 프레임워크 10종 + 도메인 전문 컨설턴트 3종을, **이미 가진 AI 구독**(Claude Pro / ChatGPT Plus / Gemini)으로 활용하는 터미널 CLI.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Made by 배움의 달인](https://img.shields.io/badge/made%20by-배움의%20달인%20✨-purple)](https://github.com/reallygood83)

```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    s u k g o
                  결 정 의   기 술

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ▌ 사고 도구 — 검증된 사고 프레임워크
      1   🛡  Steel-manning      가장 강한 반대 논리
      2   🥊  Devil's Advocate   확증편향 차단
      3   ⚰  Pre-mortem          실패 시뮬레이션
      4   🎩  6 Hats              6관점 종합
      5   🔄  Inversion           거꾸로 사고
      6   ❓  5 Whys              근본 원인
      7   ⚖  Decision Matrix    가중치 비교
      8   🧬  First Principles   본질부터
      9   🌊  OODA Loop           빠른 결정
      0   🎯  Toulmin Model       논증 5요소

   ▌ 도메인 컨설턴트 — 데이터 기반 전문 분석
      c   💼  Career              이직·커리어
      i   📈  Investment          주식 9섹션 (yfinance/FDR 자동)
      e   👶  Education           자녀 교육

                ● claude · codex · gemini · MLX · Ollama
                          비교 모드 · 옵시디언 자동 저장
```

---

## 🎯 왜 sukgo?

### 💸 추가 결제 0원
이미 내고 있는 Claude Pro · ChatGPT Plus · Gemini 구독을 **그대로 활용**.
OpenRouter, 별도 API 키 가입 필요 없음.

### ⚡ Thought Speed
회의 5분 전, 한 줄 명령으로 사고 시작.
ChatGPT 켜고 프롬프트 입력하는 30초가 사라짐.

### 🧠 AI가 답하지 않는다 — 너를 키운다
*"챗봇은 답을 준다. sukgo는 사고를 단단하게 만든다."*

검증된 사고 프레임워크(Steel-manning, Pre-mortem 등 10종)와 AI를 결합해 **사용자 자신을 더 나은 결정자로 만든다**.

### 💾 데이터 주권
모든 분석 결과는 **로컬 마크다운**으로 자동 저장. 옵시디언 볼트와 통합 가능.
ChatGPT 기록처럼 외부 서버에 갇히지 않음.

---

## 🚀 Quick Start

```bash
git clone https://github.com/reallygood83/sukgo.git
cd sukgo
./install.sh
sukgo
```

→ 첫 실행 마법사가 백엔드 + 저장 위치를 1분 만에 설정.

> 🌱 **Python·터미널 처음이신 분?** [`docs/ONBOARDING.md`](docs/ONBOARDING.md) 가이드를 따라하세요. 5분 안에 첫 분석까지.

### ✨ install.sh가 알아서 처리하는 것
- ✅ Python 자동 탐지 (없으면 설치 안내)
- ✅ **격리된 sukgo 전용 venv** 생성 (`~/.sukgo/venv`) — 사용자 다른 Python 작업과 충돌 0
- ✅ pip 자동 업그레이드 + 의존성 설치 (yfinance, finance-datareader, requests)
- ✅ Wrapper script (`sukgo` 명령어가 자체 venv 자동 사용)
- ✅ PATH 자동 등록 + 셸 설정 업데이트
- ✅ 검증 (모든 의존성 import 테스트)

→ 실행 후 어떤 환경에서든 `sukgo` 한 줄로 작동.

---

## 📋 요구사항

### 필수
- **Python 3.9+**
- **AI CLI 중 1개 이상**:
  - [Claude Code](https://docs.claude.com/en/docs/claude-code) (Pro/Max 구독자)
  - [Codex CLI](https://github.com/openai/codex) (ChatGPT Plus 구독자)
  - [Gemini CLI](https://github.com/google-gemini/gemini-cli) (Google 무료 티어)

### 선택
- **MLX** ([mlx-lm](https://github.com/ml-explore/mlx-examples/tree/main/llms)) — Apple Silicon 로컬 추론
- **Ollama** ([ollama.ai](https://ollama.ai)) — 크로스 플랫폼 로컬 추론
- **`tmux`** — Code 비교 모드 시 권장

---

## 🛠 사용법

### 메인 메뉴
```bash
$ sukgo
```
→ 메뉴에서 도구 선택 → AI 백엔드 선택 (1개 또는 비교 모드 `a`) → 주제 입력

### 사고 도구 사용 예시
```
> 4   (6 Hats 선택)
> 어떤 AI? a (모두)
> 주제: 회사를 이직해야 한다

⠋ claude · codex · gemini 가 6관점에서 분석 중...
[3개 AI의 6색 모자 관점 분석 결과 통합 출력]
💾 저장됨: ~/Documents/Vault/000-Inbox/2026-04-26_..._6hats_compare.md
```

### Investment 도구 (자동 데이터 수집)
```
> i   (Investment 선택)
> 종목: NVDA

📊 NVDA 데이터 수집 중...
✅ NVIDIA Corporation
   현재가:    $182.15
   PER:       65.40
   시가총액:  4.47T
   52주 범위: $86.62 ~ $195.31
   뉴스:      5건 수집

⠋ 9섹션 종합 리포트 생성 중...
[Executive Summary / Fundamental / Catalyst / Valuation / Risk / Technical /
 Market Positioning / Behavioral Check / 종합 평가]
💾 저장됨: ~/Documents/Vault/000-Inbox/_investments/2026-04-26_..._NVDA.md
```

한국 주식도 동일:
```
> 종목: 005930   (삼성전자)
```

---

## 🧠 사고 도구 13종

### 사고 프레임워크 (10종 — 어떤 주제든 적용)

| 키 | 도구 | 출처 | 언제 쓰나 |
|---|------|------|----------|
| 1 | 🛡 **Steel-manning** | 비판적 사고 전통 | 토론 준비, 본인 입장 검증 |
| 2 | 🥊 **Devil's Advocate** | 가톨릭 시성 절차 | 회의 준비, 확증편향 차단 |
| 3 | ⚰ **Pre-mortem** | Gary Klein (HBR 2007) | 투자·이직·창업 결정 전 |
| 4 | 🎩 **6 Hats** | Edward de Bono (1985) | 종합 의사결정 |
| 5 | 🔄 **Inversion** | Charlie Munger | 인생·투자 결정 |
| 6 | ❓ **5 Whys** | Toyota | 문제 분석, 자기 이해 |
| 7 | ⚖ **Decision Matrix** | 다기준 의사결정론 | 큰 선택지 비교 |
| 8 | 🧬 **First Principles** | Aristotle, Elon Musk | 창업·재정의 |
| 9 | 🌊 **OODA Loop** | John Boyd | 빠른 의사결정 |
| 0 | 🎯 **Toulmin Model** | Stephen Toulmin (1958) | 토론·보고서 논증 강화 |

### 도메인 컨설턴트 (3종 — 특정 영역 전문 분석)

| 키 | 도구 | 데이터 소스 | 출력 |
|---|------|-----------|------|
| **c** | 💼 **Career** | — | 이직·커리어 정량+정성 분석 (5년 시나리오) |
| **i** | 📈 **Investment** | yfinance + FDR | 9섹션 종합 리포트 (실시간 데이터) |
| **e** | 👶 **Education** | — | 자녀 교육 발달학·연구 기반 분석 |

---

## 🔌 백엔드 5종

| 백엔드 | 인증 | 비용 | 도구 사용 |
|--------|------|------|----------|
| 🥇 **claude** | Claude Code OAuth | Pro/Max 구독 | ✅ WebSearch/WebFetch |
| 🥈 **codex** | Codex CLI OAuth | ChatGPT Plus | 자체 도구 |
| 🥉 **gemini** | Gemini CLI OAuth | Google 무료 티어 | 자체 도구 |
| 4 **mlx** | 로컬 HTTP | 무료 (Apple Silicon) | 텍스트만 |
| 5 **ollama** | 로컬 HTTP | 무료 (크로스 플랫폼) | 텍스트만 |

→ 사용자가 가진 CLI 자동 감지. **여러 개 등록 시 비교 모드** (같은 질문, 다른 시각).

---

## 🏗 아키텍처

```
┌─────────────────────────────────────┐
│              User Input             │
│        (CLI args / TUI)             │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│           sukgo Core                 │
│  ┌──────┐  ┌──────┐  ┌──────────┐  │
│  │Tools │→ │Data  │→ │Renderer  │  │
│  │ (13) │  │Fetch │  │(Rich)    │  │
│  └──────┘  └──────┘  └──────────┘  │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│       Backend Adapter (5종)          │
│  claude · codex · gemini · MLX · Ollama │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│            Persistence              │
│  ~/.config/sukgo/  (설정)            │
│  $OBSIDIAN_VAULT/  (자동 저장)        │
└─────────────────────────────────────┘
```

상세 설계: [`docs/SPEC.md`](docs/SPEC.md)

---

## 🔒 보안

> **본인의 API 키는 본인 컴퓨터에만.**

- API 키는 `~/.config/sukgo/secrets.json`에 권한 600으로 저장
- 코드와 완전 분리 — `.gitignore`로 GitHub 업로드 차단
- 첫 사용 시 wizard로 안전하게 입력
- AI CLI(`claude`/`codex`/`gemini`)는 자체 OAuth 사용 — sukgo가 키 보지 않음

상세 가이드: [`docs/SECURITY.md`](docs/SECURITY.md)

---

## 📊 비교 모드 — sukgo의 진짜 강점

같은 주제를 여러 AI가 동시에 분석:

```
주제: "AI 시대에는 학생들에게 코딩보다 비판적 사고를 먼저 가르쳐야 한다"

🧠 claude     →  학술적·구조적 (Willingham, MIT Resnick 인용)
🧠 codex      →  실용적·시장 관점 (GPT-5.4 학습 지식)
🧠 gemini     →  데이터·트렌드 관점 (Google 인덱스)

→ 한 마크다운 파일에 3개 시각 통합 저장 → 옵시디언에서 한눈에 비교
```

OpenRouter 등 별도 결제 **없이** 자기 구독으로 다관점 분석 가능.

---

## 🗺 로드맵

| 버전 | 상태 | 핵심 |
|------|------|------|
| v0.0.5 | ✅ 현재 | 13 도구 + 5 백엔드 + 데이터 페처 + install.sh |
| v0.1 | 다음 | `pipx install sukgo` + slash command 동기화 |
| v0.3 | 곧 | PyPI 정식 + Windows·Linux 풀 검증 |
| v0.5 | 중기 | 도메인 컨설턴트 확장 (부동산·관계·건강) + 플러그인 시스템 |
| v1.0 | 장기 | 영문 i18n + Homebrew tap + 커뮤니티 |

상세 계획: [`docs/SPEC.md`](docs/SPEC.md), [`docs/KICK.md`](docs/KICK.md)

---

## 🤝 기여

PR / 이슈 환영합니다.

- 🐛 **버그**: GitHub Issues
- 💡 **새 도구 제안**: `prompts/` 폴더에 마크다운 추가 (PR)
- 🌐 **백엔드 추가**: `data_fetchers/` 또는 `poc.py` Backend 클래스
- 📚 **문서 개선**: `docs/`

---

## 📚 문서

- [`docs/SPEC.md`](docs/SPEC.md) — 개발 스펙 (PRD)
- [`docs/KICK.md`](docs/KICK.md) — 서비스 기획·브랜드
- [`docs/SECURITY.md`](docs/SECURITY.md) — 보안 가이드

---

## 📄 라이선스

[MIT](LICENSE) — 자유롭게 사용·수정·배포 (상업 사용 포함).

---

## 👤 Made by

**배움의 달인** — *더 잘 배우고, 더 잘 생각하는 도구를 만듭니다.*

> *"GUI는 우리에게 컴퓨터를 가르쳤고,*
> *CLI는 컴퓨터에게 우리 생각을 가르친다."*

---

<div align="center">

**⭐ 도움이 됐다면 Star 부탁드려요!**

[Issues](https://github.com/reallygood83/sukgo/issues) · [Discussions](https://github.com/reallygood83/sukgo/discussions) · [Releases](https://github.com/reallygood83/sukgo/releases)

</div>
