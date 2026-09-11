import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Callable
from uuid import UUID

from app.core.database import AsyncSessionLocal
from app.domain.models.models import ScheduledAction

logger = logging.getLogger(__name__)

class AutomationScheduler:
    def __init__(self):
        self.scheduled_tasks: Dict[str, asyncio.Task] = {}

    async def schedule_delayed_action(
        self,
        session_id: UUID,
        action_type: str,
        params: Dict[str, Any],
        delay_seconds: int,
        action_callback: Callable[[], Any]
    ) -> UUID:
        scheduled_time = datetime.now() + timedelta(seconds=delay_seconds)
        
        async with AsyncSessionLocal() as db:
            s_obj = ScheduledAction(
                session_id=session_id,
                action_type=action_type,
                params=params,
                scheduled_time=scheduled_time,
                status="PENDING"
            )
            db.add(s_obj)
            await db.commit()
            await db.refresh(s_obj)
            action_id = s_obj.id

        logger.info(f"Scheduler: Action '{action_type}' scheduled in {delay_seconds} seconds (ID={action_id}).")

        async def _delayed_runner():
            await asyncio.sleep(delay_seconds)
            try:
                if asyncio.iscoroutinefunction(action_callback):
                    await action_callback()
                else:
                    action_callback()

                async with AsyncSessionLocal() as db:
                    sa = await db.get(ScheduledAction, action_id)
                    if sa:
                        sa.status = "EXECUTED"
                        await db.commit()
            except Exception as e:
                logger.error(f"Error executing scheduled action {action_id}: {e}")

        task = asyncio.create_task(_delayed_runner())
        self.scheduled_tasks[str(action_id)] = task
        return action_id

    def cancel_scheduled_action(self, action_id: UUID) -> bool:
        sid = str(action_id)
        task = self.scheduled_tasks.pop(sid, None)
        if task and not task.done():
            task.cancel()
            return True
        return False

automation_scheduler = AutomationScheduler()
