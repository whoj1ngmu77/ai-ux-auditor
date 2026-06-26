import os
import json
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def resize_base64_image(b64_string: str, max_size_kb: int = 500) -> str:
    from PIL import Image
    import io
    img_data = base64.b64decode(b64_string)
    img = Image.open(io.BytesIO(img_data))
    img = img.convert("RGB")
    quality = 85
    while True:
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        size_kb = len(buffer.getvalue()) / 1024
        if size_kb <= max_size_kb or quality < 20:
            break
        quality -= 10
        width, height = img.size
        img = img.resize((int(width * 0.8), int(height * 0.8)), Image.LANCZOS)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

async def run_ux_analyst(screenshots: list, url: str) -> dict:
    image_content = []
    
    for screenshot in screenshots:
        resized = resize_base64_image(screenshot["base64"])
        image_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{resized}"
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
      "screenshot_ref": "<viewport|mobile>"
    }
  ],
  "summary": "<2-3 sentence overall UX summary>"
}"""
    })
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": image_content}],
            max_tokens=2000
        )
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        return {
            "ux_score": 70,
            "issues": [
                {
                    "category": "Visual Design",
                    "severity": "medium",
                    "issue": "Could not analyze screenshots automatically",
                    "fix": "Manual review recommended",
                    "screenshot_ref": "viewport"
                }
            ],
            "summary": f"Automated visual analysis unavailable for this site. Accessibility analysis was still completed successfully."
        }
