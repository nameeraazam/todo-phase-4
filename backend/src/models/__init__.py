"""
Main models module for the AI Todo Chatbot application.
Imports all individual models and defines relationships.
"""

from .task import Task, TaskCreate, TaskRead, TaskUpdate
from .conversation import Conversation, ConversationCreate, ConversationRead
from .message import Message, MessageCreate, MessageRead
from .user import User, UserCreate, UserRead

# Import SQLModel for convenience
from sqlmodel import SQLModel

# Define all models in __all__ for easy importing
__all__ = [
    "SQLModel",
    "Task",
    "TaskCreate",
    "TaskRead",
    "TaskUpdate",
    "Conversation",
    "ConversationCreate",
    "ConversationRead",
    "Message",
    "MessageCreate",
    "MessageRead",
    "User",
    "UserCreate",
    "UserRead"
]