import asyncio
from app.agents.browser_agent import run_browser_agent
from app.agents.ux_analyst import run_ux_analyst

async def test():
    print("Crawling site...")
    browser_result = await run_browser_agent("https://example.com")
    print("Running UX analysis...")
    ux_result = await run_ux_analyst(browser_result["screenshots"], "https://example.com")
    print("UX Score:", ux_result["ux_score"])
    print("Issues found:", len(ux_result["issues"]))
    print("Summary:", ux_result["summary"])

asyncio.run(test())
