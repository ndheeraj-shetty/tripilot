from fastapi import APIRouter, Depends
from typing import Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel

from app.analytics.comparison_service import comparison_service
from app.analytics.analytics_service import analytics_service

router = APIRouter(tags=["Analytics & Model Comparison"])

class ComparePayload(BaseModel):
    session_a_id: UUID
    session_b_id: UUID

@router.get("/analytics")
async def get_analytics(session_id: UUID):
    # Aggregated metrics fallback
    metrics_mock = [{"loss": 0.5, "val_loss": 0.55}, {"loss": 0.3, "val_loss": 0.45}]
    telemetry_mock = [{"gpu_utilization_pct": 85.0}]
    insights = analytics_service.generate_ai_insights(metrics_mock, telemetry_mock)
    
    return {
        "session_id": session_id,
        "metrics_summary": {"final_loss": 0.30, "best_accuracy": 0.94},
        "insights": insights
    }

@router.post("/compare")
async def compare_training_runs(payload: ComparePayload):
    res = await comparison_service.compare_sessions(payload.session_a_id, payload.session_b_id)
    return res
