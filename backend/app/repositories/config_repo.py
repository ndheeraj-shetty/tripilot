from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.models.models import Configuration

class ConfigurationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_key(self, key: str) -> Optional[Configuration]:
        result = await self.session.execute(select(Configuration).where(Configuration.key == key))
        return result.scalars().first()

    async def set_key(self, key: str, value: Any, description: Optional[str] = None) -> Configuration:
        config_obj = await self.get_by_key(key)
        if config_obj:
            config_obj.value = value
            if description:
                config_obj.description = description
        else:
            config_obj = Configuration(key=key, value=value, description=description)
            self.session.add(config_obj)
        await self.session.commit()
        await self.session.refresh(config_obj)
        return config_obj

    async def get_all(self) -> Dict[str, Any]:
        result = await self.session.execute(select(Configuration))
        configs = result.scalars().all()
        return {item.key: item.value for item in configs}
