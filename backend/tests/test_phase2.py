import pytest
import os
import sys
import asyncio
from app.adapters.pytorch_adapter import PyTorchAdapter
from app.adapters.tensorflow_adapter import TensorFlowAdapter
from app.adapters.yolo_adapter import YOLOAdapter
from app.monitoring.system_collector import SystemCollector
from app.launcher.process_manager import WindowsProcessManager

def test_environment_validation():
    adapter = PyTorchAdapter()
    sample_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts", "sample_training.py"))
    val_res = adapter.validate_environment(sample_script)
    assert val_res.is_valid is True
    assert len(val_res.errors) == 0

def test_system_collector():
    collector = SystemCollector()
    metrics = collector.collect()
    assert "cpu_utilization_pct" in metrics
    assert "ram_used_bytes" in metrics
    assert "gpu_utilization_pct" in metrics
    assert "disk_free_space_bytes" in metrics

@pytest.mark.asyncio
async def test_sample_script_execution():
    pm = WindowsProcessManager(session_id="test_session_123")
    sample_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts", "sample_training.py"))
    
    logs_captured = []
    def on_log(line: str):
        logs_captured.append(line)

    cmd = [sys.executable, sample_script, "--epochs", "1"]
    pid = await pm.start_process(cmd, cwd=os.path.dirname(sample_script), stdout_callback=on_log)
    assert pid is not None
    assert pid > 0

    # Wait for process to finish
    await asyncio.sleep(4.0)
    exit_code = await pm.stop_process()
    assert exit_code == 0
    assert len(logs_captured) > 0
    assert any("Epoch:" in line for line in logs_captured)
