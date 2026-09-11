import os
import sys
import subprocess
import asyncio
import logging
from typing import Dict, Any
from app.automation.handlers.base_handler import BaseActionHandler, ActionContext, ActionResult

logger = logging.getLogger(__name__)

class SystemPowerHandler(BaseActionHandler):
    action_type = "SYSTEM_POWER"

    async def execute(self, params: Dict[str, Any], context: ActionContext) -> ActionResult:
        mode = params.get("mode", "SHUTDOWN").upper() # SHUTDOWN, SLEEP, HIBERNATE
        grace_period_sec = int(params.get("grace_period_sec", 30))

        logger.info(f"System Power Action Triggered: Mode={mode}, GracePeriod={grace_period_sec}s")

        if sys.platform != "win32":
            return ActionResult(
                success=False,
                action_type=self.action_type,
                message="System power actions are only supported on Windows in V1.",
                details={"platform": sys.platform}
            )

        if mode == "SHUTDOWN":
            # Windows shutdown command with grace period
            cmd = f"shutdown /s /t {grace_period_sec} /c \"Zombie Run Cost Killer Training Completed. Shutting down computer.\""
            subprocess.Popen(cmd, shell=True)
            return ActionResult(
                success=True,
                action_type=self.action_type,
                message=f"Windows shutdown scheduled in {grace_period_sec} seconds.",
                details={"mode": mode, "grace_period_sec": grace_period_sec}
            )
        elif mode == "SLEEP":
            # Windows sleep command via rundll32
            cmd = "powrprof.dll,SetSuspendState 0,1,0"
            subprocess.Popen(f"rundll32.exe {cmd}", shell=True)
            return ActionResult(
                success=True,
                action_type=self.action_type,
                message="Windows sleep initiated.",
                details={"mode": mode}
            )
        elif mode == "HIBERNATE":
            cmd = "shutdown /h"
            subprocess.Popen(cmd, shell=True)
            return ActionResult(
                success=True,
                action_type=self.action_type,
                message="Windows hibernate initiated.",
                details={"mode": mode}
            )
        else:
            return ActionResult(
                success=False,
                action_type=self.action_type,
                message=f"Unknown system power mode: {mode}",
                details={"mode": mode}
            )


class NotifyUserHandler(BaseActionHandler):
    action_type = "NOTIFY_USER"

    async def execute(self, params: Dict[str, Any], context: ActionContext) -> ActionResult:
        title = params.get("title", f"Zombie Run Cost Killer Event: {context.status}")
        message = params.get("message", f"Session {context.session_id[:8]} finished with status {context.status}.")

        # Send Windows PowerShell Toast notification or stdout log
        if sys.platform == "win32":
            ps_script = f"""
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
            $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
            $toastXml = [xml]$template.GetXml()
            $toastXml.GetElementsByTagName('text')[0].AppendChild($toastXml.CreateTextNode('{title}')) > $null
            $toastXml.GetElementsByTagName('text')[1].AppendChild($toastXml.CreateTextNode('{message}')) > $null
            """
            try:
                subprocess.Popen(["powershell", "-Command", ps_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                logger.warning(f"Could not send Windows Toast notification: {e}")

        return ActionResult(
            success=True,
            action_type=self.action_type,
            message=f"User notification dispatched: {title}",
            details={"title": title, "message": message}
        )
