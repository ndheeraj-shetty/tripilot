import re
import sys
from typing import Optional, Dict, Any, List
from app.adapters.base_adapter import BaseFrameworkAdapter, ParsedMetricPayload

class PyTorchAdapter(BaseFrameworkAdapter):
    framework_name = "PyTorch"

    # Enhanced Regex Patterns for PyTorch logs
    EPOCH_PAIR_PATTERN = re.compile(r'(?:epoch|ep)[:\s]*\[?(\d+)\s*/\s*(\d+)\]?', re.IGNORECASE)
    STEP_PAIR_PATTERN = re.compile(r'(?:step|batch|iter)[:\s]*\[?(\d+)\s*/\s*(\d+)\]?', re.IGNORECASE)
    EPOCH_PATTERN = re.compile(r'(?:epoch|ep)[:\s]*\[?(\d+)\]?', re.IGNORECASE)
    STEP_PATTERN = re.compile(r'(?:step|batch|iter)[:\s]*\[?(\d+)\]?', re.IGNORECASE)
    LOSS_PATTERN = re.compile(r'(?:train[\s_]*loss|training[\s_]*loss|loss)[:\s]*([0-9]+\.?[0-9]*(?:e[-+]?[0-9]+)?|nan|inf)', re.IGNORECASE)
    VAL_LOSS_PATTERN = re.compile(r'(?:val[\s_]*loss|validation[\s_]*loss|test[\s_]*loss)[:\s]*([0-9]+\.?[0-9]*(?:e[-+]?[0-9]+)?|nan|inf)', re.IGNORECASE)
    ACC_PATTERN = re.compile(r'(?:val_acc|val_accuracy|accuracy|acc)[:\s]*([0-9]+\.?[0-9]*)', re.IGNORECASE)
    LR_PATTERN = re.compile(r'(?:lr|learning_rate)[:\s]*([0-9]+\.?[0-9]*(?:e[-+]?[0-9]+)?)', re.IGNORECASE)
    STAGE_PATTERN = re.compile(r'\[STAGE:\s*([A-Z_]+)\]', re.IGNORECASE)
    ETA_PATTERN = re.compile(r'(?:eta)[:\s]*([0-9]+\.?[0-9]*)s?', re.IGNORECASE)
    ELAPSED_PATTERN = re.compile(r'(?:elapsed)[:\s]*([0-9]+\.?[0-9]*)s?', re.IGNORECASE)

    def parse_stdout_line(self, line: str) -> Optional[ParsedMetricPayload]:
        if not line or not line.strip():
            return None

        epoch_pair = self.EPOCH_PAIR_PATTERN.search(line)
        step_pair = self.STEP_PAIR_PATTERN.search(line)
        epoch_match = epoch_pair or self.EPOCH_PATTERN.search(line)
        step_match = step_pair or self.STEP_PATTERN.search(line)
        loss_match = self.LOSS_PATTERN.search(line)
        val_loss_match = self.VAL_LOSS_PATTERN.search(line)
        acc_match = self.ACC_PATTERN.search(line)
        lr_match = self.LR_PATTERN.search(line)
        stage_match = self.STAGE_PATTERN.search(line)
        eta_match = self.ETA_PATTERN.search(line)
        elapsed_match = self.ELAPSED_PATTERN.search(line)

        if not epoch_match and not loss_match and not stage_match:
            return None

        def safe_float(match):
            if not match:
                return None
            val = match.group(1).lower()
            if val == 'nan':
                return float('nan')
            if val == 'inf':
                return float('inf')
            try:
                return float(val)
            except ValueError:
                return None

        epoch = int(epoch_match.group(1)) if epoch_match else 0
        total_epochs = int(epoch_pair.group(2)) if epoch_pair else None
        
        current_batch = int(step_match.group(1)) if step_match else 0
        total_batches = int(step_pair.group(2)) if step_pair else None
        
        loss = safe_float(loss_match)
        val_loss = safe_float(val_loss_match)
        acc = safe_float(acc_match)
        lr = safe_float(lr_match)
        stage = stage_match.group(1).upper() if stage_match else None
        eta = safe_float(eta_match)
        elapsed = safe_float(elapsed_match)

        progress_pct = None
        if epoch and total_epochs:
            if current_batch and total_batches:
                progress_pct = round((((epoch - 1) * total_batches + current_batch) / (total_epochs * total_batches)) * 100, 1)
            else:
                progress_pct = round((epoch / total_epochs) * 100, 1)

        return ParsedMetricPayload(
            epoch=epoch,
            step=current_batch,
            loss=loss,
            val_loss=val_loss,
            accuracy=acc,
            learning_rate=lr,
            total_epochs=total_epochs,
            current_batch=current_batch,
            total_batches=total_batches,
            progress_pct=progress_pct,
            eta_sec=eta,
            elapsed_sec=elapsed,
            stage=stage
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
