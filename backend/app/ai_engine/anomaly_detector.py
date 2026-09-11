import math
from typing import List, Dict, Any, Optional

class AnomalyResult:
    def __init__(self, is_anomaly: bool, anomaly_type: str, severity: str, message: str, details: Dict[str, Any]):
        self.is_anomaly = is_anomaly
        self.anomaly_type = anomaly_type # NAN_LOSS, OVERHEATING, OVERFITTING, UNDERFITTING, OOM_RISK
        self.severity = severity # CRITICAL, WARNING, INFO
        self.message = message
        self.details = details

class AnomalyDetector:
    def __init__(
        self,
        gpu_temp_threshold: float = 85.0,
        overfitting_patience_epochs: int = 5,
        underfitting_patience_epochs: int = 10
    ):
        self.gpu_temp_threshold = gpu_temp_threshold
        self.overfitting_patience_epochs = overfitting_patience_epochs
        self.underfitting_patience_epochs = underfitting_patience_epochs

    def check_nan_loss(self, loss: Optional[float]) -> Optional[AnomalyResult]:
        if loss is not None and (math.isnan(loss) or math.isinf(loss)):
            return AnomalyResult(
                is_anomaly=True,
                anomaly_type="NAN_LOSS",
                severity="CRITICAL",
                message="Training loss exploded or diverged to NaN/Infinity!",
                details={"loss_value": str(loss)}
            )
        return None

    def check_gpu_overheating(self, gpu_temp_c: Optional[float]) -> Optional[AnomalyResult]:
        if gpu_temp_c and gpu_temp_c >= self.gpu_temp_threshold:
            return AnomalyResult(
                is_anomaly=True,
                anomaly_type="OVERHEATING",
                severity="CRITICAL" if gpu_temp_c >= 90.0 else "WARNING",
                message=f"GPU temperature reached {gpu_temp_c:.1f}°C (Threshold: {self.gpu_temp_threshold}°C)!",
                details={"gpu_temperature_c": gpu_temp_c, "threshold": self.gpu_temp_threshold}
            )
        return None

    def check_overfitting(self, train_losses: List[float], val_losses: List[float]) -> Optional[AnomalyResult]:
        """Detects sustained divergence where train loss decreases but val loss increases for N consecutive epochs."""
        if len(train_losses) < self.overfitting_patience_epochs or len(val_losses) < self.overfitting_patience_epochs:
            return None

        # Check last N epochs
        recent_train = train_losses[-self.overfitting_patience_epochs:]
        recent_val = val_losses[-self.overfitting_patience_epochs:]

        train_decreasing = all(recent_train[i] <= recent_train[i-1] for i in range(1, len(recent_train)))
        val_increasing = all(recent_val[i] > recent_val[i-1] for i in range(1, len(recent_val)))

        if train_decreasing and val_increasing:
            divergence_ratio = (recent_val[-1] - recent_val[0]) / max(recent_val[0], 1e-6)
            return AnomalyResult(
                is_anomaly=True,
                anomaly_type="OVERFITTING",
                severity="WARNING",
                message=f"Overfitting detected! Validation loss diverged by {divergence_ratio*100:.1f}% over the last {self.overfitting_patience_epochs} epochs while training loss decreased.",
                details={
                    "patience_epochs": self.overfitting_patience_epochs,
                    "recent_train_losses": recent_train,
                    "recent_val_losses": recent_val
                }
            )
        return None

    def check_underfitting(self, loss_history: List[float], min_improvement: float = 0.001) -> Optional[AnomalyResult]:
        """Detects plateaued high loss over N epochs."""
        if len(loss_history) < self.underfitting_patience_epochs:
            return None

        recent = loss_history[-self.underfitting_patience_epochs:]
        delta = abs(recent[-1] - recent[0])
        if delta < min_improvement and recent[-1] > 0.5:
            return AnomalyResult(
                is_anomaly=True,
                anomaly_type="UNDERFITTING",
                severity="WARNING",
                message=f"Training appears to have plateaued at high loss ({recent[-1]:.4f}) for {self.underfitting_patience_epochs} epochs.",
                details={"current_loss": recent[-1], "flat_epochs": self.underfitting_patience_epochs}
            )
        return None
