from typing import List, Dict, Any
from pydantic import BaseModel

class RecommendationResult(BaseModel):
    title: str
    description: str
    priority: str # HIGH, MEDIUM, LOW
    category: str # HYPERPARAMETER, HARDWARE, OPTIMIZATION
    reason: str
    confidence: float
    expected_impact: str

class RecommendationService:
    def generate(
        self,
        detections: List[Any],
        telemetry: Dict[str, Any],
        current_lr: float = 0.001
    ) -> List[RecommendationResult]:
        recs: List[RecommendationResult] = []

        detection_types = set()
        for d in detections:
            if isinstance(d, dict):
                detection_types.add(d.get("detection_type"))
            else:
                detection_types.add(getattr(d, "detection_type", None))

        # 1. Hyperparameter Advice
        if "NAN_LOSS" in detection_types or "EXPLODING_LOSS" in detection_types:
            recs.append(RecommendationResult(
                title="Lower Learning Rate & Enable Gradient Clipping",
                description=f"Loss exploded or diverged. Reduce learning rate by 5x to 10x (from {current_lr:.6f} to {current_lr/10.0:.6f}) and add `torch.nn.utils.clip_grad_norm_`.",
                priority="HIGH",
                category="HYPERPARAMETER",
                reason="NaN or exploding loss detected during optimization steps.",
                confidence=0.98,
                expected_impact="Stabilizes gradient optimization and prevents numeric overflow."
            ))

        if "OVERFITTING" in detection_types:
            recs.append(RecommendationResult(
                title="Enable Early Stopping & Increase Regularization",
                description="Validation loss diverged while train loss decreased. Enable Early Stopping, add Weight Decay (0.01), or increase Dropout probability (e.g. 0.3).",
                priority="MEDIUM",
                category="HYPERPARAMETER",
                reason="Validation loss trend is diverging from training loss.",
                confidence=0.92,
                expected_impact="Prevents model from memorizing noise in training dataset."
            ))

        if "UNDERFITTING" in detection_types:
            recs.append(RecommendationResult(
                title="Increase Learning Rate or Model Capacity",
                description="Loss plateaued at high value. Consider increasing learning rate or switching to a higher capacity model architecture (e.g. ResNet101 / YOLOv8x).",
                priority="MEDIUM",
                category="HYPERPARAMETER",
                reason="Training loss stopped improving prematurely.",
                confidence=0.85,
                expected_impact="Escapes local minima and improves model representation power."
            ))

        # 2. Hardware & Optimization Advice
        gpu_pct = telemetry.get("gpu_utilization_pct", 100)
        vram_pct = (telemetry.get("gpu_memory_used_mb", 0) / max(telemetry.get("gpu_memory_total_mb", 1), 1)) * 100

        if "GPU_OVERHEATING" in detection_types:
            recs.append(RecommendationResult(
                title="Throttle GPU Fan Speed or Reduce Batch Size",
                description="GPU thermal limits exceeded. Pause job briefly to allow cooling or decrease batch size to lower thermal load.",
                priority="HIGH",
                category="HARDWARE",
                reason=f"GPU temperature reached {telemetry.get('gpu_temperature_c')}°C.",
                confidence=0.95,
                expected_impact="Prevents hardware thermal throttling and premature GPU shutdown."
            ))

        if gpu_pct < 50.0 and vram_pct < 60.0 and "GPU_OVERHEATING" not in detection_types:
            recs.append(RecommendationResult(
                title="Enable Mixed Precision (FP16/BF16) & Increase Batch Size",
                description="GPU is under-utilized. Enable automatic mixed precision (AMP) and double batch size to double training throughput.",
                priority="LOW",
                category="OPTIMIZATION",
                reason=f"GPU utilization is low ({gpu_pct:.1f}%) with {vram_pct:.1f}% VRAM available.",
                confidence=0.88,
                expected_impact="Increases training speed (samples/sec) by up to 2.5x."
            ))

        if not recs:
            recs.append(RecommendationResult(
                title="Training Appears Healthy & Optimal",
                description="No critical anomalies detected. System hardware metrics and loss convergence are operating within nominal thresholds.",
                priority="LOW",
                category="OPTIMIZATION",
                reason="Loss decay and hardware utilization are optimal.",
                confidence=0.95,
                expected_impact="Maintain current training hyperparameters."
            ))

        return recs
