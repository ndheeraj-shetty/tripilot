from typing import List, Dict, Any
from pydantic import BaseModel

class HealthScoreResult(BaseModel):
    score: int # 0 - 100
    category: str # EXCELLENT, GOOD, WARNING, CRITICAL
    sub_scores: Dict[str, int]

class HealthScoreService:
    def calculate(
        self,
        detections: List[Any],
        telemetry: Dict[str, Any],
        prediction_fail_prob: float
    ) -> HealthScoreResult:
        base_score = 100

        # Sub-score components
        loss_health = 100
        hardware_health = 100
        stability_health = 100

        # Penalty deductions
        for d in detections:
            sev = getattr(d, 'severity', d.get('severity') if isinstance(d, dict) else '')
            dtype = getattr(d, 'detection_type', d.get('detection_type') if isinstance(d, dict) else '')

            if sev == 'CRITICAL':
                if dtype in ['NAN_LOSS', 'EXPLODING_LOSS']:
                    loss_health = max(0, loss_health - 80)
                elif dtype in ['GPU_OVERHEATING', 'GPU_MEMORY_EXHAUSTION', 'CUDA_ERROR']:
                    hardware_health = max(0, hardware_health - 70)
                stability_health = max(0, stability_health - 50)
            elif sev == 'WARNING':
                if dtype == 'OVERFITTING':
                    loss_health = max(0, loss_health - 25)
                elif dtype == 'UNDERFITTING':
                    loss_health = max(0, loss_health - 20)
                hardware_health = max(0, hardware_health - 20)

        # Failure probability deduction
        fail_deduction = int(prediction_fail_prob * 50)
        overall_score = max(0, int((loss_health * 0.4) + (hardware_health * 0.3) + (stability_health * 0.3) - fail_deduction))

        category = "EXCELLENT"
        if overall_score >= 90:
            category = "EXCELLENT"
        elif overall_score >= 75:
            category = "GOOD"
        elif overall_score >= 50:
            category = "WARNING"
        else:
            category = "CRITICAL"

        return HealthScoreResult(
            score=overall_score,
            category=category,
            sub_scores={
                "loss_health": loss_health,
                "hardware_health": hardware_health,
                "stability_health": stability_health,
                "fail_prob_pct": int(prediction_fail_prob * 100)
            }
        )
