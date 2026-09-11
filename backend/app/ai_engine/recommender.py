from typing import List, Dict, Any

class RecommendationEngine:
    @staticmethod
    def generate_recommendations(
        anomalies: List[Dict[str, Any]],
        gpu_utilization: float,
        gpu_memory_pct: float,
        current_lr: float
    ) -> List[Dict[str, Any]]:
        recommendations = []

        for anomaly in anomalies:
            atype = anomaly.get("anomaly_type")
            if atype == "NAN_LOSS":
                recommendations.append({
                    "type": "HYPERPARAMETER",
                    "priority": "HIGH",
                    "title": "Reduce Learning Rate & Add Gradient Clipping",
                    "description": f"Loss exploded to NaN. Reduce learning rate by 5x-10x (from {current_lr} to {current_lr/10.0}) and add `torch.nn.utils.clip_grad_norm_`."
                })
            elif atype == "OVERFITTING":
                recommendations.append({
                    "type": "EARLY_STOPPING",
                    "priority": "MEDIUM",
                    "title": "Enable Early Stopping or Increase Regularization",
                    "description": "Validation loss is diverging from training loss. Add Weight Decay, Dropout (e.g. 0.3), or trigger Early Stopping."
                })
            elif atype == "OVERHEATING":
                recommendations.append({
                    "type": "HARDWARE",
                    "priority": "HIGH",
                    "title": "Throttle GPU / Fan Speed Adjustment Required",
                    "description": "GPU temperature exceeds safe operational limits. Pause job or decrease target batch size to lower GPU thermal output."
                })

        # Hardware Efficiency recommendations
        if gpu_utilization < 50.0 and gpu_memory_pct < 60.0:
            recommendations.append({
                "type": "PERFORMANCE",
                "priority": "LOW",
                "title": "Increase Batch Size or DataLoader Workers",
                "description": f"GPU is under-utilized ({gpu_utilization:.1f}% util, {gpu_memory_pct:.1f}% VRAM). Increase batch size or num_workers to speed up training."
            })

        return recommendations
