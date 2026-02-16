"""
Main API application for the AI Todo Chatbot.
Sets up FastAPI app, middleware, and includes API routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AI Todo Chatbot API",
    description="API for the AI-powered Todo Chatbot application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
from .routes import chat
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy", "message": "AI Todo Chatbot API is running"}

@app.get("/")
async def root():
    """Root endpoint with basic information about the API."""
    return {
        "message": "Welcome to the AI Todo Chatbot API",
        "version": "1.0.0",
        "endpoints": [
            {
                "path": "/api/{user_id}/chat",
                "method": "POST",
                "description": "Chat with the AI agent"
            },
            {
                "path": "/health",
                "method": "GET",
                "description": "Health check endpoint"
            }
        ]
    }