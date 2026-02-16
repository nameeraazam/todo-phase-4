# Quickstart Guide: AI Todo Chatbot

**Feature**: AI Todo Chatbot (001-ai-todo-chatbot)
**Date**: 2026-02-08
**Authors**: [Team]

## Overview

This guide provides a quick introduction to setting up and running the AI Todo Chatbot locally. It covers the essential steps to get the application running and start testing the core functionality.

## Prerequisites

Before getting started, ensure you have the following installed:

- Python 3.11+
- Node.js 18+ (for frontend development)
- PostgreSQL (or access to Neon PostgreSQL)
- Git
- OpenAI API key

## Environment Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up backend environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up frontend environment**:
   ```bash
   cd ../frontend
   npm install
   ```

4. **Configure environment variables**:
   Create a `.env` file in the backend directory with the following:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot
   OPENAI_API_KEY=your_openai_api_key_here
   SECRET_KEY=your_secret_key_for_jwt_tokens
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Database Setup

1. **Initialize the database**:
   ```bash
   cd backend
   python -m src.models.init_db
   ```

2. **Run migrations** (if using Alembic):
   ```bash
   alembic upgrade head
   ```

## Running the Application

### Backend Server

1. **Start the backend**:
   ```bash
   cd backend
   uvicorn src.api.main:app --reload --port 8000
   ```

2. **Verify the backend is running**:
   Visit `http://localhost:8000/docs` to see the API documentation.

### Frontend Server

1. **Start the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

2. **Access the application**:
   Visit `http://localhost:3000` in your browser.

## Testing Core Functionality

### 1. Test the Chat Endpoint

Send a POST request to the chat endpoint:

```bash
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <valid-jwt-token>" \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": null
  }'
```

### 2. Test MCP Tools (Internal)

These are called by the AI agent but can be tested directly:

```bash
# Add a task
curl -X POST http://localhost:8000/api/mcp/add_task \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <valid-jwt-token>" \
  -d '{
    "task_text": "Test task"
  }'

# List tasks
curl -X GET http://localhost:8000/api/mcp/list_tasks \
  -H "Authorization: Bearer <valid-jwt-token>"
```

## Sample User Interactions

Once the application is running, you can interact with the AI Todo Chatbot using natural language:

- "Add a task to buy groceries"
- "What tasks do I have?"
- "Mark the grocery task as complete"
- "Remove the meeting task"
- "Remind me to call John tomorrow at 3 PM"

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Verify your PostgreSQL server is running
   - Check the DATABASE_URL in your .env file

2. **OpenAI API Error**:
   - Ensure your OPENAI_API_KEY is valid and has sufficient credits
   - Check that your account is enabled for the required API access

3. **JWT Authentication Error**:
   - Verify that you're sending a valid JWT token with each request
   - Check that the token hasn't expired

### Useful Commands

- **Reset database**: `python -m src.models.reset_db` (development only)
- **Run tests**: `pytest` (from backend directory)
- **Format code**: `black . && isort .` (from backend directory)

## Next Steps

1. Explore the API documentation at `http://localhost:8000/docs`
2. Customize the frontend components in `frontend/src/components/`
3. Add new MCP tools in `backend/src/mcp_tools/`
4. Extend the data models in `backend/src/models/`