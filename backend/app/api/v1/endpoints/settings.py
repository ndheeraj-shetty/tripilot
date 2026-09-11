from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.core.database import get_db
from app.services.settings_service import SettingsService

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("", response_model=Dict[str, Any])
async def get_settings(db: AsyncSession = Depends(get_db)):
    service = SettingsService(db)
    return await service.get_settings()

@router.put("", response_model=Dict[str, Any])
async def update_settings(payload: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    service = SettingsService(db)
    return await service.update_settings(payload)
