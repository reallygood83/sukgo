# sukgo 보안 가이드

> **원칙**: 사용자 본인의 API 키는 본인 컴퓨터에만, 절대 코드와 함께 배포되지 않는다.

---

## 🔑 비밀 키 저장 위치

### 자동 위치 (권장)
```
~/.config/sukgo/secrets.json
```
- 권한: `600` (사용자 본인만 읽기·쓰기)
- sukgo 첫 사용 시 wizard로 자동 생성
- `.gitignore`로 GitHub 업로드 차단됨

### 환경 변수 (대안)
```bash
export NAVER_CLIENT_ID="..."
export NAVER_CLIENT_SECRET="..."
export DART_API_KEY="..."
```
- secrets.json 보다 우선 적용
- CI/CD·서버 환경에서 유용

---

## 📋 필요한 API 키 목록

| 서비스 | 용도 | 발급 URL | 비용 |
|--------|------|----------|------|
| **Naver Search** | 한국 뉴스 검색 | https://developers.naver.com/apps/ | 무료 (일 25,000건) |
| **DART API** | 한국 공식 공시 | https://opendart.fss.or.kr/ | 무료 (일 20,000건) |
| **Alpha Vantage** (선택) | 해외 기술적 지표 | https://www.alphavantage.co/support/#api-key | 무료 (분당 5건) |

> ⚠ **Anthropic / OpenAI / Google API 키는 sukgo가 직접 관리하지 않음.**
> sukgo는 `claude` / `codex` / `gemini` CLI를 통해 호출 → 각 CLI가 OAuth/구독으로 자체 인증.

---

## 🚫 절대 하지 말 것

### ❌ 코드에 키 하드코딩
```python
# ❌ 금지
NAVER_KEY = "abc123def456"  # GitHub에 올라가는 순간 끝
```

### ❌ 슬랙·Discord·이메일에 키 공유
- 캐시되고 검색 가능
- 봇이 스캔할 수 있음

### ❌ `secrets.json`을 git에 커밋
- `.gitignore`로 차단되어 있지만, 만약 실수로 추가했다면:
  ```bash
  git rm --cached secrets.json
  git commit -m "remove leaked secrets"
  # 그리고 즉시 키 재발급 (이미 캐시됨)
  ```

---

## ✅ 권장 워크플로

### 첫 사용
```bash
$ sukgo

🔑 처음 실행이시군요!
    Naver Search API 키가 필요합니다.
    발급: https://developers.naver.com/apps/

    Client ID: > [입력]
    Client Secret: > [입력]

✅ ~/.config/sukgo/secrets.json 에 안전하게 저장됨
```

### 키 변경
```bash
$ sukgo → s (설정) → 3 (API 키 변경)
```

### 키 삭제
```bash
rm ~/.config/sukgo/secrets.json
```

---

## 🛡 GitHub 공개 시 체크리스트

배포 전 반드시 확인:

- [ ] `.gitignore`에 `secrets.json`, `.env`, `*.key` 포함 확인
- [ ] `git status`로 의심스러운 파일 없는지 확인
- [ ] 다음 명령으로 과거 커밋에 키 유출 없는지 확인:
  ```bash
  git log -p | grep -iE "api[_-]?key|secret|token|password" | head -50
  ```
- [ ] 발견 시 → 즉시 키 재발급 + `git filter-branch` 또는 BFG 사용
- [ ] GitHub Secrets Scanning 활성화

---

## 🚨 키가 유출되었다면

1. **즉시** 해당 서비스에서 키 재발급 (1순위)
2. 유출된 위치에서 키 제거 (코드·로그·메시지)
3. git 히스토리에서 제거 (BFG Repo-Cleaner)
4. GitHub force push (필요 시)
5. 액세스 로그 확인 (오용 흔적)

---

## 📚 참고

- [GitHub Secrets Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [12 Factor App: Config](https://12factor.net/config)
