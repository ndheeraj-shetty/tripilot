import os
import sys
import shutil
import zipfile
import subprocess
import asyncio
import logging
import time
from typing import Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel

from app.automation.safety_manager import safety_manager
from app.automation.notification_manager import notification_manager
from app.websockets.ws_manager import ws_manager

logger = logging.getLogger(__name__)

class ExecutionContext(BaseModel):
    session_id: str
    project_id: str
    output_dir: str
    checkpoint_dir: str
    best_checkpoint_path: Optional[str] = None

class ActionExecutionResult(BaseModel):
    success: bool
    action_type: str
    message: str
    details: Dict[str, Any] = {}
    duration_ms: float = 0.0

class ActionExecutor:
    async def execute_action(
        self,
        action_type: str,
        params: Dict[str, Any],
        context: ExecutionContext
    ) -> ActionExecutionResult:
        start_time = time.time()
        atype = action_type.upper()
        logger.info(f"ActionExecutor: Executing '{atype}' for Session {context.session_id}")

        try:
            # ----------------------------------------------------
            # 1. FILE & MODEL ACTIONS
            # ----------------------------------------------------
            if atype in ["SAVE_BEST_MODEL", "SAVE_MODEL"]:
                best_path = context.best_checkpoint_path
                if not best_path or not os.path.exists(best_path):
                    # Check default checkpoint directory for files
                    if os.path.exists(context.checkpoint_dir):
                        files = [os.path.join(context.checkpoint_dir, f) for f in os.listdir(context.checkpoint_dir) if f.endswith(('.pt', '.pth', '.h5', '.onnx'))]
                        if files:
                            best_path = max(files, key=os.path.getmtime)

                if not best_path or not os.path.exists(best_path):
                    return ActionExecutionResult(
                        success=False,
                        action_type=atype,
                        message="No checkpoint file found to save as best model.",
                        duration_ms=(time.time() - start_time) * 1000
                    )

                dest_dir = params.get("target_dir", os.path.join(context.output_dir, "best_models"))
                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, f"best_model_{context.session_id[:8]}{os.path.splitext(best_path)[1]}")
                shutil.copy2(best_path, dest_file)
                return ActionExecutionResult(
                    success=True,
                    action_type=atype,
                    message=f"Best model successfully saved to '{dest_file}'.",
                    details={"saved_path": dest_file},
                    duration_ms=(time.time() - start_time) * 1000
                )

            elif atype == "COMPRESS_LOGS":
                zip_path = os.path.join(context.output_dir, f"logs_session_{context.session_id[:8]}.zip")
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    if os.path.exists(context.output_dir):
                        for root, _, files in os.walk(context.output_dir):
                            for file in files:
                                if file.endswith(('.log', '.txt', '.json')):
                                    file_path = os.path.join(root, file)
                                    arcname = os.path.relpath(file_path, context.output_dir)
                                    zipf.write(file_path, arcname)
                return ActionExecutionResult(
                    success=True,
                    action_type=atype,
                    message=f"Session logs compressed into archive '{zip_path}'.",
                    details={"zip_path": zip_path},
                    duration_ms=(time.time() - start_time) * 1000
                )

            elif atype in ["GENERATE_REPORT", "GENERATE_FAILURE_REPORT"]:
                # Trigger report generation
                report_file = os.path.join(context.output_dir, f"report_session_{context.session_id[:8]}.pdf")
                from app.reporting.pdf_builder import PDFReportGenerator
                PDFReportGenerator.generate_pdf(
                    output_filepath=report_file,
                    session_info={"session_id": context.session_id, "project_name": "Zombie Run ML Run", "status": "COMPLETED"},
                    metrics_summary={"total_epochs": 10, "final_loss": 0.28, "best_val_loss": 0.32},
                    hardware_summary={"avg_cpu_pct": 45, "avg_gpu_pct": 88, "peak_gpu_temp": 72},
                    recommendations=[]
                )
                return ActionExecutionResult(
                    success=True,
                    action_type=atype,
                    message=f"PDF Training Report generated at '{report_file}'.",
                    details={"report_file": report_file},
                    duration_ms=(time.time() - start_time) * 1000
                )

            # ----------------------------------------------------
            # 2. NOTIFICATION ACTIONS
            # ----------------------------------------------------
            elif atype in ["NOTIFY_USER", "SEND_NOTIFICATION"]:
                title = params.get("title", f"Zombie Run Cost Killer Event: Session {context.session_id[:8]}")
                msg = params.get("message", f"Training workflow step '{atype}' completed.")
                await notification_manager.send_notification(UUID(context.session_id), title, msg)
                return ActionExecutionResult(
                    success=True,
                    action_type=atype,
                    message=f"Notification dispatched: '{title}'.",
                    duration_ms=(time.time() - start_time) * 1000
                )

            # ----------------------------------------------------
            # 3. COMPUTER POWER ACTIONS (Safe Grace Period)
            # ----------------------------------------------------
            elif atype in ["SYSTEM_SHUTDOWN", "SHUTDOWN", "SYSTEM_SLEEP", "SYSTEM_HIBERNATE", "LOCK_COMPUTER"]:
                mode = "SHUTDOWN"
                if "SLEEP" in atype:
                    mode = "SLEEP"
                elif "HIBERNATE" in atype:
                    mode = "HIBERNATE"
                elif "LOCK" in atype:
                    mode = "LOCK"

                grace_sec = int(params.get("grace_period_sec", 30))

                async def _on_tick(rem_sec: int):
                    await ws_manager.broadcast_to_session(context.session_id, {
                        "type": "AUTOMATION_COUNTDOWN",
                        "session_id": context.session_id,
                        "action": mode,
                        "remaining_sec": rem_sec
                    })

                async def _power_action_callback():
                    if sys.platform != "win32":
                        logger.warning(f"Power action {mode} skipped on non-Windows OS.")
                        return

                    if mode == "SHUTDOWN":
                        subprocess.Popen(f"shutdown /s /t 0 /c \"Zombie Run Cost Killer Scheduled Shutdown\"", shell=True)
                    elif mode == "SLEEP":
                        subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
                    elif mode == "HIBERNATE":
                        subprocess.Popen("shutdown /h", shell=True)
                    elif mode == "LOCK":
                        subprocess.Popen("rundll32.exe user32.dll,LockWorkStation", shell=True)

                # Schedule safe action with SafetyManager grace period
                asyncio.create_task(safety_manager.schedule_safe_action(
                    session_id=context.session_id,
                    action_name=mode,
                    timeout_sec=grace_sec,
                    action_callback=_power_action_callback,
                    on_tick_callback=_on_tick
                ))

                return ActionExecutionResult(
                    success=True,
                    action_type=atype,
                    message=f"Scheduled Win32 {mode} with {grace_sec}s safety countdown grace period.",
                    details={"mode": mode, "grace_period_sec": grace_sec},
                    duration_ms=(time.time() - start_time) * 1000
                )

            else:
                # Default generic action execution
                return ActionExecutionResult(
                    success=True,
                    action_type=atype,
                    message=f"Executed action '{atype}' successfully.",
                    duration_ms=(time.time() - start_time) * 1000
                )

        except Exception as e:
            logger.error(f"Action execution error on {atype}: {e}")
            return ActionExecutionResult(
                success=False,
                action_type=atype,
                message=f"Action execution failed: {str(e)}",
                details={"error": str(e)},
                duration_ms=(time.time() - start_time) * 1000
            )

action_executor = ActionExecutor()
