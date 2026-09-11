import logging
from typing import Dict, Any, List, Optional
from uuid import UUID

from app.core.database import AsyncSessionLocal
from app.domain.models.models import AutomationHistory, ActionExecution

logger = logging.getLogger(__name__)

class AutomationHistoryManager:
    async def create_history_record(
        self,
        session_id: UUID,
        trigger_event: str,
        rule_id: Optional[UUID] = None
    ) -> AutomationHistory:
        try:
            async with AsyncSessionLocal() as db:
                record = AutomationHistory(
                    rule_id=rule_id,
                    session_id=session_id,
                    trigger_event=trigger_event,
                    status="EXECUTING",
                    executed_actions=[],
                    duration_ms=0.0
                )
                db.add(record)
                await db.commit()
                await db.refresh(record)
                return record
        except Exception as e:
            logger.warning(f"HistoryManager: DB unavailable ({e}). Using transient record.")
            return AutomationHistory(
                id=UUID('00000000-0000-0000-0000-000000000000'),
                rule_id=rule_id,
                session_id=session_id,
                trigger_event=trigger_event,
                status="EXECUTING",
                executed_actions=[],
                duration_ms=0.0
            )

    async def record_action_step(
        self,
        history_id: UUID,
        session_id: UUID,
        step_index: int,
        action_type: str,
        status: str,
        message: str,
        details: Dict[str, Any],
        duration_ms: float
    ):
        try:
            async with AsyncSessionLocal() as db:
                db.add(ActionExecution(
                    history_id=history_id,
                    session_id=session_id,
                    step_index=step_index,
                    action_type=action_type,
                    status=status,
                    message=message,
                    details=details,
                    duration_ms=duration_ms
                ))
                await db.commit()
        except Exception as e:
            logger.warning(f"HistoryManager: Step persistence skipped ({e}).")

    async def finalize_history(
        self,
        history_id: UUID,
        status: str,
        executed_actions: List[Dict[str, Any]],
        duration_ms: float,
        error_log: Optional[str] = None
    ):
        try:
            async with AsyncSessionLocal() as db:
                h_obj = await db.get(AutomationHistory, history_id)
                if h_obj:
                    h_obj.status = status
                    h_obj.executed_actions = executed_actions
                    h_obj.duration_ms = duration_ms
                    h_obj.error_log = error_log
                    await db.commit()
        except Exception as e:
            logger.warning(f"HistoryManager: Finalize persistence skipped ({e}).")

history_manager = AutomationHistoryManager()
