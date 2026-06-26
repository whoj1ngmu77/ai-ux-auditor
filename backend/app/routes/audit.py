from fastapi import APIRouter, HTTPException
from app.models.schemas import AuditRequest, AuditResponse, AuditReport
from app.graph.pipeline import run_audit_pipeline

router = APIRouter()

@router.post("/audit", response_model=AuditResponse)
async def run_audit(request: AuditRequest):
    try:
        report = await run_audit_pipeline(request.url)
        return AuditResponse(
            status="success",
            report=AuditReport(**report)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "ok"}
