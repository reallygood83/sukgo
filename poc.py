#!/usr/bin/env python3
"""
sukgo v0.0.2 — Multi-backend + Session Storage
검증된 사고 도구 + AI 코치 = 결정의 기술

made by 배움의 달인 ✨
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# ═════════════════════════════════════════════════════════════════════
# 상수
# ═════════════════════════════════════════════════════════════════════
VERSION = "0.0.7 PoC"
CONFIG_PATH = Path.home() / ".config" / "sukgo" / "config.json"

# OS별 기본 저장 위치 (Windows 사용자도 자연스럽게)
if sys.platform == "win32":
    DEFAULT_SAVE_PATH = Path.home() / "Documents" / "sukgo" / "sessions"
else:
    DEFAULT_SAVE_PATH = Path.home() / ".local" / "share" / "sukgo" / "sessions"

MLX_DEFAULT_URL = "http://localhost:8080/v1"
OLLAMA_DEFAULT_URL = "http://localhost:11434/v1"

# ═════════════════════════════════════════════════════════════════════
# ANSI 색상
# ═════════════════════════════════════════════════════════════════════
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
TEAL = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
GRAY = "\033[90m"
GREEN = "\033[32m"

# 256-color 브랜드 팔레트 (방향 A: 에디토리얼 미니멀)
PURPLE = "\033[38;5;141m"     # 브랜드 보라 (헤더 라인, 섹션 마커)
PEACH = "\033[38;5;215m"      # 따뜻한 강조 (메뉴 번호)
SOFT_CYAN = "\033[38;5;110m"  # 부드러운 강조 (비교 모드 화살표)
SLATE = "\033[38;5;245m"      # 차분한 회색 (얇은 구분선, 메타)

if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    RESET = BOLD = DIM = TEAL = YELLOW = RED = GRAY = GREEN = ""
    PURPLE = PEACH = SOFT_CYAN = SLATE = ""


# ═════════════════════════════════════════════════════════════════════
# 사고 도구 정의 (10종)
# ═════════════════════════════════════════════════════════════════════
def load_prompt_file(filename: str) -> Optional[str]:
    """prompts/ 폴더에서 프롬프트 파일 로드 (없으면 None)"""
    script_dir = Path(__file__).resolve().parent
    prompt_path = script_dir / "prompts" / filename
    if prompt_path.exists():
        try:
            return prompt_path.read_text(encoding="utf-8")
        except Exception:
            return None
    return None


@dataclass
class Tool:
    key: str          # 메뉴 단축키
    name: str         # 도구 이름 (영문)
    emoji: str        # 시각 식별자
    short_desc: str   # 한 줄 설명
    save_id: str      # 파일명용 식별자
    prompt: str       # 프롬프트 템플릿 ({topic} 포함)
    category: str = "thinking"  # "thinking" (사고 도구) / "domain" (도메인 컨설턴트)
    prompt_file: str = ""  # prompts/ 폴더 파일명 (있으면 우선 사용)
    needs_data_fetch: bool = False  # 데이터 페처 사용 여부 (Investment 등)

    def get_prompt(self) -> str:
        """프롬프트 반환 (외부 파일 우선, 없으면 내장)"""
        if self.prompt_file:
            loaded = load_prompt_file(self.prompt_file)
            if loaded:
                return loaded
        return self.prompt


TOOLS = [
    Tool(
        key="1",
        name="Steel-manning",
        emoji="🛡",
        short_desc="가장 강한 반대 논리 만들기",
        save_id="steelman",
        prompt="""당신은 전문 토론 코치이며 비판적 사고의 대가입니다.
사용자가 가진 입장/주장에 대해, 가장 강력한 반대 논거(Steel-man)를 만들어주세요.

**사용자 입장**: {topic}

다음 구조로 한국어로 답변해주세요:

## 🛡 가장 강력한 반대 논거 3가지

각 논거마다:
- **핵심 주장**: 한 문장으로 명확하게
- **근거**: 데이터·논리·사례 (가능하면 실제 인물·연구 인용)
- **이게 왜 진짜 위협적인가**: 흔한 약한 반박이 아닌, 정말 강한 반박인 이유

## 🎯 사용자가 답해야 할 핵심 질문 3가지

이 반대 논거들에 대응하기 위해 사용자가 미리 준비해야 할 질문.

## 📊 종합 평가
- **사용자 입장의 견고함**: 1~10점
- **가장 큰 약점**: 한 줄
- **보강 제안**: 한 줄 (사용자 입장을 더 강하게 만드는 방향)""",
    ),

    Tool(
        key="2",
        name="Devil's Advocate",
        emoji="🥊",
        short_desc="일부러 반대 입장 펴기 (회의·확증편향 차단)",
        save_id="devil",
        prompt="""당신은 영리하고 공격적인 Devil's Advocate(악마의 변호인)입니다.
사용자의 입장을 강력하게 공격하세요. 단순한 트집이 아닌, 진짜 약점만 찌르세요.

**사용자 입장**: {topic}

다음 구조로 한국어로 답변해주세요:

## 🥊 5가지 공격

각 공격마다:
- **공격 포인트**: 한 문장 (날카롭게)
- **왜 이게 약점인가**: 구체적 근거·사례
- **사용자가 덮으려는 진실**: 의도적/무의식적으로 회피하는 사실

## 💀 가장 위험한 단일 공격

5개 중 가장 치명적인 1개를 선정하고, 왜 가장 위험한지 설명.

## 🎯 답변 못 할 경우의 결과

이 공격에 사용자가 답변하지 못하면 어떤 결과가 나올지 (미래 시나리오 1개).

## 📊 종합 평가
- **사용자 입장의 방어 가능성**: 1~10점
- **가장 큰 사각지대**: 한 줄
- **즉시 보강해야 할 것**: 한 줄

답변은 직설적이고 도전적으로. 사용자를 보호하지 말고, 가장 강한 공격을 하세요.""",
    ),

    Tool(
        key="3",
        name="Pre-mortem",
        emoji="⚰",
        short_desc="실패 시뮬레이션 (Gary Klein, HBR)",
        save_id="premortem",
        prompt="""당신은 의사결정 분석 전문가입니다. Gary Klein의 Pre-mortem 기법으로 분석해주세요.

**사용자 계획/결정**: {topic}

핵심 가정: **이 결정이 1년 후 명백한 실패로 판명되었습니다.** 부고를 쓰는 심정으로 분석하세요.

다음 구조로 한국어로 답변해주세요:

## ⚰ 1년 후의 실패 시나리오

실패한 미래의 모습을 구체적 스토리텔링으로 그려주세요 (3~5문장).

## 🔍 가장 가능성 높은 5가지 실패 원인

각 원인마다:
- **원인**: 한 문장
- **메커니즘**: 어떻게 이게 실패로 이어지는지 (인과 사슬)
- **사전 신호**: 이 원인이 발현되기 전 보일 신호

## 🛡 사전 차단 전략

각 실패 원인에 대한 구체적 예방·완화 액션 (5개, 즉시 실행 가능한 형태).

## 📊 종합 평가
- **현재 계획의 실패 위험도**: 1~10점 (10이 가장 위험)
- **가장 치명적인 단일 원인**: 한 줄
- **계획 보강 우선순위 1번**: 한 줄

답변은 분석적이고 구체적으로.""",
    ),

    Tool(
        key="4",
        name="6 Hats",
        emoji="🎩",
        short_desc="6가지 관점 (Edward de Bono)",
        save_id="6hats",
        prompt="""당신은 Edward de Bono의 6색 모자(Six Thinking Hats) 기법 전문가입니다.
주제를 6가지 색의 모자 관점에서 차례로 분석해주세요.

**주제**: {topic}

다음 구조로 한국어로 답변하되, 각 모자별로 그 관점에 완전히 몰입해서 작성하세요:

## ⚪ 흰 모자 — 사실과 데이터
객관적 사실, 숫자, 검증 가능한 정보. (감정·의견 제외)

## 🔴 빨간 모자 — 감정과 직관
이 주제에 대한 감정적 반응, 직관, 본능적 느낌. (논리 정당화 안 해도 됨)

## ⚫ 검은 모자 — 비판과 위험
약점, 위험, 함정, 부정적 결과. (가장 까다롭게)

## 🟡 노란 모자 — 긍정과 이익
강점, 기회, 가치, 긍정적 결과. (가장 낙관적으로)

## 🟢 초록 모자 — 창의와 대안
새로운 아이디어, 대안, 창의적 가능성. (제약 없이)

## 🔵 파란 모자 — 메타·통제
앞 5개 관점을 종합한 결론. 다음 단계는 무엇? 가장 중요한 통찰은?

각 모자는 3~5문장으로 충분.""",
    ),

    Tool(
        key="5",
        name="Inversion",
        emoji="🔄",
        short_desc="거꾸로 생각하기 (Charlie Munger)",
        save_id="inversion",
        prompt="""당신은 Charlie Munger의 Inversion(역발상) 사고 전문가입니다.
사용자가 원하는 결과의 *반대*에 집중해서 분석하세요.

**사용자 목표/주제**: {topic}

다음 구조로 한국어로 답변해주세요:

## 🔄 거꾸로 질문

사용자의 목표를 뒤집어 다시 정의하세요.
예: "성공하려면?" → "확실히 실패하려면?"

## 💣 확실히 망하는 5가지 방법

이 목표를 *확실히 실패*시키려면 무엇을 해야 하는가? (5가지, 구체적으로)
각 방법마다:
- **행동**: 무엇을 한다
- **왜 망하는가**: 인과

## 🛡 그래서 피해야 할 것 (대응)

위 5가지의 정반대 = 사용자가 *반드시 피해야 할* 행동. 구체적 가이드.

## 💎 거꾸로 봐서 발견한 통찰

정방향 사고로는 안 보였던, 역발상으로만 보이는 통찰 1~2개.

## 📊 종합 평가
- **현재 계획에서 가장 위험한 행동**: 한 줄
- **즉시 멈춰야 할 것**: 한 줄
- **새로 시작해야 할 것**: 한 줄

