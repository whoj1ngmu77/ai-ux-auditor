import asyncio
import base64
import os
from playwright.async_api import async_playwright
from pathlib import Path

SCREENSHOTS_DIR = Path("app/screenshots")
SCREENSHOTS_DIR.mkdir(exist_ok=True)

async def run_browser_agent(url: str) -> dict:
    screenshots = []
    page_html = ""
    page_title = ""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception:
            await page.goto(url, wait_until="commit", timeout=60000)
        
        await page.wait_for_timeout(3000)
        
        page_title = await page.title()
        page_html = await page.content()
        
        full_path = SCREENSHOTS_DIR / "full_page.png"
        await page.screenshot(path=str(full_path), full_page=True, timeout=30000)
        with open(full_path, "rb") as f:
            screenshots.append({
                "name": "full_page",
                "base64": base64.b64encode(f.read()).decode("utf-8")
            })
        
        viewport_path = SCREENSHOTS_DIR / "viewport.png"
        await page.screenshot(path=str(viewport_path), full_page=False, timeout=30000)
        with open(viewport_path, "rb") as f:
            screenshots.append({
                "name": "viewport",
                "base64": base64.b64encode(f.read()).decode("utf-8")
            })
        
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.wait_for_timeout(1000)
        mobile_path = SCREENSHOTS_DIR / "mobile.png"
        await page.screenshot(path=str(mobile_path), full_page=True, timeout=30000)
        with open(mobile_path, "rb") as f:
            screenshots.append({
                "name": "mobile",
                "base64": base64.b64encode(f.read()).decode("utf-8")
            })
        
        await browser.close()
    
    return {
        "url": url,
        "title": page_title,
        "html": page_html,
        "screenshots": screenshots
    }
