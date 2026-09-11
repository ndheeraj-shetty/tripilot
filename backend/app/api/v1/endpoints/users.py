from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.core.security import hash_password
from app.domain.models.models import User

router = APIRouter(prefix="/users", tags=["User Management"])

class UserCreatePayload(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    role: str = "ML_ENGINEER" # ADMIN, ML_ENGINEER, VIEWER

class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str] = None
    role: str
    is_active: bool

@router.get("", response_model=List[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return users

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreatePayload, db: AsyncSession = Depends(get_db)):
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
