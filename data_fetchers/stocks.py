"""
주식 데이터 페처 — Investment 도구용

지원:
- yfinance: 해외 종목 (NVDA, AAPL, MSFT 등)
- FinanceDataReader: 한국 종목 (005930, 035420 등 6자리 코드)

API 키 불필요 (둘 다 무료 공개 데이터 소스).
"""

import re
from datetime import date, timedelta
from typing import Optional

# Optional imports — 없어도 sukgo는 작동 (그 기능만 비활성)
_YFINANCE_AVAILABLE = False
_FDR_AVAILABLE = False

try:
    import yfinance as yf
    _YFINANCE_AVAILABLE = True
except ImportError:
    pass

try:
    import FinanceDataReader as fdr
    _FDR_AVAILABLE = True
except ImportError:
    pass


# ─── 유틸 ───────────────────────────────────────────────────
def is_korean_ticker(ticker: str) -> bool:
    """한국 종목 코드 (6자리 숫자) 판별"""
    return bool(re.match(r"^\d{6}$", ticker))


def _safe(d: dict, key: str, default=None):
    """dict get with fallback for None"""
    v = d.get(key)
    return v if v is not None else default


# ─── 해외 주식 (yfinance) ────────────────────────────────────
def fetch_us_stock(ticker: str) -> dict:
    """yfinance로 해외 종목 데이터 수집 (50+ 항목)"""
    if not _YFINANCE_AVAILABLE:
        return {"error": "yfinance 미설치 — pip install yfinance"}

    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}

        if not info or len(info) < 5:
            return {"error": f"yfinance: {ticker} 정보 없음 (티커 확인 필요)"}

        data = {
            "ticker": ticker.upper(),
            "country": "US",
            "name": _safe(info, "longName") or _safe(info, "shortName"),
            "sector": _safe(info, "sector"),
            "industry": _safe(info, "industry"),

            # 가격
            "current_price": _safe(info, "currentPrice") or _safe(info, "regularMarketPrice"),
            "previous_close": _safe(info, "regularMarketPreviousClose"),
            "52w_high": _safe(info, "fiftyTwoWeekHigh"),
            "52w_low": _safe(info, "fiftyTwoWeekLow"),
            "day_high": _safe(info, "dayHigh"),
            "day_low": _safe(info, "dayLow"),
            "volume": _safe(info, "volume"),
            "avg_volume": _safe(info, "averageVolume"),

            # 밸류에이션
            "market_cap": _safe(info, "marketCap"),
            "trailing_pe": _safe(info, "trailingPE"),
            "forward_pe": _safe(info, "forwardPE"),
            "peg_ratio": _safe(info, "pegRatio") or _safe(info, "trailingPegRatio"),
            "price_to_book": _safe(info, "priceToBook"),
            "price_to_sales": _safe(info, "priceToSalesTrailing12Months"),
            "ev_to_ebitda": _safe(info, "enterpriseToEbitda"),

            # 수익성
            "profit_margins": _safe(info, "profitMargins"),
            "operating_margins": _safe(info, "operatingMargins"),
            "gross_margins": _safe(info, "grossMargins"),
            "ebitda_margins": _safe(info, "ebitdaMargins"),
            "return_on_equity": _safe(info, "returnOnEquity"),
            "return_on_assets": _safe(info, "returnOnAssets"),

            # 성장
            "revenue_growth": _safe(info, "revenueGrowth"),
            "earnings_growth": _safe(info, "earningsGrowth"),
            "earnings_quarterly_growth": _safe(info, "earningsQuarterlyGrowth"),

            # 재무 건전성
            "total_cash": _safe(info, "totalCash"),
            "total_debt": _safe(info, "totalDebt"),
            "debt_to_equity": _safe(info, "debtToEquity"),
            "current_ratio": _safe(info, "currentRatio"),
            "quick_ratio": _safe(info, "quickRatio"),
            "free_cashflow": _safe(info, "freeCashflow"),
            "operating_cashflow": _safe(info, "operatingCashflow"),

            # 배당
            "dividend_yield": _safe(info, "dividendYield"),
            "payout_ratio": _safe(info, "payoutRatio"),

            # 리스크
            "beta": _safe(info, "beta"),
            "shares_short": _safe(info, "sharesShort"),
            "short_ratio": _safe(info, "shortRatio"),
            "short_percent_of_float": _safe(info, "shortPercentOfFloat"),

            # 애널리스트
            "analyst_recommendation": _safe(info, "recommendationKey"),
            "analyst_count": _safe(info, "numberOfAnalystOpinions"),
            "target_mean_price": _safe(info, "targetMeanPrice"),
            "target_high_price": _safe(info, "targetHighPrice"),
            "target_low_price": _safe(info, "targetLowPrice"),
            "target_median_price": _safe(info, "targetMedianPrice"),
        }

        # 최근 뉴스 (5건)
        try:
            news = stock.news[:5] if hasattr(stock, "news") and stock.news else []
            data["recent_news"] = []
            for n in news:
                content = n.get("content", {}) if isinstance(n, dict) else {}
                title = n.get("title") or content.get("title", "")
                publisher = n.get("publisher") or content.get("provider", {}).get("displayName", "")
                if title:
                    data["recent_news"].append({"title": title, "publisher": publisher})
        except Exception:
            data["recent_news"] = []

        # None 제거
        data = {k: v for k, v in data.items() if v is not None}
        return data

    except Exception as e:
        return {"error": f"yfinance 호출 실패: {type(e).__name__}: {e}"}


