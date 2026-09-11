import os
import sys
import shutil
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class ParsedMetricPayload(BaseModel):
    epoch: int
    step: int
    loss: Optional[float] = None
    val_loss: Optional[float] = None
    accuracy: Optional[float] = None
    learning_rate: Optional[float] = None
    step_time_ms: Optional[float] = None
    total_epochs: Optional[int] = None
    current_batch: Optional[int] = None
    total_batches: Optional[int] = None
    progress_pct: Optional[float] = None
    eta_sec: Optional[float] = None
    elapsed_sec: Optional[float] = None
    stage: Optional[str] = None
    gpu_state: Optional[str] = None
    cost_saved: Optional[float] = None

class EnvironmentValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    cuda_available: bool = False
    device_name: Optional[str] = None
    python_version: str = sys.version

class BaseFrameworkAdapter(ABC):
    framework_name: str

    @abstractmethod
    def parse_stdout_line(self, line: str) -> Optional[ParsedMetricPayload]:
        """Parses a raw line of stdout/stderr and extracts metrics if present."""
        pass

    @abstractmethod
    def build_launch_command(
        self,
        script_path: str,
        hyperparameters: Dict[str, Any],
        extra_args: Optional[List[str]] = None
    ) -> List[str]:
        """Constructs the command list to execute the training script."""
        pass

    def validate_environment(self, script_path: str) -> EnvironmentValidationResult:
        """Validates script existence, python installation, and environment prerequisites."""
        errors = []
        warnings = []

        # 1. Script existence check
        resolved_script = script_path
        if script_path and not os.path.isabs(script_path):
            root_candidate = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", script_path))
            if os.path.exists(root_candidate):
                resolved_script = root_candidate

        if not script_path or not os.path.exists(resolved_script):
            errors.append(f"Training script not found at path: '{script_path}'")

        # 2. Python executable check
        if not sys.executable or not os.path.exists(sys.executable):
            errors.append("Python executable not found in current environment.")

        # 3. Framework check (Attempt import in current environment)
        cuda_avail = False
        dev_name = None

        fw_lower = self.framework_name.lower()
        if "pytorch" in fw_lower or "torch" in fw_lower:
            try:
                import torch
                cuda_avail = torch.cuda.is_available()
                if cuda_avail:
                    dev_name = torch.cuda.get_device_name(0)
                else:
                    warnings.append("PyTorch is installed, but CUDA GPU acceleration is not available (CPU mode).")
            except ImportError:
                warnings.append("PyTorch library is not pre-installed in the application environment.")
        elif "tensorflow" in fw_lower:
            try:
                import tensorflow as tf
                gpus = tf.config.list_physical_devices('GPU')
                cuda_avail = len(gpus) > 0
                if cuda_avail:
                    dev_name = gpus[0].name
                else:
                    warnings.append("TensorFlow is installed, but no GPU devices were detected.")
            except ImportError:
                warnings.append("TensorFlow library is not pre-installed in the application environment.")

        return EnvironmentValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            cuda_available=cuda_avail,
            device_name=dev_name
        )
