<div align="center">

# 🧠 sukgo

### 결정의 기술 — AI와 함께 더 잘 생각하기

> **챗봇은 답을 준다. sukgo는 사고를 단단하게 만든다.**

검증된 사고 프레임워크 **10종** + 도메인 전문 컨설턴트 **3종** + AI 비교 모드를
**이미 가진 AI 구독**(Claude Pro / ChatGPT Plus / Gemini)으로 활용하는 터미널 CLI.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/reallygood83/sukgo/pulls)
[![Made by 배움의 달인](https://img.shields.io/badge/made%20by-배움의%20달인%20✨-purple)](https://github.com/reallygood83)

```bash
curl -fsSL https://raw.githubusercontent.com/reallygood83/sukgo/main/get.sh | bash
```

⬆️ **한 줄로 설치 끝.** Python·venv·의존성·PATH 모두 자동.

</div>

---

## 📺 Demo

```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    s u k g o
                  결 정 의   기 술

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ▌ 사고 도구 — 검증된 사고 프레임워크
      1   🛡  Steel-manning      가장 강한 반대 논리
      2   🥊  Devil's Advocate   확증편향 차단
      3   ⚰  Pre-mortem          실패 시뮬레이션 (Gary Klein)
      4   🎩  6 Hats              6관점 종합 (de Bono)
      5   🔄  Inversion           거꾸로 사고 (Munger)
      6   ❓  5 Whys              근본 원인 (Toyota)
      7   ⚖  Decision Matrix    가중치 비교
      8   🧬  First Principles   본질부터 (Aristotle)
      9   🌊  OODA Loop           빠른 결정 (Boyd)
      0   🎯  Toulmin Model       논증 5요소

   ▌ 도메인 컨설턴트 — 데이터 기반 전문 분석
      c   💼  Career              이직·커리어 (정량+정성)
      i   📈  Investment          주식 9섹션 (yfinance/FDR 자동)
      e   👶  Education           자녀 교육 (발달학+연구)

           ● claude · codex · gemini · MLX · Ollama
                  비교 모드 · 옵시디언 자동 저장
                made by 배움의 달인 ✨   v0.0.5
```

---

## 🎯 왜 sukgo?

### 💸 **추가 결제 0원**
이미 내고 있는 **Claude Pro · ChatGPT Plus · Gemini 무료** 구독을 **그대로 활용**.
OpenRouter, 별도 API 키 가입, 추가 월 $20 — 모두 필요 없음.

### ⚡ **Thought Speed**
회의 5분 전, 한 줄 명령으로 사고 시작.
ChatGPT 켜고 프롬프트 입력하는 30초가 사라짐.

### 🧠 **AI가 답하지 않는다 — 너를 키운다**
*챗봇은 답을 준다. sukgo는 사고를 단단하게 만든다.*

검증된 사고 프레임워크 13종과 AI를 결합해 **사용자 자신을 더 나은 결정자로** 만든다.

### 💾 **데이터 주권**
모든 분석 결과는 **로컬 마크다운**으로 자동 저장. 옵시디언 볼트와 통합 가능.
ChatGPT 기록처럼 외부 서버에 갇히지 않음.

### 🌐 **AI 비교 모드**
같은 질문 → Claude · GPT · Gemini 동시 → **한 마크다운에 통합**.
*"OpenRouter 결제 없이 멀티 AI 분석"* — sukgo의 진짜 차별화.

---

## 🚀 한 줄 설치

```bash
curl -fsSL https://raw.githubusercontent.com/reallygood83/sukgo/main/get.sh | bash
```

→ 1분 안에 모든 것 자동 설치. 끝나면 새 터미널에서 `sukgo`.

### 🌱 Python·터미널 처음이신 분?
[**`docs/ONBOARDING.md`**](docs/ONBOARDING.md) — 5분 가이드 (Homebrew · Python · AI CLI 설치 안내 + FAQ).

### 🛠 개발자용 (직접 클론)
```bash
git clone https://github.com/reallygood83/sukgo.git
cd sukgo
./install.sh
```

### ✨ 자동으로 처리되는 것
- ✅ Python 3.9+ 자동 탐지 (없으면 설치 안내)
- ✅ **격리된 sukgo 전용 venv** (`~/.sukgo/venv`) 생성 — 사용자 다른 작업과 충돌 0
- ✅ pip 자동 업그레이드 + 의존성 설치 (yfinance, finance-datareader, requests)
- ✅ Wrapper script (`~/.local/bin/sukgo` — 어디서든 자기 venv 자동 사용)
- ✅ PATH 자동 등록 (`.zshrc` / `.bashrc`)
- ✅ 의존성 import 검증

---

## 📋 요구사항

| 항목 | 필수 | 비고 |
|------|------|------|
| **Python 3.9+** | ✅ | macOS는 보통 기본 설치됨 |
| **Git** | ✅ | `brew install git` |
| **AI CLI 1개 이상** | ✅ | 아래 중 택 1+ |
| ↳ Claude Code | ⭕ | Claude Pro/Max 구독 |
| ↳ Codex CLI | ⭕ | ChatGPT Plus 구독 |
| ↳ Gemini CLI | ⭕ | Google 무료 티어 |
| **MLX** | ⭕ | Apple Silicon 로컬 |
| **Ollama** | ⭕ | 크로스 플랫폼 로컬 |

> 💡 **하나만 있어도 작동**. 여러 개 등록 시 비교 모드 사용 가능.

---

## 🛠 사용법

### 메인 메뉴
```bash
sukgo
```
→ 메뉴에서 도구 선택 → AI 백엔드 선택 (1개 또는 비교 모드 `a`) → 주제 입력

### 사고 도구 사용 예시
```
> 4   (6 Hats 선택)
> 어떤 AI? a   (모두 — 비교 모드)
> 주제: 회사를 이직해야 한다

⠋ claude · codex · gemini 가 6관점에서 분석 중...

[3개 AI의 6색 모자 관점 분석 통합 출력]

💾 저장됨: ~/Documents/Vault/000-Inbox/2026-04-26_..._6hats_compare.md
   3개 AI 응답이 한 파일에 통합됨
```

### Investment 도구 (자동 데이터 수집)
```
> i   (Investment)
> 종목: NVDA

📊 NVDA 데이터 수집 중...
✅ NVIDIA Corporation
   현재가:    $182.15
   PER:       65.40
   시가총액:  4.47T
   52주 범위: $86.62 ~ $195.31
   뉴스:      5건 수집

⠋ 9섹션 종합 리포트 생성 중...

[Executive Summary / Fundamental / Catalyst / Valuation / Risk /
 Technical / Market Positioning / Behavioral Check / 종합 평가]

💾 저장됨: ~/Documents/Vault/000-Inbox/_investments/2026-04-26_..._NVDA.md
```

한국 주식도 동일 (6자리 종목코드):
```
> 종목: 005930   (← 삼성전자)
```

---

## 🧠 사고 도구 13종

### 사고 프레임워크 (10종 — 어떤 주제든 적용)

| 키 | 도구 | 출처 | 언제 쓰나 |
|---|------|------|----------|
| 1 | 🛡 **Steel-manning** | 비판적 사고 전통 | 토론 준비, 본인 입장 검증 |
| 2 | 🥊 **Devil's Advocate** | 가톨릭 시성 절차 (1500년대) | 회의 준비, 확증편향 차단 |
| 3 | ⚰ **Pre-mortem** | Gary Klein (HBR 2007) | 투자·이직·창업 결정 전 |
| 4 | 🎩 **6 Hats** | Edward de Bono (1985) | 종합 의사결정 |
| 5 | 🔄 **Inversion** | Charlie Munger | 인생·투자 결정 |
| 6 | ❓ **5 Whys** | Toyota 생산 시스템 | 문제 분석, 자기 이해 |
| 7 | ⚖ **Decision Matrix** | 다기준 의사결정론 | 큰 선택지 비교 |
| 8 | 🧬 **First Principles** | Aristotle, Elon Musk | 창업·재정의 |
| 9 | 🌊 **OODA Loop** | John Boyd | 빠른 의사결정 |
| 0 | 🎯 **Toulmin Model** | Stephen Toulmin (1958) | 토론·보고서 논증 |

### 도메인 컨설턴트 (3종 — 특정 영역 전문 분석)

| 키 | 도구 | 데이터 소스 | 출력 |
|---|------|-----------|------|
| **c** | 💼 **Career** | — | 이직·커리어 정량+정성 분석 (5년 시나리오) |
| **i** | 📈 **Investment** | yfinance + finance-datareader | 9섹션 종합 리포트 (실시간 데이터 자동 수집) |
| **e** | 👶 **Education** | — | 자녀 교육 발달학·연구 기반 분석 |

---

## 🔌 백엔드 5종

| 백엔드 | 인증 | 비용 | 도구 사용 |
|--------|------|------|----------|
| 🥇 **claude** | Claude Code OAuth | Pro/Max 구독 | ✅ WebSearch/WebFetch |
| 🥈 **codex** | Codex CLI OAuth | ChatGPT Plus | ✅ 자체 도구 |
| 🥉 **gemini** | Gemini CLI OAuth | Google 무료 | ✅ 자체 도구 |
| 4 **mlx** | 로컬 HTTP | 무료 (Apple Silicon) | 텍스트만 |
| 5 **ollama** | 로컬 HTTP | 무료 (크로스 플랫폼) | 텍스트만 |

→ 사용자가 가진 CLI 자동 감지. **여러 개 등록 시 비교 모드** (같은 질문, 다른 시각).

### 비교 모드 — sukgo의 진짜 강점

```
주제: "AI 시대에는 학생들에게 코딩보다 비판적 사고를 먼저 가르쳐야 한다"

🧠 claude    →  학술적·구조적 (Willingham, MIT Resnick 인용)
🧠 codex     →  실용적·시장 관점 (GPT-5.4 학습 지식)
🧠 gemini    →  데이터·트렌드 관점 (Google 인덱스)

→ 한 마크다운 파일에 3개 시각 통합 → 옵시디언에서 한눈에 비교
```

**OpenRouter 등 별도 결제 없이** 자기 구독으로 다관점 분석 가능.

---

## 👥 누가 쓰면 좋은가

### 🎓 학생 — 토론·디베이트 준비
```bash
sukgo → 1   (Steel-manning)
> 주제: 인공지능 규제 강화 (찬성 입장)
```
→ 가장 강한 반대 논리 + 본인 입장 보강 가이드 (Toulmin 모델 자동 적용).

### 💼 회사원 — 회의 준비
```bash
sukgo → 2   (Devil's Advocate)
> 주제: Q3 마케팅 예산 30% 증액
```
→ 예상 반대 의견 5가지 + 답변 템플릿 (5분 만에 무장).

### 💰 투자자 — 종목 검토
```bash
sukgo → i   (Investment)
> 종목: NVDA
```
→ yfinance 자동 데이터 + 9섹션 종합 리포트 + Bull/Base/Bear 시나리오.

### 👶 부모 — 자녀 교육 결정
```bash
sukgo → e   (Education)
> 고민: 초등 3학년, 영어 학원 그만두고 코딩 학원 가고 싶어함
```
→ 발달 단계 적합성 + 검증된 연구 + 한국 입시 현실 + 부모-자녀 관계 영향.

### 🤔 일반인 — 인생 결정
```bash
sukgo → 3   (Pre-mortem)
> 주제: 결혼 5년차, 둘째 아이 가질지 말지
```
→ "1년 후 후회한다면 이유 5가지" + 사전 차단 전략.

---

## 🏗 아키텍처

```
┌─────────────────────────────────────────┐
│              User Input                  │
│           (CLI args / TUI)               │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│              sukgo Core                  │
│  ┌──────┐  ┌──────┐  ┌──────────────┐  │
│  │Tools │→ │Data  │→ │Renderer      │  │
│  │ (13) │  │Fetch │  │(Rich/ANSI)   │  │
│  └──────┘  └──────┘  └──────────────┘  │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Backend Adapter (5종)            │
│  claude · codex · gemini · MLX · Ollama  │
│  (subprocess / HTTP, 자동 감지)          │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│              Persistence                 │
│  ~/.config/sukgo/    (설정)              │
│  $OBSIDIAN_VAULT/    (자동 저장)          │
└─────────────────────────────────────────┘
```

### 🔑 핵심 디자인 패턴

#### Wrapper Script Pattern
```
~/.local/bin/sukgo  (bash wrapper)
       ↓
exec ~/.sukgo/venv/bin/python ~/Desktop/sukgo/poc.py "$@"
       ↓
사용자가 어떤 venv에 있든 → 항상 자기 venv 사용
   = 영원히 의존성 안 깨짐
```

#### 외부 프롬프트 파일
```
prompts/investment.md   ← 9섹션 분석 (코드와 분리)
                        ← Claude Code 슬래시 커맨드와 동기화 가능
```

---

## 🔒 보안

> **본인의 API 키는 본인 컴퓨터에만.**

- API 키는 `~/.config/sukgo/secrets.json`에 권한 600으로 저장
- 코드와 완전 분리 — `.gitignore`로 GitHub 업로드 차단
- 첫 사용 시 wizard로 안전하게 입력
- AI CLI(`claude`/`codex`/`gemini`)는 자체 OAuth 사용 — sukgo가 키 보지 않음

---

## 🐛 트러블슈팅

### `command not found: sukgo`
새 터미널 창을 여세요. 또는:
```bash
source ~/.zshrc    # 또는 ~/.bashrc
```

### Python 의존성 에러
```bash
~/.sukgo/venv/bin/pip install --upgrade pip
~/.sukgo/venv/bin/pip install yfinance finance-datareader requests
```

### 가상환경 충돌
sukgo는 `~/.sukgo/venv` 격리 환경 사용. 사용자 다른 venv 영향 받지 않음.
재설치하려면:
```bash
rm -rf ~/.sukgo
curl -fsSL https://raw.githubusercontent.com/reallygood83/sukgo/main/get.sh | bash
```

### AI 응답이 너무 느림
- 단일 AI: 10~60초 정상
- 비교 모드 (3 AI): 1~3분 정상 (순차 호출)
- Investment 9섹션: 30~120초 정상

### 한국 주식 데이터 안 옴
6자리 종목코드만 입력. 회사명·괄호는 자동 무시되지만, 안전하게:
```
종목: 005930      ← OK
종목: 005930(삼성)  ← OK (자동 정규화)
종목: 삼성전자      ← ❌ (6자리 코드 필요)
```

### 더 많은 도움
- 📖 [`docs/ONBOARDING.md`](docs/ONBOARDING.md) — 초보자 가이드 + FAQ
- 🐛 [GitHub Issues](https://github.com/reallygood83/sukgo/issues)

---

## 🗺 로드맵

| 버전 | 상태 | 핵심 |
|------|------|------|
| v0.0.5 | ✅ 현재 | 13 도구 + 5 백엔드 + 데이터 페처 + 한 줄 설치 |
| v0.1 | 🚧 다음 | `pipx install sukgo` + slash command 동기화 + Release |
| v0.3 | 곧 | PyPI 정식 + Windows·Linux 풀 검증 + DART API |
| v0.5 | 중기 | 도메인 확장 (부동산·관계·건강) + 플러그인 시스템 |
| v1.0 | 장기 | 영문 i18n + Homebrew tap + 커뮤니티 |

상세: [`CHANGELOG.md`](CHANGELOG.md)

---

## 🤝 기여

PR / 이슈 환영합니다.

| 어떻게 | 어디 |
|--------|------|
| 🐛 **버그 신고** | [GitHub Issues](https://github.com/reallygood83/sukgo/issues) |
| 💡 **새 사고 도구 제안** | `prompts/` 폴더에 마크다운 추가 + PR |
| 🌐 **백엔드 추가** | `poc.py` Backend 클래스 상속 |
| 📊 **데이터 페처 추가** | `data_fetchers/` 폴더 |
| 📚 **문서 개선** | `docs/` 또는 `README.md` |
| 🌍 **번역** | `docs/i18n/` (예정) |

### 새 사고 도구 추가 (5분 가이드)
1. `prompts/<도구이름>.md` 작성 (Steel-manning 참고)
2. `poc.py` `TOOLS` 리스트에 항목 추가:
   ```python
   Tool(
       key="X",                    # 메뉴 단축키
       name="My Tool",
       emoji="🔮",
       short_desc="한 줄 설명",
       save_id="mytool",
       category="thinking",        # or "domain"
       prompt_file="mytool.md",    # prompts/ 폴더 파일명
   )
   ```
3. PR 생성 — 끝!

---

## 📚 문서

| 파일 | 내용 |
|------|------|
| [`README.md`](README.md) | 이 파일 (개요·설치·사용법) |
| [`docs/ONBOARDING.md`](docs/ONBOARDING.md) | 🌱 초보자 5분 가이드 + FAQ |
| [`CHANGELOG.md`](CHANGELOG.md) | 변경 기록 |

---

## 📄 라이선스

[MIT](LICENSE) — 자유롭게 사용·수정·배포 (상업 사용 포함).

> ⚠ **Investment 도구**의 분석 결과는 **교육·참고용이며 투자 자문이 아닙니다.**
> 실제 투자는 본인 판단·책임이며, 추가 리서치(공시·증권사 리포트·전문가 자문)가 필요합니다.

---

## 👤 Made by

<div align="center">

**배움의 달인**
*더 잘 배우고, 더 잘 생각하는 도구를 만듭니다.*

> *"GUI는 우리에게 컴퓨터를 가르쳤고,*
> *CLI는 컴퓨터에게 우리 생각을 가르친다."*

[![GitHub](https://img.shields.io/badge/GitHub-reallygood83-181717?logo=github)](https://github.com/reallygood83)

</div>

---

<div align="center">

**⭐ 도움이 됐다면 Star 부탁드려요!**

[Issues](https://github.com/reallygood83/sukgo/issues) · [Discussions](https://github.com/reallygood83/sukgo/discussions) · [Releases](https://github.com/reallygood83/sukgo/releases)

🚀 **한 줄 설치**
```bash
curl -fsSL https://raw.githubusercontent.com/reallygood83/sukgo/main/get.sh | bash
```

</div>
