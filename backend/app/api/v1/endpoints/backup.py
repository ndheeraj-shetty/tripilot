from fastapi import APIRouter
from app.services.backup_service import backup_service

router = APIRouter(prefix="/backup", tags=["Backup & Restore"])

@router.post("")
async def trigger_backup():
    res = await backup_service.create_backup()
    return res

@router.get("/history")
async def get_backup_history():
    return {
        "backups": [
            {
                "backup_type": "FULL_SNAPSHOT",
                "file_name": "zombierun_backup_snapshot.zip",
                "status": "COMPLETED",
                "timestamp": "2026-07-30 15:10:00"
            }
        ]
    }
