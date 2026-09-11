import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.future import select

from app.core.database import AsyncSessionLocal
from app.domain.models.models import AutomationRule
from app.automation.workflow_manager import workflow_manager
from app.automation.action_executor import ExecutionContext

logger = logging.getLogger(__name__)

class AutomationRuleEngine:
    async def evaluate_and_trigger(
        self,
        trigger_event: str,
        session_id: UUID,
        project_id: UUID,
        output_dir: str,
        checkpoint_dir: str,
        best_checkpoint_path: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        logger.info(f"AutomationRuleEngine: Evaluating rules for trigger '{trigger_event}' on Session {session_id}")

        context = ExecutionContext(
            session_id=str(session_id),
            project_id=str(project_id),
            output_dir=output_dir,
            checkpoint_dir=checkpoint_dir,
            best_checkpoint_path=best_checkpoint_path
        )

        matched_results: List[Dict[str, Any]] = []

        try:
            async with AsyncSessionLocal() as db:
                # Query active rules matching trigger_event (Project-specific or Global)
                result = await db.execute(
                    select(AutomationRule).where(
                        AutomationRule.trigger_event == trigger_event,
                        AutomationRule.is_active == True
                    )
                )
                rules = result.scalars().all()

                if not rules:
                    # Provide default built-in workflow fallback if no DB rule configured yet
                    default_actions = self.get_default_workflow_actions(trigger_event)
                    if default_actions:
                        res = await workflow_manager.execute_workflow(
                            session_id=session_id,
                            trigger_event=trigger_event,
                            actions_sequence=default_actions,
                            context=context
                        )
                        matched_results.append(res)
                    return matched_results

                for rule in rules:
                    if rule.project_id and rule.project_id != project_id:
                        continue # Skip rules belonging to another project

                    res = await workflow_manager.execute_workflow(
                        session_id=session_id,
                        trigger_event=trigger_event,
                        actions_sequence=rule.actions_sequence,
                        context=context,
                        rule_id=rule.id
                    )
                    matched_results.append(res)

        except Exception as e:
            logger.error(f"AutomationRuleEngine error evaluating rules: {e}")

        return matched_results

    def get_default_workflow_actions(self, trigger_event: str) -> List[Dict[str, Any]]:
        if trigger_event == "ON_SUCCESS":
            return [
                {"action_type": "SAVE_BEST_MODEL", "params": {}},
                {"action_type": "GENERATE_REPORT", "params": {}},
                {"action_type": "COMPRESS_LOGS", "params": {}},
                {"action_type": "NOTIFY_USER", "params": {"title": "Training Completed Successfully"}},
                {"action_type": "SYSTEM_SHUTDOWN", "params": {"grace_period_sec": 30}}
            ]
        elif trigger_event == "ON_FAILED":
            return [
                {"action_type": "GENERATE_FAILURE_REPORT", "params": {}},
                {"action_type": "COMPRESS_LOGS", "params": {}},
                {"action_type": "NOTIFY_USER", "params": {"title": "Training Job Failed"}}
            ]
        elif trigger_event == "ON_OVERHEATING":
            return [
                {"action_type": "NOTIFY_USER", "params": {"title": "GPU Overheating Warning"}}
            ]
        return []

automation_rule_engine = AutomationRuleEngine()
