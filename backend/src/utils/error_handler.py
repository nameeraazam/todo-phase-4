"""
Error handling and logging utilities for the AI Todo Chatbot application.
"""

import logging
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import traceback
import sys
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class AppException(Exception):
    """Base exception class for the application."""
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "APP_ERROR"
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self):
        """Convert the exception to a dictionary for JSON serialization."""
        return {
            "error": {
                "code": self.error_code,
                "message": self.message,
                "details": self.details,
                "timestamp": self.timestamp
            }
        }

class ValidationError(AppException):
    """Exception raised for validation errors."""
    def __init__(self, message: str, field: str = None, value: Any = None):
        details = {"field": field, "value": value} if field else {}
        super().__init__(message, "VALIDATION_ERROR", details)

class DatabaseError(AppException):
    """Exception raised for database-related errors."""
    def __init__(self, message: str, query: str = None):
        details = {"query": query} if query else {}
        super().__init__(message, "DATABASE_ERROR", details)

class BusinessLogicError(AppException):
    """Exception raised for business logic violations."""
    def __init__(self, message: str, context: Dict[str, Any] = None):
        super().__init__(message, "BUSINESS_LOGIC_ERROR", context or {})

def handle_error(exception: Exception, request_info: Dict[str, Any] = None) -> JSONResponse:
    """
    Generic error handler that logs the error and returns an appropriate response.
    
    Args:
        exception: The exception that occurred
        request_info: Information about the request context
        
    Returns:
        JSONResponse with error details
    """
    # Log the error with traceback
    logger.error(
        f"Error occurred: {str(exception)}\nTraceback: {traceback.format_exc()}",
        extra={"request_info": request_info}
    )
    
    # Handle different types of exceptions
    if isinstance(exception, HTTPException):
        # Return the existing HTTP exception
        return JSONResponse(
            status_code=exception.status_code,
            content={
                "error": {
                    "code": "HTTP_ERROR",
                    "message": exception.detail,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    elif isinstance(exception, AppException):
        # Return the application-specific exception
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=exception.to_dict()
        )
    else:
        # Handle unexpected errors
        unexpected_error = AppException(
            "An unexpected error occurred",
            "UNEXPECTED_ERROR",
            {"original_error": str(exception)}
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=unexpected_error.to_dict()
        )

def log_api_call(endpoint: str, method: str, user_id: str = None, duration: float = None):
    """
    Log an API call with relevant information.
    
    Args:
        endpoint: The API endpoint that was called
        method: The HTTP method used
        user_id: The ID of the user making the request
        duration: The time taken to process the request (in seconds)
    """
    log_data = {
        "type": "api_call",
        "endpoint": endpoint,
        "method": method,
        "user_id": user_id,
        "duration_ms": round(duration * 1000, 2) if duration else None,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.info(json.dumps(log_data))

def log_task_action(action: str, task_id: int = None, user_id: str = None, details: Dict[str, Any] = None):
    """
    Log a task-related action.
    
    Args:
        action: The action performed (e.g., 'created', 'updated', 'completed')
        task_id: The ID of the task
        user_id: The ID of the user performing the action
        details: Additional details about the action
    """
    log_data = {
        "type": "task_action",
        "action": action,
        "task_id": task_id,
        "user_id": user_id,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.info(json.dumps(log_data))