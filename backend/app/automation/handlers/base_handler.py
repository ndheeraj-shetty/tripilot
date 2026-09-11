from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class ActionContext(BaseModel):
    session_id: str
    project_id: str
    status: str
    output_dir: str
    checkpoint_dir: str
    best_checkpoint_path: Optional[str] = None
    error_message: Optional[str] = None

class ActionResult(BaseModel):
    success: bool
    action_type: str
    message: str
    details: Dict[str, Any] = {}

class BaseActionHandler(ABC):
    action_type: str

    @abstractmethod
    async def execute(self, params: Dict[str, Any], context: ActionContext) -> ActionResult:
        """Executes the specific action given user parameters and execution context."""
        pass
