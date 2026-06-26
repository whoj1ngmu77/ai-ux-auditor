import asyncio
from app.agents.browser_agent import run_browser_agent
from app.agents.ux_analyst import run_ux_analyst
from app.agents.accessibility_agent import run_accessibility_agent
from app.agents.report_agent import run_report_agent

async def test():
    print("Crawling site...")
    browser_result = await run_browser_agent("https://wikipedia.org")
    print("Running UX analysis...")
    ux_result = await run_ux_analyst(browser_result["screenshots"], "https://wikipedia.org")
    print("Running accessibility check...")
    accessibility_result = run_accessibility_agent(browser_result["html"], "https://wikipedia.org")
    print("Generating report...")
    report = run_report_agent("https://wikipedia.org", ux_result, accessibility_result)
    print("Overall Score:", report["overall_score"])
    print("UX Score:", report["ux_score"])
    print("Accessibility Score:", report["accessibility_score"])
    print("Top Fixes:")
    for i, fix in enumerate(report["top_fixes"], 1):
        print(f"  {i}. {fix}")
    print("Summary:", report["summary"])

asyncio.run(test())
