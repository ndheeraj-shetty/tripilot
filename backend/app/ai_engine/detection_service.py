import math
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DetectionResult(BaseModel):
    detection_type: str
    status: str # DETECTED, RESOLVED
    severity: str # CRITICAL, WARNING, INFO
    confidence: float # 0.0 - 1.0
    reason: str
    details: Dict[str, Any] = {}
    timestamp: float = time.time()

class DetectionService:
    def __init__(
        self,
        gpu_temp_threshold: float = 85.0,
        disk_free_gb_threshold: float = 10.0,
        overfitting_patience: int = 4
    ):
        self.gpu_temp_threshold = gpu_temp_threshold
        self.disk_free_gb_threshold = disk_free_gb_threshold
        self.overfitting_patience = overfitting_patience

    def analyze(
        self,
        metrics_history: List[Dict[str, Any]],
        latest_telemetry: Optional[Dict[str, Any]] = None,
        logs_history: Optional[List[str]] = None
    ) -> List[DetectionResult]:
        results: List[DetectionResult] = []

        # Extract metric series
        losses = [m['loss'] for m in metrics_history if m.get('loss') is not None]
        val_losses = [m['val_loss'] for m in metrics_history if m.get('val_loss') is not None]
        accuracies = [m['accuracy'] for m in metrics_history if m.get('accuracy') is not None]
        lrs = [m['learning_rate'] for m in metrics_history if m.get('learning_rate') is not None]

        # 1. NaN / Exploding Loss Detection
        if losses:
            latest_loss = losses[-1]
            if math.isnan(latest_loss) or math.isinf(latest_loss):
                results.append(DetectionResult(
                    detection_type="NAN_LOSS",
                    status="DETECTED",
                    severity="CRITICAL",
                    confidence=1.0,
                    reason="Training loss diverged to NaN or Infinity!",
                    details={"loss": str(latest_loss)}
                ))
            elif len(losses) >= 2 and latest_loss > losses[-2] * 5.0 and latest_loss > 5.0:
                results.append(DetectionResult(
                    detection_type="EXPLODING_LOSS",
                    status="DETECTED",
                    severity="CRITICAL",
                    confidence=0.92,
                    reason=f"Training loss exploded from {losses[-2]:.4f} to {latest_loss:.4f} in 1 step.",
                    details={"prev_loss": losses[-2], "curr_loss": latest_loss}
                ))

        # 2. Overfitting Detection (Val Loss diverging while Train Loss decreases)
        if len(losses) >= self.overfitting_patience and len(val_losses) >= self.overfitting_patience:
            recent_losses = losses[-self.overfitting_patience:]
            recent_val = val_losses[-self.overfitting_patience:]

            train_dec = all(recent_losses[i] <= recent_losses[i-1] for i in range(1, len(recent_losses)))
            val_inc = all(recent_val[i] > recent_val[i-1] for i in range(1, len(recent_val)))

            if train_dec and val_inc:
                diff_pct = ((recent_val[-1] - recent_val[0]) / max(recent_val[0], 1e-6)) * 100
                results.append(DetectionResult(
                    detection_type="OVERFITTING",
                    status="DETECTED",
                    severity="WARNING",
                    confidence=min(0.95, 0.70 + (diff_pct / 100.0)),
                    reason=f"Validation loss increased by {diff_pct:.1f}% over the last {self.overfitting_patience} steps while training loss decreased.",
                    details={"patience": self.overfitting_patience, "recent_val": recent_val}
                ))

        # 3. Underfitting & Stagnation Detection
        if len(losses) >= 8:
            recent_8 = losses[-8:]
            delta = abs(recent_8[-1] - recent_8[0])
            if delta < 0.002 and recent_8[-1] > 0.4:
                results.append(DetectionResult(
                    detection_type="UNDERFITTING",
                    status="DETECTED",
                    severity="WARNING",
                    confidence=0.85,
                    reason=f"Training loss has plateaued at high loss ({recent_8[-1]:.4f}) with negligible delta ({delta:.5f}) over last 8 steps.",
                    details={"plateau_loss": recent_8[-1], "delta": delta}
                ))

        # 4. Vanishing Learning Rate Detection
        if lrs and lrs[-1] <= 1e-7:
            results.append(DetectionResult(
                detection_type="VANISHING_LEARNING",
                status="DETECTED",
                severity="WARNING",
                confidence=0.90,
                reason=f"Learning rate decays down to {lrs[-1]}, causing training stagnation.",
                details={"current_lr": lrs[-1]}
            ))

        # 5. Hardware Telemetry Detections
        if latest_telemetry:
            # GPU Temperature Check
            gpu_temp = latest_telemetry.get("gpu_temperature_c")
            if gpu_temp and gpu_temp >= self.gpu_temp_threshold:
                sev = "CRITICAL" if gpu_temp >= 90.0 else "WARNING"
                results.append(DetectionResult(
                    detection_type="GPU_OVERHEATING",
                    status="DETECTED",
                    severity=sev,
                    confidence=0.98,
                    reason=f"GPU temperature reached {gpu_temp:.1f}°C (Threshold: {self.gpu_temp_threshold}°C)!",
                    details={"gpu_temp_c": gpu_temp, "threshold": self.gpu_temp_threshold}
                ))

            # GPU VRAM Exhaustion
            vram_used = latest_telemetry.get("gpu_memory_used_mb")
            vram_total = latest_telemetry.get("gpu_memory_total_mb")
            if vram_used and vram_total and (vram_used / vram_total) >= 0.95:
                results.append(DetectionResult(
                    detection_type="GPU_MEMORY_EXHAUSTION",
                    status="DETECTED",
                    severity="CRITICAL",
                    confidence=0.95,
                    reason=f"GPU VRAM near full capacity ({vram_used:.0f} MB / {vram_total:.0f} MB, {((vram_used/vram_total)*100):.1f}%). Risk of CUDA Out-Of-Memory (OOM) crash!",
                    details={"vram_used_mb": vram_used, "vram_total_mb": vram_total}
                ))

            # CPU Bottleneck Check
            cpu_pct = latest_telemetry.get("cpu_utilization_pct", 0)
            gpu_pct = latest_telemetry.get("gpu_utilization_pct", 100)
            if cpu_pct > 90.0 and gpu_pct < 45.0:
                results.append(DetectionResult(
                    detection_type="CPU_BOTTLENECK",
                    status="DETECTED",
                    severity="INFO",
                    confidence=0.80,
                    reason=f"High CPU load ({cpu_pct:.1f}%) with low GPU utilization ({gpu_pct:.1f}%). Data loading or preprocessing bottleneck detected.",
                    details={"cpu_pct": cpu_pct, "gpu_pct": gpu_pct}
                ))

            # Disk Free Space Check
            disk_free_gb = latest_telemetry.get("disk_free_space_bytes", 0) / (1024 ** 3)
            if disk_free_gb < self.disk_free_gb_threshold:
                results.append(DetectionResult(
                    detection_type="DISK_ALMOST_FULL",
                    status="DETECTED",
                    severity="WARNING",
                    confidence=0.99,
                    reason=f"Disk free space is critically low ({disk_free_gb:.1f} GB remaining). Risk of checkpoint write failures!",
                    details={"disk_free_gb": disk_free_gb}
                ))

        # 6. Console Log Exception & Error Detections
        if logs_history:
            recent_logs = logs_history[-20:]
            for line in recent_logs:
                line_lower = line.lower()
                if "cuda out of memory" in line_lower or "oom" in line_lower:
                    results.append(DetectionResult(
                        detection_type="CUDA_ERROR",
                        status="DETECTED",
                        severity="CRITICAL",
                        confidence=1.0,
                        reason="CUDA Out Of Memory Exception detected in stdout/stderr log output!",
                        details={"log_line": line}
                    ))
                    break
                elif "torch.cuda.cudaerror" in line_lower or "cudnn_status_internal_error" in line_lower:
                    results.append(DetectionResult(
                        detection_type="CUDA_ERROR",
                        status="DETECTED",
                        severity="CRITICAL",
                        confidence=1.0,
                        reason="CUDA hardware/driver internal error detected in log stream!",
                        details={"log_line": line}
                    ))
                    break
                elif "traceback (most recent call last)" in line_lower or "syntaxerror" in line_lower:
                    results.append(DetectionResult(
                        detection_type="PYTHON_EXCEPTION",
                        status="DETECTED",
                        severity="CRITICAL",
                        confidence=0.99,
                        reason="Python runtime exception / stack traceback detected in process logs.",
                        details={"log_line": line}
                    ))
                    break

        return results
