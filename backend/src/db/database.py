"""
Database setup module for the AI Todo Chatbot application.
This module handles database connection, session management, and initialization.
"""

from sqlmodel import create_engine, Session
from .models import SQLModel  # Import all models to register them with SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/todo_chatbot")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize the database by creating all tables."""
    SQLModel.metadata.create_all(engine)