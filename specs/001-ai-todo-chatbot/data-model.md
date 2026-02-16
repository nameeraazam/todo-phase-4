# Data Model: AI Todo Chatbot

**Feature**: AI Todo Chatbot (001-ai-todo-chatbot)
**Date**: 2026-02-08
**Authors**: [Team]

## Overview

This document defines the data models for the AI Todo Chatbot feature. It outlines the entities, their attributes, relationships, and validation rules based on the feature requirements.

## Entities

### 1. User

Represents an individual user of the system.

- **Fields**:
  - `id` (UUID/Integer): Unique identifier for the user
  - `email` (String): User's email address (unique)
  - `name` (String): User's display name
  - `created_at` (DateTime): Timestamp when the user account was created
  - `updated_at` (DateTime): Timestamp when the user account was last updated
  - `is_active` (Boolean): Whether the user account is active

- **Validation Rules**:
  - Email must be a valid email format
  - Email must be unique across all users
  - Name must be between 1 and 100 characters
  - Created_at and updated_at are automatically managed by the system

- **Relationships**:
  - One-to-many with Task (user has many tasks)
  - One-to-many with Conversation (user has many conversations)

### 2. Task

Represents a user's to-do item with attributes like title, description, due date/time, creation date, and completion status.

- **Fields**:
  - `id` (UUID/Integer): Unique identifier for the task
  - `user_id` (UUID/Integer): Foreign key linking to the owning user
  - `title` (String): Brief title of the task
  - `description` (Text): Detailed description of the task (optional)
  - `due_date` (DateTime): Date and time when the task is due (optional)
  - `completed` (Boolean): Whether the task has been completed
  - `completed_at` (DateTime): Timestamp when the task was marked as completed (nullable)
  - `created_at` (DateTime): Timestamp when the task was created
  - `updated_at` (DateTime): Timestamp when the task was last updated

- **Validation Rules**:
  - Title must be between 1 and 200 characters
  - Due date must be in the future if provided
  - User_id must reference an existing user
  - Completed_at must be null if completed is false
  - Completed_at must be set if completed is true

- **State Transitions**:
  - `incomplete` → `completed`: When task is marked as done
  - `completed` → `incomplete`: When task is unmarked as done

- **Relationships**:
  - Many-to-one with User (many tasks belong to one user)
  - One-to-many with TaskHistory (optional, for tracking changes)

### 3. Conversation

Represents a sequence of interactions between a user and the AI chatbot, maintaining context and history.

- **Fields**:
  - `id` (UUID/Integer): Unique identifier for the conversation
  - `user_id` (UUID/Integer): Foreign key linking to the user who owns the conversation
  - `title` (String): Auto-generated or user-provided title for the conversation
  - `created_at` (DateTime): Timestamp when the conversation was initiated
  - `updated_at` (DateTime): Timestamp when the conversation was last updated
  - `is_active` (Boolean): Whether the conversation is currently active

- **Validation Rules**:
  - User_id must reference an existing user
  - Title must be between 1 and 200 characters
  - Created_at and updated_at are automatically managed by the system

- **Relationships**:
  - Many-to-one with User (many conversations belong to one user)
  - One-to-many with Message (conversation has many messages)

### 4. Message

Represents a single message within a conversation, either from the user or the AI agent.

- **Fields**:
  - `id` (UUID/Integer): Unique identifier for the message
  - `conversation_id` (UUID/Integer): Foreign key linking to the conversation
  - `sender_type` (Enum): Either 'user' or 'agent'
  - `sender_id` (UUID/Integer): ID of the sender (user_id for users, agent_id for agents)
  - `content` (Text): The actual message content
  - `timestamp` (DateTime): When the message was sent
  - `message_type` (Enum): 'text', 'command', 'response', etc.
  - `metadata` (JSON): Additional data related to the message (optional)

- **Validation Rules**:
  - Conversation_id must reference an existing conversation
  - Sender_type must be either 'user' or 'agent'
  - Content must not be empty
  - Timestamp is automatically set when the message is created

- **Relationships**:
  - Many-to-one with Conversation (many messages belong to one conversation)

## Relationships Summary

```
User (1) -----> (Many) Task
User (1) -----> (Many) Conversation  
Conversation (1) -----> (Many) Message
```

## Indexes

For optimal performance, the following indexes should be created:

1. **User.email**: Unique index for fast user lookup by email
2. **Task.user_id**: Index for filtering tasks by user
3. **Task.due_date**: Index for sorting and filtering tasks by due date
4. **Task.completed**: Index for filtering completed/incomplete tasks
5. **Conversation.user_id**: Index for filtering conversations by user
6. **Message.conversation_id**: Index for retrieving messages in a conversation
7. **Message.timestamp**: Index for ordering messages chronologically

## Constraints

1. **Data Integrity**: Foreign key constraints to ensure referential integrity
2. **User Isolation**: All queries must be scoped to the authenticated user
3. **Soft Deletes**: Consider implementing soft deletes for important entities to maintain history
4. **Audit Trail**: Log important changes to tasks and conversations for debugging and analytics

## Future Extensions

Potential entities that might be added in future iterations:

1. **Tag**: For categorizing tasks
2. **TaskHistory**: For tracking changes to tasks over time
3. **Notification**: For reminding users about upcoming tasks
4. **Attachment**: For associating files with tasks