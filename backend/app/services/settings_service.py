from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.config_repo import ConfigurationRepository
from app.core.config import settings

class SettingsService:
    def __init__(self, db: AsyncSession):
        self.repo = ConfigurationRepository(db)

    async def get_settings(self) -> Dict[str, Any]:
        stored_configs = await self.repo.get_all()
        # Merge with application defaults
        merged = {
            "theme": settings.THEME,
            "app_env": settings.APP_ENV,
            "default_output_folder": settings.DEFAULT_OUTPUT_FOLDER,
            "default_checkpoint_folder": settings.DEFAULT_CHECKPOINT_FOLDER,
            "postgres_server": settings.POSTGRES_SERVER,
            "postgres_port": settings.POSTGRES_PORT,
            "postgres_db": settings.POSTGRES_DB
        }
        merged.update(stored_configs)
        return merged

    async def update_settings(self, new_settings: Dict[str, Any]) -> Dict[str, Any]:
        for key, val in new_settings.items():
            await self.repo.set_key(key, val)
        return await self.get_settings()
