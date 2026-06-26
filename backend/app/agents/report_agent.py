import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_report_agent(url: str, ux_result: dict, accessibility_result: dict) -> dict:
    ux_score = ux_result.get("ux_score", 0)
    accessibility_score = accessibility_result.get("accessibility_score", 0)
    overall_score = int((ux_score + accessibility_score) / 2)

    prompt = f"""
You are a UX audit expert. Given the following audit data for {url}, generate a final report summary.

UX Score: {ux_score}/100
Accessibility Score: {accessibility_score}/100
Overall Score: {overall_score}/100

UX Issues:
{json.dumps(ux_result.get("issues", []), indent=2)}

Accessibility Issues:
{json.dumps(accessibility_result.get("issues", []), indent=2)}

Return ONLY valid JSON, no markdown, no backticks, in this exact format:
{{
  "top_fixes": [
    "<most important fix 1>",
    "<most important fix 2>",
    "<most important fix 3>",
    "<most important fix 4>",
    "<most important fix 5>"
  ],
  "summary": "<3-4 sentence executive summary of the audit findings and recommendations>"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    result = json.loads(text)

    return {
        "url": url,
        "overall_score": overall_score,
        "ux_score": ux_score,
        "accessibility_score": accessibility_score,
        "ux_issues": ux_result.get("issues", []),
        "accessibility_issues": accessibility_result.get("issues", []),
        "summary": result["summary"],
        "top_fixes": result["top_fixes"]
    }
