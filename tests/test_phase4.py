import pytest
import asyncio
from uuid import uuid4
from app.automation.safety_manager import safety_manager
from app.automation.rollback_manager import rollback_manager
from app.automation.action_executor import action_executor, ExecutionContext
from app.automation.workflow_manager import workflow_manager
from app.automation.rule_engine import automation_rule_engine

@pytest.mark.asyncio
async def test_safety_manager_cancellation():
    session_id = "test_cancel_123"
    executed = []

    def mock_action():
        executed.append(True)

    # Schedule action with 5 second grace period
    task = asyncio.create_task(safety_manager.schedule_safe_action(
        session_id=session_id,
        action_name="SHUTDOWN",
        timeout_sec=5,
        action_callback=mock_action
    ))

    # Cancel countdown immediately
    await asyncio.sleep(0.5)
    cancelled = safety_manager.cancel_countdown(session_id)
    assert cancelled is True

    await asyncio.sleep(1.0)
    assert len(executed) == 0 # Action should NOT have been executed

@pytest.mark.asyncio
async def test_rollback_manager_failure_handling():
    history_id = uuid4()
    # Test strategy SKIP continues workflow
    cont = await rollback_manager.handle_action_failure(
        history_id=history_id,
        failed_action_type="COMPRESS_LOGS",
        error_message="Compression library error",
        strategy="SKIP"
    )
    assert cont is True

@pytest.mark.asyncio
async def test_action_executor_notify():
    ctx = ExecutionContext(
        session_id=str(uuid4()),
        project_id=str(uuid4()),
        output_dir="./storage/outputs",
        checkpoint_dir="./storage/checkpoints"
    )
    res = await action_executor.execute_action("NOTIFY_USER", {"title": "Test Alert"}, ctx)
    assert res.success is True

@pytest.mark.asyncio
async def test_workflow_manager_execution():
    session_id = uuid4()
    project_id = uuid4()
    ctx = ExecutionContext(
        session_id=str(session_id),
        project_id=str(project_id),
        output_dir="./storage/outputs",
        checkpoint_dir="./storage/checkpoints"
    )
    actions = [
        {"action_type": "NOTIFY_USER", "params": {"title": "Step 1"}},
        {"action_type": "NOTIFY_USER", "params": {"title": "Step 2"}},
    ]
    res = await workflow_manager.execute_workflow(session_id, "ON_SUCCESS", actions, ctx)
    assert res["status"] == "SUCCESS"
    assert len(res["executed_actions"]) == 2

def test_default_rule_actions():
    actions = automation_rule_engine.get_default_workflow_actions("ON_SUCCESS")
    assert len(actions) == 5
    assert actions[0]["action_type"] == "SAVE_BEST_MODEL"
    assert actions[-1]["action_type"] == "SYSTEM_SHUTDOWN"