답변은 명확하고 도발적으로.""",
    ),

    Tool(
        key="6",
        name="5 Whys",
        emoji="❓",
        short_desc="근본 원인 5단계 추적 (Toyota)",
        save_id="5whys",
        prompt="""당신은 Toyota의 5 Whys 분석 전문가입니다.
사용자가 제시한 문제·현상의 진짜 근본 원인을 5단계로 추적해주세요.

**문제·현상**: {topic}

다음 구조로 한국어로 답변해주세요:

## ❓ Why 1 — 표면적 원인
**질문**: 왜 [문제]가 발생하는가?
**답**: [표면적으로 보이는 원인]
**검증**: 이 답이 정말 충분한 설명인가? (반대 사례·예외 점검)

## ❓ Why 2 — 한 층 더 깊이
**질문**: 왜 [Why 1의 답]이 발생하는가?
**답**: [더 깊은 원인]
**검증**: ...

## ❓ Why 3
(같은 형식)

## ❓ Why 4
(같은 형식)

## ❓ Why 5 — 진짜 근본 원인
**질문**: 왜 [Why 4의 답]이 발생하는가?
**답**: [근본 원인 — 시스템/구조/문화 차원]
**검증**: 이게 정말 가장 깊은 층인가?

## 💎 발견한 진짜 원인

5단계 추적의 결론. **표면 원인과 근본 원인의 차이**를 명확하게 대비.

## 🎯 근본 원인 해결 액션

근본 원인을 다루는 구체적 행동 3가지 (표면 처방이 아니라).

답변은 분석적이고 끈질기게. 쉬운 답에서 멈추지 마세요.""",
    ),

    Tool(
        key="7",
        name="Decision Matrix",
        emoji="⚖",
        short_desc="옵션 × 기준 가중치 비교",
        save_id="matrix",
        prompt="""당신은 의사결정 분석 전문가입니다.
사용자가 고민 중인 선택지들을 가중치 기반으로 비교해주세요.

**의사결정 주제**: {topic}

(만약 옵션이 명시되지 않았다면, 가장 그럴듯한 옵션 2~4개를 추론해서 분석하세요.)

다음 구조로 한국어로 답변해주세요:

## 🎯 식별한 옵션
이 결정에서 비교할 선택지 (2~4개), 각각 한 줄 설명.

## 📋 평가 기준 (가중치 포함)

이 결정에 중요한 평가 기준 5~7개를 제시하고, 각각 가중치(1~10) 부여:
- **기준명** (가중치 N): 왜 이 가중치인지 짧게

## 📊 평가 매트릭스

각 옵션 × 각 기준에 대해 점수(1~10)를 매겨주세요. 표 형식으로:

| 기준 (가중치) | 옵션 A | 옵션 B | ... |
|---|---|---|---|
| 기준1 (8) | 7 | 9 | ... |
| ... | ... | ... | ... |
| **가중 총점** | **N.N** | **N.N** | **...** |

각 점수 옆에 짧은 근거 (한 줄).

## 💎 권고

- **점수 1위 옵션과 그 이유**: 정량적 + 정성적 양쪽
- **점수에 잡히지 않는 위험**: 매트릭스가 놓칠 수 있는 것
- **사용자가 추가로 답해야 할 결정적 질문 1개**

## ⚠ 주의

이 분석에서 사용자의 가치관·가중치가 다를 수 있는 부분을 명시.""",
    ),

    Tool(
        key="8",
        name="First Principles",
        emoji="🧬",
        short_desc="기본 원리부터 다시 (Aristotle, Musk)",
        save_id="principles",
        prompt="""당신은 First Principles(제1원리) 사고 전문가입니다.
유추(analogy)와 관습을 모두 제거하고, 본질에서부터 재구성하세요.

**주제**: {topic}

다음 구조로 한국어로 답변해주세요:

## 🧬 현재 가정 분해

이 주제에 대해 사람들이 (그리고 사용자가) 무의식적으로 받아들이는 가정 5가지.
각 가정마다 "이게 정말 사실인가?" 검증.

## 🔬 진짜 기본 원리

이 주제의 진짜 본질·기본 원리는 무엇인가? (물리학·논리·인간 본성·경제 등 가장 기초적인 층)
3~5개 항목으로.

## 🏗 본질로부터 재구성

위 기본 원리만으로 이 주제/문제를 처음부터 다시 설계한다면 어떤 모습일까?
관습·유추를 모두 버리고, 가장 본질적인 답.

## 💡 발견한 새로운 가능성

기본 원리부터 봤을 때 비로소 보이는, 기존 사고로는 안 보였던 가능성·해결책.

## 📊 종합 평가
- **사용자가 가장 의심해야 할 가정**: 한 줄
- **재구성으로 얻는 가장 큰 이점**: 한 줄
- **다음 단계 액션**: 한 줄

답변은 깊이 있고 도전적으로. 표면적 답에 머물지 마세요.""",
    ),

    Tool(
        key="9",
        name="OODA Loop",
        emoji="🌊",
        short_desc="관찰→정황→결정→행동 (John Boyd)",
        save_id="ooda",
        prompt="""당신은 John Boyd의 OODA Loop(관찰-정황판단-결정-행동) 전문가입니다.
빠른 의사결정이 필요한 상황을 4단계로 분석하세요.

**상황**: {topic}

다음 구조로 한국어로 답변해주세요:

## 👁 Observe — 관찰

지금 이 상황에서 객관적으로 관찰 가능한 사실들 (5~7개).
- 데이터·신호·외부 환경 변화·이해관계자 행동
- 감정·해석·예측은 제외

## 🧠 Orient — 정황 판단

관찰한 사실들이 *무엇을 의미하는가?* 사용자의 맥락에서 해석:
- **현재 위치**: 사용자는 어디에 있나?
- **기회와 위협**: 무엇이 보이나?
- **블라인드 스팟**: 사용자가 놓치고 있을 만한 것?

## ⚡ Decide — 결정

가능한 행동 옵션 3가지를 제시하고, 각각의:
- **장점·단점**
- **리스크·기댓값**
- **실행 난이도**

→ 가장 추천하는 1개를 선정 + 이유.

## 🚀 Act — 행동

추천한 결정을 *지금 당장* 실행할 수 있는 형태로:
- **첫 24시간 안에 할 일**
- **첫 1주 안에 할 일**
- **체크포인트**: 결정이 옳았는지 검증할 신호

## 🔄 Loop — 반복

이 행동 후 다시 OODA를 돌려야 할 시점·트리거.

답변은 빠르고 실행 중심으로.""",
    ),

    Tool(
        key="0",
        name="Toulmin Model",
        emoji="🎯",
        short_desc="논증 5요소 분석 (Stephen Toulmin)",
        save_id="toulmin",
        category="thinking",
        prompt="""당신은 Stephen Toulmin의 논증 모델 전문가입니다.
사용자의 주장을 5요소(Claim-Data-Warrant-Backing-Rebuttal-Qualifier)로 해부하고 강화하세요.

**사용자 주장**: {topic}

다음 구조로 한국어로 답변해주세요:

## 🎯 Claim — 주장

사용자 주장을 한 문장으로 명료하게 재진술. (모호한 부분이 있다면 가장 합리적 해석)

## 📊 Data — 근거

이 주장을 뒷받침하는 사실·데이터·예시는 무엇인가?
- 사용자가 명시한 근거 정리
- 빠진 근거 보완 (가능한 데이터 추정)
- **근거의 강도**: 1~10점

## 🌉 Warrant — 보강 (논리 다리)

근거에서 주장으로 가는 논리적 연결 고리는 무엇인가?
"왜 이 근거가 이 주장을 지지하는가?"의 답.
- **명시적 보강**: 사용자가 가정하는 것
- **숨은 보강**: 무의식적으로 의존하는 것

## 📚 Backing — 보강의 보강

Warrant를 뒷받침하는 더 깊은 권위·이론·원칙. (학술 연구·법·역사·통념 등)

## ⚠ Rebuttal — 가능한 반박

이 주장에 대한 가장 강한 반박 시나리오 3가지. 각각:
- 반박의 핵심
- 사용자가 어떻게 대응할 수 있는지

## 🔧 Qualifier — 한정·조건

이 주장이 *항상* 맞는가? *어떤 조건에서* 맞는가?
강도 부사 추가: "거의 모든 경우" / "대부분" / "특정 조건에서" 등.

## 💎 종합 진단
- **논증의 가장 약한 고리**: 한 줄
- **즉시 강화해야 할 부분**: 한 줄
- **이 주장을 더 설득력 있게 만들 한 가지 변경**: 한 줄

답변은 분석적이고 구조적으로.""",
    ),

    # ═════════════════════════════════════════════════════════════════
    # 도메인 컨설턴트 (특정 영역 전문 분석)
    # ═════════════════════════════════════════════════════════════════
    Tool(
        key="c",
        name="Career",
        emoji="💼",
        short_desc="이직·커리어 결정 (정량+정성 분석)",
        save_id="career",
        category="domain",
        prompt="""당신은 시니어 커리어 코치이자 노동시장 분석가입니다.
사용자의 커리어 결정을 정량 + 정성 데이터로 객관적으로 분석해주세요.

**상황**: {topic}

⚠ 모르는 데이터(특정 회사 연봉 등)는 "확인 필요"라고 정직하게 명시하세요. 추측으로 메우지 마세요.

다음 구조로 한국어로 답변해주세요:

## 📊 정량 분석

가능한 한 숫자로 비교:
- **연봉 변화**: 현재 vs 옵션 (5년 누적 + 기회비용 포함)
- **시장가치 변화**: 이력서 무게감, 다음 이직 시 협상력
- **시간 비용**: 출퇴근, 야근, 학습 시간
- **성장 기회 정량화**: 책임 범위, 의사결정 권한, 신기술 노출

## 🧠 정성 분석

수치화 안 되는 결정적 요소:
- **비전 적합도**: 5년 후 본인이 원하는 모습과의 거리
- **조직 문화 리스크**: 경영진·동료·정치·번아웃 가능성
- **본인 가치관 부합**: 무엇이 안 맞을 위험?

