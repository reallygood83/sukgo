# 🌱 초보자 온보딩 가이드

> **Python·터미널 안 써본 분들도 따라하실 수 있어요.**

---

## 🎯 목표

이 가이드 따라하시면 5분 안에:
- ✅ sukgo 설치 완료
- ✅ 첫 분석 (예: "이직 고민") 시연
- ✅ 결과를 옵시디언 등에 자동 저장

---

## 📋 사전 준비물 (없으면 설치)

### 1. **macOS 터미널 열기**
- `Cmd + Space` → "터미널" 입력 → Enter
- 또는 [iTerm2](https://iterm2.com/) (더 예쁨, 추천)

### 2. **Homebrew 설치 (Mac 사용자, 5분)**
터미널에 복붙:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
→ 비밀번호 입력 → 끝까지 진행 → 마지막 안내 따라 PATH 추가.

### 3. **Python 3.11 설치**
```bash
brew install python@3.11
```

### 4. **Git 설치 (Mac은 보통 있음)**
```bash
git --version
```
→ 안 보이면: `brew install git`

### 5. **AI CLI 중 1개 이상 (선택)**

#### Claude Code (Pro/Max 구독자)
```bash
brew install --cask claude
```
설치 후 한 번 실행해서 로그인.

#### ChatGPT Codex CLI (Plus 구독자)
```bash
npm install -g @openai/codex
codex login
```

#### Gemini CLI (무료)
```bash
npm install -g @google/gemini-cli
gemini   # 첫 실행 시 로그인
```

> 💡 **하나만 있어도 sukgo 작동.** 셋 다 있으면 비교 모드 사용 가능.

---

## 🚀 sukgo 설치 (3줄)

터미널에:
```bash
cd ~/Desktop
git clone https://github.com/reallygood83/sukgo.git
cd sukgo
./install.sh
```

→ 1~2분 자동 진행. 마지막에 "✅ 설치 완료!" 보이면 OK.

---

## ▶ 첫 실행

```bash
sukgo
```

처음에는 **첫 실행 마법사**가 1분 설정 도와드림:

### Step 1: AI 백엔드 선택
화면에 사용 가능한 AI 목록이 뜸. **번호 입력** (예: `1`).
여러 개 등록하고 싶으면: `1,2,3` 입력.

### Step 2: 저장 위치
"저장 위치:" 에서:
- 옵시디언 사용자: `~/Documents/MyVault/Inbox` (자기 볼트 경로)
- 그냥 폴더: 비워두고 Enter (기본값 `~/.local/share/sukgo/sessions`)

→ 끝!

---

## 🎮 첫 사용 — "이직 고민" 예시

```bash
sukgo
```

메뉴에서:
```
> 3   (Pre-mortem 선택)
> a   (모든 AI 비교 모드 — 또는 1개 골라도 OK)
> 주제: 회사 이직 — 현재 vs 30% 더 주는 외국계
```

→ AI가 "1년 후 후회할 5가지" + 사전 차단 전략 제시 → 옵시디언에 자동 저장.

---

## 💡 자주 쓰는 도구 추천

| 상황 | 도구 | 명령 |
|------|------|------|
| **회의 5분 전** | Devil's Advocate | `sukgo → 2` |
| **이직 고민** | Pre-mortem + 6 Hats | `sukgo → 3` 또는 `4` |
| **투자 검토** | Investment | `sukgo → i` |
| **자녀 교육 고민** | Education | `sukgo → e` |
| **학생 토론 연습** | Steel-manning | `sukgo → 1` |
| **큰 결정 비교** | Decision Matrix | `sukgo → 7` |

---

## ❓ 자주 묻는 질문

### Q1. "command not found: sukgo" 라고 나와요
A. 새 터미널 창을 여세요. 또는:
```bash
source ~/.zshrc
```

### Q2. AI 응답이 느려요
A. 정상입니다. claude/codex는 보통 10~60초 걸려요.
Investment 도구는 9섹션이라 30~120초 걸릴 수 있음.

### Q3. 비교 모드는 비싸지 않나요?
A. 사용자님이 가진 구독(Claude Pro / ChatGPT Plus 등) 안에서 사용. **추가 결제 0원**.

### Q4. 결과를 어디에 저장돼요?
A. 첫 실행 마법사에서 입력한 폴더에 마크다운(`.md`) 파일로 자동 저장.
파일명: `2026-04-26_HHMM_도구명_주제.md`

### Q5. 옵시디언 어디에 저장하면 좋아요?
A. **Inbox 폴더 추천**. 옵시디언에서:
- 새 마크다운 자동 표시
- frontmatter로 검색·필터 가능
- 백링크 자동 인식

### Q6. 한국 주식도 분석돼요?
A. 네, Investment 도구에서 6자리 종목코드 입력:
```
종목: 005930   (삼성전자)
종목: 035420   (네이버)
```

### Q7. 데이터가 정확해요?
A. yfinance·FinanceDataReader 라이브러리 데이터 (실시간).
하지만 AI 분석은 **참고용** — 투자 결정은 본인 책임.

### Q8. 잘못된 결정에 사용했다 손해보면?
A. sukgo는 **사고 보조 도구**. 최종 결정·책임은 사용자.
LICENSE 파일에 면책 명시.

---

## 🆘 도움이 필요하면

1. **README**: https://github.com/reallygood83/sukgo
2. **Issues**: https://github.com/reallygood83/sukgo/issues
3. **보안 가이드**: [`docs/SECURITY.md`](SECURITY.md)
4. **개발 스펙**: [`docs/SPEC.md`](SPEC.md)

---

## 🎁 다음 단계

sukgo가 익숙해졌다면:
- 매일 1번 결정에 사용 → 사고 프레임워크 자연스럽게 학습
- 결과를 옵시디언에 쌓아두기 → 시간 지나 복기
- 친구에게 추천 (한 줄 설치)
- GitHub에 ⭐ Star

---

*made by 배움의 달인 ✨ — 더 잘 배우고, 더 잘 생각하는 도구를 만듭니다.*
