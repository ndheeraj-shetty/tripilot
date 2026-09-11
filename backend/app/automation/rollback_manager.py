import logging
from typing import Dict, Any, Optional
from uuid import UUID

from app.core.database import AsyncSessionLocal
from app.domain.models.models import RollbackHistory

logger = logging.getLogger(__name__)

class RollbackManager:
    async def handle_action_failure(
        self,
        history_id: UUID,
        failed_action_type: str,
        error_message: str,
        strategy: str = "SKIP" # SKIP, RETRY, REVERT
    ) -> bool:
        """Handles an action step failure, logs rollback strategy, and allows workflow to continue safely."""
        logger.warning(f"Rollback Manager: Action '{failed_action_type}' failed ({error_message}). Strategy applied: {strategy}")

        try:
            async with AsyncSessionLocal() as db:
                db.add(RollbackHistory(
                    history_id=history_id,
                    failed_action_type=failed_action_type,
                    rollback_strategy=strategy,
                    details={"error": error_message}
                ))
                await db.commit()
        except Exception as e:
            logger.error(f"Error persisting rollback log: {e}")

        # If strategy is SKIP, we return True so workflow execution continues to next step
        return strategy == "SKIP"

rollback_manager = RollbackManager()
