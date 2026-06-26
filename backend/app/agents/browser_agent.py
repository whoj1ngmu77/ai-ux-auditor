import asyncio
import base64
import os
from playwright.async_api import async_playwright
from pathlib import Path

SCREENSHOTS_DIR = Path("app/screenshots")
SCREENSHOTS_DIR.mkdir(exist_ok=True)

async def run_browser_agent(url: str) -> dict:
    screenshots = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-extensions",
                "--disable-images",
                "--single-process",
                "--memory-pressure-off",
                "--max_old_space_size=256",
            ]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            java_script_enabled=True,
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception:
            await page.goto(url, wait_until="commit", timeout=60000)
        
        await page.wait_for_timeout(2000)
        
        page_title = await page.title()
        page_html = await page.content()
        
        viewport_path = SCREENSHOTS_DIR / "viewport.png"
        await page.screenshot(path=str(viewport_path), full_page=False, timeout=30000)
        with open(viewport_path, "rb") as f:
            screenshots.append({
                "name": "viewport",
                "base64": base64.b64encode(f.read()).decode("utf-8")
            })
        
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.wait_for_timeout(500)
        mobile_path = SCREENSHOTS_DIR / "mobile.png"
        await page.screenshot(path=str(mobile_path), full_page=False, timeout=30000)
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
