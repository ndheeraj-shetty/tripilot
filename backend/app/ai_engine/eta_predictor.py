import time
from typing import List, Optional

class ETAPredictor:
    def __init__(self, smoothing_factor: float = 0.2):
        self.smoothing_factor = smoothing_factor
        self.avg_step_time_ms: Optional[float] = None
        self.last_step_time: Optional[float] = None

    def update_and_predict(self, current_epoch: int, total_epochs: int, current_step: int, total_steps_per_epoch: int) -> float:
        """Returns estimated remaining seconds."""
        now = time.time()
        if self.last_step_time is not None:
            step_duration_ms = (now - self.last_step_time) * 1000.0
            if self.avg_step_time_ms is None:
                self.avg_step_time_ms = step_duration_ms
            else:
                self.avg_step_time_ms = (self.smoothing_factor * step_duration_ms) + ((1.0 - self.smoothing_factor) * self.avg_step_time_ms)
        self.last_step_time = now

        if self.avg_step_time_ms is None or self.avg_step_time_ms <= 0:
            return 0.0

        remaining_epochs = max(0, total_epochs - current_epoch)
        remaining_steps_in_current_epoch = max(0, total_steps_per_epoch - current_step)
        total_remaining_steps = (remaining_epochs * total_steps_per_epoch) + remaining_steps_in_current_epoch

        remaining_seconds = (total_remaining_steps * self.avg_step_time_ms) / 1000.0
        return max(0.0, remaining_seconds)
