from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from uuid import UUID
import asyncio
import logging

from app.core.database import get_db
from app.domain.schemas.session_schema import SessionLaunch, SessionResponse
from app.repositories.project_repo import ProjectRepository
from app.repositories.session_repo import SessionRepository
from app.launcher.process_manager import WindowsProcessManager
from app.adapters.pytorch_adapter import PyTorchAdapter
from app.adapters.tensorflow_adapter import TensorFlowAdapter
from app.adapters.yolo_adapter import YOLOAdapter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions", tags=["Training Sessions"])

# In-memory session process managers map: session_id -> WindowsProcessManager
active_process_managers: Dict[str, WindowsProcessManager] = {}

def get_framework_adapter(framework: str):
    fw = framework.lower()
    if "pytorch" in fw or "torch" in fw:
        return PyTorchAdapter()
    elif "tensorflow" in fw or "tf" in fw:
        return TensorFlowAdapter()
    elif "yolo" in fw or "ultralytics" in fw:
        return YOLOAdapter()
    else:
        return PyTorchAdapter() # Default fallback

@router.post("/launch", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def launch_session(payload: SessionLaunch, db: AsyncSession = Depends(get_db)):
    proj_repo = ProjectRepository(db)
    session_repo = SessionRepository(db)

    project = await proj_repo.get_by_id(payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Target Project not found")

    session_name = payload.session_name or f"Run-{project.name}-{payload.project_id.hex[:6]}"
    session_obj = await session_repo.create_session(
        project_id=payload.project_id,
        session_name=session_name,
        hyperparameters=payload.hyperparameters or {}
    )

    session_id_str = str(session_obj.id)
    adapter = get_framework_adapter(project.framework)

    launch_cmd = adapter.build_launch_command(
        script_path=project.training_script_path,
        hyperparameters=payload.hyperparameters or {},
        extra_args=payload.command_args
    )

    pm = WindowsProcessManager(session_id=session_id_str)
    active_process_managers[session_id_str] = pm

    # Callbacks for log output
    async def on_stdout(line: str):
        logger.info(f"[{session_id_str[:8]}] STDOUT: {line}")
        # Parse metric
        parsed = adapter.parse_stdout_line(line)
        if parsed:
            await session_repo.add_metric(session_obj.id, parsed)

    async def on_stderr(line: str):
        logger.warning(f"[{session_id_str[:8]}] STDERR: {line}")
        await session_repo.add_log_line(session_obj.id, "stderr", line)

    try:
        pid = await pm.start_process(
            command=launch_cmd,
            cwd=project.output_dir,
            stdout_callback=on_stdout,
            stderr_callback=on_stderr
        )
        updated = await session_repo.update_status(session_obj.id, "RUNNING", pid=pid)
        return updated
    except Exception as e:
        logger.error(f"Failed to launch session process: {e}")
        await session_repo.update_status(session_obj.id, "FAILED", exit_code=-1)
        raise HTTPException(status_code=500, detail=f"Failed to launch training process: {str(e)}")

@router.post("/{session_id}/pause")
async def pause_session(session_id: UUID, db: AsyncSession = Depends(get_db)):
    sid = str(session_id)
    pm = active_process_managers.get(sid)
    if not pm:
        raise HTTPException(status_code=404, detail="Active process manager not found for session.")

    success = await pm.pause_process()
    if success:
        repo = SessionRepository(db)
        await repo.update_status(session_id, "PAUSED")
        return {"status": "PAUSED", "session_id": sid}
    raise HTTPException(status_code=500, detail="Failed to pause process.")

@router.post("/{session_id}/resume")
async def resume_session(session_id: UUID, db: AsyncSession = Depends(get_db)):
    sid = str(session_id)
    pm = active_process_managers.get(sid)
    if not pm:
        raise HTTPException(status_code=404, detail="Active process manager not found for session.")

    success = await pm.resume_process()
    if success:
        repo = SessionRepository(db)
        await repo.update_status(session_id, "RUNNING")
        return {"status": "RUNNING", "session_id": sid}
    raise HTTPException(status_code=500, detail="Failed to resume process.")

@router.post("/{session_id}/stop")
async def stop_session(session_id: UUID, db: AsyncSession = Depends(get_db)):
    sid = str(session_id)
    pm = active_process_managers.get(sid)
    if not pm:
        raise HTTPException(status_code=404, detail="Active process manager not found for session.")

    exit_code = await pm.stop_process()
    repo = SessionRepository(db)
    await repo.update_status(session_id, "CANCELLED", exit_code=exit_code)
    active_process_managers.pop(sid, None)
    return {"status": "CANCELLED", "exit_code": exit_code}
