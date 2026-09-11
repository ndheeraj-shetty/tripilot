import os
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.models import Project
from app.domain.schemas.project_schema import ProjectCreate, ProjectUpdate
from app.repositories.project_repo import ProjectRepository
from app.core.logging_config import logger

class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repo = ProjectRepository(db)

    async def create_project(self, project_in: ProjectCreate) -> Project:
        logger.info(f"Creating new project: {project_in.name} ({project_in.framework})")
        # Ensure directories exist or create them
        os.makedirs(project_in.output_dir, exist_ok=True)
        os.makedirs(project_in.checkpoint_dir, exist_ok=True)
        return await self.repo.create(project_in)

    async def get_project(self, project_id: UUID) -> Project:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {project_id} not found")
        return project

    async def list_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        return await self.repo.get_all(skip=skip, limit=limit)

    async def update_project(self, project_id: UUID, project_in: ProjectUpdate) -> Project:
        logger.info(f"Updating project {project_id}")
        updated = await self.repo.update(project_id, project_in)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {project_id} not found")
        return updated

    async def delete_project(self, project_id: UUID) -> bool:
        logger.info(f"Deleting project {project_id}")
        deleted = await self.repo.delete(project_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with ID {project_id} not found")
        return True
