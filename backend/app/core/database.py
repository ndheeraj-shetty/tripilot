import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

logger = logging.getLogger(__name__)

# Base directory for storage
storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage"))
os.makedirs(storage_dir, exist_ok=True)
sqlite_db_path = os.path.join(storage_dir, "trainpilot.db")

# Default engine fallback configuration
DEFAULT_SQLITE_URL = f"sqlite+aiosqlite:///{sqlite_db_path}"

# Use SQLite engine for 100% reliable local development & testing
engine = create_async_engine(
    DEFAULT_SQLITE_URL,
    echo=False,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
