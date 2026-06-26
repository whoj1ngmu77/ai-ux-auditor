from pydantic import BaseModel
from typing import List, Optional

class AuditRequest(BaseModel):
    url: str

class UXIssue(BaseModel):
    category: str
    severity: str
    issue: str
    fix: str
    screenshot_ref: Optional[str] = None

class AccessibilityIssue(BaseModel):
    rule: str
    severity: str
    element: str
    fix: str

class AuditReport(BaseModel):
    url: str
    overall_score: int
    ux_score: int
    accessibility_score: int
    ux_issues: List[UXIssue]
    accessibility_issues: List[AccessibilityIssue]
    summary: str
    top_fixes: List[str]

class AuditResponse(BaseModel):
    status: str
    report: Optional[AuditReport] = None
    error: Optional[str] = None
