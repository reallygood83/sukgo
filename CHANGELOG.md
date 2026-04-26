# Changelog

All notable changes to **sukgo** are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/) · Versioning: [SemVer](https://semver.org/)

---

## [0.0.5] — 2026-04-26

### Added
- 🚀 **`install.sh`** — 한 번에 설치 스크립트 (Python 확인, 의존성, chmod, symlink)
- 📦 **`requirements.txt`** — yfinance, FinanceDataReader, requests
- 📊 **`data_fetchers/stocks.py`** — 주식 데이터 자동 수집 모듈
  - yfinance (해외 주식 50+ 항목)
  - FinanceDataReader (한국 주식)
  - 티커 형식 자동 감지 (한국 6자리 vs 해외)
  - LLM 프롬프트용 마크다운 포맷터
- 📝 **`prompts/investment.md`** — Investment 도구 외부 프롬프트 (9섹션)
- 🔄 **`load_prompt_file()`** — 외부 프롬프트 로드 헬퍼
- 🛠 **`investment_flow()`** — Investment 전용 흐름 (데이터 수집 → 프롬프트 주입 → AI 호출)
- 📂 Investment 결과는 `_investments/` 서브폴더에 자동 분류
- ⚠ 투자 분석 면책 조항 (LICENSE에도 포함)
- 📚 **`docs/SECURITY.md`** — 보안 가이드 (배포 체크리스트, 유출 시 대응)
- 🚫 **`.gitignore`**, **`.env.example`** — 시크릿 보호

### Changed
- `Tool` 데이터클래스에 `prompt_file`, `needs_data_fetch` 필드 추가
- `Tool.get_prompt()` 메서드 (외부 파일 우선, fallback to 내장)

---

## [0.0.4] — 2026-04-26

### Added
- 🎨 **새 메인 화면 디자인** — 에디토리얼 미니멀
  - 256-color 브랜드 팔레트 (purple, peach, soft cyan, slate)
  - 섹션 마커 (▌)
  - 백엔드 상태 dots (●)
- 🧠 **사고 도구 9종 추가** (Steel-manning + 9개 = 총 10종):
  - Devil's Advocate, Pre-mortem, 6 Hats, Inversion, 5 Whys
  - Decision Matrix, First Principles, OODA Loop, Toulmin Model
- 💼 **도메인 컨설턴트 카테고리 신설** + 3개 도구:
  - Career (이직), Investment (투자), Education (자녀 교육)
- 메뉴 자동 생성 (`TOOLS` 리스트에서)
- 카테고리별 메뉴 분리 표시

### Changed
- `STEELMAN_PROMPT` → `Tool` 데이터클래스로 일반화
- `steelman_flow` → `tool_flow(config, tool)` 일반화

---

## [0.0.3] — 2026-04-26

### Added
- 🔌 **백엔드 5종 통합**:
  - `MLXBackend`, `OllamaBackend` (OpenAI-호환 HTTP, 공통 베이스 클래스)
  - 모델 자동 감지 (`/v1/models` 호출)
- Windows 분기 저장 경로 (`~/Documents/sukgo/sessions`)
- `_OpenAICompatBackend` 공통 베이스 (코드 중복 제거)

### Changed
- 백엔드 우선순위 전략 명문화 (claude > codex > gemini > MLX > ollama)
- MVP 시연 = Claude/ChatGPT 사용 장면 우선

---

## [0.0.2] — 2026-04-26

### Added
- 🤖 **복수 백엔드 등록** + **비교 모드 (원탁)**:
  - 같은 주제를 여러 AI에 동시 호출
  - 한 마크다운 파일에 통합 저장
- 첫 실행 마법사 (`first_run_setup`) — 1분 설정
- 옵시디언 자동 저장 + frontmatter
- 설정 변경 메뉴 (`s`)
- `parse_indices` — 복수 선택 입력 파싱 (`1,2,3` / `all`)
- `migrate_config` — 단일 backend → 복수 backends 자동 변환
- Codex CLI 호출 수정:
  - `--skip-git-repo-check`
  - `-o <FILE>` (깨끗한 출력)
  - `stdin=subprocess.DEVNULL`

### Changed
- `config["backend"]` → `config["backends"]` (리스트)
- 메인 메뉴 하단에 등록 백엔드 표시

---

## [0.0.1] — 2026-04-26

### Added
- 🎯 첫 PoC — Claude CLI subprocess + Steel-manning 도구 1개
- ASCII 첫 화면 (sukgo + 결정의 기술 + made by 배움의 달인 ✨)
- 옵시디언 친화 마크다운 저장
- 설치: `chmod +x` + `~/.local/bin/sukgo` symlink
