# Quickstart Guide: Helm Chart for Todo Chatbot

## Overview
This guide provides instructions for quickly deploying the Todo Chatbot application using the Helm chart. The application consists of a React frontend and a Python backend API.

## Prerequisites
- Kubernetes cluster (v1.20+)
- Helm 3.0+
- Docker (for building images)
- Access to a container registry (optional, for custom images)

## Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Prepare Container Images
The Helm chart expects container images for both frontend and backend. You can either:

#### Option A: Use Pre-built Images
```bash
# Pull the images from a registry
docker pull todo-frontend:latest
docker pull todo-backend:latest
```

#### Option B: Build Images Locally
```bash
# Build frontend image
cd frontend
docker build -t todo-frontend:latest .
cd ..

# Build backend image
cd backend
docker build -t todo-backend:latest .
cd ..
```

### 3. Install the Helm Chart
```bash
# Add the Helm repository (if hosted)
helm repo add todo-chatbot <repository-url>
helm repo update

# Install the chart
helm install todo-chatbot ./helm-chart --namespace todo-app --create-namespace
```

### 4. Verify Installation
```bash
# Check the status of the release
helm status todo-chatbot --namespace todo-app

# List pods
kubectl get pods --namespace todo-app

# List services
kubectl get svc --namespace todo-app
```

### 5. Access the Application
```bash
# Get the frontend service external IP
kubectl get svc todo-chatbot-frontend --namespace todo-app

# Or use port forwarding for local testing
kubectl port-forward svc/todo-chatbot-frontend 3000:80 --namespace todo-app
```

## Configuration

### Custom Values File
Create a `custom-values.yaml` file to override default settings:

```yaml
frontend:
  replicaCount: 3
  image:
    repository: my-registry/todo-frontend
    tag: v1.0.0
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 700m
      memory: 768Mi

backend:
  replicaCount: 2
  image:
    repository: my-registry/todo-backend
    tag: v1.0.0
  resources:
    requests:
      cpu: 300m
      memory: 384Mi
    limits:
      cpu: 1.2
      memory: 1.2Gi
```

Install with custom values:
```bash
helm install todo-chatbot ./helm-chart -f custom-values.yaml --namespace todo-app --create-namespace
```

## Useful Commands

### Upgrade the Release
```bash
helm upgrade todo-chatbot ./helm-chart --namespace todo-app
```

### Uninstall the Release
```bash
helm uninstall todo-chatbot --namespace todo-app
```

### Check Current Values
```bash
helm get values todo-chatbot --namespace todo-app
```

### Troubleshooting
```bash
# Check pod logs
kubectl logs -l app.kubernetes.io/name=todo-chatbot-frontend --namespace todo-app
kubectl logs -l app.kubernetes.io/name=todo-chatbot-backend --namespace todo-app

# Describe pods for more details
kubectl describe pods -l app.kubernetes.io/name=todo-chatbot --namespace todo-app
```

## Next Steps
- Configure persistent storage for the database
- Set up ingress controller for HTTPS access
- Configure monitoring and logging
- Set up CI/CD pipeline for automated deployments