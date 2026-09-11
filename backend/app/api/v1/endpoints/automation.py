from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel

from app.core.database import get_db
from app.domain.models.models import AutomationRule, AutomationHistory, ActionExecution, ScheduledAction
from app.automation.rule_engine import automation_rule_engine
from app.automation.safety_manager import safety_manager
from app.automation.scheduler import automation_scheduler

router = APIRouter(prefix="/automation", tags=["Automation Engine"])

class RuleCreatePayload(BaseModel):
    project_id: Optional[UUID] = None
    name: str
    trigger_event: str # ON_SUCCESS, ON_FAILED, ON_OVERHEATING, ON_DISK_LOW, ON_NAN
    conditions_json: Dict[str, Any] = {}
    actions_sequence: List[Dict[str, Any]]
    is_active: bool = True

class RuleUpdatePayload(BaseModel):
    name: Optional[str] = None
    trigger_event: Optional[str] = None
    conditions_json: Optional[Dict[str, Any]] = None
    actions_sequence: Optional[List[Dict[str, Any]]] = None
    is_active: Optional[bool] = None

class ExecuteWorkflowPayload(BaseModel):
    session_id: UUID
    trigger_event: str
    project_id: UUID
    output_dir: str
    checkpoint_dir: str

class CancelActionPayload(BaseModel):
    session_id: str

@router.post("/rules", status_code=status.HTTP_201_CREATED)
async def create_automation_rule(payload: RuleCreatePayload, db: AsyncSession = Depends(get_db)):
    rule = AutomationRule(
        project_id=payload.project_id,
        name=payload.name,
        trigger_event=payload.trigger_event,
        conditions_json=payload.conditions_json,
        actions_sequence=payload.actions_sequence,
        is_active=payload.is_active
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule

@router.get("/rules")
async def list_automation_rules(project_id: Optional[UUID] = None, db: AsyncSession = Depends(get_db)):
    query = select(AutomationRule)
    if project_id:
        query = query.where(AutomationRule.project_id == project_id)
    result = await db.execute(query)
    rules = result.scalars().all()
    return rules

@router.put("/rules/{rule_id}")
async def update_automation_rule(rule_id: UUID, payload: RuleUpdatePayload, db: AsyncSession = Depends(get_db)):
    rule = await db.get(AutomationRule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Automation rule not found.")

    update_data = payload.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(rule, key, val)
    await db.commit()
    await db.refresh(rule)
    return rule

@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_automation_rule(rule_id: UUID, db: AsyncSession = Depends(get_db)):
    rule = await db.get(AutomationRule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Automation rule not found.")
    await db.delete(rule)
    await db.commit()
    return None

@router.post("/execute")
async def execute_automation_workflow(payload: ExecuteWorkflowPayload):
    results = await automation_rule_engine.evaluate_and_trigger(
        trigger_event=payload.trigger_event,
        session_id=payload.session_id,
        project_id=payload.project_id,
        output_dir=payload.output_dir,
        checkpoint_dir=payload.checkpoint_dir
    )
    return {"results": results}

@router.post("/cancel")
async def cancel_automation_countdown(payload: CancelActionPayload):
    cancelled = safety_manager.cancel_countdown(payload.session_id)
    return {"status": "CANCELLED" if cancelled else "NOT_FOUND", "session_id": payload.session_id}

@router.get("/history")
async def get_automation_history(session_id: Optional[UUID] = None, limit: int = 50, db: AsyncSession = Depends(get_db)):
    query = select(AutomationHistory).order_by(AutomationHistory.created_at.desc()).limit(limit)
    if session_id:
        query = query.where(AutomationHistory.session_id == session_id)
    result = await db.execute(query)
    history = result.scalars().all()
    return history

@router.get("/workflows")
async def get_workflows():
    return {
        "workflows": [
            {
                "id": "post-success",
                "name": "Post-Training Success Auto-Shutdown",
                "trigger_event": "ON_SUCCESS",
                "actions": ["SAVE_BEST_MODEL", "GENERATE_REPORT", "COMPRESS_LOGS", "NOTIFY_USER", "SYSTEM_SHUTDOWN"]
            },
            {
                "id": "post-failure",
                "name": "Training Failure Error Summary",
                "trigger_event": "ON_FAILED",
                "actions": ["GENERATE_FAILURE_REPORT", "COMPRESS_LOGS", "NOTIFY_USER"]
            }
        ]
    }

@router.get("/status")
async def get_automation_status():
    return {
        "safety_manager_active_countdowns": len(safety_manager.active_countdowns),
        "scheduler_active_tasks": len(automation_scheduler.scheduled_tasks)
    }
