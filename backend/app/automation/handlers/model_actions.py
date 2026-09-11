import os
import shutil
import logging
from typing import Dict, Any
from app.automation.handlers.base_handler import BaseActionHandler, ActionContext, ActionResult

logger = logging.getLogger(__name__)

class SaveBestModelHandler(BaseActionHandler):
    action_type = "SAVE_BEST_MODEL"

    async def execute(self, params: Dict[str, Any], context: ActionContext) -> ActionResult:
        if not context.best_checkpoint_path or not os.path.exists(context.best_checkpoint_path):
            return ActionResult(
                success=False,
                action_type=self.action_type,
                message="Best checkpoint file not found.",
                details={"best_checkpoint_path": context.best_checkpoint_path}
            )

        target_dir = params.get("target_dir", os.path.join(context.output_dir, "best_models"))
        os.makedirs(target_dir, exist_ok=True)

        dest_filename = f"best_model_session_{context.session_id[:8]}{os.path.splitext(context.best_checkpoint_path)[1]}"
        dest_path = os.path.join(target_dir, dest_filename)

        try:
            shutil.copy2(context.best_checkpoint_path, dest_path)
            return ActionResult(
                success=True,
                action_type=self.action_type,
                message=f"Best model saved successfully to {dest_path}",
                details={"saved_path": dest_path}
            )
        except Exception as e:
            return ActionResult(
                success=False,
                action_type=self.action_type,
                message=f"Failed to copy best model: {str(e)}",
                details={"error": str(e)}
            )
