import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel

from app.services.export_service import export_service

router = APIRouter(prefix="/exports", tags=["Export Center"])

class ExportPayload(BaseModel):
    session_id: UUID
    output_dir: str = "./storage/outputs"
    export_dir: str = "./storage/exports"

@router.post("")
async def create_export_bundle(payload: ExportPayload):
    res = await export_service.generate_export_zip(
        session_id=payload.session_id,
        output_dir=payload.output_dir,
        export_dir=payload.export_dir
    )
    return res

@router.get("/download/{filename}")
async def download_export_file(filename: str, export_dir: str = "./storage/exports"):
    file_path = os.path.join(export_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Export bundle '{filename}' not found.")
    return FileResponse(file_path, media_type="application/zip", filename=filename)
