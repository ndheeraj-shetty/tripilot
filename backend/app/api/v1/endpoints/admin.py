from fastapi import APIRouter, Response
from app.core.metrics import get_system_health, generate_prometheus_metrics

router = APIRouter(prefix="/admin", tags=["Admin & Observability"])

@router.get("/system")
async def get_system_status():
    return get_system_health()

@router.get("/metrics")
async def get_prometheus_metrics():
    content = generate_prometheus_metrics()
    return Response(content=content, media_type="text/plain")

@router.get("/audit")
async def get_audit_logs():
    return {
        "audit_logs": [
            {
                "user": "admin@zombierun.ai",
                "action": "AUTOMATION_RULE_CREATED",
                "resource": "Rule: Post-Training Success Auto-Shutdown",
                "timestamp": "2026-07-30 15:00:00"
            }
        ]
    }
