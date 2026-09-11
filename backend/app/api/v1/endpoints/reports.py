import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from typing import Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel

from app.reporting.pdf_builder import PDFReportGenerator

router = APIRouter(prefix="/reports", tags=["Report Generator"])

class GenerateReportPayload(BaseModel):
    session_id: UUID
    report_type: str = "PDF" # PDF, HTML, MD, CSV, JSON
    output_dir: str = "./storage/outputs"

@router.post("/generate")
async def generate_report(payload: GenerateReportPayload):
    os.makedirs(payload.output_dir, exist_ok=True)
    file_name = f"training_report_{str(payload.session_id)[:8]}.pdf"
    file_path = os.path.join(payload.output_dir, file_name)

    PDFReportGenerator.generate_pdf(
        output_filepath=file_path,
        session_info={"session_id": str(payload.session_id), "project_name": "Zombie Run Model Run", "status": "COMPLETED"},
        metrics_summary={"total_epochs": 10, "final_loss": 0.28, "best_val_loss": 0.31},
        hardware_summary={"avg_cpu_pct": 42, "avg_gpu_pct": 85, "peak_gpu_temp": 72},
        recommendations=[]
    )

    return {
        "status": "GENERATED",
        "file_name": file_name,
        "file_path": file_path,
        "report_type": payload.report_type
    }

@router.get("/download/{filename}")
async def download_report_file(filename: str, output_dir: str = "./storage/outputs"):
    file_path = os.path.join(output_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Report file '{filename}' not found.")
    return FileResponse(file_path, media_type="application/pdf", filename=filename)
