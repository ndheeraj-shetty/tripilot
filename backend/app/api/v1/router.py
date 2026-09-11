from fastapi import APIRouter
from app.api.v1.endpoints import (
    health, projects, settings, training, system, ai, automation,
    checkpoints, experiments, analytics, reports, exports,
    auth, users, admin, backup
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(projects.router)
api_router.include_router(settings.router)
api_router.include_router(training.router)
api_router.include_router(system.router)
api_router.include_router(ai.router)
api_router.include_router(automation.router)
api_router.include_router(checkpoints.router)
api_router.include_router(experiments.router)
api_router.include_router(analytics.router)
api_router.include_router(reports.router)
api_router.include_router(exports.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(admin.router)
api_router.include_router(backup.router)
