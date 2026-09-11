from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel

from app.core.logging_config import logger
from app.core.database import get_db
from app.services.training_manager import training_manager
from app.repositories.session_repo import SessionRepository
from app.websockets.ws_manager import ws_manager

router = APIRouter(prefix="/training", tags=["Training Management"])

class StartTrainingRequest(BaseModel):
    project_id: UUID
    session_name: Optional[str] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    extra_args: Optional[List[str]] = None

class SessionActionRequest(BaseModel):
    session_id: UUID

@router.post("/start", status_code=status.HTTP_201_CREATED)
async def start_training(req: StartTrainingRequest):
    logger.info(f"[STEP 1/6] API Request received for POST /training/start - project_id: {req.project_id}, session_name: {req.session_name}")
    try:
        res = await training_manager.start_training(
            project_id=req.project_id,
            session_name=req.session_name,
            hyperparameters=req.hyperparameters,
            extra_args=req.extra_args
        )
        logger.info(f"[STEP 6/6] Training session started successfully - session_id: {res.get('session_id')}, PID: {res.get('pid')}")
        return res
    except ValueError as ve:
        logger.warning(f"Validation failed starting training for project {req.project_id}: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        import traceback
        tb_str = traceback.format_exc()
        logger.error(f"Error starting training for project {req.project_id}: {e}\n{tb_str}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to start training: {str(e)}")

@router.post("/pause")
async def pause_training(req: SessionActionRequest):
    success = await training_manager.pause_training(str(req.session_id))
    if not success:
        raise HTTPException(status_code=400, detail="Failed to pause session or session not active.")
    return {"status": "PAUSED", "session_id": str(req.session_id)}

@router.post("/resume")
async def resume_training(req: SessionActionRequest):
    success = await training_manager.resume_training(str(req.session_id))
    if not success:
        raise HTTPException(status_code=400, detail="Failed to resume session or session not active.")
    return {"status": "RUNNING", "session_id": str(req.session_id)}

@router.post("/stop")
async def stop_training(req: SessionActionRequest):
    exit_code = await training_manager.stop_training(str(req.session_id))
    return {"status": "CANCELLED", "session_id": str(req.session_id), "exit_code": exit_code}

@router.post("/kill")
async def kill_training(req: SessionActionRequest):
    success = await training_manager.kill_process(str(req.session_id))
    return {"status": "CANCELLED", "session_id": str(req.session_id), "success": success}

@router.post("/release-gpu")
async def release_gpu(req: SessionActionRequest):
    success = await training_manager.release_gpu(str(req.session_id))
    return {"status": "RELEASED", "session_id": str(req.session_id), "success": success}

@router.get("/shutdown-status")
async def get_shutdown_status(session_id: Optional[str] = None):
    from app.automation.safety_manager import safety_manager
    return safety_manager.get_countdown_status(session_id)

@router.post("/cancel-shutdown")
async def cancel_shutdown(req: SessionActionRequest):
    from app.automation.safety_manager import safety_manager
    sid = str(req.session_id)
    cancelled = safety_manager.cancel_countdown(sid)
    await ws_manager.broadcast_to_session(sid, {
        "type": "AUTOMATION_COUNTDOWN",
        "session_id": sid,
        "action": "SHUTDOWN",
        "remaining_sec": None,
        "status": "CANCELLED"
    })
    await ws_manager.broadcast_to_session(sid, {
        "type": "CONSOLE_LOG",
        "session_id": sid,
        "stream": "stdout",
        "line": "[INFO] Automatic shutdown cancelled. The system will remain running."
    })
    return {
        "status": "CANCELLED",
        "session_id": sid,
        "cancelled": cancelled,
        "message": "Automatic shutdown cancelled. The system will remain running."
    }

@router.post("/shutdown-now")
async def shutdown_now(req: SessionActionRequest):
    from app.automation.safety_manager import safety_manager
    sid = str(req.session_id)
    await ws_manager.broadcast_to_session(sid, {
        "type": "AUTOMATION_COUNTDOWN",
        "session_id": sid,
        "action": "SHUTDOWN",
        "remaining_sec": 0,
        "status": "INITIATING"
    })
    success = safety_manager.execute_immediately(sid)
    return {"status": "SHUTDOWN_INITIATED", "session_id": sid, "success": success}

@router.post("/restart")
async def restart_training(req: SessionActionRequest):
    try:
        res = await training_manager.restart_training(str(req.session_id))
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restart training: {str(e)}")

@router.get("/status")
async def get_training_status(session_id: UUID, db: AsyncSession = Depends(get_db)):
    sid_str = str(session_id)
    if sid_str in training_manager.active_sessions:
        run = training_manager.active_sessions[sid_str]
        return {
            "session_id": sid_str,
            "status": run.status,
            "pid": run.pid,
            "is_active": True
        }
    repo = SessionRepository(db)
    sess = await repo.get_by_id(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {
        "session_id": sid_str,
        "status": sess.status,
        "pid": sess.pid,
        "exit_code": sess.exit_code,
        "is_active": False
    }

@router.get("/logs")
async def get_training_logs(session_id: UUID, limit: int = 500, db: AsyncSession = Depends(get_db)):
    sid_str = str(session_id)
    if sid_str in training_manager.active_sessions:
        return {"logs": training_manager.active_sessions[sid_str].logs_history[-limit:]}

    repo = SessionRepository(db)
    # Query database logs
    result = await db.execute(
        "SELECT stream, log_line, timestamp FROM session_logs WHERE session_id = :sid ORDER BY id ASC LIMIT :lim",
        {"sid": session_id, "lim": limit}
    )
    logs = [f"[{row[0].upper()}] {row[1]}" for row in result.fetchall()]
    return {"logs": logs}

@router.get("/metrics")
async def get_training_metrics(session_id: UUID, limit: int = 500, db: AsyncSession = Depends(get_db)):
    repo = SessionRepository(db)
    metrics = await repo.get_session_metrics(session_id, limit=limit)
    return {"metrics": metrics}

@router.websocket("/ws/{session_id}")
async def websocket_session_endpoint(websocket: WebSocket, session_id: str):
    await ws_manager.connect(websocket, session_id)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, session_id)
