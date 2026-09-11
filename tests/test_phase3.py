import pytest
from app.ai_engine.detection_service import DetectionService
from app.ai_engine.prediction_service import PredictionService
from app.ai_engine.recommendation_service import RecommendationService
from app.ai_engine.health_service import HealthScoreService
from app.ai_engine.trend_service import TrendAnalysisService

def test_healthy_training_detection():
    service = DetectionService()
    metrics = [
        {"epoch": 1, "loss": 1.20, "val_loss": 1.25, "accuracy": 0.50},
        {"epoch": 2, "loss": 0.90, "val_loss": 0.95, "accuracy": 0.65},
        {"epoch": 3, "loss": 0.70, "val_loss": 0.75, "accuracy": 0.75},
        {"epoch": 4, "loss": 0.50, "val_loss": 0.55, "accuracy": 0.85},
    ]
    telemetry = {"gpu_temperature_c": 70.0, "gpu_memory_used_mb": 8000, "gpu_memory_total_mb": 24000, "disk_free_space_bytes": 100 * (1024**3)}
    detections = service.analyze(metrics, telemetry)
    assert len(detections) == 0

def test_overfitting_detection():
    service = DetectionService(overfitting_patience=3)
    metrics = [
        {"loss": 0.80, "val_loss": 0.85},
        {"loss": 0.60, "val_loss": 0.90},
        {"loss": 0.40, "val_loss": 0.98},
        {"loss": 0.20, "val_loss": 1.10},
    ]
    detections = service.analyze(metrics)
    assert len(detections) >= 1
    assert any(d.detection_type == "OVERFITTING" for d in detections)

def test_gpu_overheating_detection():
    service = DetectionService(gpu_temp_threshold=85.0)
    telemetry = {"gpu_temperature_c": 89.5, "disk_free_space_bytes": 100 * (1024**3)}
    detections = service.analyze([], telemetry)
    assert len(detections) == 1
    assert detections[0].detection_type == "GPU_OVERHEATING"
    assert detections[0].severity == "WARNING"

def test_nan_loss_detection():
    service = DetectionService()
    metrics = [{"loss": float('nan')}]
    detections = service.analyze(metrics)
    assert len(detections) == 1
    assert detections[0].detection_type == "NAN_LOSS"
    assert detections[0].severity == "CRITICAL"

def test_cuda_error_log_detection():
    service = DetectionService()
    logs = [
        "[INFO] Epoch 1 starting...",
        "RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB"
    ]
    detections = service.analyze([], logs_history=logs)
    assert len(detections) == 1
    assert detections[0].detection_type == "CUDA_ERROR"

def test_health_score_calculation():
    health_service = HealthScoreService()
    det_service = DetectionService()
    metrics = [{"loss": float('nan')}]
    detections = det_service.analyze(metrics)
    
    health = health_service.calculate(detections, {}, prediction_fail_prob=0.80)
    assert health.score < 50
    assert health.category == "CRITICAL"

def test_recommendation_generation():
    rec_service = RecommendationService()
    det_service = DetectionService()
    metrics = [{"loss": float('nan')}]
    detections = det_service.analyze(metrics)
    
    recs = rec_service.generate(detections, {})
    assert len(recs) >= 1
    assert recs[0].category == "HYPERPARAMETER"
    assert "Lower Learning Rate" in recs[0].title
