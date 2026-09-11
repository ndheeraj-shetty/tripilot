import re
import sys
from typing import Optional, Dict, Any, List
from app.adapters.base_adapter import BaseFrameworkAdapter, ParsedMetricPayload

class YOLOAdapter(BaseFrameworkAdapter):
    framework_name = "Ultralytics YOLO"

    # Ultralytics YOLO progress bar line pattern
    YOLO_LINE_PATTERN = re.compile(
        r'^\s*(\d+)/(\d+)\s+([0-9\.]+[GM])\s+([0-9\.]+)\s+([0-9\.]+)\s+([0-9\.]+)',
        re.IGNORECASE
    )
    YOLO_MAP_PATTERN = re.compile(
        r'all\s+\d+\s+\d+\s+([0-9\.]+)\s+([0-9\.]+)\s+([0-9\.]+)\s+([0-9\.]+)',
        re.IGNORECASE
    )

    def parse_stdout_line(self, line: str) -> Optional[ParsedMetricPayload]:
        if not line or not line.strip():
            return None

        match = self.YOLO_LINE_PATTERN.search(line)
        if match:
            epoch = int(match.group(1))
            box_loss = float(match.group(4))
            cls_loss = float(match.group(5))
            dfl_loss = float(match.group(6))
            total_loss = box_loss + cls_loss + dfl_loss
            return ParsedMetricPayload(
                epoch=epoch,
                step=0,
                loss=total_loss,
                val_loss=None,
                accuracy=None
            )

        map_match = self.YOLO_MAP_PATTERN.search(line)
        if map_match:
            map50 = float(map_match.group(3))
            map50_95 = float(map_match.group(4))
            return ParsedMetricPayload(
                epoch=0,
                step=0,
                loss=None,
                val_loss=None,
                accuracy=map50_95
            )

        return None

    def build_launch_command(
        self,
        script_path: str,
        hyperparameters: Dict[str, Any],
        extra_args: Optional[List[str]] = None
    ) -> List[str]:
        if script_path.endswith(".py"):
            cmd = [sys.executable, script_path]
        else:
            cmd = ["yolo", "train"]
        for key, val in hyperparameters.items():
            cmd.append(f"{key}={val}")
        if extra_args:
            cmd.extend(extra_args)
        return cmd
