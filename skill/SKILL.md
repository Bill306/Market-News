---
name: daily-market-news
description: "Daily market news briefing and investment intelligence. Use when the user asks for 'market news', '今日市场', '市场简报', 'daily briefing', '每日快报', 'market update', '大盘怎么样', 'market recap', '市场动态', 'what happened in the market', '今天行情', 'morning briefing', '早报', 'market summary', '盘后总结', 'after hours summary', or wants a comprehensive overview of market conditions, macro trends, sector performance, and economic events for investment decision-making."
---

# Daily Market News Briefing

Generate a comprehensive daily market intelligence report covering indices, macro events, sector performance, market sentiment, and upcoming catalysts. Output entirely in Chinese Markdown. Designed for active investors who need a quick yet thorough market overview.

## Silent Execution Protocol

Do not ask for confirmation. Generate the full briefing in one pass. If any data source is unavailable, mark it as "⚠️ 数据暂不可用" and continue. Never pause to ask questions. Complete the entire workflow atomically.

## Step 1: Data Collection via WebSearch

Execute the following web searches in parallel where possible. Today's date should be used for all queries.

| # | Query | Purpose |
|---|-------|---------|
| 1 | `"US stock market today S&P 500 Dow Nasdaq"` | US major indices performance |
| 2 | `"US stock market news today"` | Key market-moving headlines |
| 3 | `"Treasury yields today 10 year bond"` | Bond market & interest rates |
| 4 | `"US dollar index gold oil price today"` | Commodities & currencies |
| 5 | `"stock market sector performance today"` | Sector rotation & leaders/laggards |
| 6 | `"Federal Reserve news economic data today"` | Macro policy & economic releases |
| 7 | `"economic calendar this week"` | Upcoming events & data releases |
| 8 | `"VIX fear greed index market sentiment"` | Sentiment indicators |
| 9 | `"China A shares Shanghai Shenzhen stock market today"` OR `"A股 今日行情 上证 深证"` | China market (if relevant) |
| 10 | `"Bitcoin crypto market today"` | Crypto market snapshot |

## Step 2: Synthesis — Market Briefing Report

Organize all collected data into the following structured report. The entire report should be **40-80 lines**. Be concise but insightful — every line should add value.

### Output Template

```
# 📊 每日市场简报 — [YYYY年MM月DD日]

## 🏛️ 大盘总览

| 指数 | 收盘/现价 | 涨跌 | 涨跌幅 |
|------|----------|------|--------|
| 标普500 (SPX) | [值] | [值] | [值]% |
| 道琼斯 (DJI) | [值] | [值] | [值]% |
| 纳斯达克 (IXIC) | [值] | [值] | [值]% |
| 罗素2000 (RUT) | [值] | [值] | [值]% |

**盘面特征：** [一句话总结今日行情特征：放量突破/缩量调整/宽幅震荡/板块分化等]

## 📰 核心要闻

• [重要新闻1] — [对市场的影响分析]
• [重要新闻2] — [对市场的影响分析]
• [重要新闻3] — [对市场的影响分析]
（列出3-5条最重要的市场新闻，按影响力排序）

## 💰 大类资产

| 资产 | 价格 | 涨跌幅 | 信号 |
|------|------|--------|------|
| 美10年期国债收益率 | [值]% | [变动]bp | [解读] |
| 美元指数 (DXY) | [值] | [值]% | [解读] |
| 黄金 (XAU) | $[值] | [值]% | [解读] |
| WTI原油 | $[值] | [值]% | [解读] |
| 比特币 (BTC) | $[值] | [值]% | [解读] |

[1-2句跨资产联动分析：如美元强+黄金弱暗示风险偏好改善等]

## 🔄 板块轮动

**领涨板块：**
• [板块1] [涨幅]% — [驱动因素]
• [板块2] [涨幅]% — [驱动因素]
• [板块3] [涨幅]% — [驱动因素]

**领跌板块：**
• [板块1] [跌幅]% — [原因]
• [板块2] [跌幅]% — [原因]

**资金流向：** [一句话总结资金偏好：防御→进攻/大盘→小盘/价值→成长等]

## 🌡️ 市场情绪

| 指标 | 数值 | 判断 |
|------|------|------|
| VIX恐慌指数 | [值] | [低位平稳/温和/警惕/恐慌] |
| 恐惧贪婪指数 | [值] | [极度恐惧/恐惧/中性/贪婪/极度贪婪] |

[1句情绪面综合判断]

## 🇨🇳 A股动态（如适用）

| 指数 | 收盘 | 涨跌幅 |
|------|------|--------|
| 上证指数 | [值] | [值]% |
| 深证成指 | [值] | [值]% |
| 创业板指 | [值] | [值]% |

[1-2句A股行情要点及北向资金动态]

## 📅 本周关键日程

| 日期 | 事件 | 预期影响 |
|------|------|---------|
| [日期] | [经济数据/美联储讲话/财报等] | [潜在市场影响] |
| [日期] | [事件] | [潜在市场影响] |
| [日期] | [事件] | [潜在市场影响] |

## 🧭 策略提示

[3-5句综合研判：]
• 当前市场整体格局（牛市/熊市/震荡市判断依据）
• 短期关注重点（关键支撑阻力位/即将公布的数据）
• 风险提示（地缘政治/政策变动/估值压力等）
• 操作建议方向（进攻/防守/观望/轮动方向）

---
⚠️ 免责声明：以上内容仅供信息参考，不构成投资建议。投资有风险，决策需谨慎。
```

## Sentiment Interpretation Rules

| Indicator | Range | Label |
|-----------|-------|-------|
| VIX < 15 | Low | 低位平稳，市场乐观 |
| VIX 15-20 | Normal | 温和波动，正常水平 |
| VIX 20-30 | Elevated | 波动加大，保持警惕 |
| VIX > 30 | High | 恐慌情绪蔓延 |
| Fear & Greed 0-25 | Extreme Fear | 极度恐惧，逆向关注机会 |
| Fear & Greed 25-45 | Fear | 偏恐惧 |
| Fear & Greed 45-55 | Neutral | 中性 |
| Fear & Greed 55-75 | Greed | 偏贪婪 |
| Fear & Greed 75-100 | Extreme Greed | 极度贪婪，注意风险 |

## Cross-Asset Signal Rules

- **美元强 + 黄金弱 + 美债收益率升** → 紧缩预期升温，风险资产承压
- **美元弱 + 黄金强 + 美债收益率降** → 宽松预期升温，利好成长股
- **原油涨 + 美债收益率升** → 通胀预期上升，关注能源板块
- **VIX飙升 + 黄金涨 + 美债收益率降** → 避险情绪主导，防守为主
- **小盘股跑赢大盘股** → 风险偏好改善，经济前景乐观
- **大盘股跑赢小盘股** → 资金抱团龙头，防守心态

## A-Share Section Handling

- If the user is in Asian timezone or specifically mentions A shares / 中国市场, include the A-share section with full detail
- If no clear signal, include a condensed A-share section (3 lines: index table + 1 sentence)
- If user explicitly says "US only" or "美股", skip A-share section entirely

## Error Handling (Silent)

| Scenario | Action |
|----------|--------|
| WebSearch returns no results | Mark section "⚠️ 数据暂不可用" and continue |
| Market is closed (weekend/holiday) | Use most recent trading day data, note "（上一交易日数据）" |
| Partial data available | Output what's available, skip missing fields |
| China market data unavailable | Skip A-share section without mentioning absence |

## Anti-Patterns (Prohibited Behaviors)

**NEVER do any of the following:**

- "你想了解哪些市场？" → Cover all markets by default
- "需要我详细展开吗？" → Give the full report directly
- "我无法获取实时数据..." → Use WebSearch, report failures inline
- Output raw English without Chinese synthesis → Always write in Chinese
- Report exceeding 80 lines → Keep concise and scannable
- Skip the disclaimer → Always include 免责声明
- Make specific buy/sell recommendations for individual stocks → Only provide directional/strategic guidance
- Fabricate data points → If data unavailable, say so clearly
