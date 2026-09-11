from typing import List, Dict, Any
from pydantic import BaseModel

class TrendAnalysisResult(BaseModel):
    metric_type: str
    moving_average_5: float
    moving_average_20: float
    slope: float
    direction: str # RISING, FALLING, FLAT

class TrendAnalysisService:
    def analyze_trends(self, metrics: List[Dict[str, Any]]) -> List[TrendAnalysisResult]:
        results: List[TrendAnalysisResult] = []

        keys = ["loss", "val_loss", "accuracy"]
        for key in keys:
            series = [m[key] for m in metrics if m.get(key) is not None]
            if not series:
                continue

            ma5 = sum(series[-5:]) / min(len(series), 5)
            ma20 = sum(series[-20:]) / min(len(series), 20)
            
            slope = 0.0
            if len(series) >= 2:
                slope = series[-1] - series[0]

            direction = "FLAT"
            if slope > 0.005:
                direction = "RISING"
            elif slope < -0.005:
                direction = "FALLING"

            results.append(TrendAnalysisResult(
                metric_type=key,
                moving_average_5=round(ma5, 4),
                moving_average_20=round(ma20, 4),
                slope=round(slope, 4),
                direction=direction
            ))

        return results
