import pytest
import math
from app.adapters.pytorch_adapter import PyTorchAdapter
from app.adapters.tensorflow_adapter import TensorFlowAdapter
from app.adapters.yolo_adapter import YOLOAdapter
from app.ai_engine.anomaly_detector import AnomalyDetector
from app.ai_engine.eta_predictor import ETAPredictor
from app.automation.engine import AutomationEngine

def test_pytorch_adapter_parsing():
    adapter = PyTorchAdapter()
    line = "Epoch 5/100 Step 50/500 Loss: 0.2815 Val Loss: 0.3210 Acc: 0.885 LR: 0.001"
    parsed = adapter.parse_stdout_line(line)
    assert parsed is not None
    assert parsed.epoch == 5
    assert parsed.step == 50
    assert abs(parsed.loss - 0.2815) < 1e-4
    assert abs(parsed.val_loss - 0.3210) < 1e-4
    assert abs(parsed.accuracy - 0.885) < 1e-4

def test_tensorflow_adapter_parsing():
    adapter = TensorFlowAdapter()
    line = "500/500 [==============================] - 2s 4ms/step - loss: 0.4512 - accuracy: 0.8120 - val_loss: 0.4910 - val_accuracy: 0.7950"
    parsed = adapter.parse_stdout_line(line)
    assert parsed is not None
    assert parsed.step == 500
    assert abs(parsed.loss - 0.4512) < 1e-4
    assert abs(parsed.val_loss - 0.4910) < 1e-4

def test_nan_anomaly_detection():
    detector = AnomalyDetector()
    res = detector.check_nan_loss(float('nan'))
    assert res is not None
    assert res.anomaly_type == "NAN_LOSS"
    assert res.severity == "CRITICAL"

def test_gpu_overheating_detection():
    detector = AnomalyDetector(gpu_temp_threshold=80.0)
    res = detector.check_gpu_overheating(87.5)
    assert res is not None
    assert res.anomaly_type == "OVERHEATING"

def test_overfitting_detection():
    detector = AnomalyDetector(overfitting_patience_epochs=4)
    train_losses = [1.0, 0.8, 0.6, 0.4, 0.2]
    val_losses = [1.0, 1.1, 1.2, 1.3, 1.4]
    res = detector.check_overfitting(train_losses, val_losses)
    assert res is not None
    assert res.anomaly_type == "OVERFITTING"

@pytest.mark.asyncio
async def test_automation_engine():
    engine = AutomationEngine()
    assert "SAVE_BEST_MODEL" in engine.handlers
    assert "SYSTEM_POWER" in engine.handlers
