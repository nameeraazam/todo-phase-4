# Docker Setup for Todo Chatbot Application

This project includes Dockerfiles for both the frontend and backend applications:

- `Dockerfile.frontend` - For the React frontend application
- `Dockerfile.backend` - For the Python backend API
- `docker-compose.yml` - For local development with all services

## Building and Running with Docker

To build and run the entire application stack locally:

```bash
docker-compose up --build
```

The services will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: http://localhost:5432 (PostgreSQL)

To run just the backend service:

```bash
docker build -f Dockerfile.backend -t todo-backend .
docker run -p 8000:8000 todo-backend
```

To run just the frontend service:

```bash
docker build -f Dockerfile.frontend -t todo-frontend .
docker run -p 3000:3000 todo-frontend
```

## Docker Compose Services

The `docker-compose.yml` file defines the following services:

- `backend`: Python FastAPI application running on port 8000
- `frontend`: React application running on port 3000
- `db`: PostgreSQL database running on port 5432

## Environment Variables

The application uses the following environment variables:

### Backend
- `DATABASE_URL`: Connection string for the PostgreSQL database
- `SECRET_KEY`: Secret key for JWT token signing

### Frontend
- `REACT_APP_BACKEND_URL`: URL of the backend API (defaults to http://localhost:8000)

## Production Considerations

For production deployments, consider:
- Using a reverse proxy like nginx
- Setting up SSL certificates
- Using secrets management for sensitive data
- Implementing proper logging and monitoring
- Configuring health checks