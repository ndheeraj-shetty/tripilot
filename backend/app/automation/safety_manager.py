import asyncio
import logging
import time
from typing import Dict, Optional, Callable, Any

logger = logging.getLogger(__name__)

class SafetyManager:
    def __init__(self):
        # Active countdown tasks: session_id -> asyncio.Task
        self.active_countdowns: Dict[str, asyncio.Task] = {}
        self.cancelled_sessions: set = set()
        self.executed_sessions: set = set()
        self.countdown_states: Dict[str, Dict[str, Any]] = {}

    async def schedule_safe_action(
        self,
        session_id: str,
        action_name: str,
        timeout_sec: int,
        action_callback: Callable[[], Any],
        on_tick_callback: Optional[Callable[[int], Any]] = None
    ) -> bool:
        """Schedules a dangerous system action with a safety countdown grace period."""
        logger.info(f"Safety Manager: Scheduling '{action_name}' for session {session_id} with {timeout_sec}s grace period.")
        
        self.cancelled_sessions.discard(session_id)
        self.executed_sessions.discard(session_id)

        start_time = time.time()
        end_time = start_time + timeout_sec

        self.countdown_states[session_id] = {
            "session_id": session_id,
            "action_name": action_name,
            "total_sec": timeout_sec,
            "start_time": start_time,
            "end_time": end_time,
            "status": "COUNTDOWN",
            "action_callback": action_callback
        }

        async def _countdown():
            try:
                for remaining in range(timeout_sec, 0, -1):
                    if session_id in self.cancelled_sessions:
                        logger.info(f"Safety Manager: Action '{action_name}' CANCELLED by user for session {session_id}.")
                        if session_id in self.countdown_states:
                            self.countdown_states[session_id]["status"] = "CANCELLED"
                        return False

                    if on_tick_callback:
                        try:
                            if asyncio.iscoroutinefunction(on_tick_callback):
                                await on_tick_callback(remaining)
                            else:
                                on_tick_callback(remaining)
                        except Exception as e:
                            logger.error(f"Error in countdown tick callback: {e}")
                    await asyncio.sleep(1.0)

                if session_id in self.cancelled_sessions:
                    if session_id in self.countdown_states:
                        self.countdown_states[session_id]["status"] = "CANCELLED"
                    return False

                # Ensure single execution
                if session_id in self.executed_sessions:
                    logger.info(f"Safety Manager: Action '{action_name}' already executed for session {session_id}.")
                    return True

                self.executed_sessions.add(session_id)
                if session_id in self.countdown_states:
                    self.countdown_states[session_id]["status"] = "INITIATING"

                logger.info(f"Safety Manager: Grace period expired with no response. Executing '{action_name}' now!")
                try:
                    if asyncio.iscoroutinefunction(action_callback):
                        await action_callback()
                    else:
                        action_callback()
                    if session_id in self.countdown_states:
                        self.countdown_states[session_id]["status"] = "EXECUTED"
                    return True
                except Exception as e:
                    logger.error(f"Error executing callback for '{action_name}': {e}")
                    return False
            finally:
                self.active_countdowns.pop(session_id, None)

        task = asyncio.create_task(_countdown())
        self.active_countdowns[session_id] = task
        return await task

    def get_countdown_status(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Returns the current countdown status for a session or latest active session."""
        target_sid = session_id
        if not target_sid and self.countdown_states:
            target_sid = list(self.countdown_states.keys())[-1]

        if not target_sid or target_sid not in self.countdown_states:
            return {"active": False, "remaining_sec": None, "status": "IDLE"}

        state = self.countdown_states[target_sid]
        status = state["status"]
        if status == "CANCELLED":
            return {"active": False, "session_id": target_sid, "remaining_sec": None, "status": "CANCELLED", "total_sec": state["total_sec"]}

        now = time.time()
        remaining = max(0, int(round(state["end_time"] - now)))
        is_active = status == "COUNTDOWN" and remaining > 0

        return {
            "active": is_active,
            "session_id": target_sid,
            "remaining_sec": remaining if is_active else 0,
            "total_sec": state["total_sec"],
            "status": status if is_active else ("EXPIRED" if remaining <= 0 and status == "COUNTDOWN" else status),
            "action_name": state["action_name"]
        }

    def cancel_countdown(self, session_id: str) -> bool:
        """Cancels an active countdown for a session."""
        logger.info(f"Safety Manager: Cancel request received for session {session_id}.")
        self.cancelled_sessions.add(session_id)
        if session_id in self.countdown_states:
            self.countdown_states[session_id]["status"] = "CANCELLED"

        task = self.active_countdowns.pop(session_id, None)
        if task and not task.done():
            task.cancel()
            return True
        return session_id in self.cancelled_sessions

    def execute_immediately(self, session_id: str) -> bool:
        """Executes the scheduled callback immediately while canceling the countdown, ensuring single execution."""
        if session_id in self.executed_sessions:
            logger.info(f"Safety Manager: Immediate execution ignored. Session {session_id} already executed.")
            return False

        state = self.countdown_states.get(session_id)
        callback = state.get("action_callback") if state else None

        self.cancel_countdown(session_id)
        self.executed_sessions.add(session_id)
        if state:
            state["status"] = "INITIATING"

        if callback:
            logger.info(f"Safety Manager: Executing action immediately for session {session_id}.")
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback())
                else:
                    callback()
                if state:
                    state["status"] = "EXECUTED"
                return True
            except Exception as e:
                logger.error(f"Safety Manager: Error in immediate execution for session {session_id}: {e}")
                return False

        # Fallback default win32 shutdown if no callback recorded
        import sys, subprocess
        if sys.platform == "win32":
            subprocess.Popen("shutdown /s /t 0 /c \"Zombie Run Cost Killer Immediate Shutdown\"", shell=True)
        return True

safety_manager = SafetyManager()

