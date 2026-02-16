---
id: 5
title: Fix chat assistant command recognition
stage: green
date: 2026-02-08
surface: agent
model: gemini-2.0-flash
feature: ai-todo-chatbot
branch: main
user: Dell
command: /sp.implement
labels: ["bug-fix", "regex", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/components/tasks/chat-ui.tsx
tests:
  - Manual verification of regex patterns
---

## User Prompt
The chat assistant is NOT recognizing these commands even though they're shown in the examples:
- "update task #1 to completed"
- "mark task #2 as completed"
- "mark task #3 as completed"
- "show tasks"

Every command returns: "❓ Sorry, I didn't understand that command. Try commands like: 'update task #1 to completed', 'mark task #2 as incomplete', or 'show tasks'."

## Implementation Details
1.  **Identified Bug**: The original regex `/^(update|mark|change)\s+(task|#)?\s*(\d+)\s+(to|as)?\s*(completed|incomplete|active|title\s+to|name\s+to)\s*(.+)?$/i` failed when both "task" and "#" were present (e.g., "task #1") because the second group `(task|#)?` only allowed one or the other.
2.  **Fixed Regex**: Updated the regex to `/^(update|mark|change)\s+(?:task\s*)?(#)?(\d+)\s+(?:to|as|is)?\s*(completed|incomplete|active|title\s+to|name\s+to)\s*(.+)?$/i`. This correctly handles "task", "#", or both, and adds "is" as an optional connector.
3.  **Adjusted Group Mapping**: Updated the code to use the new group indices resulting from the regex change.
4.  **Improved "Show Tasks"**: Expanded the matching logic for "show tasks" to include "list tasks", "what are my tasks", "tasks", and "ls", and added a safety check for the `tasks` array.

## Outcome
The chat assistant now correctly recognizes the example commands provided in the UI, improving the user experience and feature reliability.
