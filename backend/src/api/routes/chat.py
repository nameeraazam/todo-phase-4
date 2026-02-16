"""
Chat route for the AI Todo Chatbot API.
Handles user chat interactions with the AI agent.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from src.auth.authentication import get_current_active_user, User
from src.services.ai_agent_service import AI_Agent_Service
from src.mcp_tools.add_task import add_task
from src.mcp_tools.list_tasks import list_tasks

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    timestamp: datetime

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_with_agent(
    user_id: str, 
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Initiates or continues a conversation with the AI agent for a specific user.
    
    - **user_id**: The ID of the user (extracted from JWT token for validation)
    - **message**: The user's message/input
    - **conversation_id**: ID of existing conversation to continue, or null to start new
    """
    try:
        # Initialize AI agent service
        ai_agent = AI_Agent_Service()
        
        # Process the user's message through the AI agent
        response = await ai_agent.process_message(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )
        
        # Return the response
        return ChatResponse(
            conversation_id=response.get("conversation_id", str(uuid4())),
            response=response.get("response", "I processed your request."),
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )