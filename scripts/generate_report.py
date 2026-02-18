"""Generate daily market news report using Claude Agent SDK with WebSearch."""

import asyncio
import os
import pathlib
from datetime import datetime, timezone, timedelta

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)


async def main():
    # Read SKILL.md as the system prompt
    skill_path = pathlib.Path(__file__).parent.parent / "skill" / "SKILL.md"
    skill_content = skill_path.read_text(encoding="utf-8")

    # Strip YAML frontmatter (between --- delimiters) for cleaner system prompt
    if skill_content.startswith("---"):
        end = skill_content.index("---", 3)
        skill_content = skill_content[end + 3 :].strip()

    # Beijing time date
    cst = timezone(timedelta(hours=8))
    now_cst = datetime.now(cst)
    today_cn = now_cst.strftime("%Y年%m月%d日")
    date_str = now_cst.strftime("%Y-%m-%d")

    print(f"Generating market report for {today_cn} ({date_str})...")

    # Collect all text output from the agent
    report_parts = []
    result_info = None

    async for message in query(
        prompt=f"今天是{today_cn}。请按照指令生成今日每日市场简报。",
        options=ClaudeAgentOptions(
            system_prompt=skill_content,
            allowed_tools=["WebSearch"],
            model="claude-sonnet-4-20250514",
            max_turns=15,
            permission_mode="bypassPermissions",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    report_parts.append(block.text)
        elif isinstance(message, ResultMessage):
            result_info = message

    if result_info and result_info.is_error:
        print(f"Error: Agent returned error - {result_info.subtype}")
        raise SystemExit(1)

    report = "\n".join(report_parts)

    if not report.strip():
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

    if result_info:
        cost = getattr(result_info, "total_cost_usd", "N/A")
        turns = getattr(result_info, "num_turns", "N/A")
        print(f"Cost: ${cost}, Turns: {turns}")

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
