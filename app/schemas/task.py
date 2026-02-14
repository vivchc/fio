from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    """Shared properties"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$")

class TaskCreate(TaskBase):
    """Properties to receive on task creation"""
    pass

class TaskUpdate(BaseModel):
    """Properties to receive on task update"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed)$")

class TaskResponse(TaskBase):
    """Properties to return to client"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}