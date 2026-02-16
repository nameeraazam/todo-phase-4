"""
SQLModel models for the AI Todo Chatbot application.
Defines the database schema for Task, Conversation, Message, and User entities.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid

# Define the base SQLModel class that all models inherit from
class BaseSQLModel(SQLModel):
    """Base class for all SQLModels in the application."""
    pass

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
    user: User = Relationship(back_populates="tasks")

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
    user: User = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")

class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    pass

class ConversationRead(ConversationBase):
    """Schema for reading conversation data."""
    id: int
    created_at: datetime
    updated_at: datetime

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
    conversation: Conversation = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    pass

class MessageRead(MessageBase):
    """Schema for reading message data."""
    id: int
    timestamp: datetime