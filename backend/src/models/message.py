"""
SQLModel model for the Message entity in the AI Todo Chatbot application.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum

# Define the Message model
class SenderType(str, Enum):
    USER = "user"
    AGENT = "agent"

class MessageType(str, Enum):
    TEXT = "text"
    COMMAND = "command"
    RESPONSE = "response"

class MessageBase(SQLModel):
    conversation_id: int = Field(foreign_key="conversation.id")
    sender_type: SenderType
    sender_id: int
    content: str = Field(min_length=1)
    message_type: MessageType = MessageType.TEXT

class Message(MessageBase, table=True):
    """Message model representing a single message within a conversation."""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[dict] = Field(default=None)  # Store as JSON
    
    # Relationship
    # Note: The conversation relationship will be defined in the Conversation model to avoid circular imports

class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    pass

class MessageRead(MessageBase):
    """Schema for reading message data."""
    id: int
    timestamp: datetime