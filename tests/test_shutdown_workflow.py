import pytest
import asyncio
from app.automation.safety_manager import safety_manager

@pytest.mark.asyncio
async def test_safety_manager_shutdown_countdown_and_cancel():
    session_id = "test-session-123"
    executed = []

    async def fake_shutdown_callback():
        executed.append(True)

    # Schedule a 30s safe shutdown action
    task = asyncio.create_task(
        safety_manager.schedule_safe_action(
            session_id=session_id,
            action_name="SHUTDOWN",
            timeout_sec=30,
            action_callback=fake_shutdown_callback
        )
    )

    await asyncio.sleep(0.1)

    # Check status query
    status = safety_manager.get_countdown_status(session_id)
    assert status["active"] is True
    assert status["session_id"] == session_id
    assert status["remaining_sec"] is not None
    assert status["remaining_sec"] <= 30
    assert status["status"] == "COUNTDOWN"

    # Cancel shutdown
    cancelled = safety_manager.cancel_countdown(session_id)
    assert cancelled is True

    status_after = safety_manager.get_countdown_status(session_id)
    assert status_after["active"] is False
    assert status_after["status"] == "CANCELLED"

    # Ensure fake callback was not executed
    assert len(executed) == 0


@pytest.mark.asyncio
async def test_safety_manager_single_execution_lock():
    session_id = "test-session-single-exec"
    exec_count = []

    async def fake_shutdown_callback():
        exec_count.append(1)

    task = asyncio.create_task(
        safety_manager.schedule_safe_action(
            session_id=session_id,
            action_name="SHUTDOWN",
            timeout_sec=5,
            action_callback=fake_shutdown_callback
        )
    )

    await asyncio.sleep(0.1)

    # Trigger immediate execution
    res1 = safety_manager.execute_immediately(session_id)
    assert res1 is True

    # Try duplicate execution
    res2 = safety_manager.execute_immediately(session_id)
    assert res2 is False

    await asyncio.sleep(0.1)
    assert len(exec_count) == 1
