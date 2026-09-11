import os
import sys
import time
import asyncio
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass

from app.core.config import settings
from app.core.database import engine, Base, create_async_engine
from app.core.logging_config import logger, setup_logging
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Initializing Zombie Run Cost Killer Backend Core Infrastructure...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database Tables Verified & Synchronized.")
    except Exception as e:
        logger.warning(f"PostgreSQL connection error ({e}). Initializing SQLite fallback database...")
        storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage"))
        os.makedirs(storage_dir, exist_ok=True)
        sqlite_db_path = os.path.join(storage_dir, "zombierun.db")
        fallback_engine = create_async_engine(f"sqlite+aiosqlite:///{sqlite_db_path}")
        async with fallback_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(f"SQLite Fallback Database Synchronized at {sqlite_db_path}.")
    yield
    logger.info("Shutting down Zombie Run Cost Killer Backend Server...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} -> Status {response.status_code} ({duration_ms}ms)")
    return response

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Uncaught Exception on {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred.", "error": str(exc)}
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
