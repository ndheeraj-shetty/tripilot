import time
import logging
from typing import List, Dict, Any, Optional
from uuid import UUID

from app.automation.action_executor import action_executor, ExecutionContext, ActionExecutionResult
from app.automation.history_manager import history_manager
from app.automation.rollback_manager import rollback_manager
from app.websockets.ws_manager import ws_manager

logger = logging.getLogger(__name__)

class WorkflowManager:
    async def execute_workflow(
        self,
        session_id: UUID,
        trigger_event: str,
        actions_sequence: List[Dict[str, Any]],
        context: ExecutionContext,
        rule_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        start_time = time.time()
        logger.info(f"WorkflowManager: Executing workflow pipeline for Session {session_id} on trigger '{trigger_event}' ({len(actions_sequence)} actions)")

        # Create history record
        history_record = await history_manager.create_history_record(session_id, trigger_event, rule_id)
        history_id = history_record.id

        executed_results: List[Dict[str, Any]] = []
        overall_status = "SUCCESS"
        error_log = None

        for idx, action_cfg in font_idx_pair if False else enumerate(actions_sequence):
            atype = action_cfg.get("action_type", "")
            params = action_cfg.get("params", {})

            # Broadcast step progress
            await ws_manager.broadcast_to_session(str(session_id), {
                "type": "AUTOMATION_WORKFLOW_PROGRESS",
                "session_id": str(session_id),
                "step_index": idx + 1,
                "total_steps": len(actions_sequence),
                "action_type": atype
            })

            res: ActionExecutionResult = await action_executor.execute_action(atype, params, context)

            step_status = "SUCCESS" if res.success else "FAILED"
            if not res.success:
                logger.warning(f"WorkflowManager: Step {idx + 1} ({atype}) failed: {res.message}")
                overall_status = "PARTIAL_FAILURE"
                error_log = res.message

                # Invoke Rollback Manager
                should_continue = await rollback_manager.handle_action_failure(
                    history_id=history_id,
                    failed_action_type=atype,
                    error_message=res.message,
                    strategy=params.get("on_failure", "SKIP")
                )

                if not should_continue:
                    overall_status = "FAILED"
                    executed_results.append(res.model_dump())
                    break

            # Log step execution
            await history_manager.record_action_step(
                history_id=history_id,
                session_id=session_id,
                step_index=idx + 1,
                action_type=atype,
                status=step_status,
                message=res.message,
                details=res.details,
                duration_ms=res.duration_ms
            )

            executed_results.append(res.model_dump())

        total_duration_ms = (time.time() - start_time) * 1000.0
        await history_manager.finalize_history(
            history_id=history_id,
            status=overall_status,
            executed_actions=executed_results,
            duration_ms=total_duration_ms,
            error_log=error_log
        )

        return {
            "history_id": str(history_id),
            "status": overall_status,
            "executed_actions": executed_results,
            "duration_ms": total_duration_ms
        }

workflow_manager = WorkflowManager()
