"""
SQLModel model for the User entity in the AI Todo Chatbot application.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Define the User model
class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: str = Field(max_length=100)
    is_active: bool = True

class User(UserBase, table=True):
    """User model representing an individual user of the system."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

class UserRead(UserBase):
    """Schema for reading user data."""
    id: int
    created_at: datetime
    updated_at: datetime

# Also need to import and define the relationship in the Task model
# This would typically be done in a separate file or by using lazy loading