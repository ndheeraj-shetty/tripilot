from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.domain.models.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginPayload(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_email: str
    role: str

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginPayload, db: AsyncSession = Depends(get_db)):
    # Default admin login fallback for quick bootstrap / testing
    if payload.email in ["admin@zombierun.ai", "admin@trainpilot.ai"] and payload.password in ["admin123", "admin"]:
        token = create_access_token({"sub": payload.email, "role": "ADMIN"})
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user_email=payload.email,
            role="ADMIN"
        )

    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalars().first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

    token = create_access_token({"sub": user.email, "role": user.role})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_email=user.email,
        role=user.role
    )

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully."}
