from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    """ Base schema for tasks. """
    title: str = Field(..., min_length=1, max_length=200)  # Must provide a title
    description: Optional[str] = None
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$")  # Defaults to "pending". Rejects anything besides the 3 states.

class TaskCreate(TaskBase):
    """ Schema for creating a new task. """
    pass

class TaskUpdate(BaseModel):
    """ Optional fields for updating a task. If provided, must have the same validation as TaskBase. """
    title: Optional[str] = Field(None, min_length=1, max_length=200)  
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed)$")  # Rejects anything besides the 3 states

class TaskResponse(TaskBase):
    """ 
		Schema for responding with task details. 
    Converts SQLAlchemy model to Pydantic schema so FastAPI can use it to build a JSON response.
		"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}  # Tells Pydantic to access attributes (instead of dict key lookup)