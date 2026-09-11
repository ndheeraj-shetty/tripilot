import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class PredictionResult(BaseModel):
    remaining_time_sec: float
    failure_probability: float # 0.0 to 1.0
    expected_completion_time: str
    memory_growth_trend: str # STABLE, INCREASING, DANGEROUS
    speed_trend: str # STABLE, DECREASING, INCREASING
    accuracy_trend: str # RISING, PLATEAUED, FALLING
    loss_trend: str # DECREASING, STAGNANT, EXPLODING

class PredictionService:
    def predict(
        self,
        current_step: int,
        total_steps: int,
        metrics_history: List[Dict[str, Any]],
        telemetry_history: List[Dict[str, Any]],
        detections: List[Any]
    ) -> PredictionResult:
        now = time.time()

        # 1. Failure Probability Calculation based on detections & loss variance
        fail_prob = 0.05 # Baseline 5%
        for d in detections:
            sev = getattr(d, 'severity', d.get('severity') if isinstance(d, dict) else '')
            if sev == 'CRITICAL':
                fail_prob = min(1.0, fail_prob + 0.50)
            elif sev == 'WARNING':
                fail_prob = min(1.0, fail_prob + 0.15)

        # 2. Memory Growth Trend Calculation
        vram_series = [t.get('gpu_memory_used_mb') for t in telemetry_history if t.get('gpu_memory_used_mb') is not None]
        mem_trend = "STABLE"
        if len(vram_series) >= 5:
            delta_mem = vram_series[-1] - vram_series[0]
            if delta_mem > 1500.0: # Grown >1.5GB over window
                mem_trend = "DANGEROUS"
                fail_prob = min(1.0, fail_prob + 0.20)
            elif delta_mem > 400.0:
                mem_trend = "INCREASING"

        # 3. Trends for Loss & Accuracy
        losses = [m['loss'] for m in metrics_history if m.get('loss') is not None]
        accs = [m['accuracy'] for m in metrics_history if m.get('accuracy') is not None]

        loss_trend = "DECREASING"
        if len(losses) >= 4:
            if losses[-1] > losses[0] * 1.5:
                loss_trend = "EXPLODING"
            elif abs(losses[-1] - losses[0]) < 0.005:
                loss_trend = "STAGNANT"

        acc_trend = "RISING"
        if len(accs) >= 4:
            if abs(accs[-1] - accs[0]) < 0.002:
                acc_trend = "PLATEAUED"
            elif accs[-1] < accs[0]:
                acc_trend = "FALLING"

        # 4. Remaining Time Calculation
        remaining_steps = max(0, total_steps - current_step)
        step_duration_sec = 0.5 # Default fallback step duration
        if len(metrics_history) >= 2:
            step_duration_sec = max(0.01, 10.0 / max(len(metrics_history), 1))

        rem_sec = round(remaining_steps * step_duration_sec, 1)
        comp_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now + rem_sec))

        return PredictionResult(
            remaining_time_sec=rem_sec,
            failure_probability=round(fail_prob, 2),
            expected_completion_time=comp_time_str,
            memory_growth_trend=mem_trend,
            speed_trend="STABLE",
            accuracy_trend=acc_trend,
            loss_trend=loss_trend
        )
