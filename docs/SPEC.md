# sukgo — 개발 스펙 (SPEC v0.1)

> **문서 버전**: 0.1.0
> **작성일**: 2026-04-26
> **작성자**: 배움의 달인
> **상태**: Draft

---

## 0. 목차

1. [비전 & 미션](#1-비전--미션)
2. [문제 정의](#2-문제-정의)
3. [솔루션 개요](#3-솔루션-개요)
4. [타겟 사용자](#4-타겟-사용자)
5. [핵심 컨셉: 사고 도구 10종](#5-핵심-컨셉-사고-도구-10종)
6. [사용자 경험 (UX Flow)](#6-사용자-경험-ux-flow)
7. [기술 스택](#7-기술-스택)
8. [아키텍처](#8-아키텍처)
9. [백엔드 어댑터 5종](#9-백엔드-어댑터-5종)
10. [디렉터리 구조](#10-디렉터리-구조)
11. [MVP 범위 (v0.1)](#11-mvp-범위-v01)
12. [로드맵 v0.1 → v1.0](#12-로드맵-v01--v10)
13. [비기능 요구사항](#13-비기능-요구사항)
14. [데이터 저장 명세](#14-데이터-저장-명세)
15. [브랜딩 명세](#15-브랜딩-명세)
16. [성공 지표](#16-성공-지표)

---

## 1. 비전 & 미션

### 비전
> **"AI 시대, 누구나 더 잘 생각할 수 있도록."**

### 미션
검증된 사고 프레임워크와 AI를 결합해, 일상의 모든 결정·토론·고민을 더 단단하게 만드는 **개인용 사고 코치**를 보급한다.

### 슬로건 후보
- *"결정의 기술"*
- *"AI와 함께 푹 익혀 생각하기"*
- *"고민을 끝내고, 결정을 시작합니다"*

---

## 2. 문제 정의

### 사용자가 겪는 진짜 문제

| 페르소나 | 문제 상황 | 기존 해결책의 한계 |
|---------|----------|------------------|
| **회사원** | 회의 5분 전, 예상 반박이 안 떠오름 | ChatGPT 켜기 너무 느림, 매번 프롬프트 새로 침 |
| **학생** | 토론 대회 준비, 반박 패턴 학습 부족 | 멘토 부족, 친구와 연습 어려움 |
| **이직 고민자** | 머릿속에서만 빙빙 도는 비교 | 객관화 도구 없음, 후회 시뮬레이션 못함 |
| **창업자** | 비즈니스 모델 약점이 안 보임 | 자기 검증 어려움, Devil's Advocate 부재 |
| **투자자** | 매수 결정 전 다각도 검토 부족 | 확증편향, 시나리오 분석 누락 |

### 공통 본질
> **"혼자서는 보이지 않는 시선을 빌려와, 더 나은 결정 내리기"**

---

## 3. 솔루션 개요

### 핵심 가설
- 사람들이 결정을 잘 못하는 이유는 **머리가 나빠서가 아니라**, **검증된 사고 도구를 모르거나 안 쓰기 때문**.
- AI는 **다양한 관점을 즉시 시뮬레이션**하는 데 강함.
- → **사고 도구 + AI** 결합 시, 누구나 전문 컨설턴트 수준의 사고 가능.

### 차별화 포인트

| | ChatGPT 웹 | Claude Code 슬래시 | sukgo |
|---|------------|------------------|-------|
| 시작 속도 | 30초+ | Claude Code 필요 | **2초** |
| 사고 프레임워크 | 매번 직접 입력 | 매번 직접 입력 | **명령어 자체가 도구** |
| 시스템 통합 | ❌ | 제한적 | **파이프·cron·옵시디언** |
| 백엔드 자유 | ❌ | Claude만 | **5종 선택** |
| 로컬 기록 | ❌ | 수동 | **자동 마크다운** |

---

## 4. 타겟 사용자

### Primary (먼저 잡을 사용자)
- **터미널이 두렵지 않은 지식근로자** (개발자/기획자/연구자)
- **토론·디베이트 동아리 학생** (대학생·고등학생)
- **AI 도구 얼리어답터** (이미 Claude Pro / ChatGPT Plus 사용 중)

### Secondary (확장 단계)
- 일반 회사원 (영상 콘텐츠로 진입장벽 낮춰서)
- 교육자 (학생들에게 권하는 도구로)
- 컨설턴트 / 코치

### Out of Scope
- 터미널을 한 번도 안 써본 비기술 사용자 (별도 GUI 버전이 필요한 경우)

---

## 5. 핵심 컨셉: 사고 도구 10종

각 도구 = 검증된 사고 프레임워크. 명령어로 호출 가능.

| # | 도구 | 명령 | 용도 |
|---|------|------|------|
| 1 | 🥊 **Devil's Advocate** | `sukgo devil` | 일부러 반대 입장 펴기 |
| 2 | 🛡️ **Steel-manning** | `sukgo steel` | 상대 주장 가장 강한 버전 만들기 |
| 3 | ⚰️ **Pre-mortem** | `sukgo premortem` | "실패했다고 가정" 후 원인 추적 |
| 4 | 🎩 **6색 모자** | `sukgo hats` | 6가지 관점 (사실/감정/비판/긍정/창의/통제) |
| 5 | 🔄 **Inversion** | `sukgo invert` | 거꾸로 생각하기 |
| 6 | ❓ **5 Whys** | `sukgo why` | "왜?" 5번으로 근본 원인 |
| 7 | ⚖️ **Decision Matrix** | `sukgo matrix` | 옵션 × 기준 가중치 비교 |
| 8 | 🧬 **First Principles** | `sukgo principles` | 가정 다 버리고 본질부터 |
| 9 | 🌊 **OODA Loop** | `sukgo ooda` | 관찰→정황→결정→행동 |
| 10 | 🎯 **Toulmin Model** | `sukgo toulmin` | 주장-근거-보강-반박-한정 |

### 자동 추천 모드
```bash
$ sukgo
> 이직 고민 중...
🤖 추천 도구: Pre-mortem + Decision Matrix + 6 Hats
   진행하시겠어요? [y/n/select]
```

---

## 6. 사용자 경험 (UX Flow)

### 진입점 1: 단순 호출 (자동 추천)
```bash
$ sukgo
```
→ TUI 화면 → 자유 입력 → AI가 도구 추천 → 진행

### 진입점 2: 도구 직접 호출
```bash
$ sukgo steel "AI 일자리 위협 토론"
$ sukgo premortem "신규 사업 런칭"
$ sukgo matrix "이직 결정"
```

### 진입점 3: 파이프 입력
```bash
$ git diff | sukgo devil
$ cat proposal.md | sukgo critique
```

### 첫 실행 시 (`sukgo init`)
```
🎯 환영합니다! 어떤 AI를 쓰시겠어요?

  1) Claude Code (Pro/Max 구독자)  ← 추천
  2) Codex (ChatGPT Plus 구독자)
  3) Gemini CLI (무료 티어)
  4) MLX (로컬, Apple Silicon)
  5) Ollama (로컬, 크로스 플랫폼)

> 4

✅ MLX 감지. 사용 가능한 모델:
   - Qwen2.5-32B-Instruct-4bit
   - Llama-3.3-70B-Instruct-4bit

기본 모델 선택: > 1

✅ 설정 완료. ~/.config/sukgo/config.yaml 생성됨.
```

### 메인 TUI 첫 화면
```
┌──────────────────────────────────────────────────┐
│                                                    │
│                 s u k g o                          │
│              결 정 의   기 술                       │
│                                                    │
│  ─────────────────────────────────────────────   │
│                                                    │
│   1. 🤔 자유 고민 입력                              │
│   2. 🧠 사고 도구 직접 선택                          │
│   3. 📚 최근 기록                                   │
│   4. ⚙️  설정                                       │
│   q. 종료                                          │
│                                                    │
│  ─────────────────────────────────────────────   │
│              made by 배움의 달인 ✨                  │
│                  v0.1.0                            │
└──────────────────────────────────────────────────┘
>
```

---

## 7. 기술 스택

### 언어
- **Python 3.11+** (사용자 친숙도 + AI 생태계 표준 + MLX 호환)

### 핵심 라이브러리
| 라이브러리 | 용도 |
|----------|------|
| **Rich** | 터미널 색상·박스·테이블·스피너 |
| **prompt_toolkit** | 인터랙티브 입력·자동완성·히스토리 |
| **Typer** | CLI 명령어 라우팅 (Click 기반, 더 모던) |
| **Pydantic v2** | 설정·데이터 모델 검증 |
| **PyYAML** | 설정 파일 |
| **httpx** | OpenAI 호환 HTTP 호출 (MLX/Ollama용) |
| **openai** | OpenAI SDK (Codex/MLX/Ollama OpenAI 모드) |

### 선택적 (백엔드별)
- `claude` CLI (subprocess) — Claude Pro/Max 사용자
- `codex` CLI (subprocess) — ChatGPT Plus 사용자
- `gemini` CLI (subprocess) — Google 무료 티어
- `mlx_lm` (Python) 또는 `mlx_lm.server` (HTTP) — Apple Silicon 로컬
- Ollama HTTP — 크로스 플랫폼 로컬

### 배포
- **PyPI** (`pip install sukgo`)
- **Homebrew tap** (장기): `brew install sukgo`

---

## 8. 아키텍처

```
┌──────────────────────────────────────────────────┐
│                    User Input                       │
│         (CLI args / TUI / pipe stdin)              │
└──────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────┐
│                   sukgo Core                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  │
│  │  Router    │→ │  Tools     │→ │  Renderer  │  │
│  │  (Typer)   │  │  (10종)    │  │  (Rich)    │  │
│  └────────────┘  └────────────┘  └────────────┘  │
│         ↓               ↓               ↓          │
│   command parse   prompt template   pretty output  │
└──────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────┐
│                Backend Adapter                      │
│  ┌──────┐ ┌──────┐ ┌───────┐ ┌─────┐ ┌───────┐  │
│  │claude│ │codex │ │gemini │ │ mlx │ │ollama │  │
│  └──────┘ └──────┘ └───────┘ └─────┘ └───────┘  │
└──────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────┐
│                   AI Response                       │
│            (streaming → renderer)                   │
└──────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────┐
│                  Persistence                        │
│  - ~/.config/sukgo/         (설정)                  │
│  - ~/.local/share/sukgo/    (세션 기록)             │
│  - $OBSIDIAN_VAULT/         (선택, 자동 저장)        │
└──────────────────────────────────────────────────┘
```

---

## 9. 백엔드 어댑터 5종

### 9.0 백엔드 우선순위 전략 ⭐

> **핵심 원칙**: *"잠재 사용자가 이미 가진 것"* 순서로 우선순위.

| 순위 | 백엔드 | 타겟 사용자 | 시장 규모 | 메시지 가중치 |
|------|--------|-----------|----------|-------------|
| 🥇 **1** | **claude CLI** | Claude Pro/Max 구독자 | 🔥 거대 (개발자/지식근로자 다수) | "이미 내는 구독 그대로" |
| 🥈 **2** | **codex CLI** | ChatGPT Plus 구독자 | 🔥🔥 가장 큼 (전 세계 AI 1위) | "Plus 구독자는 본전 뽑기" |
| 🥉 **3** | **gemini CLI** | Google 무료 사용자 | 🟢 큼 | "결제 안 하고도 가능" |
| 4 | **MLX** | Apple Silicon 파워 유저 | 🟡 니치 (개발자 일부) | "프라이버시 + 오프라인" |
| 5 | **ollama** | 크로스 플랫폼 로컬 사용자 | 🟡 작음 | "Windows/Linux 로컬" |

### 메시지 우선순위
1. **메인 후크**: *"Claude Pro / ChatGPT Plus 이미 내고 계시죠? 그걸로 CLI 만들기."*
2. **확장 메시지**: *"무료 Gemini로도 됩니다."*
3. **파워 유저 보너스**: *"로컬 MLX/Ollama로 완전 무료·오프라인."*

### MVP 결정
- **v0.1 우선 구현**: **claude CLI** (최대 시장) + **MLX** (사용자님 개발 환경)
- 두 백엔드를 같은 인터페이스로 추상화하여 처음부터 검증
- v0.2: codex CLI 추가
- v0.3: gemini CLI + ollama

> ⚠️ **유지보수 주의**: 모든 시연 영상·썸네일·README 첫 화면은 **Claude / ChatGPT 사용 장면 우선**. MLX는 "보너스 트랙" 으로 등장.

---

### 인터페이스 (모든 백엔드가 구현)
```python
class Backend(Protocol):
    def chat(self, messages: list[Message], stream: bool = True) -> Iterator[str]:
        """메시지 → 토큰 스트림"""
        ...

    def is_available(self) -> bool:
        """이 백엔드 사용 가능한지 확인"""
        ...
```

### 1. Claude (subprocess)
```python
subprocess.run(
    ["claude", "-p", prompt, "--output-format", "json"],
    capture_output=True, text=True
)
```
- **장점**: OAuth 그대로, Max 구독 활용
- **단점**: 0.5~1초 오버헤드

### 2. Codex (subprocess)
```python
subprocess.run(["codex", "exec", prompt], ...)
```
- **장점**: ChatGPT Plus 활용
- **단점**: 출력 포맷 파싱 필요

### 3. Gemini (subprocess)
```python
subprocess.run(["gemini", "-p", prompt], ...)
```
- **장점**: 무료 티어
- **단점**: 한도 있음

### 4. MLX (HTTP, 사용자님 환경)
```bash
# 사용자가 한 번만 띄움
mlx_lm.server --model mlx-community/Qwen2.5-32B-Instruct-4bit
```
```python
client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")
client.chat.completions.create(...)
```
- **장점**: 가장 빠름, 완전 무료, 오프라인
- **단점**: Apple Silicon 한정, 모델 다운로드 필요

### 5. Ollama (HTTP)
```python
# OpenAI 호환 모드 또는 native API
```
- **장점**: 크로스 플랫폼
- **단점**: MLX 대비 느림 (Apple Silicon에서)

### 백엔드 자동 선택 로직
```
1. config.yaml에 명시된 백엔드 우선
2. 없으면 자동 감지: claude → codex → gemini → mlx → ollama 순
3. 사용 가능한 첫 번째 사용
```

---

## 10. 디렉터리 구조

### 프로젝트 루트
```
sukgo/
├── README.md
├── docs/
│   ├── SPEC.md           # ← 이 문서
│   ├── KICK.md           # 서비스 기획·브랜드
│   └── (추후) ARCHITECTURE.md, API.md
├── src/
│   └── sukgo/
│       ├── __init__.py
│       ├── __main__.py        # python -m sukgo 진입점
│       ├── cli.py             # Typer 앱
│       ├── tui.py             # 메인 TUI 화면
│       ├── config.py          # Pydantic 설정 모델
│       ├── tools/             # 사고 도구 10종
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── steelman.py
│       │   ├── devil.py
│       │   ├── premortem.py
│       │   ├── hats.py
│       │   ├── inversion.py
│       │   ├── why5.py
│       │   ├── matrix.py
│       │   ├── principles.py
│       │   ├── ooda.py
│       │   └── toulmin.py
│       ├── backends/          # AI 백엔드 어댑터
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── claude.py
│       │   ├── codex.py
│       │   ├── gemini.py
│       │   ├── mlx.py
│       │   └── ollama.py
│       ├── render/            # Rich 기반 출력
│       │   ├── __init__.py
│       │   ├── banner.py      # 시작 화면 ASCII
│       │   └── components.py
│       └── store/             # 영속 저장
│           ├── __init__.py
│           ├── session.py
│           └── obsidian.py
├── tests/
│   ├── test_backends/
│   ├── test_tools/
│   └── test_cli.py
├── pyproject.toml
├── uv.lock                # uv 사용 시 (또는 poetry.lock)
├── .gitignore
└── LICENSE                # MIT 권장
```

### 사용자 환경 파일
```
~/.config/sukgo/
└── config.yaml            # 백엔드 설정, 기본값

~/.local/share/sukgo/
├── sessions/              # 세션 기록 (마크다운)
│   └── 2026-04-26_14-30_premortem.md
└── history.jsonl          # 명령어 히스토리
```

---

## 11. MVP 범위 (v0.1)

### ✅ 포함
1. 메인 TUI 진입 (`sukgo`)
2. 백엔드 **2개** 작동:
   - **claude CLI** (대부분 시청자 타겟 — 메인 시연용) 🥇
   - **MLX** (사용자님 개발 환경 — 빠른 자체 테스트용) 🛠️
3. 사고 도구 **3개**:
   - Steel-manning
   - Pre-mortem
   - Decision Matrix
4. 자유 입력 → 도구 추천
5. 첫 화면 브랜딩 ("배움의 달인" 명시)
6. 세션 자동 저장 (마크다운)
7. `sukgo init` 설정 마법사 (Claude 옵션을 첫 번째로 노출)

### ❌ 제외 (v0.2+)
- codex / gemini / ollama 백엔드
- 사고 도구 10종 모두
- 옵시디언 자동 저장
- 파이프 입력 (`|`)
- 자동완성·히스토리 고급 기능
- 영어 i18n

### 🎯 MVP 시연 시나리오 (영상·README용)
> **반드시 Claude CLI 사용 장면으로 시연.**
> *"여러분, Claude Pro 구독 중이시죠? 그걸로 sukgo가 작동합니다. 추가 결제 없이."*

---

## 12. 로드맵 v0.1 → v1.0

| 버전 | 목표 | 핵심 기능 | 예상 기간 |
|------|------|----------|----------|
| **v0.1 (PoC)** | 본인 검증 | 도구 3종 + **Claude·MLX** 백엔드 (시연=Claude) | 1주말 |
| **v0.2** | 친구 베타 | 도구 6종 + **codex** 백엔드 추가 | 2주 |
| **v0.3** | 공개 베타 | 도구 10종 모두 + **Gemini·Ollama** 백엔드 | 1개월 |
| **v0.4** | 콘텐츠 시작 | 옵시디언 연동 + 파이프 입력 + YouTube 영상 | 1개월 |
| **v0.5** | 사용자 피드백 반영 | 템플릿 시스템 + 플러그인 | 2개월 |
| **v1.0** | 정식 출시 | PyPI + Homebrew + 영문 README + 커뮤니티 | 6개월 |

---

## 13. 비기능 요구사항

### 성능
- 명령어 실행 → 첫 토큰 출력: **1초 이내** (MLX 기준)
- 메모리 사용: 50MB 이내 (백엔드 서버 제외)

### 보안 / 프라이버시
- 사용자 데이터는 **전부 로컬에만 저장** (텔레메트리 없음)
- 외부 API 호출 시에도 **사용자 자신의 키/구독으로만**
- v1.0까지 **수집·분석 시스템 없음**

### 호환성
- macOS 14+ (MLX 백엔드용 Apple Silicon)
- Linux / Windows (claude·codex·gemini·ollama 백엔드 사용 시)

### 접근성
- 컬러를 끄는 옵션 (`--no-color`)
- 화면 너비 60자 이상 보장

### 라이선스
- **MIT** (오픈소스, 상업 사용 허용)

---

## 14. 데이터 저장 명세

### 세션 파일 포맷 (마크다운)
```yaml
---
tool: premortem
topic: "이직 결정"
created: 2026-04-26T14:30:00+09:00
backend: mlx
model: Qwen2.5-32B-Instruct-4bit
duration_sec: 327
---

# Pre-mortem: 이직 결정

## Q1. 1년 후 후회한다면 이유는?
- ...

## Q2. ...
```

### 옵시디언 자동 저장 (선택)
```bash
$ sukgo config set obsidian.vault "/Users/moon/Documents/LearningMaster/000-Inbox"
$ sukgo config set obsidian.subdir "060-Idea/decisions"
```
→ 모든 세션이 옵시디언 볼트에 frontmatter와 함께 저장

---

## 15. 브랜딩 명세

### 이름
- **표기**: `sukgo` (소문자, 영문 통일)
- **발음**: 숙고
- **유래**: 한국어 "숙고(熟考)" — 푹 익혀서 생각하다

### 표기 규칙
- 모든 코드·UI·문서·로고: **`sukgo`** (영문 소문자)
- 한자 "熟考" 는 **사용하지 않음** (호환성 + 가독성)
- 영어권 설명 시: "sukgo (sook-go) — *deep thinking* in Korean"

### 톤 & 매너
- **차분한 무게감** (가벼운 챗봇이 아닌 진지한 사고 도구)
- **친근한 한국적 정서** (어려운 한자어지만 부드럽게)
- **개발자스러운 미니멀리즘** (불필요한 장식 없음)

### 시각 언어
- **컬러**: 차분한 종이색(베이지) + 강조 청록(teal) + 경고 적색
- **이모지**: 사고 도구별 1개 고정 (🥊 🛡️ ⚰️ 🎩 🔄 ❓ ⚖️ 🧬 🌊 🎯)
- **타이포**: 등폭 폰트 (터미널 기본)

### 첫 화면 ASCII (제안)
```
┌──────────────────────────────────────────────┐
│                                                │
│                s u k g o                       │
│           결 정 의    기 술                     │
│                                                │
│  ─────────────────────────────────────────   │
│                                                │
│   1. 🤔 자유 고민 입력                          │
│   2. 🧠 사고 도구 직접 선택                      │
│   3. 📚 최근 기록                               │
│   4. ⚙️  설정                                   │
│   q. 종료                                      │
│                                                │
│  ─────────────────────────────────────────   │
│             made by 배움의 달인 ✨              │
│                 v0.1.0                         │
└──────────────────────────────────────────────┘
```

### 크리에이터 표기
- 모든 화면 하단: `made by 배움의 달인 ✨`
- README 하단: 만든 사람 소개 + YouTube 링크
- `--version` 출력에 포함

---

## 16. 성공 지표

### v0.1 (본인 검증)
- [ ] 본인이 1주일간 매일 1회 이상 사용
- [ ] 사용 후기를 마크다운 노트로 기록 (5건+)
- [ ] 실제로 도움된 결정 1건 이상

### v0.3 (공개 베타)
- [ ] GitHub Star 50+
- [ ] PyPI 다운로드 200+/월
- [ ] 베타 사용자 10명 이상

### v1.0 (정식 출시)
- [ ] GitHub Star 500+
- [ ] PyPI 다운로드 2,000+/월
- [ ] YouTube 영상 누적 조회 50,000+
- [ ] 외부 기여자 PR 10건+

---

## 부록 A. 사용 시나리오 (페르소나별)

### A1. 학생 — 토론대회 준비
```bash
$ sukgo steel "AI 규제 강화: 찬성 입장"
```
→ 반대 측 가장 강한 논리 5가지 + 본인 답변 작성 가이드

### A2. 회사원 — 회의 준비
```bash
$ sukgo devil "Q3 마케팅 예산 30% 증액 제안"
```
→ 예상 반대 의견 5가지 + 답변 템플릿

### A3. 이직 고민자 — 결정 검토
```bash
$ sukgo
> 연봉 30% 더 주는 곳에서 오퍼를 받았어요
🤖 추천: Pre-mortem + Decision Matrix + 6 Hats
```

### A4. 투자자 — 종목 분석
```bash
$ sukgo invert "AAPL 추가 매수"
```
→ "이 투자가 망하는 5가지 시나리오" + 대응 전략

### A5. 창업자 — 피칭 준비
```bash
$ sukgo devil "B2B SaaS 비즈니스 모델"
```
→ 투자자가 던질 어려운 질문 10개 + 답변 코칭

---

## 부록 B. 의존성 의사결정 기록

### 왜 Python? (vs TypeScript)
- 사용자 친숙도 ✅
- MLX 네이티브 지원 ✅
- AI/ML 생태계 표준 ✅
- 단점(배포 복잡): `pipx install sukgo` 또는 Homebrew로 해결

### 왜 Typer? (vs Click)
- 타입 힌트 기반 → IDE 친화적
- Pydantic과 자연스럽게 결합
- Click 위에 빌드되어 안정적

### 왜 Rich? (vs Textual)
- v0.1은 단순 출력 위주 → Rich로 충분
- Textual은 v0.5+에서 고려 (전면 TUI 필요할 때)

### 왜 5종 백엔드 모두? (vs 1~2개로 시작)
- v0.1은 MLX 1개만
- v0.2부터 점진적 추가
- 인터페이스 추상화는 처음부터

---

## 부록 C. 참고 자료

- **사고 프레임워크 원전**:
  - Edward de Bono, *Six Thinking Hats* (1985)
  - Stephen Toulmin, *The Uses of Argument* (1958)
  - Gary Klein, *Performing a Project Premortem* (HBR, 2007)
  - Charlie Munger, *Inversion* (Mental Models)
- **CLI 디자인 참고**:
  - `claude` (Anthropic)
  - `gh` (GitHub)
  - `lazygit`
  - `aider`
- **유사 프로젝트**:
  - OMC (oh-my-claudecode) — 멀티 에이전트
  - aider — 코딩 어시스턴트
  - llm (Simon Willison) — 범용 AI CLI
