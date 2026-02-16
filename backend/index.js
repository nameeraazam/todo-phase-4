import express from 'express';
import cors from 'cors';
import { v4 as uuidv4 } from 'uuid';

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// In-memory storage (in a real app, this would be a database)
let users = [];
let tasks = [];

// Helper function to generate timestamps
const generateTimestamp = () => new Date().toISOString();

// Authentication Middleware
const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'No token provided' });
  }

  const token = authHeader.split(' ')[1];

  // In our mock, the token is mock_token_{userId}
  if (!token.startsWith('mock_token_')) {
    return res.status(401).json({ message: 'Invalid token' });
  }

  const userId = token.replace('mock_token_', '');
  const user = users.find(u => u.id === userId);

  if (!user && userId !== 'mock_user_id') {
    return res.status(401).json({ message: 'User not found' });
  }

  // Attach user to request
  req.user = user || { id: userId, name: 'Mock User' };
  next();
};

// Root route to fix "Cannot GET /"
app.get('/', (req, res) => {
  res.send('Backend is running 🚀');
});

// Auth routes
app.post('/api/auth/signup', (req, res) => {
  const { email, password, name } = req.body;

  // Check if user already exists
  const existingUser = users.find(user => user.email === email);
  if (existingUser) {
    return res.status(400).json({ message: 'User already exists' });
  }

  // Create new user
  const newUser = {
    id: uuidv4(),
    email,
    name,
    createdAt: generateTimestamp(),
    updatedAt: generateTimestamp()
  };

  users.push(newUser);

  // Return user data with a mock token
  res.json({
    user: newUser,
    token: `mock_token_${newUser.id}`
  });
});

app.post('/api/auth/signin', (req, res) => {
  const { email, password } = req.body;

  // Find user by email
  const user = users.find(user => user.email === email);
  if (!user) {
    return res.status(401).json({ message: 'Invalid credentials' });
  }

  // In a real app, you would verify the password here
  // For this mock, we'll just accept any password

  // Return user data with a mock token
  res.json({
    user: user,
    token: `mock_token_${user.id}`
  });
});

app.post('/api/auth/signout', (req, res) => {
  // In a real app, you would invalidate the token here
  // For this mock, we'll just return success
  res.json({ message: 'Signed out successfully' });
});

app.get('/api/auth/me', authenticate, (req, res) => {
  res.json(req.user);
});

// Task routes (Protected)
app.get('/api/tasks', authenticate, (req, res) => {
  // Return only tasks belonging to the authenticated user, sorted by completion and date
  const userTasks = tasks
    .filter(task => task.userId === req.user.id)
    .sort((a, b) => {
      if (a.completed !== b.completed) {
        return a.completed ? 1 : -1;
      }
      return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
    });
  res.json(userTasks);
});

app.post('/api/tasks', authenticate, (req, res) => {
  const { title, description } = req.body;

  // Validate input
  if (!title || title.trim() === '') {
    return res.status(400).json({ message: 'Title is required' });
  }

  // Create new task
  const newTask = {
    id: uuidv4(),
    userId: req.user.id,
    title: title.trim(),
    description: description ? description.trim() : undefined,
    completed: false,
    createdAt: generateTimestamp(),
    updatedAt: generateTimestamp(),
    completedAt: null
  };

  tasks.push(newTask);

  res.status(201).json(newTask);
});

app.put('/api/tasks/:id', authenticate, (req, res) => {
  const taskId = req.params.id;
  const { title, description, completed } = req.body;

  // Find the task
  const taskIndex = tasks.findIndex(task => task.id === taskId && task.userId === req.user.id);
  if (taskIndex === -1) {
    return res.status(404).json({ message: 'Task not found' });
  }

  // Update the task
  const updatedTask = {
    ...tasks[taskIndex],
    ...(title !== undefined && { title: title.trim() }),
    ...(description !== undefined && { description: description.trim() }),
    ...(completed !== undefined && {
      completed,
      completedAt: completed ? generateTimestamp() : null
    }),
    updatedAt: generateTimestamp()
  };

  tasks[taskIndex] = updatedTask;

  res.json(updatedTask);
});

app.delete('/api/tasks/:id', authenticate, (req, res) => {
  const taskId = req.params.id;

  // Find the task
  const taskIndex = tasks.findIndex(task => task.id === taskId && task.userId === req.user.id);
  if (taskIndex === -1) {
    return res.status(404).json({ message: 'Task not found' });
  }

  // Remove the task
  tasks.splice(taskIndex, 1);

  res.json({ message: 'Task deleted successfully' });
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: generateTimestamp() });
});

// Export the app for Vercel
export default app;