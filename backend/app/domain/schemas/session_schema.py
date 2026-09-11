from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class SessionLaunch(BaseModel):
    project_id: UUID
    session_name: Optional[str] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    command_args: Optional[list[str]] = None

class SessionResponse(BaseModel):
    id: UUID
    project_id: UUID
    session_name: str
    status: str
    pid: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    exit_code: Optional[int] = None
    hyperparameters: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
