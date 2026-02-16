# API Contracts: AI Todo Chatbot

**Feature**: AI Todo Chatbot (001-ai-todo-chatbot)
**Date**: 2026-02-08
**Authors**: [Team]

## Overview

This document defines the API contracts for the AI Todo Chatbot feature. It specifies the endpoints, request/response schemas, and error handling patterns based on the functional requirements.

## Base Configuration

- **Base URL**: `/api/v1`
- **Authentication**: JWT token in Authorization header (`Authorization: Bearer <token>`)
- **Content-Type**: `application/json`
- **Response Format**: JSON

## Endpoints

### 1. Chat Endpoint

Handles user chat interactions with the AI agent.

#### POST `/api/{user_id}/chat`

Initiates or continues a conversation with the AI agent for a specific user.

**Request**:
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "uuid-string-or-null-for-new-conversation"
}
```

**Request Parameters**:
- `user_id` (path): The ID of the user (extracted from JWT token for validation)
- `message` (body, required): The user's message/input
- `conversation_id` (body, optional): ID of existing conversation to continue, or null to start new

**Response (Success)**:
```json
{
  "conversation_id": "uuid-string",
  "response": "I've added the task 'buy groceries' for you.",
  "timestamp": "2026-02-08T10:30:00Z"
}
```

**Response Fields**:
- `conversation_id`: The ID of the conversation (new or existing)
- `response`: The AI agent's response to the user's message
- `timestamp`: When the response was generated

**Response Codes**:
- `200 OK`: Successfully processed the message
- `400 Bad Request`: Invalid request format
- `401 Unauthorized`: Invalid or missing authentication token
- `403 Forbidden`: User is trying to access another user's data
- `422 Unprocessable Entity`: Unable to process the natural language input
- `500 Internal Server Error`: Unexpected server error

### 2. MCP Tools Endpoints (Internal)

These endpoints represent the MCP tools that the AI agent will use internally. They are not directly exposed to the frontend but are called by the AI agent.

#### POST `/api/mcp/add_task`

Adds a new task for the authenticated user.

**Request**:
```json
{
  "task_text": "Buy groceries",
  "due_date": "2026-02-10T18:00:00Z"
}
```

**Request Parameters**:
- `task_text` (body, required): The text description of the task
- `due_date` (body, optional): The due date for the task

**Response (Success)**:
```json
{
  "success": true,
  "task": {
    "id": 123,
    "title": "Buy groceries",
    "description": "",
    "due_date": "2026-02-10T18:00:00Z",
    "completed": false,
    "created_at": "2026-02-08T10:30:00Z"
  }
}
```

#### GET `/api/mcp/list_tasks`

Retrieves all tasks for the authenticated user.

**Request Parameters**:
- `status` (query, optional): Filter by task status ('all', 'active', 'completed')
- `limit` (query, optional): Maximum number of tasks to return (default: 50)
- `offset` (query, optional): Offset for pagination (default: 0)

**Response (Success)**:
```json
{
  "tasks": [
    {
      "id": 123,
      "title": "Buy groceries",
      "description": "",
      "due_date": "2026-02-10T18:00:00Z",
      "completed": false,
      "created_at": "2026-02-08T10:30:00Z"
    }
  ],
  "total_count": 1
}
```

#### PUT `/api/mcp/complete_task/{task_id}`

Marks a task as completed.

**Request Parameters**:
- `task_id` (path, required): The ID of the task to complete

**Response (Success)**:
```json
{
  "success": true,
  "task": {
    "id": 123,
    "title": "Buy groceries",
    "completed": true,
    "completed_at": "2026-02-08T10:30:00Z"
  }
}
```

#### DELETE `/api/mcp/delete_task/{task_id}`

Deletes a task.

**Request Parameters**:
- `task_id` (path, required): The ID of the task to delete

**Response (Success)**:
```json
{
  "success": true,
  "deleted_task_id": 123
}
```

#### PUT `/api/mcp/update_task/{task_id}`

Updates a task's information.

**Request**:
```json
{
  "new_task_text": "Buy groceries and household supplies",
  "due_date": "2026-02-12T18:00:00Z"
}
```

**Request Parameters**:
- `task_id` (path, required): The ID of the task to update
- `new_task_text` (body, optional): The updated text description of the task
- `due_date` (body, optional): The updated due date for the task

**Response (Success)**:
```json
{
  "success": true,
  "task": {
    "id": 123,
    "title": "Buy groceries and household supplies",
    "due_date": "2026-02-12T18:00:00Z",
    "completed": false
  }
}
```

## Common Error Response Format

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {} // Optional additional error details
  }
}
```

## Authentication and Authorization

All endpoints (except health checks) require a valid JWT token in the Authorization header. The token contains the user ID which is used to:

1. Verify the user's identity
2. Ensure the user can only access their own data
3. Apply appropriate rate limits

## Rate Limiting

To prevent abuse, the API implements rate limiting:

- Per-user: 100 requests per minute per endpoint
- Per-IP: 1000 requests per minute across all endpoints

Rate-limited requests receive a `429 Too Many Requests` response.

## Health Check

#### GET `/health`

Returns the health status of the service.

**Response (Success)**:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-08T10:30:00Z",
  "version": "1.0.0"
}
```