# ─── 한국 주식 (FinanceDataReader) ──────────────────────────
def fetch_kr_stock(ticker: str) -> dict:
    """FDR로 한국 종목 데이터 수집"""
    if not _FDR_AVAILABLE:
        return {"error": "FinanceDataReader 미설치 — pip install finance-datareader"}

    try:
        data = {"ticker": ticker, "country": "KR"}

        # 종목 정보 (KRX)
        try:
            stock_list = fdr.StockListing("KRX")
            match = stock_list[stock_list["Code"] == ticker]
            if not match.empty:
                row = match.iloc[0]
                data["name"] = row.get("Name")
                data["market"] = row.get("Market")
                data["sector"] = row.get("Sector")
                data["industry"] = row.get("Industry")
                if "Marcap" in row and row["Marcap"]:
                    data["market_cap"] = int(row["Marcap"])
                if "Stocks" in row and row["Stocks"]:
                    data["shares_outstanding"] = int(row["Stocks"])
        except Exception:
            pass

        # 가격 시계열 (1년)
        end = date.today()
        start = end - timedelta(days=365)
        df = fdr.DataReader(ticker, start, end)

        if df.empty:
            return {**data, "error": f"FDR: {ticker} 가격 데이터 없음"}

        latest = df.iloc[-1]
        data["current_price"] = float(latest["Close"])
        data["day_high"] = float(latest["High"])
        data["day_low"] = float(latest["Low"])
        data["volume"] = int(latest["Volume"])
        data["52w_high"] = float(df["High"].max())
        data["52w_low"] = float(df["Low"].min())

        # 등락률
        if len(df) > 1:
            data["change_1d_pct"] = float((df.iloc[-1]["Close"] / df.iloc[-2]["Close"] - 1) * 100)
        if len(df) > 30:
            data["change_30d_pct"] = float((df.iloc[-1]["Close"] / df.iloc[-30]["Close"] - 1) * 100)
        if len(df) > 250:
            data["change_1y_pct"] = float((df.iloc[-1]["Close"] / df.iloc[-250]["Close"] - 1) * 100)

        # 거래량 평균
        data["avg_volume"] = int(df["Volume"].mean())

        # None 제거
        data = {k: v for k, v in data.items() if v is not None}
        return data

    except Exception as e:
        return {"error": f"FDR 호출 실패: {type(e).__name__}: {e}"}


# ─── 통합 진입점 ──────────────────────────────────────────────
def fetch_stock_data(ticker: str) -> dict:
    """
    종목 데이터 자동 수집 (티커 형식 자동 감지).

    Args:
        ticker: 종목 코드. 한국=6자리 숫자(005930), 해외=영문(NVDA)

    Returns:
        dict: 수집된 데이터 (실패 시 'error' 키 포함)
    """
    ticker = ticker.strip().upper()

    if is_korean_ticker(ticker):
        return fetch_kr_stock(ticker)
    else:
        return fetch_us_stock(ticker)


