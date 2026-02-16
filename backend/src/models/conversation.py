"""
SQLModel model for the Conversation entity in the AI Todo Chatbot application.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Define the Conversation model
class ConversationBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    title: Optional[str] = Field(default=None, max_length=200)
    is_active: bool = True

class Conversation(ConversationBase, table=True):
    """Conversation model representing a sequence of interactions between a user and the AI chatbot."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    # Note: The user and messages relationships will be defined in the User and Message models to avoid circular imports

class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    pass

class ConversationRead(ConversationBase):
    """Schema for reading conversation data."""
    id: int
    created_at: datetime
    updated_at: datetime