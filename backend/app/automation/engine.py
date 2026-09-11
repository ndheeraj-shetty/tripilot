import logging
from typing import Dict, List, Type, Any, Optional
from app.automation.handlers.base_handler import BaseActionHandler, ActionContext, ActionResult
from app.automation.handlers.model_actions import SaveBestModelHandler
from app.automation.handlers.log_actions import CompressLogsHandler
from app.automation.handlers.system_actions import SystemPowerHandler, NotifyUserHandler

logger = logging.getLogger(__name__)

class AutomationEngine:
    def __init__(self):
        self.handlers: Dict[str, BaseActionHandler] = {}
        self.register_handler(SaveBestModelHandler())
        self.register_handler(CompressLogsHandler())
        self.register_handler(SystemPowerHandler())
        self.register_handler(NotifyUserHandler())

    def register_handler(self, handler: BaseActionHandler):
        self.handlers[handler.action_type] = handler
        logger.info(f"Registered Automation Action Handler: {handler.action_type}")

    async def execute_rule_pipeline(self, rule_name: str, actions_sequence: List[Dict[str, Any]], context: ActionContext) -> List[ActionResult]:
        results: List[ActionResult] = []
        logger.info(f"Executing Automation Pipeline '{rule_name}' with {len(actions_sequence)} actions for Session {context.session_id}")

        for action_config in actions_sequence:
            atype = action_config.get("action_type")
            params = action_config.get("params", {})

            handler = self.handlers.get(atype)
            if not handler:
                logger.error(f"No registered handler for action type: {atype}")
                results.append(ActionResult(
                    success=False,
                    action_type=atype or "UNKNOWN",
                    message=f"Handler {atype} not registered.",
                    details={}
                ))
                continue

            try:
                res = await handler.execute(params, context)
                results.append(res)
                logger.info(f"Action [{atype}] Execution Result: Success={res.success}, Message={res.message}")
            except Exception as e:
                logger.error(f"Error executing action {atype}: {e}")
                results.append(ActionResult(
                    success=False,
                    action_type=atype,
                    message=f"Execution exception: {str(e)}",
                    details={"error": str(e)}
                ))

        return results