# ─── LLM 프롬프트용 포맷 ─────────────────────────────────────
def format_data_summary(data: dict, max_chars: int = 4000) -> str:
    """수집된 데이터를 LLM 프롬프트용 마크다운으로 포맷"""
    if "error" in data and "current_price" not in data:
        return f"⚠ 데이터 수집 실패: {data['error']}\n\n(LLM 학습 지식만으로 분석 — 데이터 한계 명시 필요)"

    lines = []

    # 기본
    lines.append("### 📌 종목 기본 정보")
    lines.append(f"- 티커: **{data.get('ticker', '?')}**  ({data.get('country', '?')})")
    if data.get("name"):
        lines.append(f"- 이름: {data['name']}")
    if data.get("sector"):
        lines.append(f"- 섹터: {data['sector']}")
    if data.get("industry"):
        lines.append(f"- 산업: {data['industry']}")

    # 가격
    if any(k in data for k in ("current_price", "52w_high", "52w_low")):
        lines.append("\n### 💵 가격 동향")
        if "current_price" in data:
            lines.append(f"- **현재가: {data['current_price']:,.2f}**")
        if "previous_close" in data:
            lines.append(f"- 전일종가: {data['previous_close']:,.2f}")
        if "52w_high" in data and "52w_low" in data:
            lines.append(f"- 52주 범위: {data['52w_low']:,.2f} ~ {data['52w_high']:,.2f}")
        for k, label in [("change_1d_pct", "1일"), ("change_30d_pct", "30일"), ("change_1y_pct", "1년")]:
            if k in data:
                lines.append(f"- {label} 변동: {data[k]:+.2f}%")
        if "volume" in data:
            lines.append(f"- 거래량: {data['volume']:,}")

    # 시가총액
    if data.get("market_cap"):
        mc = data["market_cap"]
        if mc > 1e12:
            mc_str = f"{mc / 1e12:.2f}T"
        elif mc > 1e9:
            mc_str = f"{mc / 1e9:.2f}B"
        else:
            mc_str = f"{mc / 1e6:.2f}M"
        lines.append(f"- 시가총액: {mc_str}")

    # 밸류에이션
    val_keys = [
        ("trailing_pe", "PER (TTM)"),
        ("forward_pe", "Forward PER"),
        ("peg_ratio", "PEG"),
        ("price_to_book", "PBR"),
        ("price_to_sales", "PSR"),
        ("ev_to_ebitda", "EV/EBITDA"),
    ]
    if any(k in data for k, _ in val_keys):
        lines.append("\n### 📊 밸류에이션")
        for k, label in val_keys:
            if k in data:
                lines.append(f"- {label}: {data[k]:.2f}")

    # 수익성
    profit_keys = [
        ("gross_margins", "매출총이익률"),
        ("operating_margins", "영업이익률"),
        ("profit_margins", "순이익률"),
        ("return_on_equity", "ROE"),
        ("return_on_assets", "ROA"),
    ]
    if any(k in data for k, _ in profit_keys):
        lines.append("\n### 💰 수익성")
        for k, label in profit_keys:
            if k in data:
                lines.append(f"- {label}: {data[k] * 100:+.2f}%")

    # 성장
    growth_keys = [
        ("revenue_growth", "매출 성장"),
        ("earnings_growth", "이익 성장"),
        ("earnings_quarterly_growth", "분기 이익 성장"),
    ]
    if any(k in data for k, _ in growth_keys):
        lines.append("\n### 📈 성장성")
        for k, label in growth_keys:
            if k in data:
                lines.append(f"- {label}: {data[k] * 100:+.2f}%")

    # 재무 건전성
    fin_keys = [
        ("debt_to_equity", "부채비율"),
        ("current_ratio", "유동비율"),
        ("quick_ratio", "당좌비율"),
    ]
    if any(k in data for k, _ in fin_keys):
        lines.append("\n### 🏛 재무 건전성")
        for k, label in fin_keys:
            if k in data:
                lines.append(f"- {label}: {data[k]:.2f}")
        if data.get("free_cashflow"):
            fc = data["free_cashflow"]
            fc_str = f"{fc / 1e9:.2f}B" if abs(fc) > 1e9 else f"{fc / 1e6:.2f}M"
            lines.append(f"- Free Cash Flow: {fc_str}")

    # 배당
    if data.get("dividend_yield"):
        lines.append(f"\n### 💸 배당\n- 배당 수익률: {data['dividend_yield'] * 100:.2f}%")
        if data.get("payout_ratio"):
            lines.append(f"- 배당성향: {data['payout_ratio'] * 100:.2f}%")

    # 애널리스트
    if any(k in data for k in ("analyst_recommendation", "target_mean_price")):
        lines.append("\n### 👨‍💼 애널리스트 컨센서스")
        if data.get("analyst_recommendation"):
            lines.append(f"- 추천: **{data['analyst_recommendation'].upper()}**")
        if data.get("analyst_count"):
            lines.append(f"- 커버 애널리스트: {data['analyst_count']}명")
        if data.get("target_mean_price"):
            lines.append(f"- 평균 목표가: {data['target_mean_price']:,.2f}")
        if data.get("target_high_price") and data.get("target_low_price"):
            lines.append(f"- 목표가 범위: {data['target_low_price']:,.2f} ~ {data['target_high_price']:,.2f}")

    # 리스크
    if any(k in data for k in ("beta", "short_ratio", "short_percent_of_float")):
        lines.append("\n### ⚠ 리스크 지표")
        if "beta" in data:
            lines.append(f"- Beta: {data['beta']:.2f}")
        if "short_ratio" in data:
            lines.append(f"- Short Ratio: {data['short_ratio']:.2f}")
        if "short_percent_of_float" in data:
            lines.append(f"- Short % of Float: {data['short_percent_of_float'] * 100:.2f}%")

    # 뉴스
    if data.get("recent_news"):
        lines.append("\n### 📰 최근 뉴스")
        for n in data["recent_news"]:
            pub = f"[{n.get('publisher', '?')}] " if n.get("publisher") else ""
            lines.append(f"- {pub}{n.get('title', '?')}")

    text = "\n".join(lines)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n... (이하 생략)"
    return text
