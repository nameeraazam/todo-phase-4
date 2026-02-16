"""
SQLModel model for the Task entity in the AI Todo Chatbot application.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum

# Define the Task model
class TaskStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    completed: bool = False
    user_id: int = Field(foreign_key="user.id")

class Task(TaskBase, table=True):
    """Task model representing a user's to-do item."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)
    
    # Relationship
    # Note: The user relationship will be defined in the User model to avoid circular imports

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass

class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None