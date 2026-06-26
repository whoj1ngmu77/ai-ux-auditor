import asyncio
from app.agents.browser_agent import run_browser_agent

async def test():
    result = await run_browser_agent("https://example.com")
    print("Title:", result["title"])
    print("Screenshots taken:", len(result["screenshots"]))
    print("HTML length:", len(result["html"]))

asyncio.run(test())