## 🔮 5년 후 시나리오

각 옵션 선택 시 5년 후 모습을 *구체적 스토리*로:
- **옵션 A 선택 시**: ...
- **옵션 B 선택 시**: ...
- **(있다면) 옵션 C**: ...

## 💸 기회비용

한 옵션을 선택할 때 *포기*하는 것을 명시 (양쪽 모두).
사람들이 흔히 놓치는 숨은 기회비용 포함.

## 🎯 결정 가이드

- **후회 최소화 관점 추천**: "10년 뒤 더 후회할 결정은?"
- **리스크 평가**: 각 옵션의 다운사이드 + 회복 가능성
- **결정 전 추가 확인할 5가지**: 즉시 가능한 정보 수집 액션

## 📊 종합 평가

- **추천 선택지**: A / B / 더 정보 필요 (추천 이유 한 줄)
- **신뢰도**: 1~10점 (현재 정보로 결정할 수 있는지)
- **결정 전 답해야 할 핵심 질문 1개**: 가장 중요한 것 하나

답변은 객관적이고 분석적으로. 사용자를 격려하지 말고, 정직한 데이터를 보여주세요.""",
    ),

    Tool(
        key="i",
        name="Investment",
        emoji="📈",
        short_desc="주식 9섹션 분석 (yfinance·FDR 데이터 자동 수집)",
        save_id="investment",
        category="domain",
        prompt_file="investment.md",
        needs_data_fetch=True,
        prompt="""당신은 정량 분석 중심의 투자 리서치 전문가입니다.
주식·투자 결정을 객관적 데이터로 분석해주세요.

⚠⚠⚠ **이 분석은 교육·참고용이며, 투자 자문이 아닙니다.**
⚠ 실시간 데이터(현재가, PER 등)는 사용자가 추가 입력하지 않은 한 정확하지 않을 수 있습니다.
⚠ 모르는 데이터는 추측하지 말고 "확인 필요"로 명시하세요.

**투자 검토 대상**: {topic}

다음 구조로 한국어로 답변해주세요:

## 📈 펀더멘털 점검

(알려진 일반 정보 한도 + 일반적 분석 프레임워크)
- **재무 지표**: PER, PBR, ROE, 부채비율 등 (모르면 "확인 필요")
- **밸류에이션**: 저평가/적정/고평가 (역사적·동종업계 대비)
- **성장률**: 매출·이익 성장률 트렌드
- **수익성**: 마진율, 현금흐름 품질

## 📊 시장 환경

- **섹터 모먼텀**: 해당 산업의 사이클 위치
- **거시 환경 영향**: 금리·환율·경기·정책
- **경쟁사 비교**: 동종 업계에서의 위치 (1위? 추격자? 한계?)

## 🎯 진입 시나리오

3가지 액션별 가이드:
- **매수**: 어떤 가격대, 분할매수 비중 전략
- **홀드**: 보유 시 모니터링할 지표 (분기 실적·뉴스 등)
- **관망**: 어떤 신호가 나오면 진입 검토

## ⚠ 다운사이드 리스크

- **가장 큰 위험 3가지**: 펀더멘털·산업·매크로 각 1개
- **손절 기준 제안**: 가격 -X% 또는 펀더멘털 변화 트리거
- **최악 시나리오 손실 추정**: 베어 케이스에서 -%

## 🧠 행동 편향 점검

사용자가 빠질 수 있는 편향:
- **FOMO**: 다른 사람 수익 보고 들어가는가?
- **확증 편향**: 매수 근거만 찾고 있는가?
- **손실 회피**: 이미 물려서 평단 낮추려는가?
- **자기 점검 질문 3개**

## 📊 종합 평가

- **현재 시점 매력도**: 1~10점
- **추천 액션**: 매수 / 분할매수 / 홀드 / 관망 / 회피 (이유 한 줄)
- **결정 전 확인할 데이터 3가지**: 사용자가 직접 검색·확인할 항목
- **포지션 사이즈 가이드**: 전체 포트폴리오에서 비중 권고 (%)

---

⚠ **면책 재강조**: 이 분석은 사고 보조 도구입니다. 실제 투자는 본인 판단·책임이며, 추가 리서치(공시·증권사 리포트·전문가 자문)가 필요합니다.

답변은 객관적이고 분석적으로. 절대 "사야 한다/팔아야 한다" 단정하지 말고, 가능성과 리스크를 균형 있게.""",
    ),

    Tool(
        key="e",
        name="Education",
        emoji="👶",
        short_desc="자녀 교육 고민 (발달학+연구 기반)",
        save_id="education",
        category="domain",
        prompt="""당신은 아동 발달 전문가이자 교육 연구 메타 분석가입니다.
부모의 자녀 교육 고민을 발달학·교육학 연구를 기반으로 답변해주세요.

⚠ 인용하는 연구·학자는 가능한 한 실제로 검증 가능한 것만. 추측 인용은 "관련 연구가 있다는 일반적 통념"으로 명시.
⚠ 자녀 개인의 특성·맥락은 알 수 없으므로 일반 가이드 + 적용 시 고려사항을 함께 제시.

**고민**: {topic}

다음 구조로 한국어로 답변해주세요:

## 🧒 발달 단계 점검

- **추정 연령** (명시되지 않았다면 추론):
- **해당 연령의 발달 특성**: 인지·정서·사회·신체 4영역
- **이 고민이 발달 단계에 적합한가?**: 너무 이른가/늦었나/적절한가

## 📚 검증된 연구 (Evidence-based)

이 주제에 대한 신뢰도 높은 연구:
- **메타 분석/장기 종단 연구 우선** (가능한 경우 연구자명·연도)
- **연구 결과의 한계도 명시** (어떤 모집단에 적용되는지)
- **상반된 연구 결과**가 있다면 함께 제시 (단일 견해 강요 X)

## 🇰🇷 한국 맥락 고려

- **한국 교육 현실**: 입시·사교육·학교 시스템 특수성
- **글로벌 권고와 한국 현실의 갭**: 이상과 현실 사이
- **부모가 마주할 사회적 압력**: 또래 부모, 학원 마케팅, 친척

## ⚖ 장기 vs 단기 효과

- **단기 효과** (1~2년): 즉시 보이는 결과
- **장기 효과** (5~20년): 인생 전체에 미치는 영향
- **장기적으로 후회할 만한 단기 결정?**: 흔한 함정

## 💞 부모-자녀 관계 영향

이 결정이 관계에 미칠 영향. (지식보다 관계가 우선이라는 연구 다수)
- **단기 갈등 가능성**:
- **장기 신뢰 영향**:

## 🚫 피해야 할 함정

이 영역에서 부모들이 흔히 빠지는 함정 3가지:
1.
2.
3.

## 📊 종합 평가

- **권장 방향**: (구체적 액션 1~2개)
- **즉시 멈춰야 할 것**: 있다면 한 줄
- **다음 1년 가이드**: 발달 단계별 권고
- **자녀에게 직접 물어볼 만한 질문 1개**: 부모가 못 보는 것을 보기 위해

답변은 따뜻하지만 단호하게. 유행·대세보다 검증된 연구와 자녀 개인성을 우선.
부모 죄책감 자극 X. 객관적 정보 + 합리적 선택지 제공.""",
    ),
]


def get_tool(key: str) -> Optional[Tool]:
    for t in TOOLS:
        if t.key == key:
            return t
    return None


# ═════════════════════════════════════════════════════════════════════
# 협업 모드 — 다중 백엔드 협력 패턴
# ═════════════════════════════════════════════════════════════════════
PERSONAS = {
    "claude":  ("🧙", "현자", "신중·학술적·위험 우선. 역사 사례·연구 인용. 보수적 균형."),
    "codex":   ("🚀", "모험가", "도전·기회·모멘텀 중심. 시장 트렌드 강조. 적극적 진취."),
    "gemini":  ("📊", "분석가", "데이터·통계·정량 중심. 객관성 우선. 비교·벤치마크 능숙."),
    "mlx":     ("🧘", "회의주의자", "모든 가정 의심. 본질부터 재구성. First Principles 사고."),
    "ollama":  ("💎", "실용가", "즉시 실행 가능한 답. 액션 중심. 단순·명확."),
}


def get_persona(backend_name: str) -> tuple:
    """백엔드 → (이모지, 이름, 설명) 페르소나 반환"""
    return PERSONAS.get(backend_name, ("🤖", "분석가", "객관적 관점."))


def select_mode(num_backends: int) -> str:
    """다중 백엔드 선택 시 협업 모드 결정"""
    if num_backends <= 1:
        return "single"

    print(f"\n  {DIM}협업 모드 선택:{RESET}\n")
    print(f"    {BOLD}{PEACH}c{RESET}   {TEAL}비교{RESET}     각 AI 독립 답변 → 통합 저장        {DIM}(기본 · 빠름){RESET}")
    print(f"    {BOLD}{PEACH}s{RESET}   {TEAL}종합{RESET}     비교 + 한 AI가 합의·이견·권고 종합  {DIM}(+30초){RESET}")
    print(f"    {BOLD}{PEACH}d{RESET}   {TEAL}원탁{RESET}     {YELLOW}🏛{RESET} 페르소나 토론(2R) + 최종 합의   {DIM}(+3~5분){RESET}")

    while True:
        choice = input(f"\n  {BOLD}모드 [{PEACH}c{RESET}{BOLD}=비교]:{RESET} ").strip().lower()
        if not choice or choice in ("c", "compare", "비교"):
            return "compare"
        if choice in ("s", "synth", "synthesis", "종합"):
            return "synthesis"
        if choice in ("d", "debate", "원탁", "토론"):
            return "debate"
        print(f"  {RED}c / s / d 중 선택하세요.{RESET}")


def _format_responses_for_synth(responses: dict) -> str:
    """종합 모드용 — 다른 AI 응답들을 종합 prompt에 포함시킬 형식"""
    parts = []
    for name, resp in responses.items():
        parts.append(f"## 🤖 {name}\n\n{resp}\n")
    return "\n---\n\n".join(parts)


def _format_others_for_debate(others: dict) -> str:
    """원탁 Round 2용 — 다른 페르소나들의 의견 포맷"""
    parts = []
    for name, resp in others.items():
        emoji, persona_name, _ = get_persona(name)
        parts.append(f"### {emoji} {persona_name} ({name})\n\n{resp}\n")
    return "\n".join(parts)


def _format_full_history(history: dict) -> str:
    """원탁 최종 종합용 — 전체 히스토리 포맷"""
    parts = []
    for name, rounds in history.items():
        emoji, persona_name, _ = get_persona(name)
        parts.append(f"## {emoji} {persona_name} ({name})\n")
        for i, resp in enumerate(rounds, 1):
            parts.append(f"### Round {i}\n{resp}\n")
    return "\n".join(parts)


SYNTHESIS_PROMPT = """다음은 동일한 주제에 대한 {n}개 AI의 분석 결과입니다.

