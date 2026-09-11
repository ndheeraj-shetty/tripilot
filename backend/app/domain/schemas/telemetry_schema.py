from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class MetricData(BaseModel):
    epoch: int
    step: int
    loss: Optional[float] = None
    val_loss: Optional[float] = None
    accuracy: Optional[float] = None
    learning_rate: Optional[float] = None
    step_time_ms: Optional[float] = None
    total_epochs: Optional[int] = None
    current_batch: Optional[int] = None
    total_batches: Optional[int] = None
    progress_pct: Optional[float] = None
    eta_sec: Optional[float] = None
    elapsed_sec: Optional[float] = None
    stage: Optional[str] = None
    gpu_state: Optional[str] = None
    cost_saved: Optional[float] = None

class MetricResponse(MetricData):
    id: int
    session_id: UUID
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class TelemetryData(BaseModel):
    cpu_utilization_pct: float
    ram_used_bytes: int
    ram_total_bytes: int
    gpu_utilization_pct: Optional[float] = None
    gpu_memory_used_mb: Optional[float] = None
    gpu_memory_total_mb: Optional[float] = None
    gpu_temperature_c: Optional[float] = None
    gpu_power_draw_watts: Optional[float] = None
    disk_read_bytes_sec: Optional[float] = None
    disk_write_bytes_sec: Optional[float] = None
    disk_free_space_bytes: int
    gpu_state: Optional[str] = "Active"
    gpu_name: Optional[str] = "NVIDIA GeForce RTX 4090"

class TelemetryResponse(TelemetryData):
    id: int
    session_id: UUID
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
