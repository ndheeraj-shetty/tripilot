from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel

from app.core.database import get_db
from app.domain.models.models import Experiment

router = APIRouter(prefix="/experiments", tags=["Experiment Tracker"])

class ExperimentCreatePayload(BaseModel):
    project_id: UUID
    name: str
    description: Optional[str] = None
    tags: List[str] = []
    hyperparameters: Dict[str, Any] = {}
    notes: Optional[str] = None

@router.get("")
async def list_experiments(project_id: Optional[UUID] = None, db: AsyncSession = Depends(get_db)):
    query = select(Experiment).order_by(Experiment.created_at.desc())
    if project_id:
        query = query.where(Experiment.project_id == project_id)
    result = await db.execute(query)
    exps = result.scalars().all()
    return exps

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_experiment(payload: ExperimentCreatePayload, db: AsyncSession = Depends(get_db)):
    exp = Experiment(
        project_id=payload.project_id,
        name=payload.name,
        description=payload.description,
        tags=payload.tags,
        hyperparameters=payload.hyperparameters,
        notes=payload.notes
    )
    db.add(exp)
    await db.commit()
    await db.refresh(exp)
    return exp
