from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    framework: str # PyTorch, TensorFlow, YOLO
    model_name: str
    dataset_path: str
    training_script_path: str
    output_dir: str
    checkpoint_dir: str

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    framework: Optional[str] = None
    model_name: Optional[str] = None
    dataset_path: Optional[str] = None
    training_script_path: Optional[str] = None
    output_dir: Optional[str] = None
    checkpoint_dir: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
