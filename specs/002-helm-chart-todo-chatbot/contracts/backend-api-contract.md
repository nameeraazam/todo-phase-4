# API Contract: Todo Chatbot Backend Service

## Overview
This document specifies the API contract for the Todo Chatbot backend service, which provides the core functionality for managing todo items through an AI-powered interface.

## Base URL
`http://backend:8000` (internal Kubernetes service name)

## Health Check Endpoint
### GET /health
Check the health status of the backend service.

**Response:**
- Status: 200 OK
- Body: 
```json
{
  "status": "healthy",
  "timestamp": "2026-02-10T10:00:00Z"
}
```

## Todo Operations

### GET /api/todos
Retrieve all todos for the current user.

**Headers:**
- Authorization: Bearer {token}

**Response:**
- Status: 200 OK
- Body:
```json
{
  "todos": [
    {
      "id": 1,
      "task": "Complete project proposal",
      "completed": false,
      "created_at": "2026-02-10T09:00:00Z",
      "updated_at": "2026-02-10T09:00:00Z"
    }
  ]
}
```

### POST /api/todos
Create a new todo item.

**Headers:**
- Authorization: Bearer {token}
- Content-Type: application/json

**Request Body:**
```json
{
  "task": "New todo item"
}
```

**Response:**
- Status: 201 Created
- Body:
```json
{
  "id": 2,
  "task": "New todo item",
  "completed": false,
  "created_at": "2026-02-10T10:00:00Z",
  "updated_at": "2026-02-10T10:00:00Z"
}
```

### PUT /api/todos/{id}
Update an existing todo item.

**Headers:**
- Authorization: Bearer {token}
- Content-Type: application/json

**Request Body:**
```json
{
  "task": "Updated todo item",
  "completed": true
}
```

**Response:**
- Status: 200 OK
- Body:
```json
{
  "id": 2,
  "task": "Updated todo item",
  "completed": true,
  "created_at": "2026-02-10T10:00:00Z",
  "updated_at": "2026-02-10T10:30:00Z"
}
```

### DELETE /api/todos/{id}
Delete a todo item.

**Headers:**
- Authorization: Bearer {token}

**Response:**
- Status: 204 No Content

## AI Chat Interface

### POST /api/chat
Send a message to the AI chatbot and receive a response.

**Headers:**
- Authorization: Bearer {token}
- Content-Type: application/json

**Request Body:**
```json
{
  "message": "Add a new todo: buy groceries"
}
```

**Response:**
- Status: 200 OK
- Body:
```json
{
  "response": "I've added 'buy groceries' to your todo list.",
  "action": {
    "type": "add_todo",
    "result": {
      "id": 3,
      "task": "buy groceries",
      "completed": false
    }
  }
}
```

## Error Responses
All error responses follow this format:

**Response:**
- Status: 4xx/5xx
- Body:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Detailed error message",
    "details": {}
  }
}
```

## Common Headers
- Authorization: Bearer {jwt_token}
- Content-Type: application/json
- Accept: application/json

## Authentication
All endpoints (except /health) require a valid JWT token in the Authorization header.