from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel

from app.core.database import get_db
from app.domain.models.models import Checkpoint, TrainingSession
from app.services.checkpoint_manager import checkpoint_manager_service

router = APIRouter(prefix="/checkpoints", tags=["Checkpoint Manager"])

class ResumeTrainingPayload(BaseModel):
    session_id: UUID
    checkpoint_path: str
    extra_args: List[str] = []

@router.get("")
async def list_checkpoints(session_id: Optional[UUID] = None, checkpoint_dir: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    if session_id and checkpoint_dir:
        discovered = await checkpoint_manager_service.discover_checkpoints(checkpoint_dir, session_id)
        return {"checkpoints": discovered}

    query = select(Checkpoint).order_by(Checkpoint.created_at.desc())
    if session_id:
        query = query.where(Checkpoint.session_id == session_id)
    result = await db.execute(query)
    ckpts = result.scalars().all()
    return {"checkpoints": ckpts}

@router.post("/resume")
async def resume_from_checkpoint(payload: ResumeTrainingPayload):
    validation = checkpoint_manager_service.validate_checkpoint_for_resume(payload.checkpoint_path)
    if not validation["valid"]:
        raise HTTPException(status_code=400, detail=validation["reason"])

    return {
        "status": "RESUMING",
        "session_id": payload.session_id,
        "checkpoint_path": payload.checkpoint_path,
        "validation": validation
    }

@router.delete("/{checkpoint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checkpoint(checkpoint_id: UUID, db: AsyncSession = Depends(get_db)):
    ckpt = await db.get(Checkpoint, checkpoint_id)
    if ckpt:
        await db.delete(ckpt)
        await db.commit()
    return None
