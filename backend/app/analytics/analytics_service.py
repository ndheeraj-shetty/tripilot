import logging
from typing import Dict, Any, List
from uuid import UUID

logger = logging.getLogger(__name__)

class AnalyticsService:
    def generate_ai_insights(self, metrics: List[Dict[str, Any]], telemetry: List[Dict[str, Any]]) -> List[str]:
        insights = []

        if not metrics:
            insights.append("Training session initialized. Live loss curves and hardware stats are being logged.")
            return insights

        losses = [m.get("loss") for m in metrics if m.get("loss") is not None]
        val_losses = [m.get("val_loss") for m in metrics if m.get("val_loss") is not None]
        accuracies = [m.get("accuracy") for m in metrics if m.get("accuracy") is not None]

        if len(losses) >= 2:
            min_loss_idx = losses.index(min(losses))
            insights.append(f"Checkpoint / Epoch {min_loss_idx + 1} produced the best training loss ({min(losses):.4f}).")

        if len(val_losses) >= 3 and val_losses[-1] > min(val_losses):
            min_val = min(val_losses)
            insights.append(f"Validation Loss increased after reaching minimum ({min_val:.4f} -> {val_losses[-1]:.4f}), indicating slight overfitting divergence.")

        if telemetry:
            gpu_pcts = [t.get("gpu_utilization_pct", 0) for t in telemetry if t.get("gpu_utilization_pct") is not None]
            if gpu_pcts and (sum(gpu_pcts) / len(gpu_pcts)) < 50.0:
                insights.append(f"Average GPU utilization stayed below 50% ({sum(gpu_pcts)/len(gpu_pcts):.1f}%). Enabling Mixed Precision (FP16) & increasing batch size will double throughput.")

        if not insights:
            insights.append("Training convergence and hardware resource utilization are optimal.")

        return insights

analytics_service = AnalyticsService()
