from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.domain.models.models import Project
from app.domain.schemas.project_schema import ProjectCreate, ProjectUpdate

class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj_in: ProjectCreate) -> Project:
        db_obj = Project(**obj_in.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, project_id: UUID) -> Optional[Project]:
        result = await self.session.execute(select(Project).where(Project.id == project_id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        result = await self.session.execute(select(Project).offset(skip).limit(limit).order_by(Project.created_at.desc()))
        return list(result.scalars().all())

    async def update(self, project_id: UUID, obj_in: ProjectUpdate) -> Optional[Project]:
        db_obj = await self.get_by_id(project_id)
        if not db_obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, project_id: UUID) -> bool:
        db_obj = await self.get_by_id(project_id)
        if not db_obj:
            return False
        await self.session.delete(db_obj)
        await self.session.commit()
        return True
