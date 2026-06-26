from bs4 import BeautifulSoup
import re

def run_accessibility_agent(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    issues = []

    images = soup.find_all("img")
    for img in images:
        if not img.get("alt"):
            issues.append({
                "rule": "WCAG 1.1.1 - Non-text Content",
                "severity": "critical",
                "element": str(img)[:100],
                "fix": "Add descriptive alt attribute to this image"
            })

    inputs = soup.find_all("input")
    for inp in inputs:
        input_id = inp.get("id")
        if input_id:
            label = soup.find("label", {"for": input_id})
            if not label:
                issues.append({
                    "rule": "WCAG 1.3.1 - Info and Relationships",
                    "severity": "critical",
                    "element": str(inp)[:100],
                    "fix": f"Add a <label for='{input_id}'> element for this input"
                })
        else:
            if not inp.get("aria-label") and not inp.get("aria-labelledby"):
                issues.append({
                    "rule": "WCAG 1.3.1 - Info and Relationships",
                    "severity": "high",
                    "element": str(inp)[:100],
                    "fix": "Add aria-label or associate a label element to this input"
                })

    links = soup.find_all("a")
    for link in links:
        text = link.get_text(strip=True)
        if not text and not link.get("aria-label"):
            issues.append({
                "rule": "WCAG 2.4.4 - Link Purpose",
                "severity": "high",
                "element": str(link)[:100],
                "fix": "Add descriptive text or aria-label to this link"
            })
        if text.lower() in ["click here", "read more", "here", "more"]:
            issues.append({
                "rule": "WCAG 2.4.4 - Link Purpose",
                "severity": "medium",
                "element": str(link)[:100],
                "fix": f"Replace '{text}' with descriptive link text explaining the destination"
            })

    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    heading_levels = [int(h.name[1]) for h in headings]
    for i in range(1, len(heading_levels)):
        if heading_levels[i] - heading_levels[i-1] > 1:
            issues.append({
                "rule": "WCAG 1.3.1 - Heading Structure",
                "severity": "medium",
                "element": str(headings[i])[:100],
                "fix": f"Heading jumps from h{heading_levels[i-1]} to h{heading_levels[i]}, fix heading hierarchy"
            })

    h1_tags = soup.find_all("h1")
    if len(h1_tags) == 0:
        issues.append({
            "rule": "WCAG 1.3.1 - Page Structure",
            "severity": "high",
            "element": "<page>",
            "fix": "Add exactly one H1 tag to define the main page heading"
        })
    elif len(h1_tags) > 1:
        issues.append({
            "rule": "WCAG 1.3.1 - Page Structure",
            "severity": "medium",
            "element": "<page>",
            "fix": f"Page has {len(h1_tags)} H1 tags, reduce to exactly one"
        })

    buttons = soup.find_all("button")
    for button in buttons:
        text = button.get_text(strip=True)
        if not text and not button.get("aria-label"):
            issues.append({
                "rule": "WCAG 4.1.2 - Name, Role, Value",
                "severity": "critical",
                "element": str(button)[:100],
                "fix": "Add descriptive text or aria-label to this button"
            })

    html_tag = soup.find("html")
    if html_tag and not html_tag.get("lang"):
        issues.append({
            "rule": "WCAG 3.1.1 - Language of Page",
            "severity": "high",
            "element": "<html>",
            "fix": "Add lang attribute to <html> tag e.g. <html lang='en'>"
        })

    meta_viewport = soup.find("meta", {"name": "viewport"})
    if not meta_viewport:
        issues.append({
            "rule": "WCAG 1.4.4 - Resize Text",
            "severity": "high",
            "element": "<head>",
            "fix": "Add <meta name='viewport' content='width=device-width, initial-scale=1'>"
        })

    critical = [i for i in issues if i["severity"] == "critical"]
    high = [i for i in issues if i["severity"] == "high"]
    medium = [i for i in issues if i["severity"] == "medium"]
    low = [i for i in issues if i["severity"] == "low"]

    deductions = (len(critical) * 20) + (len(high) * 10) + (len(medium) * 5) + (len(low) * 2)
    score = max(0, 100 - deductions)

    return {
        "accessibility_score": score,
        "issues": issues,
        "summary": f"Found {len(issues)} accessibility issues: {len(critical)} critical, {len(high)} high, {len(medium)} medium, {len(low)} low"
    }
