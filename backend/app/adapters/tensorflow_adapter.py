import re
import sys
from typing import Optional, Dict, Any, List
from app.adapters.base_adapter import BaseFrameworkAdapter, ParsedMetricPayload

class TensorFlowAdapter(BaseFrameworkAdapter):
    framework_name = "TensorFlow"

    # TensorFlow Keras output format:
    # Epoch 1/10
    # 500/500 [==============================] - 2s 4ms/step - loss: 0.4512 - accuracy: 0.8120 - val_loss: 0.4910 - val_accuracy: 0.7950
    EPOCH_PATTERN = re.compile(r'Epoch\s+(\d+)/\d+', re.IGNORECASE)
    KERAS_METRIC_PATTERN = re.compile(r'(\d+)/\d+\s+\[=+\].*?-\s+loss:\s*([0-9\.]+)(?:.*?accuracy:\s*([0-9\.]+))?(?:.*?val_loss:\s*([0-9\.]+))?(?:.*?val_accuracy:\s*([0-9\.]+))?', re.IGNORECASE)

    def parse_stdout_line(self, line: str) -> Optional[ParsedMetricPayload]:
        if not line or not line.strip():
            return None

        epoch_match = self.EPOCH_PATTERN.search(line)
        metric_match = self.KERAS_METRIC_PATTERN.search(line)

        if not metric_match:
            return None

        step = int(metric_match.group(1))
        loss = float(metric_match.group(2)) if metric_match.group(2) else None
        acc = float(metric_match.group(3)) if metric_match.group(3) else None
        val_loss = float(metric_match.group(4)) if metric_match.group(4) else None
        val_acc = float(metric_match.group(5)) if metric_match.group(5) else acc

        return ParsedMetricPayload(
            epoch=0, # Epoch context passed from previous line if needed
            step=step,
            loss=loss,
            val_loss=val_loss,
            accuracy=val_acc
        )

    def build_launch_command(
        self,
        script_path: str,
        hyperparameters: Dict[str, Any],
        extra_args: Optional[List[str]] = None
    ) -> List[str]:
        cmd = [sys.executable, script_path]
        for key, val in hyperparameters.items():
            cmd.append(f"--{key}")
            cmd.append(str(val))
        if extra_args:
            cmd.extend(extra_args)
        return cmd
