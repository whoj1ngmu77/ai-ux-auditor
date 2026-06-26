import asyncio
from app.agents.browser_agent import run_browser_agent
from app.agents.accessibility_agent import run_accessibility_agent

async def test():
    print("Crawling site...")
    browser_result = await run_browser_agent("https://wikipedia.org")
    print("Running accessibility check...")
    result = run_accessibility_agent(browser_result["html"], "https://wikipedia.org")
    print("Accessibility Score:", result["accessibility_score"])
    print("Issues found:", len(result["issues"]))
    print("Summary:", result["summary"])

asyncio.run(test())