**원래 주제**: {topic}

{responses}

---

위 분석들을 바탕으로 다음을 한국어로 종합해주세요:

## ✅ 공통 합의점
모든 AI가 동의하는 핵심 포인트 (3~5개, 한 줄씩)

## ⚠ 이견 영역
AI들 사이에서 의견이 갈리는 지점 + 왜 갈리는지 (2~3개)

## 💎 종합 권고
사용자에게 가장 가치 있는 종합 결론 (가장 강한 인사이트 + 균형 있는 추천)

## 🎯 사용자가 추가로 답해야 할 핵심 질문
이 분석들로도 답이 안 나오는, 사용자만 답할 수 있는 질문 (1~3개)

답변은 명확하고 구조적으로, 마크다운 헤더(##) 그대로 사용해주세요."""


DEBATE_R1_PROMPT = """당신은 **{emoji} {persona_name}** 입니다.
페르소나: {persona_desc}

---

## 의안
{topic}

## 분석 프레임워크 (참고)
{base_prompt}

---

당신의 페르소나에 충실하게, 위 의안에 대한 핵심 의견을 5~8문장으로 명확하게 표현하세요.

이후 다른 페르소나들도 같은 의안에 답할 것이며, Round 2에서 서로 검토합니다.
당신의 관점만 진솔하게 — 균형 잡으려 하지 말고 페르소나 정체성에 충실하세요."""


DEBATE_R2_PROMPT = """당신은 **{emoji} {persona_name}** 입니다.
페르소나: {persona_desc}

---

## 의안
{topic}

## 당신의 Round 1 의견
{my_opinion}

## 다른 페르소나들의 Round 1 의견
{others}

---

다음 구조로 답변해주세요:

## 🤝 동의하는 점
다른 페르소나 의견에서 동의하는 부분 + 그 이유 (1~2개)

## ⚔ 반박하는 점
다른 페르소나 의견에서 동의하기 어려운 부분 + 근거 (1~2개)

## 🔄 입장 정교화
위 두 가지를 바탕으로 당신의 입장을 어떻게 더 명확히 할 것인가

5~8문장 이내로. 당신의 페르소나 정체성을 유지하면서."""


DEBATE_FINAL_PROMPT = """## 의안
{topic}

## 원탁 회의 전체 기록
{n}명의 페르소나가 2 라운드 토론했습니다.

{history}

---

이 토론을 바탕으로 사용자에게 도움이 될 최종 정리를 한국어로 작성해주세요:

## ✅ 합의된 결론
모든 페르소나가 동의하는 점 (이견 없는 영역)

## ⚠ 끝까지 갈린 의견
평행선으로 남은 영역 + 사용자가 직접 판단해야 할 차원

## 💎 사용자에게 권고하는 최종 결정
종합 결론 + 즉시 실행 가능한 다음 액션 (1~3개)

## 🎯 사용자가 자문해야 할 마지막 질문
이 결정을 자신 있게 하기 위해 사용자가 자기 자신에게 물어야 할 핵심 질문 1개

답변은 명확하고 실행 중심으로, 마크다운 헤더(##) 그대로."""


# ═════════════════════════════════════════════════════════════════════
# 백엔드
# ═════════════════════════════════════════════════════════════════════
class Backend:
    name: str = ""
    description: str = ""

    def is_available(self) -> bool:
        raise NotImplementedError

    def chat(self, prompt: str) -> Optional[str]:
        raise NotImplementedError


class ClaudeBackend(Backend):
    name = "claude"
    description = "Claude Pro/Max 구독 (claude CLI)"

    def is_available(self) -> bool:
        return shutil.which("claude") is not None

    def chat(self, prompt: str) -> Optional[str]:
        # ⚠ 중요: 도구 사용 완전 차단 (텍스트만 응답)
        #   - --tools ""        : 모든 빌트인 도구 차단
        #   - --disallowed-tools "mcp__*" : 사용자 MCP 서버 도구 전부 차단
        #   사용자 글로벌 ~/.claude/CLAUDE.md 의 명령(예: /trading-ideas)이
        #   자동 로드되어 mcp__filesystem__write_file 같은 MCP 도구로
        #   파일을 저장하려고 시도하는 문제 방지.
        try:
            r = subprocess.run(
                [
                    "claude", "-p", prompt,
                    "--output-format", "json",
                    "--tools", "",
                    "--disallowed-tools", "mcp__*",
                ],
                capture_output=True, text=True, timeout=180,
                stdin=subprocess.DEVNULL,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"  {RED}❌ claude 호출 실패: {e}{RESET}")
            return None
        if r.returncode != 0:
            print(f"  {RED}❌ claude 오류:{RESET} {DIM}{r.stderr[:300]}{RESET}")
            return None
        try:
            return json.loads(r.stdout).get("result") or r.stdout
        except json.JSONDecodeError:
            return r.stdout


class CodexBackend(Backend):
    name = "codex"
    description = "ChatGPT Plus 구독 (codex CLI)"

    def is_available(self) -> bool:
        return shutil.which("codex") is not None

    def chat(self, prompt: str) -> Optional[str]:
        # codex는 stdout에 진행 로그/이벤트를 같이 뱉으므로
        # `-o <FILE>`로 마지막 메시지만 깨끗하게 받음
        # 또한 stdin이 파이프면 codex가 읽으려 대기하므로 DEVNULL 필요
        # `--skip-git-repo-check`는 git 폴더 밖에서 실행 시 필수
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            output_file = f.name

        try:
            r = subprocess.run(
                [
                    "codex", "exec",
                    "--skip-git-repo-check",
                    "-o", output_file,
                    prompt,
                ],
                capture_output=True,
                text=True,
                timeout=180,
                stdin=subprocess.DEVNULL,
            )
            if r.returncode != 0:
                err = (r.stderr or r.stdout or "")[:400]
                print(f"  {RED}❌ codex 오류:{RESET} {DIM}{err}{RESET}")
                return None
            with open(output_file, "r", encoding="utf-8") as f:
                return f.read().strip()
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"  {RED}❌ codex 호출 실패: {e}{RESET}")
            return None
        finally:
            try:
                os.unlink(output_file)
            except OSError:
                pass


class GeminiBackend(Backend):
    name = "gemini"
    description = "Gemini CLI (무료 티어)"

    def is_available(self) -> bool:
        return shutil.which("gemini") is not None

    def chat(self, prompt: str) -> Optional[str]:
        # Gemini도 stdin 파이프를 입력으로 추가할 수 있어 DEVNULL 명시
        try:
            r = subprocess.run(
                ["gemini", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=180,
                stdin=subprocess.DEVNULL,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"  {RED}❌ gemini 호출 실패: {e}{RESET}")
            return None
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "")[:400]
            print(f"  {RED}❌ gemini 오류:{RESET} {DIM}{err}{RESET}")
            return None
        return r.stdout.strip()


