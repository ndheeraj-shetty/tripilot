import sys
import subprocess
import logging
from typing import Optional, Dict, Any
from uuid import UUID

from app.core.database import AsyncSessionLocal
from app.domain.models.models import Notification

logger = logging.getLogger(__name__)

class NotificationManager:
    async def send_notification(
        self,
        session_id: UUID,
        title: str,
        message: str,
        channel: str = "DESKTOP"
    ) -> bool:
        logger.info(f"Notification Manager: [{channel}] {title} - {message}")

        # 1. Windows Toast Notification
        if channel in ["DESKTOP", "ALL"] and sys.platform == "win32":
            try:
                ps_script = f"""
                [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
                $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
                $toastXml = [xml]$template.GetXml()
                $toastXml.GetElementsByTagName('text')[0].AppendChild($toastXml.CreateTextNode('{title}')) > $null
                $toastXml.GetElementsByTagName('text')[1].AppendChild($toastXml.CreateTextNode('{message}')) > $null
                """
                subprocess.Popen(["powershell", "-Command", ps_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                logger.warning(f"Could not trigger Windows Toast alert: {e}")

        # 2. Persist to PostgreSQL Database
        try:
            async with AsyncSessionLocal() as db:
                db.add(Notification(
                    session_id=session_id,
                    title=title,
                    message=message,
                    channel=channel,
                    status="SENT"
                ))
                await db.commit()
        except Exception as e:
            logger.error(f"Error persisting notification record: {e}")

        return True

notification_manager = NotificationManager()
