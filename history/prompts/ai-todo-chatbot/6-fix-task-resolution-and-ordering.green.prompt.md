---
id: 6
title: Fix task resolution and dynamic ordering in chat
stage: green
date: 2026-02-08
surface: agent
model: gemini-2.0-flash
feature: ai-todo-chatbot
branch: main
user: Dell
command: /sp.implement
labels: ["bug-fix", "sorting", "logging", "frontend", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/components/tasks/chat-ui.tsx
  - frontend/app/dashboard/page.tsx
  - frontend/app/tasks/page.tsx
  - backend/server.js
tests:
  - Manual verification of sorting logic
  - Manual verification of debug logs
---

## User Prompt
Task order in the UI changes dynamically (possibly sorted by completion status), but the chat might be using static IDs or database order. This mismatch could be breaking task number references.

Fix how task #1, #2, #3 map to actual tasks:
- Should use displayed order (1-based index)
- Account for sorting/filtering
- Handle dynamic task order
- Add Debug Logging

## Implementation Details
1.  **Consistent Sorting**: Implemented a unified sorting strategy across the application: Active tasks first, then sorted by `createdAt` descending (newest first).
2.  **Backend Update**: Modified `backend/server.js` to return tasks using this sorted order.
3.  **Frontend Update**: Modified `DashboardPage` and `TasksPage` to sort tasks in-memory before passing them to both `TaskList` and `ChatUI`. This guarantees that the index used by the chat always matches the 1-based index displayed in the list.
4.  **Debug Logging**: Added detailed `console.log` statements in `ChatUI.tsx` to trace:
    *   Command matching and regex groups.
    *   Task number resolution (mapping user input to array index).
    *   API update calls and results.
5.  **Robust Regex**: (From previous step) Fixed the command parsing regex to handle "task #1" style inputs correctly.

## Outcome
The task assistant now reliably resolves task numbers because it uses the exact same sorted list as the UI. Users can now confidently say "update task #1" and know it refers to the first task they see on their screen, regardless of when it was created or its completion status.