class _OpenAICompatBackend(Backend):
    """OpenAI 호환 HTTP 엔드포인트 공통 베이스 (MLX·Ollama 등)"""

    fallback_model = "default"

    def __init__(self, url: str):
        self.url = url
        self._cached_model: Optional[str] = None

    def _detect_model(self) -> Optional[str]:
        """/v1/models 호출 → 첫 번째 모델 ID 자동 감지"""
        if self._cached_model:
            return self._cached_model
        try:
            with urllib.request.urlopen(f"{self.url}/models", timeout=2) as resp:
                data = json.loads(resp.read())
                models = data.get("data", [])
                if models:
                    self._cached_model = models[0].get("id", self.fallback_model)
                    return self._cached_model
        except (urllib.error.URLError, TimeoutError, ConnectionRefusedError, OSError, json.JSONDecodeError):
            pass
        return None

    def is_available(self) -> bool:
        return self._detect_model() is not None

    def chat(self, prompt: str) -> Optional[str]:
        model = self._detect_model() or self.fallback_model
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
            "temperature": 0.7,
        }
        try:
            req = urllib.request.Request(
                f"{self.url}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
                return data["choices"][0]["message"]["content"]
        except urllib.error.URLError as e:
            print(f"  {RED}❌ {self.name} 서버 연결 실패 ({self.url}): {e}{RESET}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"  {RED}❌ {self.name} 응답 파싱 실패: {e}{RESET}")
            return None


class MLXBackend(_OpenAICompatBackend):
    name = "mlx"
    description = "로컬 MLX 서버 (Apple Silicon, 가장 빠름)"

    def __init__(self, url: str = MLX_DEFAULT_URL):
        super().__init__(url)


class OllamaBackend(_OpenAICompatBackend):
    name = "ollama"
    description = "로컬 Ollama 서버 (Win/Mac/Linux 호환)"

    def __init__(self, url: str = OLLAMA_DEFAULT_URL):
        super().__init__(url)


ALL_BACKENDS = [
    ClaudeBackend(),
    CodexBackend(),
    GeminiBackend(),
    MLXBackend(),
    OllamaBackend(),
]


def get_backend(name: str) -> Optional[Backend]:
    for b in ALL_BACKENDS:
        if b.name == name:
            return b
    return None


def parse_indices(s: str, max_idx: int) -> list:
    """
    '1,2,3' 또는 '1 2 3' 또는 'all' → [1, 2, 3]
    잘못된 입력은 무시하고 유효한 것만 반환.
    """
    s = s.strip().lower()
    if s in ("a", "all", "*"):
        return list(range(1, max_idx + 1))
    parts = re.split(r"[,\s]+", s)
    result = []
    for p in parts:
        if not p:
            continue
        try:
            idx = int(p)
            if 1 <= idx <= max_idx and idx not in result:
                result.append(idx)
        except ValueError:
            continue
    return result


# ═════════════════════════════════════════════════════════════════════
# 설정
# ═════════════════════════════════════════════════════════════════════
def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_config(config: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False))


def first_run_setup() -> dict:
    """첫 실행 마법사 — 백엔드 + 저장 위치 설정"""
    clear()
    print(f"\n  {GRAY}{'═' * 56}{RESET}\n")
    print(f"                      {BOLD}s u k g o{RESET}")
    print(f"                    {DIM}결정의 기술{RESET}\n")
    print(f"  {GRAY}{'═' * 56}{RESET}\n")
    print(f"  {BOLD}처음 실행이시군요!{RESET} 1분 설정 후 시작합니다.\n")

    # ── 1/2. 백엔드 선택 ──
    print(f"  {TEAL}── 1/2. AI 백엔드 선택 ──{RESET}\n")
    statuses = [(i, b, b.is_available()) for i, b in enumerate(ALL_BACKENDS, 1)]
    print("  사용 가능한 AI:\n")
    for i, b, avail in statuses:
        if avail:
            print(f"    {BOLD}{i}.{RESET} {GREEN}✅{RESET} {b.name:8} {DIM}{b.description}{RESET}")
        else:
            extra = ""
            if b.name == "mlx":
                extra = f"  {DIM}(서버 미실행 — `mlx_lm.server`로 띄우면 사용 가능){RESET}"
            elif b.name == "ollama":
                extra = f"  {DIM}(서버 미실행 — `ollama serve`로 띄우면 사용 가능){RESET}"
            print(f"    {DIM}{i}. ❌ {b.name:8} {b.description}{RESET}{extra}")

    available_indices = [i for i, b, avail in statuses if avail]
    if not available_indices:
        print(f"\n  {RED}❌ 사용 가능한 백엔드가 없습니다.{RESET}")
        print(f"  {DIM}claude / codex / gemini 중 하나는 설치해주세요.{RESET}")
        sys.exit(1)

    print(f"\n  {DIM}💡 여러 개를 등록하면 비교 모드(원탁)도 사용 가능합니다.{RESET}")
    print(f"  {DIM}   입력 예:  1   |   1,2,3   |   all{RESET}")

    default_idx = available_indices[0]
    while True:
        choice = input(f"\n  {BOLD}사용할 AI 번호 [{default_idx}]:{RESET} ").strip()
        if not choice:
            indices = [default_idx]
            break
        indices = parse_indices(choice, len(ALL_BACKENDS))
        # 사용 가능한 것만 필터
        indices = [i for i in indices if i in available_indices]
        if indices:
            break
        print(f"  {RED}사용 가능한 번호를 1개 이상 선택하세요.{RESET}")

    selected_backends = [ALL_BACKENDS[i - 1] for i in indices]
    backend_names = [b.name for b in selected_backends]

    # ── 2/2. 저장 위치 ──
    print(f"\n  {TEAL}── 2/2. 세션 저장 위치 ──{RESET}\n")
    print(f"  Steel-manning 결과를 마크다운으로 자동 저장합니다.")
    print(f"  {BOLD}옵시디언 볼트 경로{RESET} 또는 원하는 폴더를 입력하세요.\n")
    print(f"  {DIM}예시:{RESET}")
    print(f"  {DIM}  ~/Documents/LearningMaster/000-Inbox    (옵시디언 볼트){RESET}")
    print(f"  {DIM}  ~/Desktop/sukgo-sessions                (테스트용){RESET}")
    print(f"  {DIM}  Enter 그대로 → 기본 ({DEFAULT_SAVE_PATH}){RESET}")

    while True:
        save_input = input(f"\n  {BOLD}저장 위치:{RESET} ").strip()
        if not save_input:
            save_path = DEFAULT_SAVE_PATH
            break
        save_path = Path(save_input).expanduser().resolve()
        if save_path.exists() or save_path.parent.exists():
            break
        confirm = input(f"  {YELLOW}부모 폴더가 없습니다. 새로 만들까요? [y/N]:{RESET} ").strip().lower()
        if confirm == "y":
            break

    save_path.mkdir(parents=True, exist_ok=True)

    config = {
        "backends": backend_names,
        "save_path": str(save_path),
        "mlx_url": MLX_DEFAULT_URL,
        "ollama_url": OLLAMA_DEFAULT_URL,
        "version": VERSION,
    }
    save_config(config)

    print(f"\n  {GREEN}✅ 설정 완료!{RESET}\n")
    print(f"  {DIM}백엔드:{RESET}    {TEAL}{', '.join(backend_names)}{RESET}")
    if len(backend_names) > 1:
        print(f"  {DIM}           → 복수 등록됨. 비교 모드 사용 가능 ✨{RESET}")
    print(f"  {DIM}저장 위치:{RESET}  {save_path}")
    print(f"  {DIM}설정 파일:{RESET}  {CONFIG_PATH}")
    input(f"\n  {DIM}Enter → 시작{RESET} ")
    return config


def migrate_config(config: dict) -> dict:
    """이전 버전 호환성 — 'backend' (단수) → 'backends' (복수)"""
    if "backend" in config and "backends" not in config:
        config["backends"] = [config.pop("backend")]
    return config


# ═════════════════════════════════════════════════════════════════════
# 세션 저장
# ═════════════════════════════════════════════════════════════════════
def save_session(
    save_dir: Path,
    tool: str,
    topic: str,
    responses: dict,  # {backend_name: response_text} or with __synthesis__/__debate_final__
    mode: str = "compare",  # single / compare / synthesis / debate
) -> Path:
    """
    세션을 옵시디언 친화 마크다운으로 저장 (모드별 다른 구조)
    """
    now = datetime.now()
    safe_topic = re.sub(r"[^\w가-힣\-]+", "_", topic)[:50].strip("_")

    # 특수 키 분리
    synthesis = responses.pop("__synthesis__", None)
    debate_final = responses.pop("__debate_final__", None)

    backend_names = list(responses.keys())
    suffix_map = {
        "single": backend_names[0] if backend_names else "single",
        "compare": "compare",
        "synthesis": "synthesis",
        "debate": "debate",
    }
    suffix = suffix_map.get(mode, mode)
    filename = f"{now:%Y-%m-%d_%H%M}_{tool}_{suffix}_{safe_topic}.md"
    filepath = save_dir / filename

    backends_yaml = "[" + ", ".join(backend_names) + "]"

    body = f"""---
tool: {tool}
topic: "{topic}"
backends: {backends_yaml}
mode: {mode}
created: {now.isoformat()}
tags:
  - sukgo
  - {tool}
  - {mode}
  - decision-thinking
---

# {tool}: {topic}

"""

    # 모드별 본문 구조
    if mode == "debate" and debate_final:
        body += "> 🏛 **원탁 토론** — 여러 페르소나가 2 라운드 토론한 결과.\n\n"
        body += "## 🎯 최종 합의 및 권고\n\n" + debate_final + "\n\n"
        body += "---\n\n# 📝 토론 전체 기록\n\n"
        for backend_name, full_text in responses.items():
            emoji, persona_name, _ = get_persona(backend_name)
            body += f"\n---\n\n## {emoji} {persona_name} ({backend_name})\n\n{full_text}\n"

    elif mode == "synthesis" and synthesis:
        body += f"> 🎯 **종합 모드** — {len(backend_names)}개 AI 비교 + 종합 권고.\n\n"
        body += "## 🎯 종합 권고\n\n" + synthesis + "\n\n"
        body += "---\n\n# 📝 각 AI 분석\n\n"
        for backend_name, response in responses.items():
            body += f"\n---\n\n## 🤖 {backend_name}\n\n{response}\n"

    elif mode == "compare" or len(backend_names) > 1:
        body += f"> 📊 **비교 모드** — {len(backend_names)}개 AI 관점.\n\n"
        for backend_name, response in responses.items():
            body += f"\n---\n\n## 🤖 {backend_name}\n\n{response}\n"

    else:  # single
        if backend_names:
            body += responses[backend_names[0]]

    body += f"""

---

> Generated by **sukgo** · made by 배움의 달인 ✨
> Mode: `{mode}` · Backend: `{', '.join(backend_names)}` · {now:%Y-%m-%d %H:%M}
"""

    filepath.write_text(body, encoding="utf-8")
    return filepath


# ═════════════════════════════════════════════════════════════════════
# UI
# ═════════════════════════════════════════════════════════════════════
def clear():
    os.system("clear" if os.name == "posix" else "cls")


def banner(config: dict):
    clear()
    backends = config.get("backends", [])
    save_path = config.get("save_path", "?")
    home = str(Path.home())
    short_save = save_path.replace(home, "~") if save_path.startswith(home) else save_path

    print()
    print(f"   {PURPLE}{'━' * 50}{RESET}")
    print()
    print(f"                    {BOLD}s u k g o{RESET}")
    print(f"                  {SLATE}결 정 의   기 술{RESET}")
    print()
    print(f"   {PURPLE}{'━' * 50}{RESET}")
    print()

    # 카테고리별 도구 분리
    thinking_tools = [t for t in TOOLS if t.category == "thinking"]
    domain_tools = [t for t in TOOLS if t.category == "domain"]

    # 사고 도구 섹션
    print(f"   {PURPLE}▌{RESET} {BOLD}사고 도구{RESET}  {DIM}— 검증된 사고 프레임워크{RESET}")
    print()
    for tool in thinking_tools:
        print(f"      {PEACH}{BOLD}{tool.key}{RESET}   {tool.emoji}  {tool.name}")
        print(f"           {DIM}{tool.short_desc}{RESET}")
    print()

    # 도메인 컨설턴트 섹션
    if domain_tools:
        print(f"   {PURPLE}▌{RESET} {BOLD}도메인 컨설턴트{RESET}  {DIM}— 데이터 기반 전문 분석{RESET}")
        print()
        for tool in domain_tools:
            print(f"      {PEACH}{BOLD}{tool.key}{RESET}   {tool.emoji}  {tool.name}")
            print(f"           {DIM}{tool.short_desc}{RESET}")
        print()

    # 설정 섹션
    print(f"   {PURPLE}▌{RESET} {BOLD}설정{RESET}")
    print()
    print(f"      {PEACH}{BOLD}s{RESET}    설정 변경")
    print(f"      {PEACH}{BOLD}u{RESET}    업데이트 확인  {DIM}(최신 버전으로){RESET}")
    print(f"      {PEACH}{BOLD}q{RESET}    종료")
    print()

    # 상태 바
    print(f"   {SLATE}{'─' * 50}{RESET}")
    if backends:
        dots = "   ".join([f"{GREEN}●{RESET} {b}" for b in backends])
        compare = f"   {SOFT_CYAN}→{RESET} {DIM}비교 가능{RESET}" if len(backends) > 1 else ""
        print(f"    {dots}{compare}")
    else:
        print(f"    {DIM}백엔드 없음{RESET}")
    print(f"    {DIM}📂  {short_save}{RESET}")
    print(f"   {SLATE}{'─' * 50}{RESET}")
    print()
    print(f"                       {DIM}made by 배움의 달인 ✨{RESET}")
    print(f"                            {DIM}v{VERSION}{RESET}")
    print()


def render_response(text: str):
    print(f"\n  {GRAY}{'═' * 56}{RESET}\n")
    for line in text.split("\n"):
        if line.startswith("## "):
            print(f"\n  {BOLD}{TEAL}{line[3:]}{RESET}\n")
        elif line.startswith("### "):
            print(f"\n  {BOLD}{line[4:]}{RESET}")
        elif line.startswith("# "):
            print(f"\n  {BOLD}{line[2:]}{RESET}\n")
        elif line.startswith("- "):
            print(f"  {YELLOW}•{RESET} {line[2:]}")
        elif line.strip():
            print(f"  {line}")
        else:
            print()
    print(f"\n  {GRAY}{'═' * 56}{RESET}")


# ═════════════════════════════════════════════════════════════════════
# 흐름
# ═════════════════════════════════════════════════════════════════════
def select_backends_for_run(config: dict) -> list:
    """
    실행 시 사용할 백엔드 결정.
    - 등록 1개 → 자동 사용
    - 등록 2개 이상 → 사용자에게 선택 받기 (단일/복수/모두)
    """
    registered_names = config.get("backends", [])
    registered = [get_backend(n) for n in registered_names]
    registered = [b for b in registered if b is not None]

    # 사용 가능한 것만
    available = [b for b in registered if b.is_available()]

    if not available:
        print(f"\n  {RED}❌ 등록된 백엔드 중 사용 가능한 것이 없습니다.{RESET}")
        unavailable = [b.name for b in registered if not b.is_available()]
        if unavailable:
            print(f"  {DIM}   비활성: {', '.join(unavailable)}{RESET}")
            print(f"  {DIM}   MLX/Ollama는 서버를 띄워야 사용 가능합니다.{RESET}")
        return []

    if len(available) == 1:
        return available

    # 2개 이상 → 사용자 선택
    print(f"\n  {DIM}어떤 AI를 사용할까요? (복수 선택 가능){RESET}\n")
    for i, b in enumerate(available, 1):
        print(f"    {BOLD}{i}.{RESET} {TEAL}{b.name}{RESET}  {DIM}{b.description}{RESET}")
    print(f"    {BOLD}a.{RESET} {YELLOW}모두 (비교 모드 / 원탁){RESET}")

    while True:
        choice = input(f"\n  {BOLD}선택 [{YELLOW}a{RESET}{BOLD}=모두]:{RESET} ").strip().lower()
        if not choice or choice in ("a", "all"):
            return available
        indices = parse_indices(choice, len(available))
        if indices:
            return [available[i - 1] for i in indices]
        print(f"  {RED}유효한 번호 또는 'a'를 입력하세요.{RESET}")


def run_compare(prompt: str, selected: list, render_inline: bool = True) -> dict:
    """비교 모드 — 각 AI 독립 답변 (기존 동작)"""
    responses = {}
    for backend in selected:
        if render_inline and len(selected) > 1:
            print(f"\n  {TEAL}── {backend.name} ──{RESET}")
        print(f"  {TEAL}⠋  {backend.name} 응답 준비 중... (10~60초){RESET}")
        resp = backend.chat(prompt)
        if resp:
            responses[backend.name] = resp
            if render_inline and len(selected) > 1:
                render_response(resp)
        else:
            print(f"  {YELLOW}⚠  {backend.name} 응답 실패 — 건너뜁니다{RESET}")
    return responses


def run_synthesis(prompt: str, topic: str, selected: list) -> dict:
    """종합 모드 — 비교 + 마지막에 한 AI가 종합"""
    # 1. 비교 (각자 답)
    responses = run_compare(prompt, selected, render_inline=True)
    if len(responses) < 2:
        return responses

    # 2. 종합 (첫 백엔드가 종합)
    synthesizer = selected[0]
    print(f"\n  {BOLD}{TEAL}══ 🎯 종합 단계 ({synthesizer.name}) ══{RESET}")
    print(f"  {TEAL}⠋  {synthesizer.name}이 모든 의견을 종합 중... (30~60초){RESET}")

    synth_prompt = SYNTHESIS_PROMPT.format(
        n=len(responses),
        topic=topic,
        responses=_format_responses_for_synth(responses),
    )
    synthesis = synthesizer.chat(synth_prompt)
    if synthesis:
        responses["__synthesis__"] = synthesis
        render_response(synthesis)
    return responses


def run_debate(prompt: str, topic: str, selected: list) -> dict:
    """원탁 토론 — 페르소나 + 2 라운드 + 최종 합의"""
    history = {b.name: [] for b in selected}

    print(f"\n  {BOLD}{YELLOW}🏛  원탁 회의 시작{RESET}")
    print(f"  {DIM}참석:{RESET} {', '.join([f'{get_persona(b.name)[0]} {get_persona(b.name)[1]} ({b.name})' for b in selected])}")
    print(f"  {DIM}의안:{RESET} {topic}\n")

    # ── Round 1 ──
    print(f"  {BOLD}{PURPLE}── Round 1: 각자 의견 ──{RESET}")
    for b in selected:
        emoji, persona_name, persona_desc = get_persona(b.name)
        print(f"\n  {TEAL}⠋  {emoji} {persona_name} ({b.name}) 의견 작성 중...{RESET}")
        r1 = b.chat(DEBATE_R1_PROMPT.format(
            emoji=emoji, persona_name=persona_name, persona_desc=persona_desc,
            topic=topic, base_prompt=prompt[:1500],
        ))
        if r1:
            history[b.name].append(r1)
            print(f"\n  {BOLD}{emoji} {persona_name} ({b.name}):{RESET}")
            for line in r1.split("\n"):
                print(f"     {line}")

    if not any(history.values()):
        return {}

    # ── Round 2 ──
    print(f"\n\n  {BOLD}{PURPLE}── Round 2: 토론 (서로 반박/동의) ──{RESET}")
    for b in selected:
        if not history[b.name]:
            continue
        emoji, persona_name, persona_desc = get_persona(b.name)
        others = {n: h[-1] for n, h in history.items() if n != b.name and h}
        if not others:
            continue

        print(f"\n  {TEAL}⠋  {emoji} {persona_name} ({b.name}) 반박 작성 중...{RESET}")
        r2 = b.chat(DEBATE_R2_PROMPT.format(
            emoji=emoji, persona_name=persona_name, persona_desc=persona_desc,
            topic=topic,
            my_opinion=history[b.name][-1],
            others=_format_others_for_debate(others),
        ))
        if r2:
            history[b.name].append(r2)
            print(f"\n  {BOLD}{emoji} {persona_name}의 반박:{RESET}")
            render_response(r2)

    # ── 최종 합의 ──
    print(f"\n\n  {BOLD}{PURPLE}── 최종 합의 ──{RESET}")
    synthesizer = selected[0]
    print(f"  {TEAL}⠋  {synthesizer.name}이 토론을 종합 중... (30~60초){RESET}")
    final = synthesizer.chat(DEBATE_FINAL_PROMPT.format(
        topic=topic,
        n=len(selected),
        history=_format_full_history(history),
    ))

    # 응답 통합 (저장용)
    responses = {}
    for name, rounds in history.items():
        responses[name] = "\n\n---\n\n".join([f"### Round {i+1}\n{r}" for i, r in enumerate(rounds)])
    if final:
        responses["__debate_final__"] = final
        print(f"\n  {BOLD}{TEAL}══ 🎯 합의 및 최종 권고 ══{RESET}")
        render_response(final)

    return responses


def tool_flow(config: dict, tool: Tool):
    """선택한 사고 도구 실행 (Investment는 별도 흐름으로 분기)"""
    if tool.needs_data_fetch and tool.save_id == "investment":
        investment_flow(config, tool)
        return

    selected = select_backends_for_run(config)
    if not selected:
        return

    mode = select_mode(len(selected))  # single / compare / synthesis / debate

    mode_labels = {
        "single": f"via {selected[0].name}",
        "compare": f"비교 · {len(selected)}개 AI",
        "synthesis": f"종합 · {len(selected)}개 AI",
        "debate": f"🏛 원탁 토론 · {len(selected)}개 페르소나",
    }
    print(f"\n  {BOLD}{tool.emoji}  {tool.name}{RESET}  {DIM}({TEAL}{mode_labels[mode]}{DIM}){RESET}")
    print(f"  {DIM}{tool.short_desc}{RESET}\n")
    topic = input(f"  {BOLD}주제:{RESET} ").strip()

    if not topic:
        print(f"  {DIM}입력이 비어 있습니다.{RESET}")
        return

    prompt = tool.get_prompt().format(topic=topic)

    # 모드별 실행
    if mode == "synthesis":
        responses = run_synthesis(prompt, topic, selected)
    elif mode == "debate":
        responses = run_debate(prompt, topic, selected)
    else:  # single, compare
        responses = run_compare(prompt, selected, render_inline=(mode == "compare"))
        if mode == "single" and responses:
            render_response(list(responses.values())[0])

    if not responses:
        print(f"\n  {RED}❌ 모든 백엔드 응답 실패{RESET}")
        return

    # 자동 저장
    try:
        save_dir = Path(config["save_path"])
        save_dir.mkdir(parents=True, exist_ok=True)
        filepath = save_session(save_dir, tool.save_id, topic, responses, mode=mode)
        home = str(Path.home())
        short = str(filepath).replace(home, "~")
        print(f"\n  {GREEN}💾 저장됨:{RESET} {DIM}{short}{RESET}")
        print(f"  {DIM}   모드: {mode_labels[mode]}{RESET}")
    except Exception as e:
        print(f"\n  {YELLOW}⚠  저장 실패: {e}{RESET}")


def ensure_data_fetchers() -> bool:
    """
    Investment 도구용 의존성 자동 체크·설치.
    yfinance, finance-datareader 가 없으면 사용자에게 묻고 자동 설치.
    ⚠ FDR: PyPI 이름은 'finance-datareader' (hyphen), import는 'FinanceDataReader' (CamelCase)
    Returns: 설치 완료 여부
    """
    missing = []  # PyPI install names
    try:
        import yfinance  # noqa: F401
    except ImportError:
        missing.append("yfinance")
    try:
        import FinanceDataReader  # noqa: F401  (import name은 CamelCase)
    except ImportError:
        missing.append("finance-datareader")  # PyPI install name은 hyphenated

    if not missing:
        return True

    print(f"\n  {YELLOW}📦 Investment 도구에 필요한 라이브러리:{RESET}")
    for m in missing:
        print(f"     {DIM}-{RESET} {BOLD}{m}{RESET}")
    print(f"  {DIM}   (yfinance: 해외 주식 / FinanceDataReader: 한국 주식){RESET}")
    print()

    confirm = input(
        f"  {BOLD}자동 설치할까요? (1~2분 소요) [Y/n]:{RESET} "
    ).strip().lower()

    if confirm not in ("", "y", "yes"):
        print(f"\n  {DIM}수동 설치: pip install --user {' '.join(missing)}{RESET}")
        return False

    # virtualenv 감지: venv 안에서는 --user 플래그 사용 불가
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)

    base_cmd = [sys.executable, "-m", "pip", "install", "--quiet"]
    if not in_venv:
        base_cmd.append("--user")

    if in_venv:
        print(f"  {DIM}   (virtualenv 감지 → --user 플래그 생략){RESET}")

    # ── 0단계: pip 자동 업그레이드 (구버전 pip가 패키지 못 찾는 경우 다수) ──
    print(f"\n  {TEAL}⠋  pip 업그레이드 중...{RESET}")
    try:
        subprocess.run(
            base_cmd + ["--upgrade", "pip"],
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        pass  # 업그레이드 실패해도 계속 진행

    # ── 패키지를 한 개씩 설치 (부분 성공 허용) ──
    installed = []
    failed = []
    for pkg in missing:
        print(f"  {TEAL}⠋  설치 중... {pkg}{RESET}")
        cmd = base_cmd + [pkg]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        except subprocess.TimeoutExpired:
            print(f"  {RED}❌ {pkg} 시간 초과{RESET}")
            failed.append(pkg)
            continue

        # PEP 668 fallback
        if result.returncode != 0 and "externally-managed-environment" in (result.stderr or ""):
            print(f"  {YELLOW}⚠ PEP 668 감지 → --break-system-packages 재시도{RESET}")
            try:
                result = subprocess.run(cmd + ["--break-system-packages"], capture_output=True, text=True, timeout=180)
            except subprocess.TimeoutExpired:
                print(f"  {RED}❌ {pkg} 재시도 시간 초과{RESET}")
                failed.append(pkg)
                continue

        if result.returncode == 0:
            print(f"  {GREEN}✅ {pkg}{RESET}")
            installed.append(pkg)
        else:
            print(f"  {RED}❌ {pkg} 실패{RESET}")
            err_tail = (result.stderr or result.stdout or "").strip().split("\n")[-3:]
            for line in err_tail:
                print(f"     {DIM}{line[:120]}{RESET}")
            failed.append(pkg)

    # ── 결과 안내 ──
    if installed:
        print(f"\n  {GREEN}✅ 설치 성공:{RESET} {', '.join(installed)}")

    if failed:
        print(f"\n  {YELLOW}⚠ 설치 실패:{RESET} {', '.join(failed)}")
        print(f"  {DIM}수동 시도 (한 줄씩):{RESET}")
        for pkg in failed:
            print(f"  {DIM}    python3 -m pip install --upgrade pip && python3 -m pip install {pkg}{RESET}")
        print(f"  {DIM}또는 새 venv:{RESET}")
        print(f"  {DIM}    python3 -m venv ~/.venvs/sukgo && source ~/.venvs/sukgo/bin/activate && pip install {' '.join(failed)}{RESET}")

    if "yfinance" in installed:
        print(f"\n  {DIM}💡 yfinance만 있어도 해외 주식 분석은 정상 작동합니다.{RESET}")
        if "FinanceDataReader" in failed:
            print(f"  {DIM}   한국 주식(6자리 코드)은 일시적으로 제한.{RESET}")

    return len(installed) > 0


def investment_flow(config: dict, tool: Tool):
    """Investment 도구 전용 흐름 — 데이터 자동 수집 + 9섹션 분석"""
    print(f"\n  {BOLD}{tool.emoji}  {tool.name}{RESET}  {DIM}— 9섹션 종합 분석{RESET}")

    # ── 의존성 자동 체크·설치 ──
    if not ensure_data_fetchers():
        print(f"\n  {YELLOW}⚠  의존성 없이 진행 (LLM 학습 지식만 사용){RESET}")
        confirm = input(f"  {DIM}계속할까요? [y/N]:{RESET} ").strip().lower()
        if confirm != "y":
            return

    print(f"\n  {DIM}종목 입력 (티커 또는 6자리 코드):{RESET}")
    print(f"  {DIM}    해외 (영문 티커):{RESET}")
    print(f"  {DIM}        NVDA    AAPL    MSFT    TSLA    GOOGL{RESET}")
    print(f"  {DIM}    한국 (6자리 종목코드 — 회사명·괄호 X):{RESET}")
    print(f"  {DIM}        005930   ← 삼성전자{RESET}")
    print(f"  {DIM}        035420   ← 네이버{RESET}")
    print(f"  {DIM}        000660   ← SK하이닉스{RESET}")
    print()
    user_input = input(f"  {BOLD}종목:{RESET} ").strip()

    if not user_input:
        print(f"  {DIM}입력이 비어 있습니다.{RESET}")
        return

    # 자동 정규화 (괄호·공백 자동 제거)
    parts = user_input.split()
    user_hint = " ".join(parts[1:]) if len(parts) > 1 else ""

    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from data_fetchers.stocks import normalize_ticker
        ticker = normalize_ticker(user_input)
    except ImportError:
        ticker = parts[0].upper()

    if ticker != parts[0].upper():
        print(f"  {DIM}   → 정규화: '{parts[0]}' → '{ticker}'{RESET}")

    # ── 데이터 페처 import (방금 설치했을 수 있음) ──
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from data_fetchers.stocks import fetch_stock_data, format_data_summary
    except ImportError as e:
        print(f"\n  {RED}❌ data_fetchers 모듈 로드 실패: {e}{RESET}")
        print(f"  {DIM}   ./install.sh 실행 또는 sukgo 재시작 후 다시 시도.{RESET}")
        return

    print(f"\n  {TEAL}📊  {ticker} 데이터 수집 중...{RESET}")
    data = fetch_stock_data(ticker)

    if "error" in data and "current_price" not in data:
        print(f"  {YELLOW}⚠  {data['error']}{RESET}")
        confirm = input(f"  {DIM}LLM 학습 지식만으로 계속 분석할까요? [y/N]:{RESET} ").strip().lower()
        if confirm != "y":
            return
    else:
        print(f"  {GREEN}✅ 데이터 수집 완료:{RESET}")
        if data.get("name"):
            print(f"     {BOLD}{data['name']}{RESET}  {DIM}({ticker} · {data.get('country', '?')}){RESET}")
        if data.get("current_price"):
            print(f"     현재가:    {data['current_price']:,.2f}")
        if data.get("trailing_pe"):
            print(f"     PER:       {data['trailing_pe']:.2f}")
        if data.get("market_cap"):
            mc = data["market_cap"]
            mc_str = f"{mc/1e12:.2f}T" if mc > 1e12 else f"{mc/1e9:.2f}B" if mc > 1e9 else f"{mc/1e6:.2f}M"
            print(f"     시가총액:  {mc_str}")
        if data.get("52w_high") and data.get("52w_low"):
            print(f"     52주 범위: {data['52w_low']:,.2f} ~ {data['52w_high']:,.2f}")
        if data.get("recent_news"):
            print(f"     뉴스:      {len(data['recent_news'])}건 수집")

    data_summary = format_data_summary(data)

    # ── 백엔드 선택 + 모드 ──
    selected = select_backends_for_run(config)
    if not selected:
        return

    mode = select_mode(len(selected))
    user_topic = f"{ticker}" + (f"  ({user_hint})" if user_hint else "")

    # ── 프롬프트 조립 ──
    prompt = tool.get_prompt().format(topic=user_topic, stock_data=data_summary)

    # ── 모드별 실행 ──
    if mode == "synthesis":
        responses = run_synthesis(prompt, user_topic, selected)
    elif mode == "debate":
        responses = run_debate(prompt, user_topic, selected)
    else:  # single, compare
        print(f"\n  {TEAL}⠋  9섹션 종합 리포트 생성 중... (백엔드별 30~120초){RESET}")
        responses = run_compare(prompt, selected, render_inline=(mode == "compare"))
        if mode == "single" and responses:
            render_response(list(responses.values())[0])

    if not responses:
        print(f"\n  {RED}❌ 모든 백엔드 응답 실패{RESET}")
        return

    # ── 저장 (Investment는 별도 폴더) ──
    try:
        save_dir = Path(config["save_path"]) / "_investments"
        save_dir.mkdir(parents=True, exist_ok=True)
        filepath = save_session(save_dir, tool.save_id, user_topic, responses, mode=mode)
        home = str(Path.home())
        short = str(filepath).replace(home, "~")
        print(f"\n  {GREEN}💾 저장됨:{RESET} {DIM}{short}{RESET}")
        print(f"  {DIM}   _investments/ 하위 폴더에 자동 분류됨{RESET}")
    except Exception as e:
        print(f"\n  {YELLOW}⚠  저장 실패: {e}{RESET}")


def settings_flow(config: dict) -> dict:
    backends = config.get("backends", [])
    print(f"\n  {BOLD}⚙️  현재 설정{RESET}\n")
    print(f"  {DIM}백엔드:{RESET}    {TEAL}{', '.join(backends) if backends else '?'}{RESET}")
    print(f"  {DIM}저장 위치:{RESET}  {config.get('save_path', '?')}")
    print(f"  {DIM}설정 파일:{RESET}  {CONFIG_PATH}\n")
    print(f"    {BOLD}1.{RESET} 백엔드 변경 (복수 가능)")
    print(f"    {BOLD}2.{RESET} 저장 위치 변경")
    print(f"    {BOLD}3.{RESET} 처음부터 다시 설정")
    print(f"    {BOLD}b.{RESET} 메뉴로 돌아가기")

    choice = input(f"\n  {BOLD}>{RESET} ").strip().lower()

    if choice == "1":
        statuses = [(i, b, b.is_available()) for i, b in enumerate(ALL_BACKENDS, 1)]
        print("\n  사용 가능한 AI:\n")
        for i, b, avail in statuses:
            mark = f"{GREEN}✅{RESET}" if avail else f"{DIM}❌{RESET}"
            print(f"    {BOLD}{i}.{RESET} {mark} {b.name:8} {DIM}{b.description}{RESET}")
        available_indices = [i for i, b, avail in statuses if avail]
        print(f"\n  {DIM}복수 선택: 1,2,3  /  단일: 1  /  모두: all{RESET}")
        new = input(f"\n  새 백엔드 번호: ").strip()
        indices = parse_indices(new, len(ALL_BACKENDS))
        indices = [i for i in indices if i in available_indices]
        if indices:
            config["backends"] = [ALL_BACKENDS[i - 1].name for i in indices]
            save_config(config)
            print(f"  {GREEN}✅ 백엔드 변경:{RESET} {', '.join(config['backends'])}")
        else:
            print(f"  {RED}취소됨{RESET}")
    elif choice == "2":
        new_path = input(f"\n  새 저장 위치 (예: ~/Documents/MyVault/Inbox): ").strip()
        if new_path:
            path = Path(new_path).expanduser().resolve()
            path.mkdir(parents=True, exist_ok=True)
            config["save_path"] = str(path)
            save_config(config)
            print(f"  {GREEN}✅ 저장 위치 변경됨{RESET}")
    elif choice == "3":
        if CONFIG_PATH.exists():
            CONFIG_PATH.unlink()
        config = first_run_setup()

    return config


# ═════════════════════════════════════════════════════════════════════
# 업데이트
# ═════════════════════════════════════════════════════════════════════
SUKGO_HOME_DIR = Path.home() / ".sukgo"
SUKGO_SOURCE_DIR = SUKGO_HOME_DIR / "source"
GET_SH_URL = "https://raw.githubusercontent.com/reallygood83/sukgo/main/get.sh"


def _detect_install_dir() -> Optional[Path]:
    """sukgo 가 설치된 git 작업 폴더를 찾는다.

    1. ~/.sukgo/source/.git  (한 줄 설치로 깔린 표준 위치)
    2. 현재 실행 중인 poc.py 가 들어있는 git 저장소  (개발자 모드)
    """
    if (SUKGO_SOURCE_DIR / ".git").exists():
        return SUKGO_SOURCE_DIR

    here = Path(__file__).resolve().parent
    if (here / ".git").exists():
        return here
    return None


def update_flow():
    """현재 sukgo 를 최신으로 업데이트.

    - git 저장소가 있으면 → git fetch + reset --hard origin/main + install.sh
    - 없으면 → curl 한 줄 설치 안내
    """
    print(f"\n  {BOLD}🔄  sukgo 업데이트{RESET}\n")

    install_dir = _detect_install_dir()

    if install_dir is None:
        print(f"  {YELLOW}⚠  git 기반 설치가 아니라 자동 업데이트가 어려워요.{RESET}\n")
        print(f"  {DIM}아래 한 줄을 터미널에 붙여 넣어 주세요:{RESET}\n")
        print(f"  {GREEN}curl -fsSL {GET_SH_URL} | bash{RESET}\n")
        return

    print(f"  {DIM}설치 위치:{RESET} {install_dir}\n")

    # 1) git fetch + 최신 버전 확인
    try:
        print(f"  {TEAL}⠋  최신 버전 확인 중...{RESET}")
        subprocess.run(
            ["git", "-C", str(install_dir), "fetch", "--quiet", "origin"],
            check=True, timeout=60,
        )
        local = subprocess.run(
            ["git", "-C", str(install_dir), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        remote = subprocess.run(
            ["git", "-C", str(install_dir), "rev-parse", "origin/main"],
            check=True, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"  {RED}❌ git 호출 실패:{RESET} {e}")
        return

    if local == remote:
        print(f"  {GREEN}✅ 이미 최신입니다 (v{VERSION}){RESET}\n")
        return

    # 로컬이 원격보다 앞서 있으면 (개발자 모드) — reset 하면 커밋 유실됨
    ahead = subprocess.run(
        ["git", "-C", str(install_dir), "merge-base", "--is-ancestor", remote, local],
    ).returncode == 0
    if ahead:
        print(f"  {YELLOW}⚠  로컬이 원격보다 앞서 있어요 (개발자 모드).{RESET}")
        print(f"  {DIM}자동 업데이트는 로컬 커밋을 덮어쓰므로 건너뜁니다.{RESET}\n")
        return

    print(f"  {YELLOW}🆕 새 버전이 있습니다.{RESET}")
    print(f"  {DIM}  현재:{RESET} {local[:8]}")
    print(f"  {DIM}  최신:{RESET} {remote[:8]}\n")

    # 2) 변경 로그 미리보기
    try:
        log = subprocess.run(
            ["git", "-C", str(install_dir), "log", "--oneline", f"{local}..{remote}"],
            check=True, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        if log:
            print(f"  {BOLD}변경 사항:{RESET}")
            for line in log.splitlines()[:10]:
                print(f"    {DIM}•{RESET} {line}")
            print()
    except subprocess.CalledProcessError:
        pass

    confirm = input(f"  업데이트 할까요? [Y/n] ").strip().lower()
    if confirm and confirm not in ("y", "yes"):
        print(f"  {DIM}취소됨{RESET}\n")
        return

    # 3) git reset --hard
    try:
        print(f"\n  {TEAL}⠋  최신으로 동기화 중...{RESET}")
        subprocess.run(
            ["git", "-C", str(install_dir), "reset", "--hard", "--quiet", "origin/main"],
            check=True, timeout=30,
        )
        print(f"  {GREEN}✅ 코드 업데이트 완료{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"  {RED}❌ git reset 실패:{RESET} {e}")
        return

    # 4) install.sh 재실행 (의존성 갱신)
    install_sh = install_dir / "install.sh"
    if install_sh.exists():
        print(f"  {TEAL}⠋  의존성 동기화 중...{RESET}")
        r = subprocess.run(["bash", str(install_sh)], capture_output=True, text=True, timeout=300)
        if r.returncode == 0:
            print(f"  {GREEN}✅ 의존성 동기화 완료{RESET}")
        else:
            print(f"  {YELLOW}⚠  install.sh 경고:{RESET}\n{DIM}{r.stderr[-300:]}{RESET}")

    print(f"\n  {GREEN}{BOLD}🎉 업데이트 완료!{RESET} {DIM}sukgo 를 다시 실행하면 새 버전이 적용됩니다.{RESET}\n")


# ═════════════════════════════════════════════════════════════════════
# 메인 루프
# ═════════════════════════════════════════════════════════════════════
def main():
    # CLI 서브커맨드: `sukgo update`, `sukgo --version`
    if len(sys.argv) > 1:
        sub = sys.argv[1].lower()
        if sub in ("update", "upgrade", "u"):
            update_flow()
            return
        if sub in ("--version", "-v", "version"):
            print(f"sukgo v{VERSION}")
            return

    config = load_config()
    config = migrate_config(config)
    if not config or "backends" not in config or "save_path" not in config:
        config = first_run_setup()

    tool_keys = {t.key for t in TOOLS}

    while True:
        banner(config)
        choice = input(f"   {BOLD}>{RESET} ").strip().lower()

        if choice in ("q", "quit", "exit"):
            print(f"\n  {DIM}좋은 결정 되시길 ✨{RESET}\n")
            return

        if choice in tool_keys:
            tool = get_tool(choice)
            if tool:
                tool_flow(config, tool)
                input(f"\n  {DIM}Enter → 메인 메뉴{RESET} ")
        elif choice == "s":
            config = settings_flow(config)
            input(f"\n  {DIM}Enter → 메인 메뉴{RESET} ")
        elif choice == "u":
            update_flow()
            input(f"\n  {DIM}Enter → 메인 메뉴{RESET} ")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}중단됨{RESET}\n")
        sys.exit(0)
