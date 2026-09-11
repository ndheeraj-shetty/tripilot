from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class ActionConfig(BaseModel):
    action_type: str # SAVE_BEST_MODEL, GENERATE_REPORT, COMPRESS_LOGS, STOP_PROCESS, SYSTEM_SHUTDOWN, SYSTEM_SLEEP, SYSTEM_HIBERNATE, NOTIFY_USER
    params: Dict[str, Any] = {}

class RuleBase(BaseModel):
    project_id: Optional[UUID] = None # None = Global
    name: str
    trigger_event: str # ON_SUCCESS, ON_FAILED, ON_OVERHEATING, ON_NAN
    conditions_json: Dict[str, Any] = {}
    actions_sequence: List[ActionConfig]
    is_active: bool = True

class RuleCreate(RuleBase):
    pass

class RuleUpdate(BaseModel):
    name: Optional[str] = None
    trigger_event: Optional[str] = None
    conditions_json: Optional[Dict[str, Any]] = None
    actions_sequence: Optional[List[ActionConfig]] = None
    is_active: Optional[bool] = None

class RuleResponse(RuleBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
