"""Generate daily market news report using DeepSeek (Anthropic-compatible) + DuckDuckGo Search."""

import os
import pathlib
import time
from datetime import datetime, timezone, timedelta

import anthropic

# Support both old and new package names
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

# 10 search queries from SKILL.md
SEARCH_QUERIES = [
    "US stock market today S&P 500 Dow Nasdaq",
    "US stock market news today",
    "Treasury yields today 10 year bond",
    "US dollar index gold oil price today",
    "stock market sector performance today",
    "Federal Reserve news economic data today",
    "economic calendar this week",
    "VIX fear greed index market sentiment",
    "China A shares Shanghai Shenzhen stock market today",
    "Bitcoin crypto market today",
]

# Delay between searches to avoid rate limiting (seconds)
SEARCH_DELAY = 2
# Number of retries per search query
MAX_RETRIES = 2
# Delay between retries (seconds)
RETRY_DELAY = 5


def run_searches() -> str:
    """Execute all 10 web searches and return combined results."""
    ddgs = DDGS()
    all_results = []

    for i, query in enumerate(SEARCH_QUERIES, 1):
        print(f"  [{i}/10] Searching: {query}")

        section = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                results = ddgs.text(query, max_results=5)
                if results:
                    section = f"### Search {i}: {query}\n"
                    for r in results:
                        section += f"- **{r['title']}**: {r['body']}\n"
                    break
                else:
                    print(f"    Attempt {attempt}: empty results, retrying...")
            except Exception as e:
                print(f"    Attempt {attempt} failed: {e}")

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

        if section is None:
            all_results.append(
                f"### Search {i}: {query}\n"
                f"No results returned after {MAX_RETRIES} attempts.\n"
            )
        else:
            all_results.append(section)

        # Delay between queries to avoid rate limiting
        if i < len(SEARCH_QUERIES):
            time.sleep(SEARCH_DELAY)

    return "\n".join(all_results)


# Price data comes from Yahoo Finance, not from search snippets.
# (label, ticker, unit) — unit "yield" means the quote is a percentage yield.
MARKET_TICKERS = [
    ("标普500 (SPX)", "^GSPC", "index"),
    ("道琼斯 (DJI)", "^DJI", "index"),
    ("纳斯达克 (IXIC)", "^IXIC", "index"),
    ("罗素2000 (RUT)", "^RUT", "index"),
    ("美10年期国债收益率", "^TNX", "yield"),
    ("美元指数 (DXY)", "DX-Y.NYB", "index"),
    ("黄金期货 (GC)", "GC=F", "usd"),
    ("WTI原油期货 (CL)", "CL=F", "usd"),
    ("比特币 (BTC)", "BTC-USD", "usd"),
    ("VIX波动率指数", "^VIX", "index"),
    ("上证指数", "000001.SS", "index"),
    ("深证成指", "399001.SZ", "index"),
]


def fetch_market_data() -> str:
    """Fetch latest close and change for each ticker; returns a Markdown table.

    Rows that fail are marked as unavailable so the model never invents them.
    """
    import yfinance as yf

    rows = ["| 资产 | 最新价 | 涨跌 | 涨跌幅 | 数据日期 |", "|---|---|---|---|---|"]
    ok = 0
    for label, ticker, unit in MARKET_TICKERS:
        try:
            hist = yf.Ticker(ticker).history(period="7d", auto_adjust=False)["Close"].dropna()
            if len(hist) < 2:
                raise ValueError("not enough history")
            last, prev = float(hist.iloc[-1]), float(hist.iloc[-2])
            date = hist.index[-1].strftime("%Y-%m-%d")
            pct = (last / prev - 1) * 100
            if unit == "yield":
                rows.append(f"| {label} | {last:.3f}% | {(last - prev) * 100:+.1f}bp | — | {date} |")
            else:
                prefix = "$" if unit == "usd" else ""
                rows.append(
                    f"| {label} | {prefix}{last:,.2f} | {last - prev:+,.2f} | {pct:+.2f}% | {date} |"
                )
            ok += 1
        except Exception as e:  # network / delisted / empty
            print(f"    {ticker} failed: {e}")
            rows.append(f"| {label} | ⚠️ 数据暂不可用 | — | — | — |")
    print(f"  Market data: {ok}/{len(MARKET_TICKERS)} tickers fetched")
    return "\n".join(rows)


def generate_report(system_prompt: str, search_results: str, today_cn: str, market_data: str = "") -> str:
    """Call DeepSeek API (Anthropic-compatible) to synthesize the market report."""
    client = anthropic.Anthropic(
        auth_token=os.environ["ANTHROPIC_AUTH_TOKEN"],
        base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic"),
    )

    model = os.environ.get("ANTHROPIC_MODEL", "deepseek-chat")

    user_message = (
        f"今天是{today_cn}。\n\n"
        f"## 行情数据（来自 Yahoo Finance，权威来源）\n\n"
        f"{market_data}\n\n"
        f"指数、利率、汇率、商品、加密货币、VIX、A股的数字必须直接使用上表，"
        f"不得用搜索摘要中的数字替换或补充。上表标为不可用的项目，报告中也标为不可用。"
        f"若数据日期早于今天，说明为上一交易日数据。\n\n"
        f"## 新闻与背景（来自网络搜索，用于要闻、板块、日程和解读）\n\n"
        f"{search_results}\n\n"
        f"请根据以上数据，按照指令生成今日每日市场简报。"
    )

    print(f"Calling DeepSeek API (model={model})...")
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message},
        ],
    )

    # Extract text from response content blocks
    parts = []
    for block in response.content:
        if block.type == "text":
            parts.append(block.text)

    return "\n".join(parts)


def main():
    # Read SKILL.md as the system prompt
    skill_path = pathlib.Path(__file__).parent.parent / "skill" / "SKILL.md"
    skill_content = skill_path.read_text(encoding="utf-8")

    # Strip YAML frontmatter (between --- delimiters)
    if skill_content.startswith("---"):
        end = skill_content.index("---", 3)
        skill_content = skill_content[end + 3:].strip()

    # Beijing time date
    cst = timezone(timedelta(hours=8))
    now_cst = datetime.now(cst)
    today_cn = now_cst.strftime("%Y年%m月%d日")
    date_str = now_cst.strftime("%Y-%m-%d")

    print(f"Generating market report for {today_cn} ({date_str})...")

    # Step 1: Web searches
    print("Step 1: Running web searches...")
    search_results = run_searches()

    # Step 2: Prices from Yahoo Finance
    print("Step 2: Fetching market data...")
    market_data = fetch_market_data()

    # Step 3: Synthesize report via DeepSeek
    print("Step 3: Synthesizing report...")
    report = generate_report(skill_content, search_results, today_cn, market_data)

    if not report or not report.strip():
        print("Error: Generated report is empty")
        raise SystemExit(1)

    # Save report to reports/ directory
    report_dir = pathlib.Path(__file__).parent.parent / "reports"
    report_dir.mkdir(exist_ok=True)
    report_file = report_dir / f"{date_str}.md"
    report_file.write_text(report, encoding="utf-8")
    print(f"Report saved to {report_file}")

    # Write outputs for GitHub Actions
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"report_file=reports/{date_str}.md\n")
            f.write(f"report_date={today_cn}\n")

    print("Done.")


if __name__ == "__main__":
    main()
