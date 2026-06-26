import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def run_ux_analyst(screenshots: list, url: str) -> dict:
    image_content = []
    
    for screenshot in screenshots:
        image_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{screenshot['base64']}"
            }
        })
        image_content.append({
            "type": "text",
            "text": f"Above is the {screenshot['name']} screenshot of {url}"
        })
    
    image_content.append({
        "type": "text",
        "text": """Analyze these screenshots for UX issues. Return ONLY valid JSON, no markdown, no backticks, in this exact format:
{
  "ux_score": <number 0-100>,
  "issues": [
    {
      "category": "<Navigation|Visual Design|Mobile UX|Content|CTA|Forms|Performance>",
      "severity": "<critical|high|medium|low>",
      "issue": "<what the problem is>",
      "fix": "<how to fix it>",
      "screenshot_ref": "<full_page|viewport|mobile>"
    }
  ],
  "summary": "<2-3 sentence overall UX summary>"
}"""
    })
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": image_content}],
        max_tokens=2000
    )
    
    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)
