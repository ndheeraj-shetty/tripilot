import os
import zipfile
import logging
from typing import Dict, Any
from app.automation.handlers.base_handler import BaseActionHandler, ActionContext, ActionResult

logger = logging.getLogger(__name__)

class CompressLogsHandler(BaseActionHandler):
    action_type = "COMPRESS_LOGS"

    async def execute(self, params: Dict[str, Any], context: ActionContext) -> ActionResult:
        log_dir = params.get("log_dir", context.output_dir)
        if not os.path.exists(log_dir):
            return ActionResult(
                success=False,
                action_type=self.action_type,
                message=f"Log directory {log_dir} does not exist.",
                details={"log_dir": log_dir}
            )

        zip_path = os.path.join(context.output_dir, f"logs_session_{context.session_id[:8]}.zip")
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(log_dir):
                    for file in files:
                        if file.endswith(('.log', '.txt', '.json')):
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, log_dir)
                            zipf.write(file_path, arcname)

            return ActionResult(
                success=True,
                action_type=self.action_type,
                message=f"Logs compressed into archive {zip_path}",
                details={"zip_path": zip_path}
            )
        except Exception as e:
            return ActionResult(
                success=False,
                action_type=self.action_type,
                message=f"Failed to compress logs: {str(e)}",
                details={"error": str(e)}
            )
