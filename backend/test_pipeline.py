import asyncio
from app.graph.pipeline import run_audit_pipeline

async def test():
    print("Running full pipeline...")
    report = await run_audit_pipeline("https://wikipedia.org")
    print("Overall Score:", report["overall_score"])
    print("UX Score:", report["ux_score"])
    print("Accessibility Score:", report["accessibility_score"])
    print("Issues found:", len(report["ux_issues"]) + len(report["accessibility_issues"]))
    print("Top Fixes:")
    for i, fix in enumerate(report["top_fixes"], 1):
        print(f"  {i}. {fix}")
    print("Summary:", report["summary"])

asyncio.run(test())
