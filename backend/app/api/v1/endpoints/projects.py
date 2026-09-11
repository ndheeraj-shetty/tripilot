from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.domain.schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_in: ProjectCreate, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    return await service.create_project(project_in)

@router.get("", response_model=List[ProjectResponse])
async def list_projects(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    return await service.list_projects(skip=skip, limit=limit)

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    return await service.get_project(project_id)

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: UUID, project_in: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    return await service.update_project(project_id, project_in)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: UUID, db: AsyncSession = Depends(get_db)):
    service = ProjectService(db)
    await service.delete_project(project_id)
    return None
