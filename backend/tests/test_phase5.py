import os
import pytest
from uuid import uuid4
from app.services.checkpoint_manager import checkpoint_manager_service
from app.analytics.comparison_service import comparison_service
from app.analytics.analytics_service import analytics_service
from app.reporting.pdf_builder import PDFReportGenerator
from app.services.export_service import export_service

def test_checkpoint_validation():
    res = checkpoint_manager_service.validate_checkpoint_for_resume("./storage/non_existent.pt")
    assert res["valid"] is False
    assert "does not exist" in res["reason"]

@pytest.mark.asyncio
async def test_comparison_service():
    sa_id = uuid4()
    sb_id = uuid4()
    comp = await comparison_service.compare_sessions(sa_id, sb_id)
    assert "session_a" in comp
    assert "session_b" in comp
    assert "deltas" in comp
    assert "accuracy_delta" in comp["deltas"]

def test_ai_insights_generation():
    metrics = [
        {"loss": 0.90, "val_loss": 0.95},
        {"loss": 0.70, "val_loss": 0.75},
        {"loss": 0.50, "val_loss": 0.85},
        {"loss": 0.40, "val_loss": 0.95},
    ]
    telemetry = [{"gpu_utilization_pct": 35.0}]
    insights = analytics_service.generate_ai_insights(metrics, telemetry)
    assert len(insights) >= 2
    assert any("Validation Loss increased" in i for i in insights)

def test_pdf_report_generation(tmp_path):
    output_pdf = str(tmp_path / "test_report.pdf")
    PDFReportGenerator.generate_pdf(
        output_filepath=output_pdf,
        session_info={"session_id": "test-123", "project_name": "Test Run", "status": "COMPLETED"},
        metrics_summary={"total_epochs": 5, "final_loss": 0.2, "best_val_loss": 0.25},
        hardware_summary={"avg_cpu_pct": 40, "avg_gpu_pct": 80, "peak_gpu_temp": 70},
        recommendations=[]
    )
    assert os.path.exists(output_pdf)
    assert os.path.getsize(output_pdf) > 0

@pytest.mark.asyncio
async def test_export_service_zip(tmp_path):
    session_id = uuid4()
    out_dir = str(tmp_path / "outputs")
    exp_dir = str(tmp_path / "exports")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(exp_dir, exist_ok=True)

    res = await export_service.generate_export_zip(session_id, out_dir, exp_dir)
    assert os.path.exists(res["file_path"])
    assert res["file_path"].endswith(".zip")
    assert res["file_size_bytes"] > 0
